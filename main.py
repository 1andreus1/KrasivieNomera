import sqlite3

db = 'cgi-bin/sitebase.db'


class DataConn:

    def __init__(self, db_name):
        """Конструктор"""
        self.db_name = db_name

    def __enter__(self):
        """Открываем подключение с базой данных."""
        self.conn = sqlite3.connect(self.db_name)
        self.conn.load_extension("/usr/lib/sqlite3/pcre.so")
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Закрываем подключение."""
        self.conn.close()
        if exc_val:
            raise


def check(letters="...", digits="...", region="..", full_word=True):
    for i in letters:
        if (i == '.' and full_word) or i not in ('А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х', '.'):
            raise ValueError("Letters")

    for i in digits:
        if (i == '.' and full_word) or (not i.isdigit() and i != '.'):
            raise ValueError("Digits")

    for i in region:
        if (i == '.' and full_word) or (not i.isdigit() and i != '.'):
            raise ValueError("Region")


def filter(letters="...", digits="...", region="."):
    try:
        check(letters, digits, region, False)
    except ValueError:
        return ValueError
    else:
        with DataConn(db) as conn:
            cursor = conn.cursor()
            if region == ".":
                cursor.execute("SELECT * FROM numbers WHERE letters REGEXP ? AND digits REGEXP ? AND region REGEXP ?",
                               ('^' + letters, '^' + digits, region + '$'))
            else:
                cursor.execute("SELECT * FROM numbers WHERE letters REGEXP ? AND digits REGEXP ? AND region REGEXP ?",
                               ('^' + letters, '^' + digits, '^' + region + '$'))
            results = cursor.fetchall()
            return results


def add_number(letters, digits, region, cost):
    try:
        check(letters, digits, region, True)
    except ValueError:
        return ValueError
    else:
        with DataConn(db) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO numbers(letters, digits, region, cost) VALUES (?, ?, ?, ?)", (letters, digits, region, cost))
            conn.commit()
        return True


def delete_number(idx):
    with DataConn(db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM numbers WHERE idx=?", (idx,))
        if cursor.fetchall():
            cursor.execute("DELETE FROM numbers WHERE idx=?", (idx, ))
            conn.commit()
            return True
        return False


if __name__ == '__main__':
    with DataConn(db) as conn:
        cursor = conn.cursor()
        print(filter("...", "...", "."))
