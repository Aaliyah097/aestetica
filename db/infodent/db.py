import fdb


class Connector:
    def __init__(self,
                 address: str,
                 port: str,
                 name: str,
                 user: str = "SYSDBA",
                 password: str = "masterkey"):
        self.address = address
        self.port = port
        self.name = name
        self.user = user
        self.password = password

    def __enter__(self):
        self.con = fdb.connect(
            dsn=self.address + ":" + self.port + self.name,
            user=self.user,
            password=self.password
        )
        print("[v] connection opened")
        self.cursor = self.con.cursor()
        return self.cursor

    def __exit__(self, e_type, e_msg, traceback):
        if e_type or e_msg:
            print(f"[x] rollback. {str(e_type)}: {str(e_msg)}")
            self.con.rollback()
        else:
            self.con.commit()

        if self.cursor:
            self.cursor.close()
            self.cursor = None

        if hasattr(self, 'conn'):
            if self.con:
                self.con.close()
                self.con = None
                print("[v] connection closed")
