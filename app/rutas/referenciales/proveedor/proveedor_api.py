from flask import Blueprint, jsonify, current_app as app
from app.dao.referenciales.proveedor.proveedor_dao import ProveedorDao

proapi = Blueprint('proapi', __name__)

# --- Proveedores ---
@proapi.route('/proveedores', methods=['GET'])
def get_proveedores():
    dao = ProveedorDao()
    try:
        proveedores = dao.get_proveedores()
        return jsonify({
            'success': True,
            'data': proveedores,
            'error': False
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener proveedores: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno. Consulte con el administrador.'
        }), 500




