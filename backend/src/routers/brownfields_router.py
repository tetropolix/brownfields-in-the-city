from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from pydantic_schemas.brownfield_schemas import BrownfieldID, FormFields, NewBrownfield
from crud.brownfields_cruds import get_union_lookup_values, insert_new_brownfield
from dependencies import get_session

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
def insert_brownfield(new_brownfield: NewBrownfield,sess: Session = Depends(get_session)):
    '''
    New brownfield record insertion
    '''
    print(new_brownfield)
    id = insert_new_brownfield(new_brownfield,sess)
    if(id== None):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Unable to store specified brownfield'
        )
    return BrownfieldID(id=id)
