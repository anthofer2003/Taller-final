from flask import current_app as app
from app.conexion.Conexion import Conexion
from app.dao.gestionar_compras.registrar_ajustes.dto.ajustes_dto import AjusteDto

class AjusteDao:

    def obtener_ajustes(self):
        query = """
        SELECT
            a.id_ajuste,
            a.nro_ajuste,
            a.id_empleado,
            p.nombres,
            p.apellidos,
            a.id_sucursal,
            a.id_deposito,
            a.fecha,
            a.tipo_ajuste,
            eaj.descripcion as estado,
            a.empresa,
            a.funcionario,
            a.motivo_general
        FROM ajuste a
        LEFT JOIN empleados e ON e.id_empleado = a.id_empleado
        LEFT JOIN personas p ON p.id_persona = e.id_empleado
        LEFT JOIN estado_ajuste eaj ON eaj.id_ea = a.id_ea
        ORDER BY a.id_ajuste DESC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            return [{
                'id_ajuste': r[0],
                'nro_ajuste': r[1],
                'id_empleado': r[2],
                'empleado': f'{r[3]} {r[4]}',
                'id_sucursal': r[5],
                'id_deposito': r[6],
                'fecha': r[7].strftime("%Y-%m-%d") if r[7] else None,
                'tipo_ajuste': r[8],
                'estado': r[9],
                'empresa': r[10],
                'funcionario': r[11],
                'motivo_general': r[12]
            } for r in rows]
        except Exception as e:
            app.logger.error(f"Error al obtener ajustes: {str(e)}")
        finally:
            cur.close()
            con.close()
        return []

    def agregar(self, ajuste_dto: AjusteDto) -> bool:
        insertCabecera = """
        INSERT INTO ajuste
        (nro_ajuste, id_empleado, id_sucursal, id_deposito, empresa, funcionario, fecha, tipo_ajuste, id_ea, motivo_general)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id_ajuste
        """
        insertDetalle = """
        INSERT INTO ajuste_detalle
        (id_ajuste, id_item, cantidad, precio_unitario, motivo)
        VALUES (%s,%s,%s,%s,%s)
        """
        conexion = Conexion()
        con = conexion.getConexion()
        con.autocommit = False
        cur = con.cursor()
        try:
            parametros = (
                ajuste_dto.nro_ajuste,
                ajuste_dto.id_empleado,
                ajuste_dto.id_sucursal,
                ajuste_dto.id_deposito,
                ajuste_dto.empresa,
                ajuste_dto.funcionario,
                ajuste_dto.fecha,
                ajuste_dto.tipo_ajuste,
                ajuste_dto.estado.id if ajuste_dto.estado else None,
                ajuste_dto.motivo_general
            )
            cur.execute(insertCabecera, parametros)
            id_ajuste = cur.fetchone()[0]

            if ajuste_dto.detalle_ajuste:
                for det in ajuste_dto.detalle_ajuste:
                    cur.execute(insertDetalle, (
                        id_ajuste,
                        det.id_item,
                        det.cantidad,
                        det.precio_unitario,
                        det.motivo
                    ))

            con.commit()
        except Exception as e:
            app.logger.error(f"Error al agregar ajuste: {str(e)}")
            con.rollback()
            return False
        finally:
            con.autocommit = True
            cur.close()
            con.close()
        return True

    def anular(self, id_ajuste: int) -> bool:
        update = """
        UPDATE ajuste
        SET id_ea = (
            SELECT id_ea FROM estado_ajuste WHERE descripcion = 'Anulado'
        )
        WHERE id_ajuste = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(update, (id_ajuste,))
            con.commit()
        except Exception as e:
            app.logger.error(f"Error al anular ajuste: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
        return True
