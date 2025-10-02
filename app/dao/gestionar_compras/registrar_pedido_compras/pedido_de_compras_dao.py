from flask import current_app as app
from app.conexion.Conexion import Conexion
from app.dao.gestionar_compras.registrar_pedido_compras.dto.pedido_de_compras_dto import PedidoDeComprasDto

class PedidoDeComprasDao:
    
    def obtener_pedidos(self):
        query_pedidos = """
        SELECT
            pdc.id_pedido_compra
            , pdc.id_empleado
            , p.nombres
            , p.apellidos
            , pdc.id_sucursal
            , pdc.id_epc
            , edpc.descripcion estado
            , pdc.fecha_pedido
            , pdc.id_deposito
        FROM
            public.pedido_de_compra pdc
        LEFT JOIN empleados e
            ON e.id_empleado = pdc.id_empleado
        LEFT JOIN personas p
            ON p.id_persona = e.id_empleado
        LEFT JOIN estado_de_pedido_compras edpc
            ON pdc.id_epc = edpc.id_epc
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query_pedidos)
            pedidos = cur.fetchall()
            return [{
                'id_pedido_compra': pedido[0],
                'id_empleado': pedido[1],
                'empleado': f'{pedido[2]} {pedido[3]}',
                'id_sucursal': pedido[4],
                'id_epc': pedido[5],
                'estado': pedido[6],
                'fecha_pedido': pedido[7].strftime("%Y-%m-%d") if pedido[7] else None,
                'id_deposito': pedido[8]
            } for pedido in pedidos]
        except Exception as e:
            app.logger.error(f"Error al obtener los pedidos: {str(e)}")
        finally:
            cur.close()
            con.close()
        return []

    def agregar(self, pedido_dto: PedidoDeComprasDto) -> bool:
        insertPedidoCompraCabecera = """
        INSERT INTO public.pedido_de_compra
        (id_empleado, id_sucursal, id_epc, fecha_pedido, id_deposito)
        VALUES(%s, %s, %s, %s, %s)
        RETURNING id_pedido_compra
        """

        insertDetalleCompra = """
        INSERT INTO public.pedido_de_compra_detalle
        (id_pedido_compra, id_producto, cantidad)
        VALUES(%s, %s, %s)
        """

        conexion = Conexion()
        con = conexion.getConexion()
        con.autocommit = False
        cur = con.cursor()
        try:
            parametros = (
                pedido_dto.id_empleado,
                pedido_dto.id_sucursal,
                pedido_dto.estado.id,
                pedido_dto.fecha_pedido,
                pedido_dto.id_deposito,
            )
            cur.execute(insertPedidoCompraCabecera, parametros)
            id_pedido_compra = cur.fetchone()[0]

            if pedido_dto.detalle_pedido:
                for pedido in pedido_dto.detalle_pedido:
                    parametrosdetalle = (id_pedido_compra, pedido.id_producto, pedido.cantidad)
                    cur.execute(insertDetalleCompra, parametrosdetalle)

            con.commit()
        except Exception as e:
            app.logger.error(f"Error al agregar un nuevo pedido: {str(e)}")
            con.rollback()
            return False
        finally:
            con.autocommit = True
            cur.close()
            con.close()
        return True

    def anular(self, id_pedido_compra: int) -> bool:
        updateEstadoPedido = """
        UPDATE public.pedido_de_compra
        SET id_epc = (
            SELECT id_epc FROM estado_de_pedido_compras WHERE descripcion = 'Anulado'
        )
        WHERE id_pedido_compra = %s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(updateEstadoPedido, (id_pedido_compra,))
            con.commit()
        except Exception as e:
            app.logger.error(f"Error al anular el pedido: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
        return True
