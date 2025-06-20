"""
Script para crear la tabla uploaded_files en SQLite manualmente.
"""
import sqlite3

DB_PATH = "leones.db"  # Cambia si tu base es app.db

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS uploaded_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    categoria TEXT NOT NULL,
    descripcion TEXT,
    proyecto TEXT NOT NULL DEFAULT 'demo_metasketch',
    upload_time DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    conn.close()
    print("Tabla uploaded_files creada o verificada correctamente.")

if __name__ == "__main__":
    main()
