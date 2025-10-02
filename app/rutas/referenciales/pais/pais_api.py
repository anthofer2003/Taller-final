import re
from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.pais.PaisDao import PaisDao

paisapi = Blueprint('paisapi', __name__)

# Expresión regular para validar sólo letras (mayúsculas/minúsculas), espacios y tildes
VALIDAR_DESCRIPCION = re.compile(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$')

def es_descripcion_valida(descripcion):
    return bool(VALIDAR_DESCRIPCION.fullmatch(descripcion.strip()))

# Trae todos los países
@paisapi.route('/paises', methods=['GET'])
def getPaises():
    paisdao = PaisDao()
    try:
        paises = paisdao.getPaises()
        return jsonify({
            'success': True,
            'data': paises,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los países: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae un país por ID
@paisapi.route('/paises/<int:pais_id>', methods=['GET'])
def getPais(pais_id):
    paisdao = PaisDao()
    try:
        pais = paisdao.getPaisById(pais_id)
        if pais:
            return jsonify({
                'success': True,
                'data': pais,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el país con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener país: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo país
@paisapi.route('/paises', methods=['POST'])
def addPais():
    data = request.get_json()
    paisdao = PaisDao()

    if not data or 'descripcion' not in data or not data['descripcion'].strip():
        return jsonify({
            'success': False,
            'error': 'El campo descripcion es obligatorio y no puede estar vacío.'
        }), 400

    descripcion = data['descripcion'].strip()

    if not es_descripcion_valida(descripcion):
        return jsonify({
            'success': False,
            'error': 'La descripción solo puede contener letras y espacios.'
        }), 400

    try:
        resultado = paisdao.guardarPais(descripcion)

        if resultado["success"]:
            return jsonify({
                'success': True,
                'data': {
                    'id': resultado["id"],
                    'descripcion': descripcion.upper()
                },
                'message': resultado["message"]
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': resultado["message"]
            }), 409

    except Exception as e:
        app.logger.error(f"Error al agregar país: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza un país existente
@paisapi.route('/paises/<int:pais_id>', methods=['PUT'])
def updatePais(pais_id):
    data = request.get_json()
    paisdao = PaisDao()

    if not data or 'descripcion' not in data or not data['descripcion'].strip():
        return jsonify({
            'success': False,
            'error': 'El campo descripcion es obligatorio y no puede estar vacío.'
        }), 400

    descripcion = data['descripcion'].strip()

    if not es_descripcion_valida(descripcion):
        return jsonify({
            'success': False,
            'error': 'La descripción solo puede contener letras y espacios.'
        }), 400

    try:
        resultado = paisdao.updatePais(pais_id, descripcion)

        if resultado["success"]:
            return jsonify({
                'success': True,
                'data': {'id': pais_id, 'descripcion': descripcion.upper()},
                'message': resultado.get("message", "País actualizado exitosamente."),
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': resultado.get("message", "No se pudo actualizar el país.")
            }), 409

    except Exception as e:
        app.logger.error(f"Error al actualizar país: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina un país por ID
@paisapi.route('/paises/<int:pais_id>', methods=['DELETE'])
def deletePais(pais_id):
    paisdao = PaisDao()
    try:
        if paisdao.deletePais(pais_id):
            return jsonify({
                'success': True,
                'mensaje': f'País con ID {pais_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el país con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar país: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
