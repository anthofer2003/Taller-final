# presupuesto_proveedor_dao.py

from flask import current_app as app
from app.conexion.Conexion import Conexion
from app.dao.gestionar_compras.registrar_presupuesto_proveedor.dto.presupuesto_proveedor_dto import PresupuestoProveedorDto
from app.dao.gestionar_compras.registrar_presupuesto_proveedor.dto.presupuesto_proveedor_detalle_dto import PresupuestoProveedorDetalleDto

class PresupuestoProveedorDao:

    def obtener_presupuestos(self):
        query = """
        SELECT pp.id_presupuesto,
               pp.id_proveedor,
               pr.nombre_proveedor,
               pp.id_empleado,
               e.nombres || ' ' || e.apellidos AS empleado,
               pp.id_sucursal,
               pp.id_estado_presupuesto,
               ep.descripcion AS estado,
               pp.fecha_presupuesto
        FROM presupuesto_proveedor pp
        LEFT JOIN proveedor pr ON pr.id_proveedor = pp.id_proveedor
        LEFT JOIN empleados e ON e.id_empleado = pp.id_empleado
        LEFT JOIN estado_presupuesto ep ON ep.id = pp.id_estado_presupuesto
        ORDER BY pp.id_presupuesto DESC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            resultados = []

            for r in rows:
                fecha_valor = None
                # proteger el formateo de fecha
                if r[8]:
                    try:
                        fecha_valor = r[8].strftime("%Y-%m-%d")
                    except Exception:
                        fecha_valor = str(r[8])  # fallback seguro

                resultados.append({
                    "id_presupuesto": r[0],
                    "id_proveedor": r[1],
                    "proveedor": r[2],
                    "id_empleado": r[3],
                    "empleado": r[4],
                    "id_sucursal": r[5],
                    "id_estado_presupuesto": r[6],
                    "estado": r[7],
                    "fecha_presupuesto": fecha_valor
                })

            return resultados

        except Exception as e:
            app.logger.error(f"Error al obtener presupuestos: {str(e)}")
            # devolver mensaje genérico para debug
            return [{"error": f"Error al obtener presupuestos: {str(e)}"}]
        finally:
            cur.close()
            con.close()

    def agregar(self, presupuesto_dto: PresupuestoProveedorDto) -> bool:
        insert_cabecera = """
        INSERT INTO presupuesto_proveedor
            (id_proveedor, id_empleado, id_sucursal, id_estado_presupuesto, fecha_presupuesto)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_presupuesto
        """
        insert_detalle = """
        INSERT INTO presupuesto_proveedor_detalle
            (id_presupuesto, id_producto, cantidad, precio_unitario)
        VALUES (%s, %s, %s, %s)
        """
        conexion = Conexion()
        con = conexion.getConexion()
        con.autocommit = False
        cur = con.cursor()
        try:
            params = (
                presupuesto_dto.id_proveedor,
                presupuesto_dto.id_empleado,
                presupuesto_dto.id_sucursal,
                presupuesto_dto.estado.id,
                presupuesto_dto.fecha_presupuesto
            )
            cur.execute(insert_cabecera, params)
            id_presupuesto = cur.fetchone()[0]

            # insertar detalles
            if presupuesto_dto.detalle_presupuesto:
                for det in presupuesto_dto.detalle_presupuesto:
                    params_det = (id_presupuesto, det.id_producto, det.cantidad, det.precio_unitario)
                    cur.execute(insert_detalle, params_det)

            con.commit()
            return True
        except Exception as e:
            app.logger.error(f"Error al agregar presupuesto: {str(e)}")
            con.rollback()
            return False
        finally:
            con.autocommit = True
            cur.close()
            con.close()

    def anular(self, id_presupuesto: int) -> bool:
        update_sql = """
        UPDATE presupuesto_proveedor
        SET id_estado_presupuesto = (
            SELECT id FROM estado_presupuesto WHERE descripcion = 'Anulado'
        )
        WHERE id_presupuesto = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(update_sql, (id_presupuesto,))
            con.commit()
            return True
        except Exception as e:
            app.logger.error(f"Error al anular presupuesto: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
