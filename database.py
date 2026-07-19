import sqlite3

conn = sqlite3.connect("chat_history.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    message TEXT
)
""")

conn.commit()


def save_message(role, message):
    cursor.execute(
        "INSERT INTO chats(role, message) VALUES (?, ?)",
        (role, message)
    )
    conn.commit()


def load_messages():
    cursor.execute(
        "SELECT role, message FROM chats"
    )

    rows = cursor.fetchall()

    return [
        {
            "role": row[0],
            "content": row[1]
        }
        for row in rows
    ]


def clear_messages():
    cursor.execute("DELETE FROM chats")
    conn.commit()