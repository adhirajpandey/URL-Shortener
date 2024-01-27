import database.dao as dao

DB_FILE = "database/database.db"

db = dao.create_connection(DB_FILE)
dao.create_table(db)
