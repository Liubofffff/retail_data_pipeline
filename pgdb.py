import psycopg2

# Класс для работы с PostgreSQL базой данных
class PGDatabase:
    # Соединение с БД и настройка курсора
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

        self.connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

        self.cursor = self.connection.cursor()
        self.connection.autocommit = True

    # Выполнение запроса на изменение данных
    def post(self, query, args=()):
        try:
            self.cursor.execute(query, args)
            return True
        except Exception as err:
            print(repr(err))
            return False