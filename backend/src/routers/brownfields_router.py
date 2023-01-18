from pathlib import Path
from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    UploadFile,
    Response,
    Query,
)
from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound, IntegrityError
from crud.crud_utils import get_bf_dials_by_key, get_dial_by_key
from custom_exceptions import EntityWasNotStored
from database.brownfield_models import Brownfield as BrownfieldModel
from pydantic_schemas.brownfield_schemas import (
    AvailableBrownfieldsFilters,
    BrownfieldExportCSV,
    BrownfieldID,
    BrownfieldsDials,
    NewBrownfield,
    Brownfield,
    BrownfieldCore,
    BrownfieldsFilters,
    BrownfieldsDialsByKey,
    BrownfieldDialUpdate,
)
from crud.brownfields_cruds import (
    create_new_dial_value,
    get_brownfield_schema__from_db_object,
    get_brownfields_dials,
    insert_new_brownfield,
    query_brownfield,
    query_brownfields,
    get_brownfield_cores,
    get_available_bf_filters,
    update_existing_dial_value,
)
from dependencies import Protected, get_session, validate_raw_json_new_brownfield
from .routers_utils import (
    get_csv_string,
    get_kml_string,
    new_brownfield_image_upload,
    clear_images_dir,
    LimitOffsetParams,
    LimitOffsetPage,
    paginate,
    create_bf_images_dir,
)
from uuid import uuid4
from globals import PERMISSIONS, EnvVars
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/brownfields", tags=["brownfields"])


@router.get("/form-fields", response_model=BrownfieldsDials)
def form_data(
    sess: Session = Depends(get_session),
    current_user: Protected = Depends(Protected([PERMISSIONS.BF_READ])),
):
    """
    Returns fields for dropdown menus - used to load values for brownfields creation form
    """
    return get_brownfields_dials(sess)


@router.post("/insert", response_model=BrownfieldID)
def insert_brownfield(
    new_brownfield: NewBrownfield = Depends(validate_raw_json_new_brownfield),
    files: list[UploadFile] | None = None,
    sess: Session = Depends(get_session),
    current_user: Protected = Depends(
        Protected([PERMISSIONS.BF_READ, PERMISSIONS.BF_CREATE])
    ),
):
    """
    New brownfield record insertion.
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
    """
    Queries brownfield specified by id.
    404 return if brownfield does not exist.
    """
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
    """Queries brownfields (filter funcionality is not provided at this route)"""
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
    """
    Queries brownfields which are selected based on conditions specified in filters object.
    """
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
def get_dials_by_key(
    current_user: Protected = Depends(Protected([PERMISSIONS.BF_READ])),
):
    return get_bf_dials_by_key()


@router.post("/update-dial", status_code=status.HTTP_202_ACCEPTED)
def update_dial(
    to_update: BrownfieldDialUpdate,
    sess: Session = Depends(get_session),
    current_user: Protected = Depends(
        Protected([PERMISSIONS.BF_READ, PERMISSIONS.BF_UPDATE])
    ),
):
    """
    Updates value of existing dial
    """
    dial = get_dial_by_key(to_update)
    if dial is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )
    try:
        if to_update.dial_value_id is None:  # create new dial value
            create_new_dial_value(dial, to_update, sess)
        else:
            update_existing_dial_value(dial, to_update, sess)
    except MultipleResultsFound:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not valid values"
        )


@router.get("/export-csv/{bf_id}", response_class=Response)
def export_brownfield(
    bf_id: int,
    sess: Session = Depends(get_session),
    current_user: Protected = Depends(Protected([PERMISSIONS.BF_READ])),
):
    """
    Exports brownfield specified by id in CSV format
    """
    bf = query_brownfield(bf_id, sess)
    if bf is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )
    bf = BrownfieldExportCSV(**bf.dict(), WKT=bf.polygon)
    headers = list(bf.dict().keys())
    content = get_csv_string(headers, [bf.dict()])
    return Response(
        content=content,
        media_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="brownfield_%s.csv"' % bf_id
        },
    )


@router.get("/export-csv", response_class=Response)
def export_brownfields(
    ids: list[int] = Query(),
    sess: Session = Depends(get_session),
    current_user: Protected = Depends(Protected([PERMISSIONS.BF_READ])),
):
    """
    Exports multiple brownfields specified by list of ids in query param in CSV format
    If no record was found for some of the ids then record for specified id is not included in final csv

    list of ids in query params should be in this format: .../brownfields/export?ids=1&ids=2&ids=11

    If no records are found at all 404 response is raised

    Maximum of ids for one request is 200
    """
    if len(ids) > 200:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Too many resources requested",
        )
    bfs_db = query_brownfields(sess, filters=BrownfieldsFilters(id=ids))
    if len(bfs_db) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )
    bfs = [get_brownfield_schema__from_db_object(b) for b in bfs_db]
    bf = BrownfieldExportCSV(**bfs[0].dict(), WKT=bfs[0].polygon)
    headers = list(bf.dict().keys())
    content = get_csv_string(
        headers, [BrownfieldExportCSV(**b.dict(), WKT=b.polygon).dict() for b in bfs]
    )
    return Response(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="brownfields.csv"'},
    )


@router.get("/export-kml/{bf_id}", response_class=Response)
def export_brownfield_kml(
    bf_id: int,
    sess: Session = Depends(get_session),
    current_user: Protected = Depends(Protected([PERMISSIONS.BF_READ])),
):
    """
    Exports brownfield specified by id in KML format
    """
    bf = query_brownfield(bf_id, sess)
    if bf is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )
    content = get_kml_string([bf])
    return Response(
        content=content,
        media_type="application/vnd.google-earth.kml+xml",
        headers={
            "Content-Disposition": 'attachment; filename="brownfield_%s.kml"' % bf_id
        },
    )


@router.get("/export-kml", response_class=Response)
def export_brownfields_kml(
    ids: list[int] = Query(),
    sess: Session = Depends(get_session),
    current_user: Protected = Depends(Protected([PERMISSIONS.BF_READ])),
):
    """
    Exports multiple brownfields specified by list of ids in query param in KML format
    If no record was found for some of the ids then record for specified id is not included in final KML

    list of ids in query params should be in this format: .../brownfields/export?ids=1&ids=2&ids=11

    If no records are found at all 404 response is raised

    Maximum of ids for one request is 200
    """
    if len(ids) > 200:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Too many resources requested",
        )
    bfs_db = query_brownfields(sess, filters=BrownfieldsFilters(id=ids))
    if len(bfs_db) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )
    bfs = [get_brownfield_schema__from_db_object(b) for b in bfs_db]
    content = get_kml_string(bfs)
    return Response(
        content=content,
        media_type="application/vnd.google-earth.kml+xml",
        headers={"Content-Disposition": 'attachment; filename="brownfields.kml'},
    )
