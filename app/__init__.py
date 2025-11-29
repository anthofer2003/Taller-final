from flask import Flask
from werkzeug.security import generate_password_hash 
## instancia para arrancar el proyecto
app = Flask (__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# Contraseña que deseas hashear
password = ""

# Generar el hash de la contraseña con un algoritmo de scrypt
hashed_password = generate_password_hash(password, method='scrypt', salt_length=16)

# Asegurarse de que el hash tenga 300 caracteres
print(hashed_password[:300])

# importar referenciales
from app.rutas.referenciales.ciudad.ciudad_routes import ciumod
from app.rutas.referenciales.pais.pais_routes import paimod
from app.rutas.referenciales.persona.persona_routes import persomod
from app.rutas.referenciales.estudiante.estudiante_routes import estumod
from app.rutas.referenciales.profesor.profesor_routes import profemod
from app.rutas.referenciales.facultad.facultad_routes import facumod
from app.rutas.referenciales.carrera.carrera_routes import carremod
from app.rutas.referenciales.examen.examen_routes import examod
from app.rutas.referenciales.certificado.certificado_routes import certimod
from app.rutas.referenciales.turno.turno_routes import turmod

from app.rutas.login.login_routes import login_bp

app.register_blueprint(login_bp)

# registrar referenciales
modulo0 = '/referenciales'
app.register_blueprint(ciumod, url_prefix=f'{modulo0}/ciudad')
app.register_blueprint(paimod, url_prefix=f'{modulo0}/pais')
app.register_blueprint(persomod, url_prefix=f'{modulo0}/persona')
app.register_blueprint(estumod, url_prefix=f'{modulo0}/estudiante')
app.register_blueprint(profemod, url_prefix=f'{modulo0}/profesor')
app.register_blueprint(facumod, url_prefix=f'{modulo0}/facultad')
app.register_blueprint(carremod, url_prefix=f'{modulo0}/carrera')
app.register_blueprint(examod, url_prefix=f'{modulo0}/examen')
app.register_blueprint(certimod, url_prefix=f'{modulo0}/certificado')
app.register_blueprint(turmod, url_prefix=f'{modulo0}/turno')

# importar gestionar compras
from app.rutas.gestionar_compras.registrar_pedido_compras.registrar_pedido_compras_routes \
    import pdcmod
from app.rutas.gestionar_compras.registrar_presupuesto_proveedor.registrar_presupuesto_proveedor_routes \
    import pp_mod
from app.rutas.gestionar_compras.registrar_orden_compras.registrar_orden_compras_routes \
    import ordmod
from app.rutas.gestionar_compras.registrar_ajustes.registrar_ajustes_routes \
    import ajmod

# registro de modulos - gestionar compras
modulo1 = '/gestionar-compras'
app.register_blueprint(pdcmod, url_prefix=f'{modulo1}/registrar-pedido-compras')
app.register_blueprint(pp_mod, url_prefix=f'{modulo1}/registrar-presupuesto-compras')
app.register_blueprint(ordmod, url_prefix=f'{modulo1}/registrar-orden-compras')
app.register_blueprint(ajmod, url_prefix=f'{modulo1}/registrar-ajustes')

from app.rutas.referenciales.ciudad.ciudad_api import ciuapi
from app.rutas.referenciales.sucursal.sucursal_api import sucapi
from app.rutas.referenciales.proveedor.proveedor_api import provapi
from app.rutas.referenciales.item.item_api import itemsapi
from app.rutas.referenciales.deposito.deposito_api import depoapi

from app.rutas.gestionar_compras.registrar_pedido_compras.registrar_pedido_compras_api \
    import pdcapi
from app.rutas.gestionar_compras.registrar_presupuesto_proveedor.registrar_presupuesto_proveedor_api \
    import pp_api
from app.rutas.gestionar_compras.registrar_orden_compras.registrar_orden_compras_api \
    import ordapi
from app.rutas.gestionar_compras.registrar_ajustes.registrar_ajustes_api \
    import ajapi
from app.rutas.referenciales.pais.pais_api import paisapi
from app.rutas.referenciales.persona.persona_api import persona_api
from app.rutas.referenciales.estudiante.estudiante_api import estudiante_api
from app.rutas.referenciales.profesor.profesor_api import profesor_api
from app.rutas.referenciales.facultad.facultad_api import facultad_api
from app.rutas.referenciales.carrera.carrera_api import carrera_api
from app.rutas.referenciales.examen.examen_api import tipo_examen_api
from app.rutas.referenciales.certificado.certificado_api import tipocertificado_api
from app.rutas.referenciales.turno.turno_api import turno_api

# APIS v1
apiversion1 = '/api/v1'
app.register_blueprint(ciuapi, url_prefix=apiversion1)
app.register_blueprint(sucapi, url_prefix=apiversion1)
app.register_blueprint(provapi, url_prefix=apiversion1)
app.register_blueprint(depoapi, url_prefix=apiversion1)
app.register_blueprint(itemsapi, url_prefix=apiversion1)
app.register_blueprint(persona_api, url_prefix=apiversion1)
app.register_blueprint(estudiante_api, url_prefix=apiversion1)
app.register_blueprint(profesor_api, url_prefix=apiversion1)
app.register_blueprint(facultad_api, url_prefix=apiversion1)
app.register_blueprint(carrera_api, url_prefix=apiversion1)
app.register_blueprint(tipo_examen_api, url_prefix=apiversion1)
app.register_blueprint(tipocertificado_api, url_prefix=apiversion1)
app.register_blueprint(turno_api, url_prefix=apiversion1)

# Gestionar compras API
app.register_blueprint(pdcapi, url_prefix=f'{apiversion1}/{modulo1}/registrar-pedido-compras')
app.register_blueprint(pp_api, url_prefix=f'{apiversion1}/{modulo1}/registrar-presupuesto-compras')
app.register_blueprint(ordapi, url_prefix=f'{apiversion1}/{modulo1}/registrar-orden-compras')
app.register_blueprint(ajapi, url_prefix=f'{apiversion1}/{modulo1}/registrar-ajustes')