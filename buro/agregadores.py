from dataclasses import dataclass, field
from datetime import date
from typing import List

from app.buro.models import (VariablesBuroConsultasModel,
                             VariablesBuroCuentasModel,
                             VariablesBuroScoreModel)
from mlwrapper.campo.models import Campo, CampoAgregado


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


@dataclass
class MapeoVariablesCuentas:
    var_buro_cuentas: VariablesBuroCuentasModel
    var_cuentas: dict = field(init=False)

    @property
    def subcampos(self):
        return []

    @property
    def clase_subcampo(self):
        return dict

    def __post_init__(self):
        self.var_cuentas = self.clase_subcampo(**{
            campo.nombre: self.construye_variable_cuentas(campo)
            for campo in self.subcampos
        })

    def construye_variable_cuentas(self, campo: Campo):
        if campo.variable == 'apr' and campo.sufijo in ('bk_op_acc', 'nbk_op_acc', 'op_acc'):
            if campo.sufijo == 'bk_op_acc':
                return getattr(self.var_buro_cuentas, campo.variable, None) \
                    if self.var_buro_cuentas.bk_au_op_acc \
                    or self.var_buro_cuentas.bk_m_op_acc \
                    or self.var_buro_cuentas.bk_pl_op_acc else None
            elif campo.sufijo == 'nbk_op_acc':
                return getattr(self.var_buro_cuentas, campo.variable, None) \
                    if self.var_buro_cuentas.nbk_au_op_acc \
                    or self.var_buro_cuentas.nbk_m_op_acc \
                    or self.var_buro_cuentas.nbk_pl_op_acc else None
            elif campo.sufijo == 'op_acc':
                return getattr(self.var_buro_cuentas, campo.variable, None) \
                    if self.var_buro_cuentas.au_op_acc \
                    or self.var_buro_cuentas.m_op_acc \
                    or self.var_buro_cuentas.pl_op_acc else None
        elif not campo.sufijo:
            return getattr(self.var_buro_cuentas, campo.variable, None) \
                if not self.var_buro_cuentas.tu else None
        elif campo.sufijo in ['mop_actual', 'by_mop01', 'by_mop02', 'by_mop03', 'by_mop04', 'by_mop05',
                              'by_mop06', 'by_mop07', 'by_mop09']:
            return getattr(self.var_buro_cuentas, campo.nombre, None)

        elif campo.sufijo == 'tu_all':
            return getattr(self.var_buro_cuentas, campo.variable, None) \
                if self.var_buro_cuentas.tu_all_acc else None
        elif campo.sufijo == 'tu':
            return getattr(self.var_buro_cuentas, campo.variable, None) \
                if self.var_buro_cuentas.tu else None
        elif campo.sufijo == 'tu_all_op_acc':
            return getattr(self.var_buro_cuentas, campo.variable, None) \
                if self.var_buro_cuentas.tu_op_acc else None
        elif campo.sufijo == 'tu_op_acc':
            return getattr(self.var_buro_cuentas, campo.variable, None) \
                if self.var_buro_cuentas.tu_op_acc \
                and self.var_buro_cuentas.tu else None
        elif campo.sufijo == 'tu_all_cl_acc':
            return getattr(self.var_buro_cuentas, campo.variable, None) \
                if self.var_buro_cuentas.tu_cl_acc else None
        elif campo.sufijo == 'tu_cl_acc':
            return getattr(self.var_buro_cuentas, campo.variable, None) \
                if self.var_buro_cuentas.tu_cl_acc \
                and self.var_buro_cuentas.tu else None
        elif campo.sufijo == 'nbk_tu':
            return getattr(self.var_buro_cuentas, campo.variable, None) \
                if self.var_buro_cuentas.nbk_tu else None
        elif campo.sufijo == 'nbk_tu_op_acc':
            return getattr(self.var_buro_cuentas, campo.variable, None) \
                if self.var_buro_cuentas.tu_op_acc \
                and self.var_buro_cuentas.nbk_tu else None
        elif campo.sufijo == 'nbk_tu_cl_acc':
            return getattr(self.var_buro_cuentas, campo.variable, None) \
                if self.var_buro_cuentas.tu_cl_acc \
                and self.var_buro_cuentas.nbk_tu else None
        else:
            return getattr(self.var_buro_cuentas, campo.variable, None) \
                if getattr(self.var_buro_cuentas, campo.sufijo, False) \
                and not self.var_buro_cuentas.tu else None


