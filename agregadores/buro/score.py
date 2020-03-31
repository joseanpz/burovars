from dataclasses import dataclass, field
from typing import List

from buro.models import VariablesBuroScoreModel
from campo.models import CampoAgregado


@dataclass
class ControladorSubVariablesScore:
    lista_var_buro_score: List[VariablesBuroScoreModel]
    lista_var_score: List[dict] = field(init=False)

    @property
    def clase_subcampo(self):
        return dict

    @property
    def subcampos(self):
        return []

    def __post_init__(self):
        self.lista_var_score = [
            self.clase_subcampo(**{
                campo.nombre: getattr(var_buro_score, campo.nombre, None)
                for campo in self.subcampos
            })
            for var_buro_score in self.lista_var_buro_score
        ]


@dataclass
class CtrlVariablesScore(ControladorSubVariablesScore):
    var_agregadas_score: dict = field(init=False)

    @property
    def campos(self):
        return []

    @property
    def clase_variables(self):
        return dict

    def __post_init__(self):
        super().__post_init__()
        self.var_agregadas_score = self.clase_variables(**{
            campo_agregado.nombre: self.contruye_variables_agregadas_score(campo_agregado)
            for campo_agregado in self.campos
        })

    def contruye_variables_agregadas_score(self, campo_agr: CampoAgregado):
        if campo_agr.agregacion == 'val':
            values = list(map(lambda x: getattr(x, campo_agr.campo.nombre, 0),
                              self.lista_var_score))
            return sum(values)
        else:
            return None