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
