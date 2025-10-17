from flask import current_app as app
from app.conexion.Conexion import Conexion
from app.dao.gestionar_compras.registrar_orden_compras.dto.orden_compras_dto import OrdenDeCompraDto

class OrdenDeCompraDao:

    def obtener_ordenes(self):
        query = """
        SELECT
            oc.id_orden_compra,
            oc.nro_orden,
            oc.id_empleado,
            p.nombres,
            p.apellidos,
            oc.id_proveedor,
            pr.nombre_proveedor,
            oc.id_sucursal,
            oc.id_deposito,
            oc.fecha,
            oc.fecha_vencimiento,
            oc.factura,
            oc.tipo_pago,
            eoc.descripcion AS estado,
            oc.empresa,
            oc.funcionario
        FROM
            orden_de_compra oc
        LEFT JOIN empleados e ON e.id_empleado = oc.id_empleado
        LEFT JOIN personas p ON p.id_persona = e.id_empleado
        LEFT JOIN proveedores pr ON pr.id_proveedor = oc.id_proveedor
        LEFT JOIN estado_orden_compra eoc ON eoc.id_eoc = oc.id_eoc
        ORDER BY oc.id_orden_compra DESC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            return [{
                'id_orden_compra': r[0],
                'nro_orden': r[1],
                'id_empleado': r[2],
                'empleado': f'{r[3]} {r[4]}',
                'id_proveedor': r[5],
                'proveedor': r[6],
                'id_sucursal': r[7],
                'id_deposito': r[8],
                'fecha': r[9].strftime("%Y-%m-%d") if r[9] else None,
                'fecha_vencimiento': r[10].strftime("%Y-%m-%d") if r[10] else None,
                'factura': r[11],
                'tipo_pago': r[12],
                'estado': r[13],
                'empresa': r[14],
                'funcionario': r[15]
            } for r in rows]
        except Exception as e:
            app.logger.error(f"Error al obtener ordenes de compra: {str(e)}")
        finally:
            cur.close()
            con.close()
        return []

    def agregar(self, orden_dto: OrdenDeCompraDto) -> bool:
        insertCabecera = """
        INSERT INTO orden_de_compra
        (nro_orden, id_empleado, id_proveedor, id_sucursal, id_deposito, empresa, funcionario,
         fecha, fecha_vencimiento, factura, tipo_pago, nro_pedido, id_eoc)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id_orden_compra
        """
        insertDetalle = """
        INSERT INTO orden_de_compra_detalle
        (id_orden_compra, id_item, cantidad, precio_unitario)
        VALUES (%s, %s, %s, %s)
        """
        conexion = Conexion()
        con = conexion.getConexion()
        con.autocommit = False
        cur = con.cursor()
        try:
            parametros = (
                orden_dto.nro_orden,
                orden_dto.id_empleado,
                orden_dto.id_proveedor,
                orden_dto.id_sucursal,
                orden_dto.id_deposito,
                orden_dto.empresa,
                orden_dto.funcionario,
                orden_dto.fecha,
                orden_dto.fecha_vencimiento,
                orden_dto.factura,
                orden_dto.tipo_pago,
                orden_dto.nro_pedido,
                orden_dto.estado.id if orden_dto.estado else None
            )
            cur.execute(insertCabecera, parametros)
            id_orden = cur.fetchone()[0]

            if orden_dto.detalle_orden:
                for det in orden_dto.detalle_orden:
                    cur.execute(insertDetalle, (
                        id_orden,
                        det.id_item,
                        det.cantidad,
                        det.precio_unitario
                    ))

            con.commit()
        except Exception as e:
            app.logger.error(f"Error al agregar orden de compra: {str(e)}")
            con.rollback()
            return False
        finally:
            con.autocommit = True
            cur.close()
            con.close()
        return True

    def anular(self, id_orden_compra: int) -> bool:
        update = """
        UPDATE orden_de_compra
        SET id_eoc = (
            SELECT id_eoc FROM estado_orden_compra WHERE descripcion = 'Anulado'
        )
        WHERE id_orden_compra = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(update, (id_orden_compra,))
            con.commit()
        except Exception as e:
            app.logger.error(f"Error al anular la orden de compra: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
        return True
