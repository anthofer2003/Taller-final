from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.deposito.deposito_dao import DepositoDao


depoapi = Blueprint('depoapi', __name__)


@depoapi.route('/depositos', methods=['GET'])
def get_depositos():
    dao = DepositoDao()
    try:
        depositos = dao.get_depositos()
        return jsonify({
            'success': True,
            'data': depositos,
            'error': False
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener depósitos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno. Consulte con el administrador.'
        }), 500
