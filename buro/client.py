from dataclasses import asdict
from datetime import date

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


def configura_consultas_buro(consultas):
    lista_var_buro_consultas = []
    for consulta in consultas:
        tmp = BuroConsultaFormatter(**consulta)
        lista_var_buro_consultas.append(VariablesBuroConsultasModel(**asdict(tmp)))

    return lista_var_buro_consultas


def configura_score_buro(scores):
    lista_var_buro_score = []
    for puntuacion in scores:
        tmp = BuroScoreFormatter(**puntuacion)
        lista_var_buro_score.append(VariablesBuroScoreModel(**asdict(tmp)))

    return lista_var_buro_score
