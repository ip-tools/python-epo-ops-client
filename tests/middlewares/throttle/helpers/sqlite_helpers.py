def single_value_query(storage, *params):
    return storage.db.execute(*params).fetchone()[0]


def table_count(storage):
    sql = "SELECT COUNT(*) FROM throttle_history"
    return single_value_query(storage, sql)
