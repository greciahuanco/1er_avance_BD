import oracledb

usuario = "system"
contrasena = "74698741"
dsn = "192.168.1.44:1521/XE"

try:
    conexion = oracledb.connect(user=usuario, password=contrasena, dsn=dsn)
    print("Conexión exitosa\n")

    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, apellido FROM ESTUDIANTE")
    
    for fila in cursor:
        print(fila[0], fila[1])

except Exception as e:
    print("Error:", e)

finally:
    if 'conexion' in locals():
        conexion.close()
        print("\nConexión cerrada.")