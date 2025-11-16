import oracledb

class GestorBaseDatos:
    def __init__(self):
        self.usuario = "system"
        self.contrasena = "74698741"
        self.dsn = "192.168.1.44:1521/XE"
        self.conexion = None
    
    def conectar(self):
        try:
            self.conexion = oracledb.connect(
                user=self.usuario, 
                password=self.contrasena, 
                dsn=self.dsn
            )
            print("Conexión exitosa a Oracle Database")
            return True
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False
    
    def desconectar(self):
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada")
    
    def insertar_estudiante(self, nombre, apellido, dni, email):
        try:
            cursor = self.conexion.cursor()
            sql = """
                INSERT INTO Estudiante 
                VALUES (seq_estudiante.NEXTVAL, :1, :2, :3, :4)
            """
            cursor.execute(sql, (nombre, apellido, dni, email))
            self.conexion.commit()
            print(f"Estudiante {nombre} {apellido} insertado correctamente")
            return True
        except Exception as e:
            print(f"Error al insertar estudiante: {e}")
            return False
    
    def consultar_estudiantes(self):
        try:
            cursor = self.conexion.cursor()
            cursor.execute("SELECT * FROM Estudiante ORDER BY id_estudiante")
            resultados = cursor.fetchall()
            
            print("\n Lista de estudiantes:")
            print("-" * 80)
            for fila in resultados:
                print(f"ID: {fila[0]}, Nombre: {fila[1]} {fila[2]}, DNI: {fila[3]}, Email: {fila[4]}")
            print("-" * 80)
            return resultados
        except Exception as e:
            print(f"Error al consultar estudiantes: {e}")
            return []
    
    def actualizar_estudiante(self, id_estudiante, nuevo_email):
        try:
            cursor = self.conexion.cursor()
            sql = "UPDATE Estudiante SET email = :1 WHERE id_estudiante = :2"
            cursor.execute(sql, (nuevo_email, id_estudiante))
            self.conexion.commit()
            
            if cursor.rowcount > 0:
                print(f"Email del estudiante {id_estudiante} actualizado correctamente")
                return True
            else:
                print(f"No se encontró el estudiante con ID {id_estudiante}")
                return False
        except Exception as e:
            print(f"Error al actualizar estudiante: {e}")
            return False
    
    def eliminar_estudiante(self, id_estudiante):
        try:
            cursor = self.conexion.cursor()
            
            cursor.execute("DELETE FROM Matricula WHERE id_estudiante = :1", [id_estudiante])
            
            sql = "DELETE FROM Estudiante WHERE id_estudiante = :1"
            cursor.execute(sql, [id_estudiante])
            self.conexion.commit()
            
            if cursor.rowcount > 0:
                print(f"Estudiante {id_estudiante} eliminado correctamente")
                return True
            else:
                print(f"No se encontró el estudiante con ID {id_estudiante}")
                return False
        except Exception as e:
            print(f"Error al eliminar estudiante: {e}")
            self.conexion.rollback()
            return False
    
    def estudiantes_por_curso(self):
        try:
            cursor = self.conexion.cursor()
            sql = """
                SELECT c.nombre AS curso, 
                       COUNT(m.id_estudiante) AS total_estudiantes,
                       c.modalidad
                FROM Curso c
                LEFT JOIN Matricula m ON c.id_curso = m.id_curso
                GROUP BY c.id_curso, c.nombre, c.modalidad
                ORDER BY total_estudiantes DESC
            """
            cursor.execute(sql)
            resultados = cursor.fetchall()
            
            print("\n Estudiantes por curso:")
            print("-" * 60)
            for fila in resultados:
                print(f"Curso: {fila[0]}, Estudiantes: {fila[1]}, Modalidad: {fila[2]}")
            print("-" * 60)
            return resultados
        except Exception as e:
            print(f"Error en consulta avanzada: {e}")
            return []

def demostrar_operaciones_crud():
    gestor = GestorBaseDatos()
    
    if gestor.conectar():
        print("\n" + "="*50)
        print("Demostración de operaciones CRUD")
        print("="*50)
        
        gestor.consultar_estudiantes()
        
        gestor.insertar_estudiante("Laura", "Martinez", "75567890", "laura.martinez@email.com")
        
        gestor.actualizar_estudiante(1, "grecia.lopez.actualizado@universidad.edu")
        
        gestor.estudiantes_por_curso()
        
        # gestor.eliminar_estudiante(5)
        
        gestor.consultar_estudiantes()
        
        gestor.desconectar()

if __name__ == "__main__":
    demostrar_operaciones_crud()