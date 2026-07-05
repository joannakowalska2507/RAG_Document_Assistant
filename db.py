import sqlite3

def get_connection():
    conn = sqlite3.connect("app.db", check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS conversations (
    conversation_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id)
        REFERENCES conversations(conversation_id)
        ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        doc_id TEXT PRIMARY KEY,
        filename TEXT,
        filepath TEXT,
        upload_time TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_document(doc_id, filename, filepath):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO documents (doc_id, filename, filepath, upload_time)
        VALUES (?, ?, ?, datetime('now'))
    """, (doc_id, filename, filepath))

    conn.commit()
    conn.close()

def get_documents():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT doc_id, filename, filepath, upload_time FROM documents")
    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "doc_id": row[0],
            "filename": row[1],
            "filepath": row[2],
            "upload_time": row[3]
        }
        for row in rows
    ]
def delete_document(doc_id):
    conn= get_connection()
    cursor= conn.cursor()
    cursor.execute("""
        DELETE FROM documents WHERE doc_id = ?
    """, (doc_id,))
    conn.commit()
    conn.close()


def save_message(conversation_id, role, content):
    conn =get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages (conversation_id, role, content)
        VALUES (?, ?, ?)
    """, (conversation_id, role, content))

    conn.commit()
    conn.close()
def save_conversation(conversation_id, title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversations (conversation_id, title)
        VALUES (?, ?)
    """, (conversation_id, title))

    conn.commit()
    conn.close()

def get_all_conversations():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT conversation_id, title, created_at
        FROM conversations
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "conversation_id": row["conversation_id"],
            "title": row["title"],
            "created_at": row["created_at"]
        }
        for row in rows
    ]
def get_conversation(conversation_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, content, created_at
        FROM messages
        WHERE conversation_id = ?
        ORDER BY created_at ASC
    """, (conversation_id,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "role": row["role"],
            "content": row["content"],
            "created_at": row["created_at"]
        }
        for row in rows
    ]
def delete_conversation(conversation_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM conversations
        WHERE conversation_id = ?
    """, (conversation_id,))

    conn.commit()
    conn.close()
def get_recent_messages(conversation_id, limit=4):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, content
        FROM messages
        WHERE conversation_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (conversation_id, limit))

    rows = cursor.fetchall()
    conn.close()

    return list(reversed(rows))


