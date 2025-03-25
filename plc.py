import snap7
from snap7.util import *

# Tworzenie klienta
client = snap7.client.Client()

try:
    client.connect('192.168.0.1', 0, 1)
    if client.get_connected():
        print("Połączono z PLC")
        data = client.db_read(1, 0, 4)
        value = get_real(data, 0)
        print(f"Odczytana wartość: {value}")
    else:
        print("Nie udało się połączyć z PLC")
except Exception as e:
    print(f"Błąd połączenia: {e}")
finally:
    client.disconnect()


# Zamykanie połączenia
client.disconnect()