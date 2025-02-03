import pymysql

class Database:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Conexión exitosa a la base de datos.")
        except pymysql.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
    
    def get_cursor(self):
        """
        Retorna un cursor para ejecutar consultas.
        """
        if self.connection:
            return self.connection.cursor()
        else:
            raise Exception("No hay una conexión activa a la base de datos.")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada.")

    def execute_query(self, query, params=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                self.connection.commit()
                return cursor
        except pymysql.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None