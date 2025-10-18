from datetime import date
from flask import Blueprint, jsonify, request, current_app as app
from app.dao.gestionar_compras.registrar_ajustes.ajustes_dao import AjusteDao
from app.dao.gestionar_compras.registrar_ajustes.dto.ajustes_dto import AjusteDto
from app.dao.gestionar_compras.registrar_ajustes.dto.ajustes_detalle_dto import AjusteDetalleDto
from app.dao.referenciales.estado_ajustes.estado_ajustes_dto import EstadoAjuste
from app.dao.referenciales.sucursal.sucursal_dao import SucursalDao

ajapi = Blueprint('ajapi', __name__)

@ajapi.route('/ajustes', methods=['GET'])
def get_ajustes():
    dao = AjusteDao()
    try:
        ajustes = dao.obtener_ajustes()
        return jsonify({'success': True, 'data': ajustes, 'error': False}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener ajustes: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@ajapi.route('/ajustes', methods=['POST'])
def add_ajuste():
    dao = AjusteDao()
    data = request.get_json()
    required = ['nro_ajuste','id_empleado','id_sucursal','id_deposito','fecha','tipo_ajuste','detalle_ajuste']
    for campo in required:
        if campo not in data or data[campo] is None or data[campo] == '':
            return jsonify({'success': False, 'error': f'El campo {campo} es obligatorio.'}), 400
    try:
        detalle = [AjusteDetalleDto(
                    id_ajuste=None,
                    id_item=item['id_item'],
                    cantidad=item['cantidad'],
                    precio_unitario=item.get('precio_unitario',0),
                    motivo=item.get('motivo')
                   ) for item in data['detalle_ajuste']]

        estado = EstadoAjuste(id=1, descripcion='Pendiente')

        cabecera = AjusteDto(
            id_ajuste=None,
            nro_ajuste=data['nro_ajuste'],
            id_empleado=data['id_empleado'],
            id_sucursal=data['id_sucursal'],
            id_deposito=data['id_deposito'],
            empresa=data.get('empresa'),
            funcionario=data.get('funcionario'),
            fecha=date.fromisoformat(data['fecha']),
            tipo_ajuste=data['tipo_ajuste'],
            estado=estado,
            motivo_general=data.get('motivo_general'),
            detalle_ajuste=detalle
        )

        result = dao.agregar(cabecera)
        if result:
            return jsonify({'success': True, 'error': None}), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el ajuste.'}), 500
    except Exception as e:
        app.logger.error(f"Error al crear ajuste: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@ajapi.route('/sucursal-depositos/<int:id_sucursal>', methods=['GET'])
def get_depositos_sucursal(id_sucursal):
    dao = SucursalDao()
    try:
        depositos = dao.get_sucursal_depositos(id_sucursal)
        return jsonify({'success': True, 'data': depositos, 'error': False}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener depositos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@ajapi.route('/ajustes/<int:id_ajuste>', methods=['DELETE'])
def anular_ajuste(id_ajuste):
    dao = AjusteDao()
    try:
        ok = dao.anular(id_ajuste)
        if ok:
            return jsonify({'success': True, 'message': 'Ajuste anulado.' , 'error': False}), 200
        return jsonify({'success': False, 'error': 'No se pudo anular.'}), 500
    except Exception as e:
        app.logger.error(f"Error al anular ajuste: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
