from pathlib import Path
from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, Request
from sqlalchemy.orm import Session
from crud.crud_utils import get_bf_dials_by_key
from custom_exceptions import EntityWasNotStored
from database.brownfield_models import Brownfield as BrownfieldModel
from pydantic_schemas.brownfield_schemas import (
    AvailableBrownfieldsFilters,
    BrownfieldID,
    BrownfieldsDials,
    NewBrownfield,
    Brownfield,
    BrownfieldCore,
    BrownfieldsFilters,
    BrownfieldsDialsByKey,
)
from crud.brownfields_cruds import (
    get_brownfields_dials,
    insert_new_brownfield,
    query_brownfield,
    query_brownfields,
    get_brownfield_cores,
    get_available_bf_filters,
)
from dependencies import get_session, validate_raw_json_new_brownfield
from .routers_utils import (
    new_brownfield_image_upload,
    clear_images_dir,
    LimitOffsetParams,
    LimitOffsetPage,
    paginate,
    create_bf_images_dir,
)
from uuid import uuid4
from globals import EnvVars
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/brownfields", tags=["brownfields"])


@router.get("/form-fields", response_model=BrownfieldsDials)
def form_data(sess: Session = Depends(get_session)):
    """
    Returns fields for dropdown menus - used to load values for brownfields creation form
    """
    return get_brownfields_dials(sess)


@router.post("/insert", response_model=BrownfieldID)
def insert_brownfield(
    new_brownfield: NewBrownfield = Depends(validate_raw_json_new_brownfield),
    files: list[UploadFile] | None = None,
    sess: Session = Depends(get_session),
):
    """
    New brownfield record insertion
    """

    bf_images_dir = str(uuid4())
    dir_path = Path(EnvVars.BROWNFIELDS_IMAGES_DIR, bf_images_dir)
    if files is not None:
        new_brownfield_image_upload(files, dir_path)
    else:  # try create at least bf images dir
        try:
            create_bf_images_dir(dir_path)
        except FileExistsError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    try:
        id = insert_new_brownfield(new_brownfield, bf_images_dir, sess)
        if not id:
            raise EntityWasNotStored("Inserting new brownfield was not successful")
        return BrownfieldID(id=id)
    except (SQLAlchemyError, EntityWasNotStored) as e:
        clear_images_dir(dir_path)
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to store specified brownfield",
        )


@router.get("/brownfield/{bf_id}", response_model=Brownfield)
def get_brownfield(bf_id: int, sess: Session = Depends(get_session)):
    bf = query_brownfield(bf_id, sess)
    if bf is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )
    return bf


@router.get(
    "/brownfields",
    response_model=LimitOffsetPage[BrownfieldCore],
)
def get_brownfields(
    params: LimitOffsetParams = Depends(),
    sess: Session = Depends(get_session),
):
    res = query_brownfields(sess, params.offset, params.limit, filters=None)
    if len(res) == 0 and params.offset == 0:  # no brownfield in DB
        return paginate([], 0, params)
    elif len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )
    bf_cores = get_brownfield_cores(res)
    total = sess.query(BrownfieldModel.id).count()
    return paginate(bf_cores, total, params)


@router.post(
    "/brownfields",
    response_model=LimitOffsetPage[BrownfieldCore],
)
def get_brownfields_with_filters(
    filters: BrownfieldsFilters,
    params: LimitOffsetParams = Depends(),
    sess: Session = Depends(get_session),
):
    res = query_brownfields(sess, params.offset, params.limit, filters)
    if len(res) == 0 and params.offset == 0:  # no brownfield in DB
        return paginate([], 0, params)
    elif len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )
    bf_cores = get_brownfield_cores(res)
    total = sess.query(BrownfieldModel.id).count()
    return paginate(bf_cores, total, params)


@router.get("/filters", response_model=AvailableBrownfieldsFilters)
def get_filters(sess: Session = Depends(get_session)):
    return get_available_bf_filters(sess)


@router.get("/dials-by-key", response_model=BrownfieldsDialsByKey)
def get_dials_by_key():
    return get_bf_dials_by_key()


@router.get("/update_dial/{key}", status_code=status.HTTP_202_ACCEPTED)
def update_dial(key: int):
    pass
