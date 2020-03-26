from dataclasses import make_dataclass

from app.buro.agregadores import (ConstructorVariablesAgregadasCuentas,
                                  CtrlVariablesConsultas,
                                  MapeoVariablesCuentas)
from mlwrapper.campo.models import CampoAgregado

max_ms_op_tu_all = CampoAgregado('cuentas', 'max', 'ms_op', 'tu_all')
num_iq_03_no_impl = CampoAgregado('consultas', 'num', 'iq_03m_no_impl')


VariablesConsultasNoHit = make_dataclass(
    'VariablesConsultasNoHit',
    [(num_iq_03_no_impl.nombre, float, None),]
)

SubVariablesConsultasNoHit = make_dataclass(
    'SubVariablesConsultas',
    [(num_iq_03_no_impl.campo.nombre, float, None)]
)

VariablesCuentasNoHit = make_dataclass(
    'VariablesCuentasNoHit',
    [(max_ms_op_tu_all.nombre, float, None)]
)

SubVariablesCuentasNoHit = make_dataclass(
    'SubVariablesCuentasNoHit',
    [(max_ms_op_tu_all.campo.nombre, float, None)]
)


class ControladorVariablesConsultasNoHit(CtrlVariablesConsultas):

    @property
    def campos(self):
        return [num_iq_03_no_impl]

    @property
    def subcampos(self):
        return [num_iq_03_no_impl.campo]

    @property
    def clase_variables(self):
        return VariablesConsultasNoHit

    @property
    def clase_subcampo(self):
        return SubVariablesConsultasNoHit


class ControladorSubVariablesCuentasNoHit(MapeoVariablesCuentas):

    @property
    def subcampos(self):
        return [max_ms_op_tu_all.campo]

    @property
    def clase_subcampo(self):
        return SubVariablesCuentasNoHit


class ControladorVariablesCuentasNoHit(ConstructorVariablesAgregadasCuentas):

    @property
    def campos(self):
        return [max_ms_op_tu_all]

    @property
    def clase_variables(self):
        return VariablesCuentasNoHit

    @property
    def clase_subvar(self):
        return ControladorSubVariablesCuentasNoHit
