from sqlalchemy.orm import Session

from database.brownfield_models import AreaSize, DegradationLevel, EconomicPotential, EnvironmentalBurdenInclusion, InfrastructureAvailability, Location, NaturalAndArchitecturalValue, OriginalFunctionalUtilization, OwnershipType, ResidentionalAreaCategory, Revitalization, Settlement, Utilization

def get_union_lookup_values(session: Session):
    column_alias = "table_name"
    tables = [OwnershipType,Utilization,AreaSize,Location,DegradationLevel,ResidentionalAreaCategory,Settlement,
              InfrastructureAvailability,NaturalAndArchitecturalValue,
              Revitalization,EconomicPotential,EnvironmentalBurdenInclusion]
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
            ''' % (tuple(["brownfields." + tbname for tbname in table_names]))).format(column_alias = column_alias)
    keys = ["t" + str(val) for val in range(0,len(tables))]
    dynamic_values = dict(zip(keys,table_names))
    return session.execute(stmt,dynamic_values)