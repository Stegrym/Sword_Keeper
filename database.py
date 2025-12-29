import sqlite3
from typing import List, Optional, Tuple


class Database:

    def __init__(self, db_path: str = "passwords.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Создание таблицы если её нет"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service TEXT NOT NULL,
                    username TEXT NOT NULL,
                    encrypted_password BLOB NOT NULL,
                    url TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                )
            ''')
        # Индекс для поиска
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_service
            ON passwords (service)
        ''')
        conn.commit()

    def add_password(self, service: str, username: str, encrypted_password: bytes, url: str = '',
                     notes: str = '') -> int:
        """ Добавляет запись, возвращает её ID"""
        service_normalized = service.strip().lower()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO passwords (service, username, encrypted_password, url, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (service_normalized, username, encrypted_password, url, notes))
            conn.commit()
            return cursor.lastrowid

    def get_all_password(self) -> List[Tuple]:
        """Возвращает все пароли без расшифровки"""

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row  # Получение доступа к полям по имени
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, service, username, url, notes, created_at, updated_at
                FROM  passwords
                ORDER by service, username
                """)
            return cursor.fetchall()

    def get_password_by_id(self, record_id: int) -> Optional[Tuple]:
        """Возвращает запись по ID"""

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM passwords WHERE id = ?
            ''', (record_id,))
            return cursor.fetchone()

    def get_encrypted_password(self, record_id: int) -> Optional[bytes]:
        """Возвращает зашифрованный пароль по id"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT encrypted_password FROM passwords WHERE id = ?
                ''', (record_id,))
            result = cursor.fetchone()
            return result[0] if result else None

    def update_password(self, record_id: int, service: str, username: str, encrypted_password: bytes, url: str = '',
                        notes: str = '') -> bool:
        """Обновление записи по record_id"""

        service_normalized = service.strip().lower()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE passwords
                SET service = ?,
                    username = ?,
                    encrypted_password = ?,
                    url = ?,
                    notes = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                ''', (service_normalized, username, encrypted_password, url, notes, record_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_password(self, record_id: int) -> bool:
        """Удаляет данные по ID"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM passwords WHERE id = ?', (record_id,))
            conn.commit()
            return cursor.rowcount > 0

    def search_password(self, search_term: str) -> List[Tuple]:
        """Поиск по service, username , note"""

        service_normalized = search_term.strip().lower()
        search_pattern = f"%{service_normalized}%"

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''  
                SELECT id, service, username, url, notes, created_at, updated_at
                FROM passwords
                WHERE service LIKE ? OR username LIKE ? OR notes LIKE ?
                ORDER BY service, username
            ''', (search_pattern, search_pattern, search_pattern))
            return cursor.fetchall()

    def get_service_list(self) -> List[str]:
        """Возвращает список уникальных сервисов"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT service FROM passwords ORDER BY service')
            return [row[0] for row in cursor.fetchall()]
