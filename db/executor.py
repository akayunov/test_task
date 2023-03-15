class Db:
    def execute(self, sql, args):
        return mysql_connector.execute(sql, args)


db = Db()