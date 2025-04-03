import psycopg2

def create_tables(cursor):
    cursor.execute("""
CREATE TABLE IF NOT EXISTS client (
id SERIAL PRIMARY KEY,
first_name VARCHAR(50) NOT NULL,
last_name VARCHAR(50) NOT NULL,
e_mail VARCHAR(50) NOT NULL UNIQUE CHECK (e_mail LIKE '%@%')
    );
    """)
    cursor.execute("""
CREATE TABLE IF NOT EXISTS client_phone(
id SERIAL PRIMARY KEY,
phone VARCHAR(20) UNIQUE NOT NULL,
client_id INT REFERENCES client(id) ON DELETE CASCADE NOT NULL
    );
    """)
    conn.commit()

def add_client(cursor, first_name, last_name, e_mail):
    cursor.execute("""
    INSERT INTO client (first_name, last_name, e_mail) VALUES (%s, %s, %s);
    """,(first_name, last_name, e_mail))
    conn.commit()

def add_phone(cursor, client_id, phone):
    cursor.execute("""
    INSERT INTO client_phone (phone, client_id) VALUES (%s, %s);
    """,(phone, client_id))
    conn.commit()

def change_client(cursor, id, first_name=None, last_name=None, e_mail=None, phone=None):
    for attr, value in zip(("first_name", "last_name", "e_mail"),(first_name, last_name, e_mail)):
        if value:
            cursor.execute("""
            UPDATE client SET """ + f'{attr}' + """ = %s WHERE id = %s;
            """,(  value, id))
    conn.commit()
    if phone:
        add_phone(cursor, id, phone)

def del_phone(cursor, id, phone = None):
    if phone:
        cursor.execute('DELETE FROM client_phone WHERE client_id = %s and phone = %s;',(id, phone))
    else:
        cursor.execute('DELETE FROM client_phone WHERE client_id = %s;',(id,))
    conn.commit()

def del_client(cursor, id):
    cursor.execute('DELETE FROM client WHERE id = %s;',(id,))
    conn.commit()

def find_client(cursor, first_name=None, last_name=None, e_mail=None, phone=None):   
    if  not first_name and not last_name and not e_mail and not phone:
        return 'Нет данных для поиска'
    if phone:
        cursor.execute('SELECT * FROM client WHERE id in (SELECT client_id FROM client_phone where phone = %s);',(phone,))
        return cursor.fetchall()
    for attr, value in zip(("first_name", "last_name", "e_mail"),(first_name, last_name, e_mail)):
            if value:
                cursor.execute('SELECT * FROM client WHERE ' + f'{attr}' + ' = %s;',(value,))
                return cursor.fetchall()


conn = psycopg2.connect(database="homework_music", user="postgres", password='iswms')

with conn.cursor() as cur:
    create_tables(cur)
    # add_client(cur, 'Alexander', 'Ovechkin', 'alexthegr8@nhl.com')
    # add_phone(cur, 1, '555')  
    # change_client(cur, 3, first_name='Alex', phone = '911', e_mail='alexanderthegr8@nhl.com')
    # del_phone(cur, 1)
    # del_client(cur, 3)
    print(find_client(cur))
conn.close()