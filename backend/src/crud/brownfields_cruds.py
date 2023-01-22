from typing import Any

from geoalchemy2.functions import ST_AsGeoJSON
from geoalchemy2.shape import to_shape
from sqlalchemy.orm import Session
from pydantic_schemas.brownfield_schemas import (
    NewBrownfield,
    Brownfield as BrownfieldSchema,
    BrownfieldCore,
    BrownfieldsFilters,
    BrownfieldsDials,
    AvailableBrownfieldsFilters,
    BrownfieldColorDial,
    BrownfieldDialUpdate,
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
    bf_dict = bf.dict()
    if bf.polygon is not None:
        # creation of polygon format for insertion into postgres DB according to geoalchemy2 docs - ex.: 'POLYGON((0 0,1 0,1 1,0 1,0 0))' // better option is to use shapely -> TODO
        polygon_tuples = [
            str(coord_tuple[0]) + " " + str(coord_tuple[1])
            for coord_tuple in bf.polygon
        ]
        polygon_format = "POLYGON((" + (",").join(polygon_tuples) + "))"
        bf_dict["polygon"] = polygon_format

    new_brownfield = Brownfield(**bf_dict, image_directory_uuid=image_dir_uuid)
    sess.add(new_brownfield)
    sess.commit()
    return new_brownfield.id  # type: ignore

def get_brownfield_schema__from_db_object(bf : Brownfield):
    urls = get_static_image_paths_bf(bf.image_directory_uuid)  # type: ignore
    return BrownfieldSchema(
        id=bf.id,  # type: ignore
        color=BrownfieldColorDial(
            id=bf.color.id, name=bf.color.name, hex_value=bf.color.hex_value
        ),
        description=bf.description,  # type: ignore
        street=bf.street,  # type: ignore
        area_ha=bf.area_ha,  # type: ignore
        mapping_year=bf.mapping_year,  # type: ignore
        altitude=bf.altitude,  # type: ignore
        ownership_type=bf.ownership_type.value,
        original_functional_utilization=bf.original_functional_utilization.value,
        utilization=bf.utilization.value,
        area_size=bf.area_size.value,
        location=bf.location.value,
        degradation_level=bf.degradation_level.value,
        residentional_area_category=bf.residentional_area_category.value,
        settlement=bf.settlement.value,
        infrastructure_availability=bf.infrastructure_availability.value,
        natural_and_architectural_value=bf.natural_and_architectural_value.value,
        revitalization=bf.revitalization.value,
        economic_potential=bf.economic_potential,  # type: ignore # TODO return value of DIAL
        environmental_burden_inclusion=bf.environmental_burden_inclusion,  # type: ignore # TODO return value of DIAL
        image_urls=urls,
        polygon=list(to_shape(bf.polygon).exterior.coords)  # type: ignore
        if bf.polygon is not None
        else None,
    )

def query_brownfield(bf_id: int, sess: Session) -> BrownfieldSchema | None:
    stmt = select(Brownfield).where(Brownfield.id == bf_id)
    res: Brownfield | None = sess.execute(stmt).scalar_one_or_none()
    if res is None:
        return None
    return get_brownfield_schema__from_db_object(res)


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
                description=bf.description,  # type: ignore
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


def update_existing_dial_value(
    dial: Any, to_update: BrownfieldDialUpdate, sess: Session
):
    dial = sess.execute(
        select(dial).where(dial.id == to_update.dial_value_id)
    ).scalar_one()
    if to_update.color_update is not None:  # update color
        color_updt = to_update.color_update
        if color_updt.hex_value:
            dial.hex_value = color_updt.hex_value
        if color_updt.name:
            dial.name = color_updt.name
    else:  # update other dials
        dial.value = to_update.value
    sess.add(dial)
    sess.commit()


def create_new_dial_value(dial: Any, to_update: BrownfieldDialUpdate, sess: Session):
    new_dial = dial()
    if to_update.color_update is not None:  # create new color
        color_updt = to_update.color_update
        if color_updt.hex_value:
            new_dial.hex_value = color_updt.hex_value
        if color_updt.name:
            new_dial.name = color_updt.name
    else:  # create new value in other dials
        new_dial.value = to_update.value
    sess.add(new_dial)
    sess.commit()
