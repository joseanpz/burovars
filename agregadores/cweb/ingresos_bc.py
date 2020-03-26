from app.buro.agregadores import (ConstructorVariablesAgregadasCuentas,
                                  CtrlVariablesConsultas,
                                  MapeoVariablesCuentas,
                                  VariablesVectorFechaCuentasIngresos)
from mlwrapper.variables.cweb.ingresos_bc import (SubVariablesConsultas,
                                                  SubVariablesCuentas,
                                                  SubVariablesCuentasIngresos,
                                                  VariablesConsultas,
                                                  VariablesCuentas,
                                                  VariablesCuentas2,
                                                  xgb_ingresos_bc_model)


class ControladorVariablesConsultas(CtrlVariablesConsultas):

    @property
    def campos(self):
        return xgb_ingresos_bc_model.campos_consultas

    @property
    def subcampos(self):
        return xgb_ingresos_bc_model.subcampos_consultas

    @property
    def clase_variables(self):
        return VariablesConsultas

    @property
    def clase_subcampo(self):
        return SubVariablesConsultas


# segmento cuentas
class ControladorSubVariablesCuentas(MapeoVariablesCuentas):

    @property
    def subcampos(self):
        return xgb_ingresos_bc_model.subcampos_cuentas

    @property
    def clase_subcampo(self):
        return SubVariablesCuentas


class ControladorSubVariablesCuentasIngresos(VariablesVectorFechaCuentasIngresos):

    @property
    def subcampos(self):
        return xgb_ingresos_bc_model.subcampos_cuentas_ingresos

    @property
    def clase_subcampo(self):
        return SubVariablesCuentasIngresos


class ControladorVariablesCuentas(ConstructorVariablesAgregadasCuentas):

    @property
    def campos(self):
        return xgb_ingresos_bc_model.campos_cuentas[:254]

    @property
    def clase_variables(self):
        return VariablesCuentas

    @property
    def clase_subvar(self):
        return ControladorSubVariablesCuentas

    @property
    def clase_subvar_vec(self):
        return ControladorSubVariablesCuentasIngresos


class ControladorVariablesCuentas2(ConstructorVariablesAgregadasCuentas):

    @property
    def campos(self):
        return xgb_ingresos_bc_model.campos_cuentas[254:]

    @property
    def clase_variables(self):
        return VariablesCuentas2

    @property
    def clase_subvar(self):
        return ControladorSubVariablesCuentas

    @property
    def clase_subvar_vec(self):
        return ControladorSubVariablesCuentasIngresos
