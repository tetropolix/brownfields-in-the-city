from pydantic import BaseModel


class BrownfieldColorDial(BaseModel):
    id: int
    name: str
    hex_value: str


class BrownfieldsDials(BaseModel):
    colors: list[BrownfieldColorDial]
    ownership_types: dict[int, str]
    original_functional_utilizations: dict[int, str]
    utilizations: dict[int, str]
    area_sizes: dict[int, str]
    locations: dict[int, str]
    degradation_levels: dict[int, str]
    residentional_area_categories: dict[int, str]
    settlements: dict[int, str]
    infrastructure_availabilities: dict[int, str]
    natural_and_architectural_values: dict[int, str]
    revitalizations: dict[int, str]
    economic_potentials: dict[int, str] | None  # TO DO
    environmental_burden_inclusions: dict[int, str] | None  # TO DO


class BrownfieldsFilters(BaseModel):
    street: str | None
    area_ha_max: int | None
    area_ha_min: int | None
    mapping_year_max: int | None
    mapping_year_min: int | None
    altitude_max: int | None
    altitude_min: int | None
    colors: list[int] | None
    ownership_types: list[int] | None
    original_functional_utilizations: list[int] | None
    utilizations: list[int] | None
    area_sizes: list[int] | None
    locations: list[int] | None
    degradation_levels: list[int] | None
    residentional_area_categories: list[int] | None
    settlements: list[int] | None
    infrastructure_availabilities: list[int] | None
    natural_and_architectural_values: list[int] | None
    revitalizations: list[int] | None
    economic_potentials: list[int] | None
    environmental_burden_inclusions: list[int] | None


class AvailableBrownfieldsFilters(BrownfieldsDials):
    area_ha_max: float | None = None
    area_ha_min: float | None = None
    mapping_year_max: int | None = None
    mapping_year_min: int | None = None
    altitude_max: float | None = None
    altitude_min: float | None = None


class BrownfieldID(BaseModel):
    id: int


class NewBrownfield(BaseModel):
    street: str
    area_ha: float
    mapping_year: int
    altitude: float
    color_id: int
    ownership_type_id: int
    original_functional_utilization_id: int
    utilization_id: int
    area_size_id: int
    location_id: int
    degradation_level_id: int
    residentional_area_category_id: int
    settlement_id: int
    infrastructure_availability_id: int
    natural_and_architectural_value_id: int
    revitalization_id: int
    economic_potential_id: int | None  # TO DO
    environmental_burden_inclusion_id: int | None  # TO DO


class BrownfieldCore(BaseModel):
    id: int
    street: str
    area_ha: float
    mapping_year: int
    altitude: float
    ownership_type: str
    image_urls: str | None


class Brownfield(BrownfieldCore):
    color: BrownfieldColorDial
    original_functional_utilization: str
    utilization: str
    area_size: str
    location: str
    degradation_level: str
    residentional_area_category: str
    settlement: str
    infrastructure_availability: str
    natural_and_architectural_value: str
    revitalization: str
    economic_potential: str | None  # TO DO
    environmental_burden_inclusion: str | None  # TO DO
    image_urls: list[str]
