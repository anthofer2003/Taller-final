from datetime import date
from flask import Blueprint, jsonify, request, current_app as app
from app.dao.gestionar_compras.registrar_presupuesto_compras.presupuesto_compras_dao import PresupuestoDeComprasDao
from app.dao.gestionar_compras.registrar_presupuesto_compras.dto.presupuesto_compras_dto import PresupuestoDeComprasDto
from app.dao.gestionar_compras.registrar_presupuesto_compras.dto.presupuesto_compra_detalle_dto import PresupuestoDeComprasDetalleDto
from app.dao.referenciales.estado_presupuesto_compra.estado_presupuesto_compra_dto import EstadoPresupuestoCompra
from app.dao.referenciales.sucursal.sucursal_dao import SucursalDao

pdpmodapi = Blueprint('pdpmodapi', __name__)

# ===============================
#   GET - Listar presupuestos
# ===============================
@pdpmodapi.route('/presupuestos', methods=['GET'])
def get_presupuestos():
    dao = PresupuestoDeComprasDao()

    try:
        presupuestos = dao.obtener_presupuestos()
        return jsonify({
            'success': True,
            'data': presupuestos,
            'error': False
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener los presupuestos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
#   POST - Crear presupuesto
# ===============================
@pdpmodapi.route('/presupuestos', methods=['POST'])
def add_presupuesto():
    dao = PresupuestoDeComprasDao()
    data = request.get_json()

    # Campos requeridos en el JSON
    campos_requeridos = [
        'nro_presupuesto',
        'id_empleado',
        'id_proveedor',
        'id_sucursal',
        'id_deposito',
        'empresa',
        'funcionario',
        'fecha',
        'detalle_presupuesto'
    ]

    # Validación de campos requeridos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or data[campo] == '':
            return jsonify({
                'success': False,
                'error': f'El campo "{campo}" es obligatorio y no puede estar vacío.'
            }), 400

    try:
        nro_presupuesto = data['nro_presupuesto']
        id_empleado = data['id_empleado']
        id_proveedor = data['id_proveedor']
        id_sucursal = data['id_sucursal']
        id_deposito = data['id_deposito']
        empresa = data['empresa']
        funcionario = data['funcionario']
        fecha = date.fromisoformat(data['fecha'])
        detalle_presupuesto = data['detalle_presupuesto']

        # Crear los DTOs del detalle
        detalle_dto = [
            PresupuestoDeComprasDetalleDto(
                id_presupuesto=None,
                id_item=item['id_item'],
                cantidad=item['cantidad'],
                precio_iva=item.get('precio_iva', 0)
            )
            for item in detalle_presupuesto
        ]

        # Estado inicial = Pendiente (id=1 o 2 según configuración)
        estado = EstadoPresupuestoCompra(id=1, descripcion='Pendiente')

        # Crear DTO cabecera
        cabecera_dto = PresupuestoDeComprasDto(
            id_presupuesto=None,
            nro_presupuesto=nro_presupuesto,
            id_empleado=id_empleado,
            id_proveedor=id_proveedor,
            id_sucursal=id_sucursal,
            id_deposito=id_deposito,
            empresa=empresa,
            funcionario=funcionario,
            fecha=fecha,
            estado=estado,
            detalle_presupuesto=detalle_dto
        )

        # Insertar en BD
        resultado = dao.agregar(presupuesto_dto=cabecera_dto)

        if resultado:
            return jsonify({
                'success': True,
                'error': None,
                'message': 'Presupuesto creado correctamente.'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo registrar el presupuesto. Consulte con el administrador.'
            }), 500

    except Exception as e:
        app.logger.error(f"Error al crear presupuesto: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# =====================================
#   GET - Obtener depósitos por sucursal
# =====================================
@pdpmodapi.route('/sucursal-depositos/<int:id_sucursal>', methods=['GET'])
def get_sucursal_depositos(id_sucursal):
    dao = SucursalDao()

    try:
        depositos = dao.get_sucursal_depositos(id_sucursal)
        return jsonify({
            'success': True,
            'data': depositos,
            'error': False
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener depósitos por sucursal: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# =====================================
#   DELETE - Anular presupuesto
# =====================================
@pdpmodapi.route('/presupuestos/<int:id_presupuesto>', methods=['DELETE'])
def anular_presupuesto(id_presupuesto):
    dao = PresupuestoDeComprasDao()

    try:
        resultado = dao.anular(id_presupuesto)
        if resultado:
            return jsonify({
                'success': True,
                'message': 'Presupuesto anulado correctamente.',
                'error': False
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo anular el presupuesto. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al anular el presupuesto: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
