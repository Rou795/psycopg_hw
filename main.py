import psycopg2

conn = psycopg2.connect(database='netology_hw1', user='postgres', password='Tdutybq2020')
atr_all = {'phone', 'first_name', 'last_name', 'mail'}

with conn.cursor() as cur:
    cur.execute("""
        DROP TABLE clients;
        """)
    conn.commit()

# функция создания БД

def bd_creator(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(40) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                mail TEXT UNIQUE NOT NULL,
                phone VARCHAR(12) ARRAY 
            );
            """)
        conn.commit()

# Функция добавления клиента

def add_client(conn, table: str, first_name: str, last_name: str,
               mail: str, phone: list = []):
    with conn.cursor() as cur:
        cur.execute(f"""
            INSERT INTO {table} (first_name, last_name, mail, phone)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
            """, (first_name, last_name, mail, phone))
        id_client = cur.fetchone()[0]
    print(f'Клиент {last_name} {first_name} добавлен успешно. Его id: {id_client}.')

# Функция получения телефонов клиента. Дополнительная, нужна для реализации логики
# работы с данными в этом атрибуте

def get_phone(conn, table:str, id_client: int)-> list:
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT phone FROM {table}
            WHERE id=%s;
            """, (id_client,))
        phone = cur.fetchone()
    return phone

# Функция добавления телефона существующему клиенту.
# Логика в том, чтобы получить текущий список по клиенту,
# добавить в этот список новый, удалить старые данные и записать обновленные

def add_phone(conn, table: str, phone: str, id_client: int):
    phone_old = get_phone(conn, table, id_client)
    if phone_old != None:
        phone_old = phone_old[0]
    else:
        phone_old = []
    phone_old.append(phone)
    phone_new = phone_old.copy()
    del_phone(conn, table, id_client)
    with conn.cursor() as cur:
        cur.execute(f"""
            UPDATE {table} SET phone = %s WHERE id = %s;
        """, (phone_new, id_client))
        conn.commit()
    print(f'Телефон {phone} добавлен.')

# Функция изменения данных клиента

def data_change(conn, table: str, id_client: int, atr: str, data: str):
    if atr == 'phone':
        add_phone(conn, table, data, id_client)
    elif atr in atr_all:
        with conn.cursor() as cur:
            cur.execute(f"""
                UPDATE {table} SET {atr} = %s WHERE id = %s;
            """, (data, id_client))
            conn.commit()
            print(f'Данные изменены.')
    else:
        print(f'Такого атрибута нет.')

# Удаление телефона клиента

def del_phone(conn, table: str, id_clients: int):
    phone = []
    with conn.cursor() as cur:
        cur.execute(f"""
            UPDATE {table} SET phone = %s WHERE id=%s;
        """, (phone, id_clients))
        conn.commit()
        print(f'Данные удалены.')

# Функция удаления клиента

def del_client(conn, table: str, id_client: int):
    with conn.cursor() as cur:
        cur.execute(f"""
            DELETE FROM {table} WHERE id=%s;
        """, (id_client,))
        conn.commit()
        print(f'Данные о клиенте id: {id_client} удалены')

# Функция поиска клиента

def find_client(conn, table: str, atr: str, value: str) -> int:
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT id, first_name, last_name, mail, phone FROM {table}
            WHERE {atr}=%s;
        """, (value,))
        print(cur.fetchone())

# создание базы

bd_creator(conn)

# Добавление клиентов

add_client(conn, 'clients', 'Евгений', 'Кукарский', 'jon.795@mail.ru')
add_client(conn, 'clients', 'Томас', 'Кукарский', 'jon.795555@mail.ru')

# Добавление телефона

add_phone(conn, 'clients', '1234567890', 1)

# изменение данных по клиенту

data_change(conn, 'clients', '1', 'first_name', 'Женя')
data_change(conn, 'clients', '1', 'phone', '3216549870')

# Удаление телефона клиента

del_phone(conn, 'clients', 1)

# Добавление телефона

add_phone(conn, 'clients', '1234567890', 1)

# Поиск клиента

find_client(conn, 'clients', 'first_name', 'Томас')

# Удаление клиента
del_client(conn, 'clients', 1)


conn.close()