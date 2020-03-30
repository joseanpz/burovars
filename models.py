import pickle
from dataclasses import astuple, dataclass, field
from typing import List

import numpy as np

from mlwrapper import config
from mlwrapper.campo.models import Campo, CampoAgregado
from xgboost import Booster, DMatrix

replaces = [
    # originacion
    "avg_cred_max_nbk_tu_cl_acc",
    "avg_max_mop_bal_nbk_tu_op_acc",
    "num_max_mop_bal_nbk_tu_op_acc",
    "num_num_dlq_bal_nbk_tu_cl_acc",
    # ingresos
]


@dataclass
class FeaturesBuro:
    features: List[str]
    campos: List[CampoAgregado] = field(init=False)

    def __post_init__(self):
        self.campos = self.construye_campos() 

    def construye_campos(self):
        for i in range(0, len(self.features)):
            for rep in replaces:
                if self.features[i] == rep:
                    self.features[i] = rep.replace('_tu', '')
        _campos = {}
        with open('varmap.csv') as varmap_file:
            for line in varmap_file:
                line_split = line.strip('\n').split('|')
                for feature in self.features:
                    if line_split[0] == feature:
                        try:
                            field_split = line_split[1].split(',')
                            subfield_split = field_split[2].split('-')
                            if len(subfield_split) > 1:
                                field_split[2] = CampoAgregado(*subfield_split)
                            if field_split[-1] == '':
                                field_split[-1] = None
                            _campos[feature] = CampoAgregado(*field_split)
                        except TypeError as e:
                            print(e)
                            raise e

        return [_campos[feature] for feature in self.features]

    @property
    def campos_cuentas(self):
        return tuple(filter(lambda x: x.segmento == 'cuentas', self.campos))

    @property
    def campos_consultas(self):
        return tuple(filter(lambda x: x.segmento == 'consultas', self.campos))

    @property
    def subcampos_cuentas(self):
        subcampos = set(map(
            lambda x: x.campo,
            filter(lambda x: not isinstance(x.campo, CampoAgregado), self.campos_cuentas)
        ))
        ret = set([])
        while subcampos:
            subcampo = subcampos.pop()
            if subcampo.variable == 'mop':
                ret.add(Campo('cuentas', 't_mop', subcampo.sufijo))
                ret.add(Campo('cuentas', 'peso_mop', subcampo.sufijo))
            else:
                ret.add(subcampo)
        return ret

    @property
    def subcampos_cuentas_ingresos(self):
        return set(map(
            lambda x: x.campo,
            filter(lambda x: getattr(x.campo, 'segmento', None) == 'ingreso', self.campos_cuentas)
        ))

    @property
    def subcampos_consultas(self):
        return set(map(lambda x: x.campo, self.campos_consultas))

    @property
    def subcampos_score(self):
        return set(map(lambda x: x.campo, self.campos_score))


