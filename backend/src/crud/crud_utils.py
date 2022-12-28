from pathlib import Path
from typing import Any
from pydantic_schemas.brownfield_schemas import (
    BrownfieldsFilters,
    BrownfieldsDialsByKey,
    DialByKey,
    BrownfieldDialUpdate,
)
from sqlalchemy.orm import Query
from database.brownfield_models import Brownfield
from os.path import join, isfile
from os import listdir
from globals import EnvVars
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

# crud utils
BROWNFIELDS_DIALS_BY_KEY: dict[int, Any] = {
    1: AreaSize,
    2: DegradationLevel,
    3: EconomicPotential,
    4: EnvironmentalBurdenInclusion,
    5: InfrastructureAvailability,
    6: Location,
    7: NaturalAndArchitecturalValue,
    8: OriginalFunctionalUtilization,
    9: OwnershipType,
    10: ResidentionalAreaCategory,
    11: Revitalization,
    12: Settlement,
    13: Utilization,
    14: Color,
}


def get_dial_by_key(to_update: BrownfieldDialUpdate) -> Any | None:
    return BROWNFIELDS_DIALS_BY_KEY.get(to_update.dial_key)


def get_bf_dials_by_key() -> BrownfieldsDialsByKey:
    dials = []
    for key, val in BROWNFIELDS_DIALS_BY_KEY.items():
        dials.append(DialByKey(key=key, dial=val.__table__.name))
    return BrownfieldsDialsByKey(dials_by_key=dials)


def get_static_image_paths_bf(image_directory_uuid: str) -> list[str]:
    images_dir = join(EnvVars.BROWNFIELDS_IMAGES_DIR, image_directory_uuid)
    paths = [
        str(
            Path(
                EnvVars.BROWFIELDS_STATIC_PATH_IMAGES,
                image_directory_uuid,
                f,
            )
        )
        for f in listdir(images_dir)
        if isfile(join(images_dir, f))
    ]
    return paths


def assign_filters_bf_query(query: Query, filters: BrownfieldsFilters):
    if filters.street is not None:
        query = query.filter(Brownfield.street.ilike("%" + filters.street + "%"))
    if filters.area_ha_max is not None:
        query = query.filter(Brownfield.area_ha <= filters.area_ha_max)
    if filters.area_ha_min is not None:
        query = query.filter(Brownfield.area_ha >= filters.area_ha_min)
    if filters.mapping_year_max is not None:
        query = query.filter(Brownfield.mapping_year <= filters.mapping_year_max)
    if filters.mapping_year_min is not None:
        query = query.filter(Brownfield.mapping_year >= filters.mapping_year_min)
    if filters.altitude_max is not None:
        query = query.filter(Brownfield.altitude <= filters.altitude_max)
    if filters.altitude_min is not None:
        query = query.filter(Brownfield.altitude >= filters.altitude_min)
    if filters.colors is not None:
        query = query.filter(Brownfield.color.has(Color.id.in_(filters.colors)))
    if filters.ownership_types is not None:
        query = query.filter(
            Brownfield.ownership_type.has(OwnershipType.id.in_(filters.ownership_types))
        )
    if filters.original_functional_utilizations is not None:
        query = query.filter(
            Brownfield.original_functional_utilization.has(
                OriginalFunctionalUtilization.id.in_(
                    filters.original_functional_utilizations
                )
            )
        )
    if filters.utilizations is not None:
        query = query.filter(
            Brownfield.utilization.has(Utilization.id.in_(filters.utilizations))
        )
    if filters.area_sizes is not None:
        query = query.filter(
            Brownfield.area_size.has(AreaSize.id.in_(filters.area_sizes))
        )
    if filters.locations is not None:
        query = query.filter(
            Brownfield.location.has(Location.id.in_(filters.locations))
        )
    if filters.degradation_levels is not None:
        query = query.filter(
            Brownfield.degradation_level.has(
                DegradationLevel.id.in_(filters.degradation_levels)
            )
        )
    if filters.residentional_area_categories is not None:
        query = query.filter(
            Brownfield.residentional_area_category.has(
                ResidentionalAreaCategory.id.in_(filters.residentional_area_categories)
            )
        )
    if filters.settlements is not None:
        query = query.filter(
            Brownfield.settlement.has(Settlement.id.in_(filters.settlements))
        )
    if filters.infrastructure_availabilities is not None:
        query = query.filter(
            Brownfield.infrastructure_availability.has(
                InfrastructureAvailability.id.in_(filters.infrastructure_availabilities)
            )
        )
    if filters.natural_and_architectural_values is not None:
        query = query.filter(
            Brownfield.natural_and_architectural_value.has(
                NaturalAndArchitecturalValue.id.in_(
                    filters.natural_and_architectural_values
                )
            )
        )
    if filters.revitalizations is not None:
        query = query.filter(
            Brownfield.revitalization.has(
                Revitalization.id.in_(filters.revitalizations)
            )
        )
    if filters.economic_potentials is not None:
        query = query.filter(
            Brownfield.economic_potential.has(
                EconomicPotential.id.in_(filters.economic_potentials)
            )
        )
    if filters.environmental_burden_inclusions is not None:
        query = query.filter(
            Brownfield.environmental_burden_inclusion.has(
                EnvironmentalBurdenInclusion.id.in_(
                    filters.environmental_burden_inclusions
                )
            )
        )
    return query
