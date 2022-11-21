from sqlalchemy.orm import Session
from pydantic_schemas.brownfield_schemas import NewBrownfield, Brownfield as BrownfieldSchema
from sqlalchemy import select
from database.brownfield_models import Brownfield
from os.path import join, isfile
from os import listdir
from globals import BROWNFIELD_IMAGES_DIR

from database.brownfield_models import AreaSize, Brownfield, DegradationLevel, EconomicPotential, EnvironmentalBurdenInclusion, InfrastructureAvailability, Location, NaturalAndArchitecturalValue, OriginalFunctionalUtilization, OwnershipType, ResidentionalAreaCategory, Revitalization, Settlement, Utilization

def get_union_lookup_values(session: Session):
    column_alias = "table_name"
    tables = [OwnershipType,Utilization,AreaSize,Location,DegradationLevel,ResidentionalAreaCategory,Settlement,
              InfrastructureAvailability,NaturalAndArchitecturalValue,
              Revitalization,EconomicPotential,EnvironmentalBurdenInclusion,OriginalFunctionalUtilization]
    table_names = [table.__tablename__ for table in tables]
    stmt = ('''
            select *,:t0 AS {column_alias} from %s
            union select *,:t1 AS {column_alias} from %s
            union select *,:t2 AS {column_alias} from %s
            union select *,:t3 AS {column_alias} from %s
            union select *,:t4 AS {column_alias} from %s
            union select *,:t5 AS {column_alias} from %s
            union select *,:t6 AS {column_alias} from %s
            union select *,:t7 AS {column_alias} from %s
            union select *,:t8 AS {column_alias} from %s
            union select *,:t9 AS {column_alias} from %s
            union select *,:t10 AS {column_alias} from %s
            union select *,:t11 AS {column_alias} from %s
            union select *,:t12 AS {column_alias} from %s
            ''' % (tuple(["brownfields." + tbname for tbname in table_names]))).format(column_alias = column_alias)
    keys = ["t" + str(val) for val in range(0,len(tables))]
    dynamic_values = dict(zip(keys,table_names))
    return session.execute(stmt,dynamic_values)

def insert_new_brownfield(bf:NewBrownfield,image_dir_uuid:str,sess:Session) -> int | None:
    new_brownfield = Brownfield(
        **bf.dict(),image_directory_uuid = image_dir_uuid
    )
    sess.add(new_brownfield)
    sess.commit()
    return new_brownfield.id  # type: ignore
     
def query_brownfield(bf_id:int,sess:Session) -> BrownfieldSchema | None:
    stmt = select(Brownfield).where(Brownfield.id == bf_id)
    res : Brownfield | None = sess.execute(stmt).scalar_one_or_none()
    if res is None:
        return None
    images_dir = join(BROWNFIELD_IMAGES_DIR,res.image_directory_uuid)  # type: ignore
    urls = [f for f in listdir(images_dir) if isfile(join(images_dir, f))]
    return BrownfieldSchema(
        street  = res.street,# type: ignore
        area_ha  = res.area_ha,# type: ignore
        mapping_year  = res.mapping_year,# type: ignore
        altitude  = res.altitude, # type: ignore
        ownership_type  = res.ownership_type.value,
        original_functional_utilization  = res.original_functional_utilization.value,
        utilization  = res.utilization.value,
        area_size  = res.area_size.value,
        location  = res.location.value,
        degradation_level  = res.degradation_level.value,
        residentional_area_category  = res.residentional_area_category.value,
        settlement  = res.settlement.value,
        infrastructure_availability  = res.infrastructure_availability.value,
        natural_and_architectural_value  = res.natural_and_architectural_value.value,
        revitalization  = res.revitalization.value,
        economic_potential  = res.economic_potential, # TODO return value of CISELNIK
        environmental_burden_inclusion  = res.environmental_burden_inclusion, # TODO return value of CISELNIK
        image_urls = urls
    )