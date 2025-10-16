from flask import current_app as app
from app.conexion.Conexion import Conexion

class ProveedorDao:

    def get_proveedores(self):
        query = """
        SELECT 
            id_proveedor,
            nombre_proveedor,
            ruc,
            telefono,
            direccion
        FROM proveedores
        WHERE estado = true
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query)
            proveedores = cur.fetchall()
            return [{
                'id_proveedor': p[0],
                'nombre_proveedor': p[1],
                'ruc': p[2],
                'telefono': p[3],
                'direccion': p[4]
            } for p in proveedores]
        except Exception as e:
            app.logger.error(f"Error al obtener proveedores: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
