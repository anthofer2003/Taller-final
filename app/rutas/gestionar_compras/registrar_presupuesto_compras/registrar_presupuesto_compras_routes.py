from flask import Blueprint, render_template
from app.dao.referenciales.sucursal.sucursal_dao import SucursalDao
from app.dao.referenciales.proveedor.proveedor_dao import ProveedorDao
from app.dao.referenciales.deposito.deposito_dao import DepositoDao
from app.dao.referenciales.item.item_dao import ItemDao

# ===========================================================
# Definición del Blueprint con carpeta de plantillas local
# ===========================================================
# Flask buscará los archivos HTML dentro de:
# app/routes/gestionar_compras/registrar_presupuesto_compras/templates/
pdpmod = Blueprint('pdpmod', __name__, template_folder='templates')

# ==============================================
#   INDEX - Página principal de presupuestos
# ==============================================
@pdpmod.route('/presupuestos-index')
def presupuestos_index():
    # Renderiza el template: templates/presupuesto-index.html
    return render_template('presupuestos-index.html')

# ==============================================
#   FORMULARIO - Página de agregar presupuesto
# ==============================================
@pdpmod.route('/presupuestos-agregar')
def presupuestos_agregar():
    sdao = SucursalDao()
    pdao = ProveedorDao()
    ddao = DepositoDao()
    idao = ItemDao()

    return render_template(
        'presupuestos-agregar.html',
        sucursales=sdao.get_sucursales(),
        proveedores=pdao.get_proveedores(),
        depositos=ddao.get_depositos(),
        items=idao.get_items()
    )
