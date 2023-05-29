import psycopg2

from face_recognizer import FaceRecognizer


class DB_interactor:

    connection = psycopg2.connect(dbname='postgres', user = 'postgres', password = 'postgres', host = 'localhost')
    cursor = connection.cursor()

    @staticmethod
    def setup():
        DB_interactor.cursor.execute(
            'CREATE TABLE users ('
            'id  SERIAL PRIMARY KEY, '
            'name text'
            ');'
            'CREATE TABLE rooms ('
            'id  SERIAL PRIMARY KEY, '
            'name text'
            '); '
            'CREATE TABLE user_embedding_vector ('
            'user_id INT NOT NULL,'
            'embedding float8[128],'
            'CONSTRAINT user_id FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE'
            ');'
            'CREATE TABLE access ('
            'room_id INT NOT NULL,'
            'user_id INT NOT NULL,'
            'last_access timestamp,'
            'CONSTRAINT user_id FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,'
            'CONSTRAINT room_id FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE'
            ');'
        )
        DB_interactor.connection.commit()
        return 'Готово'

    @staticmethod
    def show():
        pass

    @staticmethod
    def add_user(name, path):
        vector = FaceRecognizer.get_vector(path)
        arr = ", ".join([str(i) for i in vector]).join(['{', '}'])
        DB_interactor.cursor.execute(
            "INSERT INTO users (name) VALUES ('{}')".format(name)
        )
        DB_interactor.cursor.execute(
            "INSERT INTO user_embedding_vector VALUES ("
            "(select id from users where name = '{}' limit 1)"
            ",'{}')"
                .format(name, arr)
        )
        DB_interactor.connection.commit()
        return 'Готово'

    @staticmethod
    def remove_user(iid):
        DB_interactor.cursor.execute(
            "DELETE FROM users WHERE id = '{}';".format(iid)
        )
        DB_interactor.connection.commit()
        return 'Готово'

    @staticmethod
    def add_room(name):
        DB_interactor.cursor.execute(
            "INSERT INTO rooms(name) VALUES ('{}')".format(name)
        )
        DB_interactor.connection.commit()
        return 'Готово'

    @staticmethod
    def remove_room(id):
        DB_interactor.cursor.execute(
            "DELETE FROM rooms WHERE id = '{}';".format(id)
        )
        DB_interactor.connection.commit()
        return 'Готово'

    @staticmethod
    def grant_access(user_id, room_id):
        DB_interactor.cursor.execute(
            "INSERT INTO access VALUES ('{}', '{}')".format(room_id, user_id)
        )
        DB_interactor.connection.commit()
        return 'Готово'

    @staticmethod
    def remove_access(room_id, user_id):
        DB_interactor.cursor.execute(
            "delete from access where (room_id='{}' and user_id='{}')".format(room_id, user_id)
        )
        DB_interactor.connection.commit()
        return 'Готово'

    @staticmethod
    def load_all():
        DB_interactor.cursor.execute(
            '''
            SELECT users.name, user_embedding_vector.embedding FROM users JOIN user_embedding_vector ON users.id = user_embedding_vector.user_id;
            ''')
        return DB_interactor.cursor.fetchall()

    @staticmethod
    def red_button_drop_all():
        DB_interactor.cursor.execute(
            "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
        )
        DB_interactor.connection.commit()
        return 'Готово'

def run(func, args):
    r = 'Слишком много аргументов'
    if len(args) == 0:
        r = func()
    elif len(args) == 1:
        r = func(args[0])
    elif len(args) == 2:
        r = func(args[0], args[1])
    print(r)

if __name__ == '__main__':
    command_line_comands = {'setup': DB_interactor.setup,
                            'add_user': DB_interactor.add_user,
                            'remove_user': DB_interactor.remove_user,
                            'add_room': DB_interactor.add_room,
                            'remove_room': DB_interactor.remove_room,
                            'grant_access': DB_interactor.grant_access,
                            'remove_access': DB_interactor.remove_access,
                            'drop': DB_interactor.red_button_drop_all,
                            'exit': quit
                            }
    print('Это модуль управления базами данных')

    while True:
        comm = (input('Введите команду: ')).split(' ')
        try:
            run(
                command_line_comands[comm[0]], comm[1:]
            )
        except Exception as e:
            print(repr(e))
#     test remaining:   show load_all


