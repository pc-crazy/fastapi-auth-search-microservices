# from sqlalchemy import create_engine, text
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# DATABASE_URL = os.getenv("SEARCH_SERVICE_DATABASE_URL")
# engine = create_engine(DATABASE_URL)
#
# index_statements = [
#     # Employee indexes
#     "CREATE INDEX IF NOT EXISTS idx_employee_org_id ON employee (org_id);",
#     "CREATE INDEX IF NOT EXISTS idx_employee_status ON employee (status);",
#     "CREATE INDEX IF NOT EXISTS idx_employee_first_name ON employee (first_name);",
#     "CREATE INDEX IF NOT EXISTS idx_employee_last_name ON employee (last_name);",
#     "CREATE INDEX IF NOT EXISTS idx_employee_location_id ON employee (location_id);",
#     "CREATE INDEX IF NOT EXISTS idx_employee_company_id ON employee (company_id);",
#     "CREATE INDEX IF NOT EXISTS idx_employee_department_id ON employee (department_id);",
#     "CREATE INDEX IF NOT EXISTS idx_employee_position_id ON employee (position_id);",
#
#     # Department
#     "CREATE INDEX IF NOT EXISTS idx_department_name ON department (name);",
#
#     # Company
#     "CREATE INDEX IF NOT EXISTS idx_company_name ON company (name);",
#
#     # Position
#     "CREATE INDEX IF NOT EXISTS idx_position_name ON position (name);",
#
#     # Location
#     "CREATE INDEX IF NOT EXISTS idx_location_name ON location (name);"
# ]
#
# with engine.begin() as conn:
#     for stmt in index_statements:
#         conn.execute(text(stmt))
#         print(f"Executed: {stmt}")
