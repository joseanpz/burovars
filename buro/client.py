import asyncio
from dataclasses import asdict, dataclass, field
from datetime import date
from typing import List

from aiohttp_requests import requests

from app import config
from app.buro.formatters import (BuroConsultaFormatter, BuroCuentasFormatter,
                                 BuroScoreFormatter)
from app.buro.models import (VariablesBuroConsultasModel,
                             VariablesBuroCuentasModel,
                             VariablesBuroScoreModel)


@dataclass
class InfoBuroTitular:
    folio: str
    fecha_alta: date
    lista_var_buro_cuentas: List[VariablesBuroCuentasModel] = field(init=False)
    lista_var_buro_consultas: List[VariablesBuroConsultasModel] = field(init=False)
    lista_var_buro_score: List[VariablesBuroScoreModel] = field(init=False)
    lista_codigos_postales: list = field(init=False)

    async def configura(self):
        await asyncio.gather(*[
            self.configura_cuentas(),
            self.configura_consultas(),
            self.configura_score(),
            self.configura_codigos_postales()
        ])

    async def configura_cuentas(self):
        cuentas_futuro = await requests.get(f'{config.RUTA_SERVICIO_BURO}/solicitudes/{self.folio}/cuentas')
        cuentas = await cuentas_futuro.json()
        self.lista_var_buro_cuentas = []
        for cuenta in cuentas:
            buro_cuenta = VariablesBuroCuentasModel(**asdict(BuroCuentasFormatter(**cuenta)), fecAlta=self.fecha_alta)
            if not buro_cuenta.valido:
                raise ValueError('El micro servicio de buro regreso cuentas sin cotizacion de moneda.')
            self.lista_var_buro_cuentas.append(buro_cuenta)

    async def configura_consultas(self):
        consultas_futuro = await requests.get(f'{config.RUTA_SERVICIO_BURO}/solicitudes/{self.folio}/consultas')
        consultas = await consultas_futuro.json()
        self.lista_var_buro_consultas = []
        for consulta in consultas:
            tmp = BuroConsultaFormatter(**consulta)
            self.lista_var_buro_consultas.append(VariablesBuroConsultasModel(**asdict(tmp)))

    async def configura_score(self):
        puntuaciones_futuro = await requests.get(f'{config.RUTA_SERVICIO_BURO}/solicitudes/{self.folio}/puntuaciones')
        puntuaciones = await puntuaciones_futuro.json()
        self.lista_var_buro_score = []
        for puntuacion in puntuaciones:
            tmp = BuroScoreFormatter(**puntuacion)
            self.lista_var_buro_score.append(VariablesBuroScoreModel(**asdict(tmp)))

    async def configura_codigos_postales(self):
        cps_futuro = await requests.get(f'{config.RUTA_SERVICIO_BURO}/solicitudes/{self.folio}/direcciones')
        cps = set(map(lambda x: x['difCodPos'], await cps_futuro.json()))
        self.lista_codigos_postales = cps
