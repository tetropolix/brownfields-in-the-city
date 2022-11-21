from sqlalchemy import ForeignKey,Integer,Column,String,Float,Numeric
from sqlalchemy.orm import relationship
from .database import Base

class Brownfield(Base):
    __tablename__ = "brownfields"
    __table_args__ = {"schema":"brownfields"}
    id = Column(Integer,primary_key=True,index=True)
    image_directory_uuid = Column(String(128),index=True,nullable=False)
    street = Column(String(256),nullable=False)
    area_ha = Column(Numeric(12,4),nullable=False)
    mapping_year = Column(Integer,nullable=False)
    altitude = Column(Float(precision=4),nullable=False)

    ownership_type_id = Column(Integer,ForeignKey("brownfields.ownership_types.id"),nullable=False)
    original_functional_utilization_id = Column(Integer,ForeignKey("brownfields.original_functional_utilizations.id"),nullable=False)
    utilization_id = Column(Integer,ForeignKey("brownfields.utilizations.id"),nullable=False)
    area_size_id = Column(Integer,ForeignKey("brownfields.area_sizes.id"),nullable=False)
    location_id = Column(Integer,ForeignKey("brownfields.locations.id"),nullable=False)
    degradation_level_id = Column(Integer,ForeignKey("brownfields.degradation_levels.id"),nullable=False)
    residentional_area_category_id = Column(Integer,ForeignKey("brownfields.residentional_area_categories.id"),nullable=False)
    settlement_id = Column(Integer,ForeignKey("brownfields.settlements.id"),nullable=False)
    infrastructure_availability_id = Column(Integer,ForeignKey("brownfields.infrastructure_availabilities.id"),nullable=False)
    natural_and_architectural_value_id = Column(Integer,ForeignKey("brownfields.natural_and_architectural_values.id"),nullable=False)
    revitalization_id = Column(Integer,ForeignKey("brownfields.revitalizations.id"),nullable=False)
    economic_potential_id = Column(Integer,ForeignKey("brownfields.economic_potentials.id"))
    environmental_burden_inclusion_id = Column(Integer,ForeignKey("brownfields.environmental_burden_inclusions.id"))

    ownership_type = relationship("OwnershipType",back_populates = "brownfields", lazy="joined")
    original_functional_utilization = relationship("OriginalFunctionalUtilization",back_populates = "brownfields", lazy="joined")
    utilization = relationship("Utilization",back_populates = "brownfields", lazy="joined")
    area_size = relationship("AreaSize",back_populates = "brownfields", lazy="joined")
    location = relationship("Location",back_populates = "brownfields", lazy="joined")
    degradation_level = relationship("DegradationLevel",back_populates = "brownfields", lazy="joined")
    residentional_area_category = relationship("ResidentionalAreaCategory",back_populates = "brownfields", lazy="joined")
    settlement = relationship("Settlement",back_populates = "brownfields", lazy="joined")
    infrastructure_availability = relationship("InfrastructureAvailability",back_populates = "brownfields", lazy="joined")
    natural_and_architectural_value = relationship("NaturalAndArchitecturalValue",back_populates = "brownfields", lazy="joined")
    revitalization = relationship("Revitalization",back_populates = "brownfields", lazy="joined")
    economic_potential = relationship("EconomicPotential",back_populates = "brownfields", lazy="joined")
    environmental_burden_inclusion = relationship("EnvironmentalBurdenInclusion",back_populates = "brownfields", lazy="joined")



    def __repr__(self):
        return f"""
                {self.id}, 
                {self.street}, 
                {self.area_ha}, 
                {self.mapping_year}, 
                {self.altitude}, 
                {self.ownership_type_id}, 
                {self.original_functional_utilization_id}, 
                {self.utilization_id}, 
                {self.area_size_id}, 
                {self.location_id}, 
                {self.degradation_level_id}, 
                {self.residentional_area_category_id}, 
                {self.settlement_id}, 
                {self.infrastructure_availability_id}, 
                {self.natural_and_architectural_value_id}, 
                {self.revitalization_id}, 
                {self.economic_potential_id}, 
                {self.environmental_burden_inclusion_id}, 
                """

### Lookup tables
### Note: 1.ONDELETE for child tables (child tables of lookup tables below) is not specified = default = prevent from deleting if some child references it
### ..... -> for now, this seems to be requested feature
###       2. Lazy parameter for Lookup tables (relationship to brownfields) uses default "select" value which loads brownfields lazily

class OwnershipType(Base):
    __tablename__="ownership_types"
    __table_args__ = {"schema":"brownfields"}
    id = Column(Integer,primary_key=True,index=True)
    value=Column(String(128),unique=True,nullable=False)

    brownfields = relationship("Brownfield",back_populates="ownership_type")

    def __repr__(self):
        return f"Ownership type (id = {self.id}) with value = {self.value}"


