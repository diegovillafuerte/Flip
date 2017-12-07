import psycopg2
try:
    conn = psycopg2.connect("dbname='flipDB' user='diego' host='localhost' password='diego93'")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()

cur.execute('''CREATE TABLE usuarios
      (IDusuario INT PRIMARY KEY     NOT NULL,
      nombre varchar(100));''')

cur.execute('''CREATE TABLE transacciones
      (IDusuario 	INT  NOT NULL references usuarios (IDusuario),
      tipo          varchar(50)    NOT NULL,
      monto            money,
      concepto            varchar(150));''')




conn.commit()
conn.close()