# Data Access Object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class ProveedorDao:

    def get_proveedores(self):
        query = """
        SELECT id_proveedor, nombre_proveedor, ruc, telefono, direccion
        FROM proveedor
        ORDER BY nombre_proveedor
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(query)
            rows = cur.fetchall()
            return [
                {
                    'id_proveedor': r[0],
                    'nombre_proveedor': r[1],
                    'ruc': r[2],
                    'telefono': r[3],
                    'direccion': r[4]
                }
                for r in rows
            ]
        except Exception as e:
            app.logger.error(f"Error al obtener proveedores: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getProveedorById(self, id):
        query = "SELECT id_proveedor, nombre_proveedor, ruc, telefono, direccion FROM proveedor WHERE id_proveedor=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query, (id,))
            r = cur.fetchone()
            if r:
                return {
                    'id_proveedor': r[0],
                    'nombre_proveedor': r[1],
                    'ruc': r[2],
                    'telefono': r[3],
                    'direccion': r[4]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener proveedor: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def guardarProveedor(self, nombre, ruc, telefono, direccion):
        query = """
        INSERT INTO proveedor(nombre_proveedor, ruc, telefono, direccion)
        VALUES(%s, %s, %s, %s) RETURNING id_proveedor
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query, (nombre, ruc, telefono, direccion))
            new_id = cur.fetchone()[0]
            con.commit()
            return new_id
        except Exception as e:
            app.logger.error(f"Error al insertar proveedor: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateProveedor(self, id, nombre, ruc, telefono, direccion):
        query = """
        UPDATE proveedor
        SET nombre_proveedor=%s, ruc=%s, telefono=%s, direccion=%s
        WHERE id_proveedor=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query, (nombre, ruc, telefono, direccion, id))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar proveedor: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteProveedor(self, id):
        query = "DELETE FROM proveedor WHERE id_proveedor=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query, (id,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar proveedor: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
