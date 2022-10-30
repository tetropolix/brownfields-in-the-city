from sqlalchemy.orm import Session
from sqlalchemy import select

from src.database.brownfield_models import AreaSize, DegradationLevel, EconomicPotential, EnvironmentalBurdenInclusion, InfrastructureAvailability, Location, NaturalAndArchitecturalValue, OriginalFunctionalUtilization, OwnershipType, ResidentionalAreaCategory, Revitalization, Settlement, Utilization

def get_form_lookup_values(session: Session):
    stmt = select(OwnershipType.id,OwnershipType.value,
                  OriginalFunctionalUtilization.id,OriginalFunctionalUtilization.value,
                  Utilization.id,Utilization.value,
                  AreaSize.id,AreaSize.value,
                  Location.id,Location.value,
                  DegradationLevel.id,DegradationLevel.value,
                  ResidentionalAreaCategory.id,ResidentionalAreaCategory.value,
                  Settlement.id,Settlement.value,
                  InfrastructureAvailability.id,InfrastructureAvailability.value,
                  NaturalAndArchitecturalValue.id,NaturalAndArchitecturalValue.value,
                  Revitalization.id,Revitalization.value,
                  EconomicPotential.id,EconomicPotential.value,
                  EnvironmentalBurdenInclusion.id,EnvironmentalBurdenInclusion.value)
    return session.execute(stmt)