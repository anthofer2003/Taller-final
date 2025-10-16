from flask import current_app as app
from app.conexion.Conexion import Conexion

class ItemDao:

    def get_items(self):
        query = """
        SELECT 
            id_item,
            descripcion,
            precio_unitario,
            stock_actual
        FROM items
        WHERE estado = true
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query)
            items = cur.fetchall()
            return [{
                'id_item': i[0],
                'descripcion': i[1],
                'precio_unitario': float(i[2]),
                'stock_actual': int(i[3])
            } for i in items]
        except Exception as e:
            app.logger.error(f"Error al obtener los items: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
