import sqlite3
from config import DATABASE

class DB_Manager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_table()

    def create_connection(self):
        conn = sqlite3.connect(self.db_path)
        return conn

    def create_table(self):
        with self.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    description TEXT,
                    id_of_question INTEGER,
                    status TEXT,
                    user_id INTEGER
                )
            ''')
            conn.commit()

    def add_question(self, name, description, id_of_question, status, user_id):
        with self.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO questions (name, description, id_of_question, status, user_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, description, id_of_question, status, user_id))
            conn.commit()

    def get_questions(self, user_id):
        with self.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, description, id_of_question, status, user_id
                FROM questions
                WHERE user_id = ?
            ''', (user_id,))
            return cursor.fetchall()

    def delete_question(self, question_id):
        with self.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM questions WHERE id = ?', (question_id,))
            conn.commit()

if __name__ == "__main__":
    db_manager = DB_Manager(DATABASE)
    db_manager.create_tables()
