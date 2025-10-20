from sqlalchemy import create_engine , MetaData# sirve para interactuar con la base de datos esta usa otras bibliotecas para conectarse a cualquier BD

engine=create_engine("mysql+pymysql://u1cmd7n4ngjc20s5:KKXzAXh6K6Ax1HtTxeEw@but9mopf5hhipe7hjibl-mysql.services.clever-cloud.com:3306/but9mopf5hhipe7hjibl")#pide un especie de url en el cual pide un user, contra el servidor, el puerto y la BD 
#y para hacer eso hay una bibloteca 
meta=MetaData()
conn= engine.connect()#esta es la funcion de conexion y es la que llamaremos