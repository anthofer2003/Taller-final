from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.item.item_dao import ItemDao


itemsapi = Blueprint('itemsapi', __name__)

# --- Items ---
@itemsapi.route('/items', methods=['GET'])
def get_items():
    dao = ItemDao()
    try:
        items = dao.get_items()
        return jsonify({
            'success': True,
            'data': items,
            'error': False
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener items: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno. Consulte con el administrador.'
        }), 500
