from fastapi import Form,status,HTTPException,UploadFile
from fastapi.encoders import jsonable_encoder
from pydantic_schemas.brownfield_schemas import NewBrownfield
from pydantic import ValidationError
from globals import MAX_IMAGE_UPLOAD_SIZE
from pathlib import Path
from shutil import rmtree

def validate_raw_json_new_brownfield(data : str = Form(...)) -> NewBrownfield:
    try:
        new_brownfield = NewBrownfield.parse_raw(data)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return new_brownfield

def new_brownfield_image_upload(files: list[UploadFile],bf_images_dir_path:Path) -> None:
    # check if all uploaded files are valid content_type and max of 8 files were uploaded
    valid_mime_types = all([file.content_type in ('image/jpeg','image/png') for file in files])
    if(not valid_mime_types):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        )
    elif len(files) > 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    #start writing files to disk, in case some of the file exceeds max size throw exception and delete everything that was written    
    try:
        bf_images_dir_path.mkdir(exist_ok=False)
    except FileExistsError:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
    for file in files:
        content = file.file.read(MAX_IMAGE_UPLOAD_SIZE)
        if(len(file.file.read(1)) != 0):
            clear_images_dir(bf_images_dir_path)
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        with open(Path(bf_images_dir_path,file.filename), 'wb') as f:
            f.write(content)

def clear_images_dir(dir_path: Path):
    rmtree(dir_path)
