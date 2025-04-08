def get_conn_string():
    username = "admin"          # Hardcoded username
    password = "SingingBananaPie1238"   # Hardcoded password
    host = "kiwi-analytics-db.cx64gs48yq90.us-east-2.rds.amazonaws.com"         # Hardcoded host
    port = "3306"              # Hardcoded port
    database = "Kiwi-Analytics-DB"   # Hardcoded database name

    return f"mysql://{username}:{password}@{host}:{port}/{database}"