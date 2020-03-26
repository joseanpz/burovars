from dataclasses import make_dataclass

from mlwrapper.mlmodelos.cweb.models import xgb_originacion_model

SubVariablesCuentas = make_dataclass(
    'SubVariablesCuentas',
    [(campo.nombre, float, None) for campo in xgb_originacion_model.subcampos_cuentas]
)

SubVariablesCuentasIngresos = make_dataclass(
    'SubVariablesCuentasIngresos',
    [(campo.nombre, float, None) for campo in xgb_originacion_model.subcampos_cuentas_ingresos]
)

SubVariablesConsultas = make_dataclass(
    'SubVariablesConsultas',
    [(campo.nombre, float, None) for campo in xgb_originacion_model.subcampos_consultas]
)

SubVariablesScore = make_dataclass(
    'SubVariablesScore',
    [(campo.nombre, float, None) for campo in xgb_originacion_model.subcampos_score]
)

SubVariablesInegiPV = make_dataclass(
    'SubVariablesInegiPV',
    [(campo.nombre, float, None) for campo in xgb_originacion_model.subcampos_inegi_pv]
)

SubVariablesInegiVivienda = make_dataclass(
    'SubVariablesInegiVivienda',
    [(campo.nombre, float, None) for campo in xgb_originacion_model.subcampos_inegi_vivienda]
)

SubVariablesInegiHogar = make_dataclass(
    'SubVariablesInegiHogar',
    [(campo.nombre, float, None) for campo in xgb_originacion_model.subcampos_inegi_hogar]
)

VariablesCuentas = make_dataclass(
    'VariablesCuentas',
    [(campo.nombre, float, None) for campo in xgb_originacion_model.campos_cuentas]
)

VariablesConsultas = make_dataclass(
    'VariablesConsultas',
    [(campo.nombre, float, None) for campo in xgb_originacion_model.campos_consultas]
)

VariablesScore = make_dataclass(
    'VariablesScore',
    [(campo.nombre, float, None) for campo in xgb_originacion_model.campos_score]
)

VariablesInegiPV = make_dataclass(
    'VariablesInegiPV',
    [(campo.nombre, float, None) for campo in xgb_originacion_model.campos_inegi_pv]
)

VariablesInegiVivienda = make_dataclass(
    'VariablesInegiVivienda',
    [(campo.nombre, float, None) for campo in xgb_originacion_model.campos_inegi_vivienda]
)

VariablesInegiHogar = make_dataclass(
    'VariablesInegiHogar',
    [(campo.nombre, float, None) for campo in xgb_originacion_model.campos_inegi_hogar]
)

VariablesOrig = make_dataclass(
    'VariablesOrig',
    [(campo.nombre, float, None) for campo in xgb_originacion_model.campos]
)
