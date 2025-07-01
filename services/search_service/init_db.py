# from .models import Base, Location, Company, Department, Position, Employee
# from .db import engine, SessionLocal
#
# Base.metadata.create_all(bind=engine)
# db = SessionLocal()
#
# # Seed lookup tables
# locations = [Location(name="Delhi"), Location(name="Mumbai")]
# companies = [Company(name="Google"), Company(name="TCS")]
# departments = [Department(name="Engineering"), Department(name="HR")]
# positions = [Position(name="Developer"), Position(name="Manager")]
#
# db.add_all(locations + companies + departments + positions)
# db.commit()
#
# # Helper function to get ids
# def get_id_by_name(model, name):
#     return db.query(model).filter(model.name == name).first().id
#
# # Seed Employees
# employees = [
#     Employee(
#         org_id=1,
#         first_name="John",
#         last_name="Doe",
#         status=1,  # active
#         contact="alice.smith@example.com",
#         location_id=get_id_by_name(Location, "Delhi"),
#         company_id=get_id_by_name(Company, "Google"),
#         department_id=get_id_by_name(Department, "Engineering"),
#         position_id=get_id_by_name(Position, "Developer"),
#     ),
#     Employee(
#         org_id=1,
#         first_name="Alice",
#         last_name="Smith",
#         contact="john.doe@example.com",
#         status=2,  # not started
#         location_id=get_id_by_name(Location, "Mumbai"),
#         company_id=get_id_by_name(Company, "TCS"),
#         department_id=get_id_by_name(Department, "HR"),
#         position_id=get_id_by_name(Position, "Manager"),
#     ),
# ]
#
# db.add_all(employees)
# db.commit()
#
# print("search_service database initialized successfully.")
