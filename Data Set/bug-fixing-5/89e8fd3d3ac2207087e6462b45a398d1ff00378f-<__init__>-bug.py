def __init__(self, conn, db):
    self.conn = conn
    self.db = db
    self.cursor = conn.cursor()
    self.logging = False