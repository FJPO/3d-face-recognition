import psycopg2

class DB_interactor:

    connection = psycopg2.connect(dbname='postgres', user = 'postgres', password = 'postgres', host = 'localhost')
    cursor = connection.cursor()

    @staticmethod
    def setup():
        DB_interactor.cursor.execute(
            'CREATE TABLE users ('
            'name            text,'
            'vector float8[128] PRIMARY KEY'
            ');'
        )
        DB_interactor.connection.commit()

    @staticmethod
    def add_faces(name, vector):
        arr = ", ".join([str(i) for i in vector]).join(['{', '}'])
        DB_interactor.cursor.execute(
            "INSERT INTO users VALUES ('{}', '{}')".format(name, arr)
        )
        DB_interactor.connection.commit()

    @staticmethod
    def load_all():
        DB_interactor.cursor.execute(
            '''
            SELECT * FROM USERS
            ''')
        return DB_interactor.cursor.fetchall()

if __name__ == '__main__':
    print('Это модуль управления бахами данных')