@dataclass(unsafe_hash=True, order=True)
class VariablesVectorFechaCuentasIngresos:
    fecha: date
    vector: tuple = field(compare=False)
    var_cuentas_ingreso: dict = field(init=False, compare=False)

    @property
    def subcampos(self):
        return []

    @property
    def clase_subcampo(self):
        return dict

    def __post_init__(self):
        self.fecha = self.fecha.replace(day=1)

    def contruye_var_cuentas_ingreso(self, lista_var_buro_cuentas: List[VariablesBuroCuentasModel]):
        self.var_cuentas_ingreso = self.clase_subcampo(**{
            campo_agregado.nombre: self.contruye_variable(campo_agregado, lista_var_buro_cuentas)
            for campo_agregado in self.subcampos
        })
        return self

    def contruye_variable(self, campo_agr: CampoAgregado,
                          lista_var_buro_cuentas: List[VariablesBuroCuentasModel]):
        lista = zip(self.vector, lista_var_buro_cuentas)

        filtro = filter(lambda x: x[0] == 1 and getattr(x[1], campo_agr.variable, None) is not None
                        and (campo_agr.sufijo is None or getattr(x[1], campo_agr.sufijo, True)),
                        lista)

        values = list(map(lambda x: getattr(x[1], campo_agr.variable, 0), filtro))

        if campo_agr.agregacion == 'sum':
            if len(values) > 0:
                return sum(values)
            else:
                return None
        elif campo_agr.agregacion == 'max':
            if len(values) > 0:
                return max(values)
            else:
                return None
        elif campo_agr.agregacion == 'min':
            if len(values) > 0:
                return min(values)
            else:
                return None
        elif campo_agr.agregacion == 'avg':
            if len(values) > 0:
                return sum(values) / len(values)
            else:
                return None
        else:
            return None


