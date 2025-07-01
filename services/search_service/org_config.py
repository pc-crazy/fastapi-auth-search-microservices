ORG_COLUMN_CONFIG = {
    1: ["first_name", "last_name", "status", "contact", "location", "company", "department", "position"],
    2: ["first_name", "department", "location", "position"],
}


def get_org_columns(org_id: int) -> list[str]:
    return ORG_COLUMN_CONFIG.get(org_id, [])
