from pydantic import BaseModel 

class FormFields(BaseModel):
    ownership_types : dict[int,str]
    original_functional_utilizations : dict[int,str]
    utilizations : dict[int,str]
    area_sizes : dict[int,str]
    locations : dict[int,str]
    degradation_levels : dict[int,str]
    residentional_area_categories : dict[int,str]
    settlements : dict[int,str]
    infrastructure_availabilities : dict[int,str]
    natural_and_architectural_values : dict[int,str]
    revitalizations : dict[int,str]
    economic_potentials : dict[int,str] | None # TO DO
    environmental_burden_inclusions : dict[int,str] | None # TO DO

class BrownfieldID(BaseModel):
    id: int

class NewBrownfield(BaseModel):
    street = str
    area_ha = float
    mapping_year = int
    altitude : float
    ownership_type_id : int
    original_functional_utilization_id : int
    utilization_id : int
    area_size_id : int
    location_id : int
    degradation_level_id : int
    residentional_area_category_id : int
    settlement_id : int
    infrastructure_availability_id : int
    natural_and_architectural_value_id : int
    revitalization_id : int
    economic_potential_id : int | None # TO DO
    environmental_burden_inclusion_id : int | None # TO DO