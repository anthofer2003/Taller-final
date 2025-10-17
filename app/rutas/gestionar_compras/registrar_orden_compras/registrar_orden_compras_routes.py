from flask import Blueprint, render_template
from app.dao.referenciales.sucursal.sucursal_dao import SucursalDao
from app.dao.referenciales.proveedor.proveedor_dao import ProveedorDao
from app.dao.referenciales.deposito.deposito_dao import DepositoDao
from app.dao.referenciales.item.item_dao import ItemDao
from app.dao.referenciales.empleado.empleado_dao import EmpleadoDao

ordmod = Blueprint('ordmod', __name__, template_folder='templates')

@ordmod.route('/orden-index')
def orden_index():
    return render_template("orden-index.html")


@ordmod.route('/orden-agregar')
def orden_agregar():
    sdao = SucursalDao()
    pdao = ProveedorDao()
    ddao = DepositoDao()
    idao = ItemDao()
    edao = EmpleadoDao()

    return render_template(
        'orden-agregar.html',
        sucursales=sdao.get_sucursales(),
        proveedores=pdao.get_proveedores(),
        depositos=ddao.get_depositos(),
        items=idao.get_items(),
        empleados=edao.get_empleados()
    )
