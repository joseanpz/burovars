from dataclasses import dataclass, field
from typing import List

from app.buro.agregadores import (ConstructorVariablesAgregadasCuentas,
                                  CtrlVariablesConsultas, CtrlVariablesScore,
                                  MapeoVariablesCuentas,
                                  VariablesVectorFechaCuentasIngresos)
from app.inegi.agregadores import (CensoHogar, CensoPVAgeb, CensoVivienda,
                                   CPACensoHogar, CPACensoPV, CPACensoVivienda)
from app.inegi.models import M2MCodigoPostalAgeb
from mlwrapper.variables.cweb.originacion import (SubVariablesConsultas,
                                                  SubVariablesCuentas,
                                                  SubVariablesCuentasIngresos,
                                                  SubVariablesInegiHogar,
                                                  SubVariablesInegiPV,
                                                  SubVariablesInegiVivienda,
                                                  SubVariablesScore,
                                                  VariablesConsultas,
                                                  VariablesCuentas,
                                                  VariablesInegiHogar,
                                                  VariablesInegiPV,
                                                  VariablesInegiVivienda,
                                                  VariablesScore,
                                                  xgb_originacion_model)


class ControladorVariablesConsultas(CtrlVariablesConsultas):

    @property
    def campos(self):
        return xgb_originacion_model.campos_consultas

    @property
    def subcampos(self):
        return xgb_originacion_model.subcampos_consultas

    @property
    def clase_variables(self):
        return VariablesConsultas

    @property
    def clase_subcampo(self):
        return SubVariablesConsultas


class ControladorVariablesScore(CtrlVariablesScore):

    @property
    def campos(self):
        return xgb_originacion_model.campos_score

    @property
    def subcampos(self):
        return xgb_originacion_model.subcampos_score

    @property
    def clase_variables(self):
        return VariablesScore

    @property
    def clase_subcampo(self):
        return SubVariablesScore


class ControladorSubVariablesCuentas(MapeoVariablesCuentas):

    @property
    def subcampos(self):
        return xgb_originacion_model.subcampos_cuentas

    @property
    def clase_subcampo(self):
        return SubVariablesCuentas


class ControladorSubVariablesCuentasIngresos(VariablesVectorFechaCuentasIngresos):

    @property
    def subcampos(self):
        return xgb_originacion_model.subcampos_cuentas_ingresos

    @property
    def clase_subcampo(self):
        return SubVariablesCuentasIngresos


class ControladorVariablesCuentas(ConstructorVariablesAgregadasCuentas):

    @property
    def campos(self):
        return xgb_originacion_model.campos_cuentas

    @property
    def clase_variables(self):
        return VariablesCuentas

    @property
    def clase_subvar(self):
        return ControladorSubVariablesCuentas

    @property
    def clase_subvar_vec(self):
        return ControladorSubVariablesCuentasIngresos
