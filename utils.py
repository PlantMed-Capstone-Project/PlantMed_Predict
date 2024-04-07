from pyodbc import Cursor


def get_by_name(name: str, sql: Cursor) -> dict:
    sql.execute("SELECT * FROM Plant WHERE name = ?", (name,))
    row = sql.fetchone()
    response = {
        "id": row.id.lower(),
        "name": row.name,
        "internationalName": row.international_name,
        "surName": row.sur_name,
        "placeOfBirth": row.place_of_birth,
        "shopBase": row.shop_base,
        "origin": row.origin,
        "usage": row.usage,
    }
    return response


def format(results: list) -> float:
    if not results:
        return 0.0

    map = {}
    for rs in results:
        if rs in map:
            map[rs] += 1
        else:
            map[rs] = 1

    if not map:
        return 0.0

    max_value = max(map.values())

    percentage = (max_value / len(results)) * 100
    return round(percentage, 2) if percentage else 0.0

def save(data: dict, sql: Cursor):
    pass