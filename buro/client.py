import asyncio
from dataclasses import asdict, dataclass, field
from datetime import date
from typing import List

from buro.formatters import (BuroConsultaFormatter, BuroCuentasFormatter,
                                 BuroScoreFormatter)
from buro.models import (VariablesBuroConsultasModel,
                         VariablesBuroCuentasModel,
                         VariablesBuroScoreModel)


def configura_cuentas_buro(cuentas, fecha_alta: date = None):
    lista_var_buro_cuentas = []
    for cuenta in cuentas:
        buro_cuenta = VariablesBuroCuentasModel(**asdict(BuroCuentasFormatter(**cuenta)),
                                                fecAlta=cuenta['fecFecBur'] if fecha_alta is None else fecha_alta)
        if not buro_cuenta.valido:
            raise ValueError('El registro de buro tiene cuentas sin cotizacion de moneda.')
        lista_var_buro_cuentas.append(buro_cuenta)

    return lista_var_buro_cuentas

@dataclass
class InfoBuro:
    # folio: str
    # fecha_alta: date
    lista_var_buro_cuentas: List[VariablesBuroCuentasModel] = field(init=False)
    lista_var_buro_consultas: List[VariablesBuroConsultasModel] = field(init=False)
    lista_var_buro_score: List[VariablesBuroScoreModel] = field(init=False)
    lista_codigos_postales: list = field(init=False)

    # async def configura(self):
    #     await asyncio.gather(*[
    #         self.configura_cuentas(),
    #         self.configura_consultas(),
    #         self.configura_score(),
    #         self.configura_codigos_postales()
    #     ])

    def configura_cuentas(self, dataframe_cuentas):
        # cuentas_futuro = await requests.get(f'{config.RUTA_SERVICIO_BURO}/solicitudes/{self.folio}/cuentas')
        # cuentas = await cuentas_futuro.json()
        self.lista_var_buro_cuentas = []
        for cuenta in dataframe_cuentas:
            buro_cuenta = VariablesBuroCuentasModel(**asdict(BuroCuentasFormatter(**cuenta)), fecAlta=self.fecha_alta)
            if not buro_cuenta.valido:
                raise ValueError('El micro servicio de buro regreso cuentas sin cotizacion de moneda.')
            self.lista_var_buro_cuentas.append(buro_cuenta)


    def configura_consultas(self, dataframe_consultas):
        # consultas_futuro = await requests.get(f'{config.RUTA_SERVICIO_BURO}/solicitudes/{self.folio}/consultas')
        # consultas = await consultas_futuro.json()
        self.lista_var_buro_consultas = []
        for consulta in dataframe_consultas:
            tmp = BuroConsultaFormatter(**consulta)
            self.lista_var_buro_consultas.append(VariablesBuroConsultasModel(**asdict(tmp)))

    def configura_score(self, dataframe_score):
        # puntuaciones_futuro = await requests.get(f'{config.RUTA_SERVICIO_BURO}/solicitudes/{self.folio}/puntuaciones')
        # puntuaciones = await puntuaciones_futuro.json()
        self.lista_var_buro_score = []
        for puntuacion in dataframe_score:
            tmp = BuroScoreFormatter(**puntuacion)
            self.lista_var_buro_score.append(VariablesBuroScoreModel(**asdict(tmp)))
