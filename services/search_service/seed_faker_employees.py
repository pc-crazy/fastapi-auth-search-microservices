# from faker import Faker
# from sqlalchemy.orm import Session
# from .db import SessionLocal
# from .models import Employee
# import random
#
# fake = Faker()
# db: Session = SessionLocal()
#
# # Assuming these FK tables already have at least 2 records each with ids 1 and 2
# location_ids = [1, 2]
# company_ids = [1, 2]
# department_ids = [1, 2]
# position_ids = [1, 2]
# status_choices = [1, 2, 3]  # 1=active, 2=not started, 3=terminated
#
# BATCH_SIZE = 500
# TOTAL = 5000
#
# employees = []
#
# for i in range(1, TOTAL + 1):
#     emp = Employee(
#         org_id=1,
#         first_name=fake.name(),
#         last_name=fake.name(),
#         contact=fake.email(),
#         status=random.choice(status_choices),
#         location_id=random.choice(location_ids),
#         company_id=random.choice(company_ids),
#         department_id=random.choice(department_ids),
#         position_id=random.choice(position_ids)
#     )
#     employees.append(emp)
#
#     # Insert in batches
#     if i % BATCH_SIZE == 0:
#         db.bulk_save_objects(employees)
#         db.commit()
#         print(f"Inserted {i} records...")
#         employees = []
#
# # Insert remaining
# if employees:
#     db.bulk_save_objects(employees)
#     db.commit()
#     print(f"Inserted final {len(employees)} records.")
#
# db.close()
# print("5000 fake employees inserted.")
