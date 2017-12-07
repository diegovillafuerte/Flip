import pandas as pd
import datetime
import smtplib
import os
import psycopg2



class transaccion:
   	Count = 0

   	def __init__(self, idUsuario, tipo, monto, concepto):
	      self.tipo = tipo
	      self.idUsuario = idUsuario
	      self.monto = monto
	      self.fecha = datetime.datetime.now()
	      self.concepto = concepto
	      transaccion.Count += 1

	def getTipo(self):
		return self.tipo

	def getMonto(self):
		return self.monto

	def getFecha(self):
		return self.fecha

	def getConcepto(self):
		return self.concepto

	def verTransaccion(self):
      		print("Tipo : ", self.tipo,  ", Fecha: ", self.fecha, ", concepto: ", self.concepto)

	def registro(self):
	      if self.tipo == "efectivo":
	         res = [self.fecha,self.monto,0,0,0,self.concepto]
	      elif self.tipo == "debito":
	         res = [self.fecha,0,self.monto,0,0,self.concepto]
	      elif self.tipo == "credito":
	         res = [self.fecha,0,0,self.monto,0,self.concepto]
	      elif self.tipo == "deuda":
	         res = [self.fecha,0,0,0,self.monto,self.concepto]
	      else:
	      		res = "no"
	      return res


class usuario:
	Count = 0

	def __init__(self, id, nombre):
		self.id = id
		self.nombre = nombre
		usuario.Count += 1

	def nombre(self):
		return self.nombre




base = pd.DataFrame(columns=["Fecha","Efectivo","Debito","Credito","Deudas","Concepto"])

transacciones = []
flag = True
while flag == True:
	var1 = input("¿Que tipo de transaccion es? Puede ser efectivo, debito, credito o deuda\n")
	var2 = input("Ingresa el monto de la transacción.\n")
	var3 = input("Ingresa el concepto de la transacción\n")
	var4 = input("Quieres ingresar otra transacción? Si o no\n")
	transacciones.append(transaccion(1,var1,int(var2),var3))
	if (var4 != "si") and (var4 != "Si"):
		flag = False



'''transacciones.append(transaccion(1,"efectivo",200,"Saldo Inicial"))
transacciones.append(transaccion(1,"debito",10364.77,"Saldo Inicial"))
transacciones.append(transaccion(1,"credito",-6513.81,"Saldo Inicial"))
transacciones.append(transaccion(1,"deuda",1555,"Libros escuela"))
transacciones.append(transaccion(1,"deuda",10355,"Expenses"))'''



try:
    conn = psycopg2.connect("dbname='flipDB' user='diego' host='localhost' password='diego93'")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()

for i in transacciones:
	if i.registro() != "in":
		base.loc[len(base)] = i.registro()

		IDusuario = 1

		query = '''select nombre from usuarios where IDusuario == %;'''
		data = (IDusuario)
		cur.execute(query,data)

		nombre = cur.fetchone()

		query = '''insert into usuarios(IDusuario, nombre) values (%,%);'''
		data = (IDusuario, nombre)
		cur.execute(query,data)

		tipo = i.getTipo()
		monto = i.getMonto()
		concepto = i.getConcepto()

		query = '''insert into transacciones(IDusuario, tipo, monto, concepto) values (%,%,%,%);'''
		data = (IDusuario, tipo, monto, concepto)
		cur.execute()


conn.commit()
conn.close()
    

def reporte(panda):
	#Create the excel file
	resumen = pd.DataFrame(columns=["Saldo débito","Saldo crédito","Saldo efectivo","Subtotal","Total Deudas","Total general"])
	debito = panda["Debito"].sum()
	credito = panda["Credito"].sum()
	efectivo = panda["Efectivo"].sum()
	deudas = panda["Deudas"].sum()
	subtotal = debito + credito + efectivo
	total = deudas + subtotal
	resumen.loc[0] = [debito,credito,efectivo,subtotal,deudas,total]
	writer = pd.ExcelWriter("ResumenFinanciero.xlsx")
	resumen.to_excel(writer,'Resumen')
	panda.to_excel(writer,'Detalle')
	writer.save()
	os.system("open ResumenFinanciero.xlsx")

	#Send via email


	'''sender = 'diegovillafuertesoraiz@gmail.com'
	receivers = ['diegovillafuertesoraiz@gmail.com']
	subject = "Prueba"
	msg = "Hola"
	email = """\  
	From: %s  
	To: %s  
	Subject: %s

	%s
	""" % (sender, ", ".join(receivers), subject, msg)
	email = email.encode()

	try:
		server = smtplib.SMTP(host='smtp.gmail.com', port=587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login("diegovillafuertesoraiz@gmail.com", "kilimanJaro93")
		server.sendmail(sender, receivers, msg)
		server.close()

		print("Email sent")
	except Exception as e: 
		print(e)
		print("something went wrong...")'''
print("Tus transacciones son las siguientes:")
print(base)
print()
print("Tu resumen de situación financiera es el siguiente")
reporte(base)


