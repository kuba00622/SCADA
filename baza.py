import mysql.connector
from mysql.connector import Error

# Funkcja do nawiązania połączenia z bazą danych
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",      # Zmień na adres serwera MySQL, jeśli używasz zdalnej bazy
            user="root",           # Zmień na swojego użytkownika MySQL
            password="password",   # Podaj hasło do bazy danych
            database="scada_db"    # Zmień na nazwę swojej bazy danych
        )

        if connection.is_connected():
            print("Połączono z bazą danych MySQL")
            return connection
    except Error as e:
        print(f"Błąd połączenia: {e}")
        return None

# Funkcja do tworzenia tabeli w bazie
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS process_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                sensor_name VARCHAR(50),
                value FLOAT
            )
        """)
        print("Tabela utworzona lub już istnieje.")
    except Error as e:
        print(f"Błąd tworzenia tabeli: {e}")

# Funkcja do wstawiania danych
def insert_data(connection, sensor_name, value):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO process_data (sensor_name, value) VALUES (%s, %s)"
        cursor.execute(query, (sensor_name, value))
        connection.commit()
        print("Dane zapisane do bazy.")
    except Error as e:
        print(f"Błąd zapisu danych: {e}")

# Funkcja do odczytu danych
def read_data(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM process_data ORDER BY timestamp DESC LIMIT 10")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Error as e:
        print(f"Błąd odczytu danych: {e}")

# Główna część programu
if __name__ == "__main__":
    conn = connect_to_db()
    if conn:
        create_table(conn)
        insert_data(conn, "Temperatura", 23.5)
        read_data(conn)
        conn.close()
        print("Połączenie zamknięte.")
