# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class PaisDao:

    def getPaises(self):
        paisSQL = """
        SELECT id, descripcion
        FROM paises
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(paisSQL)
            lista_paises = cur.fetchall()
            lista_ordenada = []
            for item in lista_paises:
                lista_ordenada.append({
                    "id": item[0],
                    "descripcion": item[1]
                })
            return lista_ordenada
        except con.Error as e:
            app.logger.info(e)
        finally:
            cur.close()
            con.close()

    def getPaisById(self, id):
        paisSQL = """
        SELECT id, descripcion
        FROM paises WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(paisSQL, (id,))
            paisEncontrado = cur.fetchone()
            if paisEncontrado:
                return {
                    "id": paisEncontrado[0],
                    "descripcion": paisEncontrado[1]
                }
            return None
        except con.Error as e:
            app.logger.info(e)
        finally:
            cur.close()
            con.close()

    def guardarPais(self, descripcion):
        descripcion_normalizada = descripcion.strip().upper()

        verificarSQL = """
        SELECT id FROM paises WHERE UPPER(TRIM(descripcion)) = %s
        """
        insertSQL = """
        INSERT INTO paises(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(verificarSQL, (descripcion_normalizada,))
            existente = cur.fetchone()

            if existente:
                return {
                    "success": False,
                    "message": "El país ya existe en la base de datos.",
                    "id": existente[0]
                }

            cur.execute(insertSQL, (descripcion_normalizada,))
            nuevo_id = cur.fetchone()[0]
            con.commit()

            return {
                "success": True,
                "message": "País guardado exitosamente.",
                "id": nuevo_id
            }

        except con.Error as e:
            app.logger.info(e)
            return {
                "success": False,
                "message": "Error al guardar el país.",
                "id": None
            }

        finally:
            cur.close()
            con.close()

    def updatePais(self, id, descripcion):
        descripcion_normalizada = descripcion.strip().upper()

        # Verificar que no exista otro país con la misma descripción diferente al que actualizamos
        verificarSQL = """
        SELECT id FROM paises WHERE UPPER(TRIM(descripcion)) = %s AND id != %s
        """

        updatePaisSQL = """
        UPDATE paises
        SET descripcion=%s
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(verificarSQL, (descripcion_normalizada, id))
            existente = cur.fetchone()

            if existente:
                # Ya existe otro país con esa descripción
                return {
                    "success": False,
                    "message": "El país ya existe en la base de datos."
                }

            cur.execute(updatePaisSQL, (descripcion_normalizada, id,))
            con.commit()
            return {
                "success": True,
                "message": "País actualizado exitosamente."
            }
        except con.Error as e:
            app.logger.info(e)
            return {
                "success": False,
                "message": "Error al actualizar el país."
            }
        finally:
            cur.close()
            con.close()

    def deletePais(self, id):
        deletePaisSQL = """
        DELETE FROM paises
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(deletePaisSQL, (id,))
            con.commit()
            return True
        except con.Error as e:
            app.logger.info(e)
        finally:
            cur.close()
            con.close()
        return False
