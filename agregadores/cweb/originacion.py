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


class SubControladorCensoHogar(CensoHogar):

    @property
    def subcampos_inegi_hogar(self):
        return xgb_originacion_model.subcampos_inegi_hogar

    @property
    def clase_subcampo(self):
        return SubVariablesInegiHogar


class ControladorCPACensoHogar(CPACensoHogar):

    @property
    def campos_inegi_hogar_agregados(self):
        return xgb_originacion_model.campos_inegi_hogar

    @property
    def clase_subvar(self):
        return SubControladorCensoHogar

    @property
    def clase_variables(self):
        return VariablesInegiHogar


class SubControladorCensoVivienda(CensoVivienda):

    @property
    def subcampos_inegi_hogar(self):
        return xgb_originacion_model.subcampos_inegi_vivienda

    @property
    def clase_subcampo(self):
        return SubVariablesInegiVivienda


class ControladorCPACensoVivienda(CPACensoVivienda):

    @property
    def campos_inegi_vivienda_agregados(self):
        return xgb_originacion_model.campos_inegi_vivienda

    @property
    def clase_subvar(self):
        return SubControladorCensoVivienda

    @property
    def clase_variables(self):
        return VariablesInegiVivienda


class SubControladorCensoPV(CensoPVAgeb):

    @property
    def subcampos_inegi_pv(self):
        return xgb_originacion_model.subcampos_inegi_pv

    @property
    def clase_subcampo(self):
        return SubVariablesInegiPV


class ControladorCPACPACensoPV(CPACensoPV):

    @property
    def campos_inegi_pv_agregados(self):
        return xgb_originacion_model.campos_inegi_pv

    @property
    def clase_subvar(self):
        return SubControladorCensoPV

    @property
    def clase_variables(self):
        return VariablesInegiPV


@dataclass
class ControladorInegi:
    cps: List[str]
    m2mcpa: M2MCodigoPostalAgeb = field(init=False)
    segmento_pv: ControladorCPACPACensoPV = field(init=False)
    segmento_vivienda: ControladorCPACensoVivienda = field(init=False)
    segmento_hogar: ControladorCPACensoHogar = field(init=False)

    def __post_init__(self):
        self.m2mcpa = M2MCodigoPostalAgeb(self.cps)
        self.segmento_pv = ControladorCPACPACensoPV(cps=self.cps, m2m_cps_agebs=self.m2mcpa)
        self.segmento_vivienda = ControladorCPACensoVivienda(cps=self.cps, m2m_cps_agebs=self.m2mcpa)
        self.segmento_hogar = ControladorCPACensoHogar(cps=self.cps, m2m_cps_agebs=self.m2mcpa)
