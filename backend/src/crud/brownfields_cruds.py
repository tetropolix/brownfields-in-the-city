from sqlalchemy.orm import Session
from pydantic_schemas.brownfield_schemas import (
    NewBrownfield,
    Brownfield as BrownfieldSchema,
    BrownfieldCore,
    BrownfieldsFilters,
    BrownfieldsDials,
    AvailableBrownfieldsFilters,
    BrownfieldColorDial,
)
from sqlalchemy import select, text, func
from database.brownfield_models import Brownfield


from database.brownfield_models import (
    AreaSize,
    Brownfield,
    DegradationLevel,
    EconomicPotential,
    EnvironmentalBurdenInclusion,
    InfrastructureAvailability,
    Location,
    NaturalAndArchitecturalValue,
    OriginalFunctionalUtilization,
    OwnershipType,
    ResidentionalAreaCategory,
    Revitalization,
    Settlement,
    Utilization,
    Color,
)
from .crud_utils import assign_filters_bf_query, get_static_image_paths_bf


def get_brownfields_dials(sess: Session) -> BrownfieldsDials:
    column_alias = "table_name"
    tables = [
        OwnershipType,
        Utilization,
        AreaSize,
        Location,
        DegradationLevel,
        ResidentionalAreaCategory,
        Settlement,
        InfrastructureAvailability,
        NaturalAndArchitecturalValue,
        Revitalization,
        EconomicPotential,
        EnvironmentalBurdenInclusion,
        OriginalFunctionalUtilization,
    ]
    table_names = [table.__tablename__ for table in tables]
    stmt = (
        """
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
            """
        % (tuple(["brownfields." + tbname for tbname in table_names]))
    ).format(column_alias=column_alias)
    keys = ["t" + str(val) for val in range(0, len(tables))]
    dynamic_values = dict(zip(keys, table_names))
    result = sess.execute(text(stmt), dynamic_values)
    form_fields = {}
    for row in result:
        row = dict(row)
        row_table_name = row["table_name"]
        if not form_fields.get(row_table_name):
            form_fields[row_table_name] = {}
        form_fields[row_table_name][row["id"]] = row["value"]
    # get brownfield colors separately, as they are in separe "format"
    colors = sess.execute(select(Color))
    colors_list = [
        BrownfieldColorDial(
            id=row.Color.id, name=row.Color.name, hex_value=row.Color.hex_value
        )
        for row in colors
    ]

    return BrownfieldsDials(**form_fields, colors=colors_list)


# Very poor approach of querying min/max values - TODO better approach
def get_available_bf_filters(sess: Session) -> AvailableBrownfieldsFilters:
    bf_dials = get_brownfields_dials(sess)
    max_values = {
        "area_ha_max": sess.query(func.max(Brownfield.area_ha)).scalar(),
        "area_ha_min": sess.query(func.min(Brownfield.area_ha)).scalar(),
        "mapping_year_max": sess.query(func.max(Brownfield.mapping_year)).scalar(),
        "mapping_year_min": sess.query(func.min(Brownfield.mapping_year)).scalar(),
        "altitude_max": sess.query(func.max(Brownfield.altitude)).scalar(),
        "altitude_min": sess.query(func.min(Brownfield.altitude)).scalar(),
    }
    return AvailableBrownfieldsFilters(**bf_dials.dict(), **max_values)


def insert_new_brownfield(
    bf: NewBrownfield, image_dir_uuid: str, sess: Session
) -> int | None:
    new_brownfield = Brownfield(**bf.dict(), image_directory_uuid=image_dir_uuid)
    sess.add(new_brownfield)
    sess.commit()
    return new_brownfield.id  # type: ignore


def query_brownfield(bf_id: int, sess: Session) -> BrownfieldSchema | None:
    stmt = select(Brownfield).where(Brownfield.id == bf_id)
    res: Brownfield | None = sess.execute(stmt).scalar_one_or_none()
    if res is None:
        return None
    urls = get_static_image_paths_bf(res.image_directory_uuid)  # type: ignore
    return BrownfieldSchema(
        id=res.id,  # type: ignore
        color=BrownfieldColorDial(
            id=res.color.id, name=res.color.name, hex_value=res.color.hex_value
        ),
        street=res.street,  # type: ignore
        area_ha=res.area_ha,  # type: ignore
        mapping_year=res.mapping_year,  # type: ignore
        altitude=res.altitude,  # type: ignore
        ownership_type=res.ownership_type.value,
        original_functional_utilization=res.original_functional_utilization.value,
        utilization=res.utilization.value,
        area_size=res.area_size.value,
        location=res.location.value,
        degradation_level=res.degradation_level.value,
        residentional_area_category=res.residentional_area_category.value,
        settlement=res.settlement.value,
        infrastructure_availability=res.infrastructure_availability.value,
        natural_and_architectural_value=res.natural_and_architectural_value.value,
        revitalization=res.revitalization.value,
        economic_potential=res.economic_potential,  # type: ignore # TODO return value of CISELNIK
        environmental_burden_inclusion=res.environmental_burden_inclusion,  # type: ignore # TODO return value of CISELNIK
        image_urls=urls,
    )


def query_brownfields(
    sess: Session,
    offset: int = 0,
    limit: int | None = None,
    filters: BrownfieldsFilters | None = None,
) -> list[Brownfield]:
    query = sess.query(Brownfield)
    if not (filters is None):
        query = assign_filters_bf_query(query, filters)
    if limit:
        query = query.limit(limit)
    if offset and limit:
        query = query.offset(offset)

    return query.all()


def get_brownfield_cores(brownfields: list[Brownfield]) -> list[BrownfieldCore]:
    bf_cores = []
    for bf in brownfields:
        bf_cores.append(
            BrownfieldCore(
                id=bf.id,  # type: ignore
                street=bf.street,  # type: ignore
                area_ha=bf.area_ha,  # type: ignore
                mapping_year=bf.mapping_year,  # type: ignore
                altitude=bf.altitude,  # type: ignore
                ownership_type=bf.ownership_type.value,
                image_urls=next(
                    (
                        p
                        for p in get_static_image_paths_bf(
                            bf.image_directory_uuid  # type:ignore
                        )
                    ),
                    None,
                ),
            )
        )
    return bf_cores
