from flask import current_app as app
from app.conexion.Conexion import Conexion

class LoginDao:

    def buscarUsuario(self, usu_nick: str):
        buscar_usuario_sql = """
        SELECT
            u.usu_id
            , TRIM(u.usu_nick) nick
            , u.usu_clave
            , u.usu_nro_intentos
            , u.fun_id
            , u.gru_id
            , u.usu_estado
            , CONCAT(p.nombres, ' ', p.apellidos) nombre_persona
            , g.gru_des grupo
        FROM
            usuarios u
        LEFT JOIN
            personas p ON p.id_persona = u.fun_id
        LEFT JOIN
            grupos g ON g.gru_id = u.gru_id
        WHERE
            u.usu_nick = %s AND u.usu_estado IS TRUE
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(buscar_usuario_sql, (usu_nick,))
            usuario_encontrado = cur.fetchone()
            if usuario_encontrado:
                app.logger.info(f"Usuario encontrado: {usuario_encontrado}")  # Log de éxito
                return {
                    "usu_id": usuario_encontrado[0],
                    "usu_nick": usuario_encontrado[1],
                    "usu_clave": usuario_encontrado[2],
                    "usu_nro_intentos": usuario_encontrado[3],
                    "fun_id": usuario_encontrado[4],
                    "gru_id": usuario_encontrado[5],
                    "usu_estado": usuario_encontrado[6],
                    "nombre_persona": usuario_encontrado[7],
                    "grupo": usuario_encontrado[8],
                }
            else:
                app.logger.warning("Usuario no encontrado o estado inactivo.")
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener usuario '{usu_nick}': {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