@dataclass
class ConstructorVariablesAgregadasCuentas:
    # input vars
    lista_var_buro_cuentas: List[VariablesBuroCuentasModel]

    # middle vars
    lista_var_cuentas: List[dict] = field(init=False)
    lista_var_cuentas_ingresos: List[VariablesVectorFechaCuentasIngresos] = field(init=False)

    # output vars
    var_agregadas_cuentas: dict = field(init=False)

    @property
    def campos(self):
        return []

    @property
    def clase_variables(self):
        return dict

    @property
    def clase_subvar(self):
        return MapeoVariablesCuentas

    @property
    def clase_subvar_vec(self):
        return VariablesVectorFechaCuentasIngresos

    def __post_init__(self):
        self.configura_lista_var_cuentas_ingresos()
        self.configura_lista_var_cuentas()
        self.configura_var_agregadas_cuentas()

    def vector_fecha_limite(self, fecha_limite: date):
        fecha_limite = fecha_limite.replace(day=1)
        return tuple(map(lambda x: x.cuf_fec_ape.replace(day=1) <= fecha_limite
                         and (fecha_limite <= min(x.cuf_fec_cie, x.fecha_alta).replace(day=1)
                              if x.cuf_fec_cie else True),
                         self.lista_var_buro_cuentas))

    def configura_lista_var_cuentas_ingresos(self):
        vectores_fecha = []
        for var_buro_cuenta in self.lista_var_buro_cuentas:
            vectores_fecha.append(self.clase_subvar_vec(var_buro_cuenta.cuf_fec_ape,
                                  self.vector_fecha_limite(var_buro_cuenta.cuf_fec_ape)))
            vectores_fecha.append(
                self.clase_subvar_vec(var_buro_cuenta.cuf_fec_cie, self.vector_fecha_limite(var_buro_cuenta.cuf_fec_cie))
                if var_buro_cuenta.cuf_fec_cie
                else self.clase_subvar_vec(var_buro_cuenta.fecha_alta, self.vector_fecha_limite(var_buro_cuenta.fecha_alta)))

        vectores_fecha = list(set(vectores_fecha))
        vectores_fecha.sort(reverse=True)

        prev = None
        for vf in vectores_fecha:
            if prev and prev.vector == vf.vector:
                vf.fecha = prev.fecha
            prev = vf

        vectores_fecha = list(set(vectores_fecha))
        vectores_fecha.sort()

        self.lista_var_cuentas_ingresos = [
            vector_fecha.contruye_var_cuentas_ingreso(self.lista_var_buro_cuentas)
            for vector_fecha in vectores_fecha
        ]

    def configura_lista_var_cuentas(self):
        self.lista_var_cuentas = [
            self.clase_subvar(var_buro_cuenta).var_cuentas
            for var_buro_cuenta in self.lista_var_buro_cuentas
        ]

    def configura_var_agregadas_cuentas(self):
        self.var_agregadas_cuentas = self.clase_variables(**{
            campo_agregado.nombre: self.construye_variables_agregadas_cuentas(campo_agregado)
            for campo_agregado in self.campos
        })

    def construye_variables_agregadas_cuentas(self, campo_agr: CampoAgregado):
        if isinstance(campo_agr.campo, CampoAgregado):
            lista = self.lista_var_cuentas_ingresos
            filtro = list(filter(lambda x: getattr(x.var_cuentas_ingreso, campo_agr.campo.nombre, None) is not None, lista))
            filtro.sort()
            valores = list(map(lambda x: getattr(x.var_cuentas_ingreso, campo_agr.campo.nombre, 0), filtro))
        elif campo_agr.agregacion == 'wa':
            lista = self.lista_var_cuentas  # self.lista_var_cuentas
            filtro1 = list(filter(lambda x: getattr(x, f't_mop_{campo_agr.campo.sufijo}', None) is not None, lista))
            filtro2 = list(filter(lambda x: getattr(x, f'peso_mop_{campo_agr.campo.sufijo}', None) is not None, lista))
            values1 = list(map(lambda x: getattr(x, f't_mop_{campo_agr.campo.sufijo}', 0), filtro1))
            values2 = list(map(lambda x: getattr(x, f'peso_mop_{campo_agr.campo.sufijo}', 0), filtro2))
            if len(filtro1) > 0 and len(filtro2) > 0 and sum(values2) != 0:
                return sum(values1) / sum(values2)
            else:
                return None
        else:
            lista = self.lista_var_cuentas  # self.lista_var_cuentas
            filtro = list(filter(lambda x: getattr(x, campo_agr.campo.nombre, None) is not None, lista))
            valores = list(map(lambda x: getattr(x, campo_agr.campo.nombre, 0), filtro))

        if campo_agr.agregacion == 'sum':
            if len(valores) > 0:
                return sum(valores)
            else:
                return None
        if campo_agr.agregacion == 'pct_sum':  # Cuentas que son true/1 (variable+sufijo) entre el total
            if len(lista) > 0:
                return sum(valores) / len(lista)  # todo: check this value
            else:
                return None
        elif campo_agr.agregacion == 'num':
            return len(filtro)
        elif campo_agr.agregacion == 'pct_num':  # Cuantas cuentas (variable+sufijo) hay entre el total
            if len(lista) > 0:
                return len(filtro) / len(lista)
            else:
                return None
        elif campo_agr.agregacion == 'max':
            if len(valores) > 0:
                return max(valores)
            else:
                return None
        elif campo_agr.agregacion == 'min':
            if len(valores) > 0:
                return min(valores)
            else:
                return None
        elif campo_agr.agregacion == 'avg':
            if len(valores) > 0:
                try:
                    return sum(valores) / len(valores)
                except Exception as e:
                    print(e)
            else:
                return None
        elif campo_agr.agregacion == 'dif':
            if len(valores) > 0:
                return max(valores) - min(valores)
            else:
                return None
        elif campo_agr.agregacion == 'dec':
            cont = 0
            prev = None
            if len(valores) > 0:
                for val in valores:
                    if prev is not None and prev != 0 and val is not None and val / prev <= 0.9:
                        cont += 1
                    prev = val
                return cont
            else:
                return 0
        elif campo_agr.agregacion == 'inc':
            cont = 0
            prev = None
            if len(valores) > 0:
                for val in valores:
                    if prev is not None and prev != 0 and val is not None:
                        try:
                            tmp = val / prev
                        except ZeroDivisionError as e:
                            print(e)
                            tmp = 1
                        if tmp >= 1.1:
                            cont += 1
                    prev = val
                return cont
            else:
                return 0
        else:
            return None
