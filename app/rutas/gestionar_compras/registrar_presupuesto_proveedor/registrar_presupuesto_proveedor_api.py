# presupuesto_proveedor_api.py

from datetime import date
from flask import Blueprint, jsonify, request, current_app as app
from app.dao.gestionar_compras.registrar_presupuesto_proveedor.presupuesto_proveedor_dao import PresupuestoProveedorDao
from app.dao.gestionar_compras.registrar_presupuesto_proveedor.dto.presupuesto_proveedor_dto import PresupuestoProveedorDto
from app.dao.gestionar_compras.registrar_presupuesto_proveedor.dto.presupuesto_proveedor_detalle_dto import PresupuestoProveedorDetalleDto
from app.dao.referenciales.estado_presupuesto_proveedor.estado_presupuesto_proveedor_dto import EstadoPresupuesto

pp_api = Blueprint('pp_api', __name__, url_prefix='/api/v1/presupuestos-proveedor')


# ✅ GET — listado de presupuestos (DataTables)
@pp_api.route('/presupuestos', methods=['GET'])
def get_presupuestos():
    dao = PresupuestoProveedorDao()
    try:
        datos = dao.obtener_presupuestos()

        # ⚠️ DataTables espera la clave "data"
        # y un código 200 con JSON válido SIEMPRE
        return jsonify({
            'data': datos,    # DataTables leerá esta clave
            'success': True,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener presupuestos: {str(e)}")
        return jsonify({
            'data': [],
            'success': False,
            'error': f"Error interno: {str(e)}"
        }), 500


# ✅ POST — crear presupuesto
@pp_api.route('/presupuestos', methods=['POST'])
def add_presupuesto():
    dao = PresupuestoProveedorDao()
    data = request.get_json()

    required = ['id_proveedor', 'id_empleado', 'id_sucursal', 'fecha_presupuesto', 'detalle_presupuesto']
    for campo in required:
        if campo not in data or data[campo] in (None, '', []):
            return jsonify({'success': False, 'error': f"El campo '{campo}' es obligatorio."}), 400

    try:
        id_proveedor = int(data['id_proveedor'])
        id_empleado = int(data['id_empleado'])
        id_sucursal = int(data['id_sucursal'])
        fecha_presupuesto = data['fecha_presupuesto']
        detalle = data['detalle_presupuesto']

        # validar formato fecha
        try:
            fecha_parsed = date.fromisoformat(fecha_presupuesto)
        except Exception:
            return jsonify({'success': False, 'error': 'Formato de fecha inválido (YYYY-MM-DD)'}), 400

        detalle_dto = [
            PresupuestoProveedorDetalleDto(
                id_presupuesto=None,
                id_producto=int(item['id_producto']),
                cantidad=float(item['cantidad']),
                precio_unitario=float(item.get('precio_unitario', 0.0))
            )
            for item in detalle
        ]

        cabecera = PresupuestoProveedorDto(
            id_presupuesto=None,
            id_proveedor=id_proveedor,
            id_empleado=id_empleado,
            id_sucursal=id_sucursal,
            estado=EstadoPresupuesto(id=1, descripcion=None),  # 1 = Pendiente
            fecha_presupuesto=fecha_parsed,
            detalle_presupuesto=detalle_dto
        )

        resultado = dao.agregar(cabecera)
        if resultado:
            return jsonify({'success': True, 'error': None, 'message': 'Presupuesto creado correctamente'}), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo crear el presupuesto.'}), 500

    except Exception as e:
        app.logger.error(f"Error al crear presupuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor.'}), 500


# ✅ DELETE — anular presupuesto
@pp_api.route('/presupuestos/<int:id_presupuesto>', methods=['DELETE'])
def anular_presupuesto(id_presupuesto):
    dao = PresupuestoProveedorDao()
    try:
        res = dao.anular(id_presupuesto)
        if res:
            return jsonify({
                'success': True,
                'message': 'Presupuesto anulado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo anular presupuesto.'
            }), 400
    except Exception as e:
        app.logger.error(f"Error al anular presupuesto: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor.'
        }), 500
