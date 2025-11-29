from flask import Blueprint, jsonify, request, current_app as app
from app.dao.referenciales.proveedor.proveedor_dao import ProveedorDao

provapi = Blueprint('provapi', __name__)

@provapi.route('/api/v1/proveedores', methods=['GET'])
def get_proveedores():
    dao = ProveedorDao()
    try:
        proveedores = dao.get_proveedores()
        return jsonify({'success': True, 'data': proveedores, 'error': False}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener proveedores: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500
