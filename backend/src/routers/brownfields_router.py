from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from crud.brownfields_cruds import get_union_lookup_values
from dependencies import get_session

router =  APIRouter(
    prefix='/brownfields',
    tags=['brownfields']
)

@router.get('/form-fields')
def form_data(sess: Session = Depends(get_session)):
    result = get_union_lookup_values(sess)
    form_data = {}
    for row in result:
        row = dict(row)
        row_table_name = row['table_name']
        if(not form_data.get(row_table_name)):
            form_data[row_table_name] = {}
        form_data[row_table_name][row['id']] = row['value']
    return form_data