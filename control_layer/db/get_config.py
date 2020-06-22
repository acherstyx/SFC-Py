import psycopg2


class SFCDatabase:
    def __init__(self, host, port, database, user, password):
        connection = psycopg2.connect(host=host,
                                      port=port,
                                      database=database,
                                      user=user,
                                      password=password)
        self.cursor = connection.cursor()

    def get_sf(self):
        sql = "select * from sf"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        for sf in data:
            print(sf)

        return data

    def get_sfc(self):
        sql = "select * from sfc"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        for sf in data:
            print(sf)

        return data


if __name__ == "__main__":
    db_connection = SFCDatabase("localhost",
                                "5432",
                                "sfc",
                                "postgres",
                                "123456")
    db_connection.get_sf()
    db_connection.get_sfc()
