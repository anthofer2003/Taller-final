from flask import current_app as app
from app.conexion.Conexion import Conexion
from app.dao.gestionar_compras.registrar_presupuesto_compras.dto.presupuesto_compras_dto import PresupuestoDeComprasDto

class PresupuestoDeComprasDao:

    def obtener_presupuestos(self):
        query = """
        SELECT
            pc.id_presupuesto,
            pc.nro_presupuesto,
            pc.id_empleado,
            p.nombres,
            p.apellidos,
            pc.id_proveedor,
            pr.razon_social AS proveedor,
            pc.id_sucursal,
            pc.id_deposito,
            pc.fecha,
            epc.descripcion AS estado,
            pc.empresa,
            pc.funcionario
        FROM
            presupuesto_de_compra pc
        LEFT JOIN empleados e ON e.id_empleado = pc.id_empleado
        LEFT JOIN personas p ON p.id_persona = e.id_empleado
        LEFT JOIN proveedores pr ON pr.id_proveedor = pc.id_proveedor
        LEFT JOIN estado_de_presupuesto_compras epc ON epc.id_epc = pc.id_epc
        ORDER BY pc.id_presupuesto DESC;
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query)
            resultados = cur.fetchall()
            return [{
                'id_presupuesto': r[0],
                'nro_presupuesto': r[1],
                'id_empleado': r[2],
                'empleado': f'{r[3]} {r[4]}',
                'id_proveedor': r[5],
                'proveedor': r[6],
                'id_sucursal': r[7],
                'id_deposito': r[8],
                'fecha': r[9].strftime("%Y-%m-%d") if r[9] else None,
                'estado': r[10],
                'empresa': r[11],
                'funcionario': r[12]
            } for r in resultados]
        except Exception as e:
            app.logger.error(f"Error al obtener presupuestos: {str(e)}")
        finally:
            cur.close()
            con.close()
        return []

    def agregar(self, presupuesto_dto: PresupuestoDeComprasDto) -> bool:
        insertCabecera = """
        INSERT INTO presupuesto_de_compra
        (nro_presupuesto, id_empleado, id_proveedor, id_sucursal, id_deposito, empresa, funcionario, fecha, id_epc)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id_presupuesto
        """

        insertDetalle = """
        INSERT INTO presupuesto_de_compra_detalle
        (id_presupuesto, id_item, cantidad, precio_iva)
        VALUES (%s, %s, %s, %s)
        """

        conexion = Conexion()
        con = conexion.getConexion()
        con.autocommit = False
        cur = con.cursor()
        try:
            parametros = (
                presupuesto_dto.nro_presupuesto,
                presupuesto_dto.id_empleado,
                presupuesto_dto.id_proveedor,
                presupuesto_dto.id_sucursal,
                presupuesto_dto.id_deposito,
                presupuesto_dto.empresa,
                presupuesto_dto.funcionario,
                presupuesto_dto.fecha,
                presupuesto_dto.estado.id
            )
            cur.execute(insertCabecera, parametros)
            id_presupuesto = cur.fetchone()[0]

            if presupuesto_dto.detalle_presupuesto:
                for detalle in presupuesto_dto.detalle_presupuesto:
                    cur.execute(insertDetalle, (
                        id_presupuesto,
                        detalle.id_item,
                        detalle.cantidad,
                        detalle.precio_iva
                    ))

            con.commit()
        except Exception as e:
            app.logger.error(f"Error al agregar presupuesto: {str(e)}")
            con.rollback()
            return False
        finally:
            con.autocommit = True
            cur.close()
            con.close()
        return True

    def anular(self, id_presupuesto: int) -> bool:
        query = """
        UPDATE presupuesto_de_compra
        SET id_epc = (
            SELECT id_epc FROM estado_de_presupuesto_compras WHERE descripcion = 'Anulado'
        )
        WHERE id_presupuesto = %s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query, (id_presupuesto,))
            con.commit()
        except Exception as e:
            app.logger.error(f"Error al anular el presupuesto: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
        return True
