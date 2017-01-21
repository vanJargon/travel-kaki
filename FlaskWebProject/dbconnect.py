import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="1@mVTyh311296", db="travel_kaki")
    c = conn.cursor()

    return c, conn