class OriginalFunctionalUtilization(Base):
    __tablename__="original_functional_utilizations"
    __table_args__ = {"schema":"brownfields"}
    id = Column(Integer,primary_key=True,index=True)
    value=Column(String(256),unique=True,nullable=False)

    brownfields = relationship("Brownfield",back_populates="original_functional_utilization")

    def __repr__(self):
        return f"Original functional utilizations (id = {self.id}) with value = {self.value}"


class Utilization(Base):
    __tablename__="utilizations"
    __table_args__ = {"schema":"brownfields"}
    id = Column(Integer,primary_key=True,index=True)
    value=Column(String(256),unique=True,nullable=False)

    brownfields = relationship("Brownfield",back_populates="utilization")

    def __repr__(self):
        return f"Utilization (id = {self.id}) with value = {self.value}"


class AreaSize(Base):
    __tablename__="area_sizes"
    __table_args__ = {"schema":"brownfields"}
    id = Column(Integer,primary_key=True,index=True)
    value=Column(String(128),unique=True,nullable=False)

    brownfields = relationship("Brownfield",back_populates="area_size")

    def __repr__(self):
        return f"Area size (id = {self.id}) with value = {self.value}"


class Location(Base):
    __tablename__="locations"
    __table_args__ = {"schema":"brownfields"}
    id = Column(Integer,primary_key=True,index=True)
    value=Column(String(256),unique=True,nullable=False)

    brownfields = relationship("Brownfield",back_populates="location")

    def __repr__(self):
        return f"Location (id = {self.id}) with value = {self.value}"


class DegradationLevel(Base):
    __tablename__="degradation_levels"
    __table_args__ = {"schema":"brownfields"}
    id = Column(Integer,primary_key=True,index=True)
    value=Column(String(256),unique=True,nullable=False)

    brownfields = relationship("Brownfield",back_populates="degradation_level")

    def __repr__(self):
        return f"Level of degradation (id = {self.id}) with value = {self.value}"


class ResidentionalAreaCategory(Base):
    __tablename__="residentional_area_categories"
    __table_args__ = {"schema":"brownfields"}
    id = Column(Integer,primary_key=True,index=True)
    value=Column(String(256),unique=True,nullable=False)

    brownfields = relationship("Brownfield",back_populates="residentional_area_category")

    def __repr__(self):
        return f"Residentional area category (id = {self.id}) with value = {self.value}"


class Settlement(Base):
    __tablename__="settlements"
    __table_args__ = {"schema":"brownfields"}
    id = Column(Integer,primary_key=True,index=True)
    value=Column(String(256),unique=True,nullable=False)

    brownfields = relationship("Brownfield",back_populates="settlement")

    def __repr__(self):
        return f"Settlement category (id = {self.id}) with value = {self.value}"


class InfrastructureAvailability(Base):
    __tablename__="infrastructure_availabilities"
    __table_args__ = {"schema":"brownfields"}
    id = Column(Integer,primary_key=True,index=True)
    value=Column(String(256),unique=True,nullable=False)

    brownfields = relationship("Brownfield",back_populates="infrastructure_availability")

    def __repr__(self):
        return f"Infrastructure availability category (id = {self.id}) with value = {self.value}"


class NaturalAndArchitecturalValue(Base):
    __tablename__="natural_and_architectural_values"
    __table_args__ = {"schema":"brownfields"}
    id = Column(Integer,primary_key=True,index=True)
    value=Column(String(256),unique=True,nullable=False)

    brownfields = relationship("Brownfield",back_populates="natural_and_architectural_value")

    def __repr__(self):
        return f"Atural and architectural value category (id = {self.id}) with value = {self.value}"


class Revitalization(Base):
    __tablename__="revitalizations"
    __table_args__ = {"schema":"brownfields"}
    id = Column(Integer,primary_key=True,index=True)
    value=Column(String(256),unique=True,nullable=False)

    brownfields = relationship("Brownfield",back_populates="revitalization")

    def __repr__(self):
        return f"Revitalization category (id = {self.id}) with value = {self.value}"


class EconomicPotential(Base):
    __tablename__="economic_potentials"
    __table_args__ = {"schema":"brownfields"}
    id = Column(Integer,primary_key=True,index=True)
    value=Column(String(256),unique=True,nullable=True) ## TO DO - value is nullable because eventual values = TBA

    brownfields = relationship("Brownfield",back_populates="economic_potential")

    def __repr__(self):
        return f"Economic potential category (id = {self.id}) with value = {self.value}"


class EnvironmentalBurdenInclusion(Base):
    __tablename__="environmental_burden_inclusions"
    __table_args__ = {"schema":"brownfields"}
    id = Column(Integer,primary_key=True,index=True)
    value=Column(String(256),unique=True,nullable=True) ## TO DO - value is nullable because eventual values = TBA

    brownfields = relationship("Brownfield",back_populates="environmental_burden_inclusion")

    def __repr__(self):
        return f"Environmental burden inclusions category (id = {self.id}) with value = {self.value}"
