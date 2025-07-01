from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    employees = relationship("Employee", back_populates="location")


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    employees = relationship("Employee", back_populates="company")


class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    employees = relationship("Employee", back_populates="department")


class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    employees = relationship("Employee", back_populates="position")


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, index=True)
    first_name = Column(String)
    last_name = Column(String)
    contact = Column(String)
    status = Column(Integer, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    position_id = Column(Integer, ForeignKey("positions.id"))

    location = relationship("Location", back_populates="employees")
    company = relationship("Company", back_populates="employees")
    department = relationship("Department", back_populates="employees")
    position = relationship("Position", back_populates="employees")