@dataclass
class MLModel:
    xgb_model_path: str
    xgb_model: Booster = field(init=False)
    campos: List[CampoAgregado] = field(init=False)

    def __post_init__(self):
        self.xgb_model = pickle.load(open(self.xgb_model_path, 'rb'))
        self.campos = self.construye_campos()

    def construye_campos(self):
        features = getattr(self.xgb_model, '_feature_names', getattr(self.xgb_model, 'feature_names', None))
        # features = feature_names
        for i in range(0, len(features)):
            for rep in replaces:
                if features[i] == rep:
                    features[i] = rep.replace('_tu', '')
        _campos = {}
        with open('mlwrapper/varmap.csv') as varmap_file:
            for line in varmap_file:
                line_split = line.strip('\n').split('|')
                for feature in features:
                    if line_split[0] == feature:
                        try:
                            field_split = line_split[1].split(',')
                            subfield_split = field_split[2].split('-')
                            if len(subfield_split) > 1:
                                field_split[2] = CampoAgregado(*subfield_split)
                            if field_split[-1] == '':
                                field_split[-1] = None
                            _campos[feature] = CampoAgregado(*field_split)
                        except TypeError as e:
                            print(e)
                            raise e

        return [_campos[feature] for feature in features]

    @property
    def campos_score(self):
        return tuple(filter(lambda x: x.segmento == 'score', self.campos))

    @property
    def campos_cuentas(self):
        return tuple(filter(lambda x: x.segmento == 'cuentas', self.campos))

    @property
    def campos_consultas(self):
        return tuple(filter(lambda x: x.segmento == 'consultas', self.campos))

    @property
    def campos_inegi(self):
        return tuple(filter(lambda x: x.segmento == 'inegi', self.campos))

    @property
    def campos_inegi_pv(self):
        return tuple(filter(lambda x: x.campo.segmento == 'pv', self.campos_inegi))

    @property
    def campos_inegi_vivienda(self):
        return tuple(filter(lambda x: x.campo.segmento == 'vivienda', self.campos_inegi))

    @property
    def campos_inegi_hogar(self):
        return tuple(filter(lambda x: x.campo.segmento == 'hogar', self.campos_inegi))

    @property
    def subcampos_inegi_pv(self):
        return set(map(lambda x: x.campo, self.campos_inegi_pv))

    @property
    def subcampos_inegi_vivienda(self):
        return set(map(lambda x: x.campo, self.campos_inegi_vivienda))

    @property
    def subcampos_inegi_hogar(self):
        return set(map(lambda x: x.campo, self.campos_inegi_hogar))

    @property
    def subcampos_cuentas(self):
        subcampos = set(map(
            lambda x: x.campo,
            filter(lambda x: not isinstance(x.campo, CampoAgregado), self.campos_cuentas)
        ))
        ret = set([])
        while subcampos:
            subcampo = subcampos.pop()
            if subcampo.variable == 'mop':
                ret.add(Campo('cuentas', 't_mop', subcampo.sufijo))
                ret.add(Campo('cuentas', 'peso_mop', subcampo.sufijo))
            else:
                ret.add(subcampo)
        return ret

    @property
    def subcampos_cuentas_ingresos(self):
        return set(map(
            lambda x: x.campo,
            filter(lambda x: getattr(x.campo, 'segmento', None) == 'ingreso', self.campos_cuentas)
        ))

    @property
    def subcampos_consultas(self):
        return set(map(lambda x: x.campo, self.campos_consultas))

    @property
    def subcampos_score(self):
        return set(map(lambda x: x.campo, self.campos_score))

    def prediccion(self, variables):  # variables <-> campos
        dm = DMatrix(data=np.array(list(astuple(variables))).reshape(1, -1), feature_names=self.xgb_model.feature_names)
        return self.xgb_model.predict(dm)[0]

    def segmentos_prediccion(self, *variables):  # *variables <-> campos
        lista_variables = []
        for campo in self.campos:
            for vars in variables:
                if hasattr(vars, campo.nombre):
                    lista_variables.append(getattr(vars, campo.nombre))
                    break
        dm = DMatrix(data=np.array(lista_variables).reshape(1, -1), feature_names=self.xgb_model.feature_names)
        return self.xgb_model.predict(dm)[0]


# ingresos
xgb_ingresos_model = MLModel(
    f'mlwrapper/mlmodelos/cweb/bmodels/ingresos_xgb_{config.XGB_CWEB_ING_VERSION}.model')
xgb_ingresos_bc_model = MLModel(
    f'mlwrapper/mlmodelos/cweb/bmodels/xgb_ingresos_bc_{config.XGB_CWEB_ING_BC_VERSION}.model')

# originacion
xgb_originacion_model = MLModel(
    f'mlwrapper/mlmodelos/cweb/bmodels/xgb_originaciontdc_{config.XGB_CWEB_ORI_VERSION}.model')
