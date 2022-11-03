from pathlib import Path
from fastapi import APIRouter,Depends,status,HTTPException, UploadFile,Form
from sqlalchemy.orm import Session
from custom_exceptions import EntityWasNotStored
from pydantic_schemas.brownfield_schemas import BrownfieldID, FormFields, NewBrownfield
from crud.brownfields_cruds import get_union_lookup_values, insert_new_brownfield
from dependencies import get_session
from .routers_utils import new_brownfield_image_upload, validate_raw_json_new_brownfield, clear_images_dir
from uuid import uuid4
from globals import EnvVars
from sqlalchemy.exc import SQLAlchemyError

router =  APIRouter(
    prefix='/brownfields',
    tags=['brownfields']
)

@router.get('/form-fields',response_model=FormFields)
def form_data(sess: Session = Depends(get_session)):
    '''
    Returns fields for dropdown menus - used to load values for brownfields creation form
    '''
    result = get_union_lookup_values(sess)
    form_fields = {}
    for row in result:
        row = dict(row)
        row_table_name = row['table_name']
        if(not form_fields.get(row_table_name)):
            form_fields[row_table_name] = {}
        form_fields[row_table_name][row['id']] = row['value']
    return form_fields

@router.post('/insert',response_model=BrownfieldID)
def insert_brownfield(new_brownfield: NewBrownfield = Depends(validate_raw_json_new_brownfield),files: list[UploadFile]  | None = None,sess: Session = Depends(get_session)):
    '''
    New brownfield record insertion
    '''
    
    bf_images_dir = str(uuid4())
    dir_path = Path(EnvVars.BROWNFIELD_IMAGES_DIR ,bf_images_dir)
    if files is not None:
        new_brownfield_image_upload(files,dir_path)
    try:
        id = insert_new_brownfield(new_brownfield,bf_images_dir,sess)
        if(not id):
            raise EntityWasNotStored('Inserting new brownfield was not successful')
        return BrownfieldID(id=id)
    except (SQLAlchemyError, EntityWasNotStored) as e :
        clear_images_dir(dir_path)
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Unable to store specified brownfield'
        )