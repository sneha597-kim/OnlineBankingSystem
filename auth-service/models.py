from database import get_db_connection

def add_user(fullname, email, username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (fullname, email, username, password) VALUES (?, ?, ?, ?)",
            (fullname, email, username, password)
        )
        conn.commit()
        return True
    except Exception as e:
        print("Error inserting user:", e)
        return False
    finally:
        conn.close()

def get_user(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    conn.close()
    return user
