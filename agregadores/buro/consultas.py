from dataclasses import dataclass, field
from typing import List

from buro.models import VariablesBuroConsultasModel
from campo.models import CampoAgregado


@dataclass
class ControladorSubVariablesConsultas:
    lista_var_buro_consultas: List[VariablesBuroConsultasModel]
    lista_var_consultas: List[dict] = field(init=False)

    @property
    def clase_subcampo(self):
        return dict

    @property
    def subcampos(self):
        return []

    def __post_init__(self):
        self.configura_lista_var_consultas()

    def configura_lista_var_consultas(self):
        self.lista_var_consultas = [
            self.clase_subcampo(**{
                campo.nombre: getattr(var_buro_consultas, campo.nombre, None)
                for campo in self.subcampos
            })
            for var_buro_consultas in self.lista_var_buro_consultas
        ]


@dataclass
class CtrlVariablesConsultas(ControladorSubVariablesConsultas):
    var_agregadas_consultas: dict = field(init=False)

    @property
    def campos(self):
        return []

    @property
    def clase_variables(self):
        return dict

    def __post_init__(self):
        super().__post_init__()
        self.var_agregadas_consultas = self.clase_variables(**{
            campo_agregado.nombre: self.contruye_variables_agregadas_consultas(campo_agregado)
            for campo_agregado in self.campos
        })

    def contruye_variables_agregadas_consultas(self, campo_agr: CampoAgregado):
        if campo_agr.agregacion == 'num':
            values = list(map(
                lambda x: x.get(campo_agr.campo.nombre, 0)
                if isinstance(x, dict) else getattr(x, campo_agr.campo.nombre, 0)
                , self.lista_var_consultas))
            return sum(values)
        elif campo_agr.agregacion == 'pct_num':
            # porcentaje de las consultas del sufijo y
            # las que se hicieron en total a los meses buscados
            values = list(map(lambda x: getattr(x, campo_agr.campo.nombre, 0),
                              self.lista_var_consultas))
            values2 = list(map(lambda x: getattr(x, campo_agr.variable, 0),
                               self.lista_var_buro_consultas))
            if sum(values2) == 0:
                return None
            return sum(values) / sum(values2)
        else:
            return None
