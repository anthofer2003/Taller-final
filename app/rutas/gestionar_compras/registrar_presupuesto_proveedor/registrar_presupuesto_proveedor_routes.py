# presupuesto_routes.py

from flask import Blueprint, render_template
from app.dao.referenciales.sucursal.sucursal_dao import SucursalDao
from app.dao.referenciales.proveedor.proveedor_dao import ProveedorDao
from app.dao.referenciales.empleado.empleado_dao import EmpleadoDao
from app.dao.referenciales.producto.producto_dao import ProductoDao

pp_mod = Blueprint('pp_mod', __name__, template_folder='templates')

@pp_mod.route('/presupuestos-index')
def presupuestos_index():
    return render_template('presupuestos-index.html')

@pp_mod.route('/presupuestos-agregar')
def presupuestos_agregar():
    sdao = SucursalDao()
    prov_dao = ProveedorDao()
    emp_dao = EmpleadoDao()
    pdao = ProductoDao()
    return render_template('presupuestos-agregar.html',
                           sucursales=sdao.get_sucursales(),
                           proveedores=prov_dao.get_proveedores(),
                           empleados=emp_dao.get_empleados(),
                           productos=pdao.get_productos())
