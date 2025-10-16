from flask import current_app as app
from app.conexion.Conexion import Conexion

class DepositoDao:

    def get_depositos(self):
        query = """
        SELECT 
            id_deposito,
            descripcion AS nombre_deposito,
            ubicacion
        FROM depositos
        WHERE estado = true
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query)
            depositos = cur.fetchall()
            return [{
                'id_deposito': d[0],
                'nombre_deposito': d[1],
                'ubicacion': d[2]
            } for d in depositos]
        except Exception as e:
            app.logger.error(f"Error al obtener los depósitos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
