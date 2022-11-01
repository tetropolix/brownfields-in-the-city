from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from pydantic_schemas.brownfield_schemas import FormFields
from crud.brownfields_cruds import get_union_lookup_values
from dependencies import get_session

router =  APIRouter(
    prefix='/brownfields',
    tags=['brownfields']
)

@router.get('/form-fields',response_model=FormFields)
def form_data(sess: Session = Depends(get_session)):
    '''
    Returns fields for dropdown menus - used to load values for brownfields creation form.
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