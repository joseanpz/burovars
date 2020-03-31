from dataclasses import dataclass, field, make_dataclass
from typing import List, Any

from campo.models import Campo, CampoAgregado

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

    # types
    subvariables_cuentas: type = field(init=False)  # container class
    subvariables_vector_cuentas: type = field(init=False)  # container class
    variables_cuentas: type = field(init=False)  # container class

    subvariables_consultas: type = field(init=False) # container class
    variables_consultas: type = field(init=False) # container class

    subvariables_score: type = field(init=False) # container class
    variables_score: type = field(init=False) # container class

    def __post_init__(self):
        self.campos = self.construye_campos()
        self.configura_features_consultas()
        self.configura_features_score()
        self.configura_features_cuentas()

    def configura_features_consultas(self):
        self.subvariables_consultas = make_dataclass(
            'SubVariablesConsultas',
            [(campo.nombre, float, None) for campo in self.subcampos_consultas]
        )

        self.variables_consultas = make_dataclass(
            'VariablesConsultas',
            [(campo.nombre, float, None) for campo in self.campos_consultas]
        )

    def configura_features_score(self):
        self.subvariables_score = make_dataclass(
            'SubVariablesScore',
            [(campo.nombre, float, None) for campo in self.subcampos_score]
        )

        self.variables_score = make_dataclass(
            'VariablesScore',
            [(campo.nombre, float, None) for campo in self.campos_score]
        )

    def configura_features_cuentas(self):
        self.subvariables_cuentas = make_dataclass(
            'SubVariablesCuentas',
            [(campo.nombre, float, None) for campo in self.subcampos_cuentas]
        )

        self.subvariables_vector_cuentas = make_dataclass(
            'SubVariablesVectorCuentas',
            [(campo.nombre, float, None) for campo in self.subcampos_vector_cuentas]
        )

        self.variables_cuentas = make_dataclass(
            'VariablesCuentas',
            [(campo.nombre, float, None) for campo in self.campos_cuentas]
        )

    def construye_campos(self):
        for i in range(0, len(self.features)):
            for rep in replaces:
                if self.features[i] == rep:
                    self.features[i] = rep.replace('_tu', '')
        _campos = {}
        with open('caracteristicas/varmap.csv') as varmap_file:
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
    def campos_score(self):
        return tuple(filter(lambda x: x.segmento == 'score', self.campos))

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
    def subcampos_vector_cuentas(self):
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
