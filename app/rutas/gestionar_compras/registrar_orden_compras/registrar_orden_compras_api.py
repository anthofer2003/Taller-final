from datetime import date
from flask import Blueprint, jsonify, request, current_app as app
from app.dao.gestionar_compras.registrar_orden_compras.orden_compras_dao import OrdenDeCompraDao
from app.dao.gestionar_compras.registrar_orden_compras.dto.orden_compras_dto import OrdenDeCompraDto
from app.dao.gestionar_compras.registrar_orden_compras.dto.orden_compra_detalle_dto import OrdenDeCompraDetalleDto
from app.dao.referenciales.estado_orden_compra.estado_orden_compra_dto import EstadoOrdenCompra
from app.dao.referenciales.sucursal.sucursal_dao import SucursalDao

ordapi = Blueprint('ordapi', __name__)

@ordapi.route('/ordenes', methods=['GET'])
def get_ordenes():
    dao = OrdenDeCompraDao()
    try:
        ordenes = dao.obtener_ordenes()
        return jsonify({'success': True, 'data': ordenes, 'error': False}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener ordenes: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@ordapi.route('/ordenes', methods=['POST'])
def add_orden():
    dao = OrdenDeCompraDao()
    data = request.get_json()
    required = ['nro_orden','id_empleado','id_proveedor','id_sucursal','id_deposito','fecha','detalle_orden']
    for campo in required:
        if campo not in data or data[campo] is None or data[campo] == '':
            return jsonify({'success': False, 'error': f'El campo {campo} es obligatorio.'}), 400
    try:
        detalle = [OrdenDeCompraDetalleDto(
                    id_orden_compra=None,
                    id_item=item['id_item'],
                    cantidad=item['cantidad'],
                    precio_unitario=item.get('precio_unitario',0)
                   ) for item in data['detalle_orden']]

        estado = EstadoOrdenCompra(id=1, descripcion='Pendiente')

        cabecera = OrdenDeCompraDto(
            id_orden_compra=None,
            nro_orden=data['nro_orden'],
            id_empleado=data['id_empleado'],
            id_proveedor=data['id_proveedor'],
            id_sucursal=data['id_sucursal'],
            id_deposito=data['id_deposito'],
            empresa=data.get('empresa'),
            funcionario=data.get('funcionario'),
            fecha=date.fromisoformat(data['fecha']),
            fecha_vencimiento=date.fromisoformat(data['fecha_vencimiento']) if data.get('fecha_vencimiento') else None,
            factura=data.get('factura'),
            tipo_pago=data.get('tipo_pago'),
            nro_pedido=data.get('nro_pedido'),
            estado=estado,
            detalle_orden=detalle
        )

        result = dao.agregar(cabecera)
        if result:
            return jsonify({'success': True, 'error': None}), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la orden.'}), 500
    except Exception as e:
        app.logger.error(f"Error al crear orden: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@ordapi.route('/sucursal-depositos/<int:id_sucursal>', methods=['GET'])
def get_depositos_sucursal(id_sucursal):
    dao = SucursalDao()
    try:
        depositos = dao.get_sucursal_depositos(id_sucursal)
        return jsonify({'success': True, 'data': depositos, 'error': False}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener depositos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@ordapi.route('/ordenes/<int:id_orden>', methods=['DELETE'])
def anular_orden(id_orden):
    dao = OrdenDeCompraDao()
    try:
        ok = dao.anular(id_orden)
        if ok:
            return jsonify({'success': True, 'message': 'Orden anulada.' , 'error': False}), 200
        return jsonify({'success': False, 'error': 'No se pudo anular.'}), 500
    except Exception as e:
        app.logger.error(f"Error al anular orden: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
