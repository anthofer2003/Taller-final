from flask import Blueprint, render_template
from app.dao.referenciales.sucursal.sucursal_dao import SucursalDao
from app.dao.referenciales.item.item_dao import ItemDao
from app.dao.referenciales.empleado.empleado_dao import EmpleadoDao
from app.dao.referenciales.deposito.deposito_dao import DepositoDao

ajmod = Blueprint('ajmod', __name__, template_folder='templates')

@ajmod.route('/ajustes-index')
def ajustes_index():
    return render_template('ajustes-index.html')

@ajmod.route('/ajustes-agregar')
def ajustes_agregar():
    sdao = SucursalDao()
    idao = ItemDao()
    edao = EmpleadoDao()
    ddao = DepositoDao()

    return render_template(
        'ajustes-agregar.html',
        sucursales = sdao.get_sucursales(),
        items = idao.get_items(),
        empleados = edao.get_empleados(),
        depositos = ddao.get_depositos()
    )
