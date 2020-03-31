import math
from datetime import date

from pydantic import BaseModel, Field

TIPOS_CUENTAS_BANCARIAS = (
    'AUTO REGIO', 'BANCO REGIONAL D', 'BANREGIO', 'TC BANREGIO',
    'HIPOTEC BANREGIO', 'BANREGIO, S.A.', 'BANCO', 'BANCOS'
)

TIPOS_COMUNICACIONES_SERVICIOS = ('COMUNICACIONES', 'SERVICIOS')


class BuroFechaReporteModel(BaseModel):
    fech_rep: date = Field(None, title='FECHA DE REPORTE', alias='fechRep')
    dolar: float = Field(None, title='Valor de dolar en la fecha del reporte', alias='dolar')
    udi: float = Field(None, title='Valor de la udi en la fecha dle reporte', alias='udi')


class BuroConsultaModel(BaseModel):
    folio: str = Field(None, title='NÚMERO DE CUENTA CONSULTADA', alias='cofFolio')
    fecha_buro: date = Field(None, title='FECHA DE RESPUESTA DE BURO', alias='cofFecBur')
    cof_consec: int = Field(None, title='CONSECUTIVO, INDICE', alias='cofConsec')
    cof_fec_con: date = Field(None, title='FECHA DE CONSULTA DE LA CUENTA', alias='cofFecCon')
    cof_cve_oto: str = Field(None, title='CLAVE DE OTORGANTE', alias='cofCveOto')
    cof_buro_id: str = Field(None, title="Id de buro", description="descripcion del id de buró", alias='cofBuroId')
    cof_nom_oto: str = Field(None, title='NOMBRE DE OTORGANTE', alias='cofNomOto')
    cof_tip_con: str = Field(None, title='TIPO DE CONTRATO', alias='cofTipCon')
    cof_cve_mon: str = Field(None, title='MONEDA DEL CREDITO', alias='cofCveMon')
    cof_import: str = Field(None, title='', alias='cofImport')
    cof_tip_res: str = Field(None, title='', alias='cofTipRes')
    cof_consumo: str = Field(None, title='', alias='cofConsum')
    cof_result: int = Field(None, title='', alias='cofResult')

    @staticmethod
    def fnc_dif_meses(fec_ini: date, fec_fin: date):
        if fec_ini is None or fec_fin is None:
            return None
        mes_ini = fec_ini.year * 12 + fec_ini.month
        mes_fin = fec_fin.year * 12 + fec_fin.month
        meses = mes_fin - mes_ini
        if fec_fin.day < fec_ini.day:
            meses -= 1
        return meses

    @property
    def iq_01m(self):
        return self.fnc_dif_meses(self.cof_fec_con, self.fecha_buro) < 1

    @property
    def iq_03m(self):
        return self.fnc_dif_meses(self.cof_fec_con, self.fecha_buro) <= 3

    @property
    def iq_06m(self):
        return self.fnc_dif_meses(self.cof_fec_con, self.fecha_buro) <= 6

    @property
    def iq_12m(self):
        return self.fnc_dif_meses(self.cof_fec_con, self.fecha_buro) <= 12

    @property
    def iq_18m(self):
        return self.fnc_dif_meses(self.cof_fec_con, self.fecha_buro) <= 18

    @property
    def iq_24m(self):
        return self.fnc_dif_meses(self.cof_fec_con, self.fecha_buro) <= 24

    @property
    def bk(self):
        return self.cof_nom_oto in ['BANCO', 'BANCOS']

    @property
    def nbk(self):
        return self.cof_nom_oto not in ['BANCO', 'BANCOS', 'BANREGIO', 'BURO DE CREDITO', 'CIRCULO CREDITO',
                                        'CONSUMIDOR FINAL', 'PRUEBA DE CONSUL', 'PRUEBAS BC', 'REPORTE ESPECIAL', 'SIC',
                                        'UNION DE CREDITO', 'COMUNICACIONES', 'SERVICIOS']

    @property
    def r(self):
        return self.cof_tip_con == 'CC'

    @property
    def au(self):
        return self.cof_tip_con in ['AL', 'AU', 'LS']

    @property
    def amx(self):
        return self.cof_tip_con == 'AMX'

    @property
    def pl(self):
        return self.cof_tip_con in ['PL', 'PN', 'PQ', 'SE', 'ST', 'TE', 'US']

    @property
    def m(self):
        return self.cof_tip_con in ['HE', 'HI', 'RE']

    @property
    def all_iq(self):
        return self.bk or self.nbk

    @property
    def bk_au(self):
        return self.bk and self.au

    @property
    def bk_m(self):
        return self.bk and self.m

    @property
    def bk_pl(self):
        return self.bk and self.pl

    @property
    def bk_r(self):
        return self.bk and self.r

    @property
    def nbk_au(self):
        return self.nbk and self.au

    @property
    def nbk_m(self):
        return self.nbk and self.m

    @property
    def nbk_pl(self):
        return self.nbk and self.pl

    @property
    def nbk_r(self):
        return self.nbk and self.r

    @property
    def relevante(self):
        return self.cof_nom_oto not in ('BURO DE CREDITO', 'CIRCULO CREDITO', 'CONSUMIDOR FINAL',
                                        'PRUEBA DE CONSUL', 'PRUEBAS BC', 'REPORTE ESPECIAL', 'SIC',
                                        'UNION DE CREDITO', 'COMUNICACIONES', 'SERVICIOS',
                                        'REPORTE DE CREDI') \
               and (self.cof_consec != 1 or self.cof_nom_oto != 'BANREGIO')

    @property
    def iq_03m_relevante(self):
        return self.iq_03m and self.relevante

    @property
    def iq_01m_relevante(self):
        return self.iq_01m and self.relevante

    @property
    def implicito(self):
        return self.fecha_buro == self.cof_fec_con and (self.cof_nom_oto in ('BANREGIO', 'BURO DE CREDITO'))


class BuroCuentasModel(BaseModel):
    folio: str = Field(None, title='NÚMERO DE CUENTA CONSULTADA', alias='cufFolio')
    fecha_buro: date = Field(None, title='FECHA DE RESPUESTA DE BURO', alias='fecFecBur')
    cuf_consec: int = Field(None, title='FECHA DE ACTUALIZACIÓN DE LA CUENTA EN TL', alias='cufConsec')
    cuf_fec_act: date = Field(None, title='FECHA DE ACTUALIZACIÓN DE LA CUENTA EN TL', alias='cufFecAct')
    cuf_reg_imp: str = Field(None, title='REGISTRO IMPUGNADO', alias='cufRegImp')
    cuf_cve_oto: str = Field(None, title='CLAVE DE OTORGANTE', alias='cufCveOto')
    cuf_nom_oto: str = Field(None, title='NOMBRE DE OTORGANTE', alias='cufNomOto')
    cuf_num_cue: str = Field(None, title='NUMERO DE CUENTA', alias='cufNumCue')
    cuf_tip_res: str = Field(None, title='TIPO DE RESPONSABILIDAD', alias='cufTipRes')
    cuf_tip_cue: str = Field(None, title='TIPO DE CUENTA', alias='cufTipCue')
    cuf_tip_con: str = Field(None, title='TIPO DE CONTRATO', alias='cufTipCon')
    cuf_cve_mon: str = Field(None, title='MONEDA DEL CREDITO', alias='cufCveMon')
    cuf_val_act: int = Field(None, title='IMPORTE DEL AVALUO', alias='cufValAct')
    cuf_num_pag: int = Field(None, title='NÚMERO DE PAGOS', alias='cufNumPag')
    cuf_fre_pag: str = Field(None, title='FRECUENCIA DE PAGO', alias='cufFrePag')
    cuf_monto: float = Field(None, title='MONTO A PAGAR', alias='cufMonto')
    cuf_fec_ape: date = Field(None, title='FECHA DE APERTURA', alias='cufFecApe')
    cuf_ult_pag: date = Field(None, title='FECHA DE ÚLTIMO PAGO', alias='cufUltPag')
    cuf_ult_com: date = Field(None, title='FECHA DE ÚLTIMA COMPRA', alias='cufUltCom')
    cuf_fec_cie: date = Field(None, title='FECHA DE CIERRE', alias='cufFecCie')
    cuf_fec_rep: date = Field(None, title='FECHA DE REPORTE', alias='cufFecRep')
    cuf_fma_rep: str = Field(None, title='MODO DE REPORTAR', alias='cufFmaRep')
    cuf_ult_sal: date = Field(None, title='ÚLTIMA FECHA CON SALDO CERO', alias='cufUltSal')
    cuf_garant: str = Field(None, title='GARANTÍA', alias='cufGarant')
    cuf_max_cre: float = Field(None, title='CRÉDITO MÁXIMO AUTORIZADO', alias='cufMaxCre')
    cuf_sal_act: float = Field(None, title='SALDO ACTUAL', alias='cufSalAct')
    cuf_lim_cre: float = Field(None, title='LÍMITE DE CRÉDITO', alias='cufLimCre')
    cuf_sal_ven: float = Field(None, title='SALDO VENCIDO', alias='cufSalVen')
    cuf_pag_ven: float = Field(None, title='NÚMERO DE PAGOS VENCIDOS', alias='cufPagVen')
    cuf_fma_pag: str = Field(None, title='CLASIFICACIÓN DE PUNTUALIDAD DE PAGO MOP', alias='cufFmaPag')
    cuf_hist_pag: str = Field(None, title='HISTÓRICO DE PAGOS', alias='cufHisPag')
    cuf_fec_rec: date = Field(None, title='FECHA MAS RECIENTE DEL HISTÓRICO DE PAGOS', alias='cufFecRec')
    cuf_fec_ant: date = Field(None, title='FECHA MAS ANTIGUA DEL HISTÓRICO DE PAGOS', alias='cufFecAnt')
    cuf_cve_obs: str = Field(None, title='CLAVE DE OBSERVACIÓN', alias='cufCveObs')
    cuf_tot_pag: int = Field(None, title='TOTAL DE PAGOS REPORTADOS', alias='cufTotPag')
    cuf_mop_02: int = Field(None, title='TOTAL DE PAGOS CON MOP = 02', alias='cufMop02')
    cuf_mop_03: int = Field(None, title='TOTAL DE PAGOS CON MOP = 03', alias='cufMop03')
    cuf_mop_04: int = Field(None, title='TOTAL DE PAGOS CON MOP = 04', alias='cufMop04')
    cuf_mop_05: int = Field(None, title='TOTAL DE PAGOS CON MOP = 05 O MAYOR', alias='cufMop05')
    cuf_imp_sal: int = Field(None, title='SALDO EN LA MOROSIDAD HISTÓRICA MAS ALTA', alias='cufImpSal')
    cuf_fec_mor: date = Field(None, title='FECHA DE LA MOROSIDAD HISTÓRICA MAS ALTA', alias='cufFecMor')
    cuf_mop_mor: str = Field(None, title='MOP EN LA MOROSIDAD MAS ALTA', alias='cufMopMor')
    cuf_reestr: date = Field(None, title='FECHA DE INICIO DE LA REESTRUCTURA', alias='cufReestr')

    # variables economicas
    dlr_fec_rep: float = Field(None, title='VALOR DE DOLAR EN LA FECHA DE REPORTE', alias='fecRepDol')
    udi_fec_rep: float = Field(None, title='VALOR DEL UDI EN LA FECHA DE REPORTE', alias='fecRepUdi')
    udi_fec_ape: float = Field(None, title='VALOR DE UDI EN LA FECHA DE APERTURA', alias='fecApeUdi')
    udi_fec_buro: float = Field(None, title='VALOR DE UDI EN LA FECHA DE BURO', alias='fecConUdi')

    # variable de entrada
    fecha_alta: date = Field(None, title='', alias='fecAlta')

    @staticmethod
    def fnc_dif_meses(fec_ini: date, fec_fin: date):
        if fec_ini is None or fec_fin is None:
            return None
        mes_ini = fec_ini.year * 12 + fec_ini.month
        mes_fin = fec_fin.year * 12 + fec_fin.month
        meses = mes_fin - mes_ini
        if fec_fin.day < fec_ini.day:
            meses -= 1
        return meses

    @staticmethod
    def ratio(num, den):
        if not num or num == 0:
            return 0
        elif not den or den == 0:
            return None
        else:
            return num / den

    def val_to_mon(self, value: float):
        """
        Convertidor a moneda pesos
        :param value: valor en udi, dolar, etc
        :return: conversion a pesos
        """
        if self.cuf_cve_mon == 'UD':
            return value * self.udi_fec_rep
        elif self.cuf_cve_mon == 'US':
            return value * self.dlr_fec_rep
        elif self.cuf_cve_mon == 'MX' or self.cuf_cve_mon == 'N$' or not self.cuf_cve_mon:  # 'N$' <- nuevos pesos
            return value

    @staticmethod
    def fnc_interes_mensual(interes_inicial: float, cred_max: float, num_pmt: float, pmt: float):

        # interes = None
        aux = 1
        i = 0
        iteracion_interes = None

        if not num_pmt or not pmt or not cred_max:
            aux = 0
        elif cred_max < 0.0 or num_pmt == 0 or pmt == 0:
            aux = 0

        if aux == 1:
            interes = interes_inicial
            aux = 0
            while i <= 100 and aux == 0:
                iteracion_interes = \
                    interes - ((pmt / interes) * (1 - pow(1 + interes, - num_pmt)) - cred_max) / \
                    (
                            (pmt / interes) * (num_pmt * pow(1 + interes, - num_pmt - 1))
                            - (pmt / pow(interes, 2)) * (1 - pow(1 + interes, - num_pmt))
                    )
                if (iteracion_interes - interes) < pow(10, -6):
                    aux = 1
                else:
                    interes = iteracion_interes
                i = i + 1

        if not iteracion_interes:
            return None
        else:
            return iteracion_interes

    def fnc_moda(self):
        moda = None
        conteo_max = 0
        aux = 1
        # largo = None
        arreglo = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        mop_actuales = ["02", "03", "04", "05", "06", "07", "96", "97", "99"]
        mop_9 = ["96", "97", "99"]
        mop_historicos = ["2", "3", "4", "5", "6", "7", "9"]

        if not self.cuf_hist_pag:
            largo = None
        else:
            largo = len(self.cuf_hist_pag)

        if self.cuf_fma_pag not in mop_actuales:
            arreglo[0] = 1
        elif self.cuf_fma_pag in mop_9:
            arreglo[8] = 1
        else:
            arreglo[int(self.cuf_fma_pag) - 1] = 1

        if largo:
            while aux <= largo:
                if self.cuf_hist_pag[aux - 1:aux] not in mop_historicos:
                    arreglo[0] = arreglo[0] + 1
                else:
                    arreglo[int(self.cuf_hist_pag[aux - 1:aux]) - 1] = \
                        arreglo[int(self.cuf_hist_pag[aux - 1:aux]) - 1] + 1
                aux = aux + 1
            # largo = None

        aux = 9

        while aux >= 1 and (self.cuf_fma_pag or self.cuf_hist_pag):
            if arreglo[aux - 1] > 0 and conteo_max < arreglo[aux - 1]:
                moda = aux
                conteo_max = arreglo[aux - 1]
            aux = aux - 1

        return moda

    def fnc_mop_promedio(self):
        mop_promedio = 0
        mop_conteo = 0
        # largo = None
        aux = 1

        mop_actuales = ["02", "03", "04", "05", "06", "07", "96", "97", "99"]
        mop_9 = ["96", "97", "99"]
        mop_historicos = ["2", "3", "4", "5", "6", "7", "9"]

        if not self.cuf_fma_pag and not self.cuf_hist_pag:
            mop_promedio = None

        if not self.cuf_hist_pag:
            largo = 0
        else:
            largo = len(self.cuf_hist_pag)

        if mop_promedio == 0:
            if self.cuf_fma_pag not in mop_actuales:
                mop_promedio = mop_promedio + 1
                mop_conteo = mop_conteo + 1
            elif self.cuf_fma_pag in mop_9:
                mop_promedio = mop_promedio + 9
                mop_conteo = mop_conteo + 1
            else:
                mop_promedio = mop_promedio + float(self.cuf_fma_pag)
                mop_conteo = mop_conteo + 1

            while aux <= largo:
                if self.cuf_hist_pag[aux - 1:aux] not in mop_historicos:
                    mop_promedio = mop_promedio + 1
                    mop_conteo = mop_conteo + 1
                else:
                    mop_promedio = mop_promedio + float(self.cuf_hist_pag[aux - 1:aux])
                    mop_conteo = mop_conteo + 1
                aux = aux + 1

        if mop_conteo == 0:
            return None
        else:
            return round(mop_promedio / mop_conteo * 10000.0) / 10000.0

    def fnc_mopmaximo(self, n: int):
        # mopmax = 0
        largo = None
        ms_diff = 0
        aux = 1
        # mophist_x = 0

        mop_actuales = ["02", "03", "04", "05", "06", "07", "96", "97", "99"]
        mop_9 = ["96", "97", "99"]
        mop_historicos = ["2", "3", "4", "5", "6", "7", "9"]

        if not self.cuf_fec_act:
            mopmax = None
        elif self.fnc_dif_meses(self.cuf_fec_act, self.fecha_buro) > n:
            mopmax = None
        else:
            if self.cuf_fma_pag not in mop_actuales:
                mopmax = 1
            elif self.cuf_fma_pag in mop_9:
                mopmax = 9
            else:
                mopmax = int(self.cuf_fma_pag)

        if mopmax and self.fecha_buro and self.cuf_fec_rec:
            ms_diff = float(self.fnc_dif_meses(self.cuf_fec_rec, self.fecha_buro))
            if not self.cuf_hist_pag:
                largo = 0
            else:
                largo = len(self.cuf_hist_pag)

        if mopmax and self.fecha_buro and self.cuf_fec_rec:
            if ms_diff <= n:
                while aux <= (n - ms_diff):
                    if largo >= aux:
                        if self.cuf_hist_pag[aux - 1:aux] in mop_historicos:
                            mopmax = max(mopmax,  float(self.cuf_hist_pag[aux - 1:aux]))
                    aux = aux + 1

        return mopmax

    def fnc_mopmax_relevantes(self, n: int, cur_bal: float, cred_lim: float, cred_max: float):
        mopmax = 0
        largo = None
        ms_diff = None
        aux = 1
        # mophist_x = 0
        # valor = 0
        saldo_actual = 0

        mop_actuales = ["02", "03", "04", "05", "06", "07", "96", "97", "99"]
        mop_9 = ["96", "97", "99"]
        mop_historicos = ["2", "3", "4", "5", "6", "7", "9"]

        if self.cuf_tip_cue == 'R':
            if not cred_lim:
                valor = cred_max
            elif cred_lim > 0:
                valor = cred_lim
            else:
                valor = cred_max
        else:
            if not cred_max:
                valor = cred_lim
            elif cred_max > 0:
                valor = cred_max
            else:
                valor = cred_lim

        if cur_bal:
            saldo_actual = cur_bal

        if not self.cuf_fec_act:
            mopmax = None
        elif self.cuf_fec_act == '':
            mopmax = None
        elif self.fnc_dif_meses(self.cuf_fec_act, self.fecha_buro) > n:
            mopmax = None

        if mopmax is not None and self.fecha_buro and self.cuf_fec_rec and self.cuf_fec_rec != '':
            ms_diff = float(self.fnc_dif_meses(self.cuf_fec_rec, self.fecha_buro))
            if not self.cuf_hist_pag:
                largo = 0
            else:
                largo = len(self.cuf_hist_pag)

        if not valor:
            mopmax = None
            # valor = 0
        elif valor <= 0:
            mopmax = None
        elif not saldo_actual:
            mopmax = None
        elif not self.udi_fec_rep:
            mopmax = None
        elif valor <= 0 and saldo_actual <= (500 * self.udi_fec_rep):
            mopmax = None
        elif saldo_actual <= (500 * self.udi_fec_rep) and (saldo_actual / valor) < 0.05:
            mopmax = None

        if mopmax is not None:
            if not self.cuf_fec_act:
                mopmax = None
            elif self.cuf_fec_act == '':
                mopmax = None
            elif self.fnc_dif_meses(self.cuf_fec_act, self.fecha_buro) > n:
                mopmax = None
            else:
                if self.cuf_fma_pag not in mop_actuales:
                    mopmax = 1
                elif self.cuf_fma_pag in mop_9:
                    mopmax = 9
                else:
                    mopmax = int(self.cuf_fma_pag)

        if mopmax is not None and self.fecha_buro and self.cuf_fec_rec and self.cuf_fec_rec != '' and ms_diff:
            if ms_diff <= n:
                while aux <= (n - ms_diff):
                    if largo >= aux:
                        if self.cuf_hist_pag[aux - 1:aux] in mop_historicos:
                            mopmax = max(mopmax, float(self.cuf_hist_pag[aux - 1:aux]))

                    aux = aux + 1

        return mopmax

    def fnc_t_mop(self):
        t_mop = 0
        # largo = None
        aux = 1

        mop_actuales = ["01", "02", "03", "04", "05", "06", "07", "96", "97", "99"]
        mop_9 = ["96", "97", "99"]
        mop_historicos = ["1", "2", "3", "4", "5", "6", "7", "9"]

        if not self.cuf_hist_pag:
            largo = 0
        else:
            largo = len(self.cuf_hist_pag)

        if self.cuf_fma_pag:
            if self.cuf_fma_pag not in mop_actuales:
                t_mop = 0
            elif self.cuf_fma_pag in mop_9:
                t_mop = t_mop + 9 / math.sqrt(1.2)
            else:
                t_mop = t_mop + float(self.cuf_fma_pag) / math.sqrt(1.2)

        while aux <= largo <= 24:
            # aux <= largo and largo <= 24
            if self.cuf_hist_pag[aux - 1:aux] in mop_historicos:
                t_mop = t_mop + float(self.cuf_hist_pag[aux - 1:aux]) / math.sqrt(aux)
            aux = aux + 1

        return t_mop

    def fnc_peso_mop(self):
        peso_mop = 0
        # largo = None
        aux = 1

        mop_actuales = ["01", "02", "03", "04", "05", "06", "07", "96", "97", "99"]
        mop_historicos = ["1", "2", "3", "4", "5", "6", "7", "9"]

        if not self.cuf_hist_pag:
            largo = 0
        else:
            largo = len(self.cuf_hist_pag)

        if self.cuf_fma_pag:
            if self.cuf_fma_pag in mop_actuales:
                peso_mop = 1

        while aux <= largo <= 24:
            if self.cuf_hist_pag[aux - 1:aux] in mop_historicos:
                peso_mop = peso_mop + 1
            aux = aux + 1

        return peso_mop

    def fnc_lect_hispag(self, indice: str):
        crecimientos = 0
        decrecimientos = 0
        consecutivos = 0
        max_consec = 0
        # largo = 0
        # mop_n = ''
        mop_aux = 0
        aux = 0
        valor_retorno = 0
        # concat = None

        mop_actuales = ["01", "02", "03", "04", "05", "06", "07", "96", "97", "99"]
        mop_9 = ["96", "97", "99"]
        mop_historicos = ["1", "2", "3", "4", "5", "6", "7", "9"]

        if self.cuf_fma_pag:
            if self.cuf_fma_pag not in mop_actuales:
                concat = '1'
            elif self.cuf_fma_pag in mop_9:
                concat = '9'
            else:
                concat = self.cuf_fma_pag[1:2]

            if self.cuf_hist_pag:
                concat = concat + self.cuf_hist_pag
        else:
            if not self.cuf_hist_pag:
                concat = ''
            else:
                concat = self.cuf_hist_pag

        if not concat:
            largo = 0
        else:
            largo = len(concat)

        if largo > 0:
            while aux <= (largo - 1):
                aux = aux + 1
                if aux == 1:
                    if concat[aux - 1:aux] in mop_historicos:
                        mop_aux = float(concat[aux - 1:aux])
                    else:
                        mop_aux = 1

                    if mop_aux == 1:
                        consecutivos += 1
                        max_consec = max_consec + 1
                else:
                    mop_n = concat[aux - 1:aux]

                    if mop_n not in mop_historicos:
                        mop_n = '1'

                    # CÁLCULO DE CONSECUTIVOS MÁXIMOS
                    if float(mop_n) == 1:
                        consecutivos += 1
                        max_consec = max(max_consec, consecutivos)
                    else:
                        consecutivos = 0

                    # CÁLCULO DE CRECIMIENTOS
                    if float(mop_n) < mop_aux:
                        crecimientos = crecimientos + 1

                    # CÁLCULO DE DECRECIMIENTOS
                    if float(mop_n) > mop_aux:
                        decrecimientos += 1

                    mop_aux = float(mop_n)

        if indice != 'CONSECUTIVOS' and indice != 'CRECIMIENTOS' and indice != 'DECRECIMIENTOS':
            valor_retorno = None
        elif aux == 0:
            valor_retorno = None
        elif indice == 'CONSECUTIVOS':
            valor_retorno = max_consec
        elif indice == 'CRECIMIENTOS':
            valor_retorno = crecimientos
        elif indice == 'DECRECIMIENTOS':
            valor_retorno = decrecimientos

        return valor_retorno

    def fnc_log_basemop_saldo(self, max_mop_bal: float):
        log_basemop_saldo = None
        # basemop = None

        mop_actuales = ["02", "03", "04", "05", "06", "07", "96", "97", "99"]
        mop_9 = ["96", "97", "99"]

        if max_mop_bal is not None:
            if max_mop_bal > 0 and self.cuf_mop_mor in mop_actuales:
                if self.cuf_mop_mor in mop_9:
                    basemop = 9
                else:
                    basemop = float(self.cuf_mop_mor)

                log_basemop_saldo = math.log(max_mop_bal) / math.log(basemop)

        return log_basemop_saldo

    def fnc_ms_lst_def(self, n: int):
        ms_lst = None
        # largo = None
        aux = 1
        # mophist_x = None

        mop_actuales = ["01", "02", "03", "04", "05", "06", "07", "96", "97", "99"]
        mop_9 = ["96", "97", "99"]
        mop_historicos = ["1", "2", "3", "4", "5", "6", "7", "9"]

        if self.cuf_fma_pag not in mop_actuales:
            mophist_x = 1
        elif self.cuf_fma_pag in mop_9:
            mophist_x = 9
        else:
            mophist_x = float(self.cuf_fma_pag)

        if not mophist_x:
            ms_lst = None

        if mophist_x > n:
            ms_lst = self.fnc_dif_meses(self.cuf_fec_act, self.fecha_buro)

        if not self.cuf_hist_pag:
            largo = 0
        else:
            largo = len(self.cuf_hist_pag)

        if not self.cuf_fec_act and not self.cuf_fec_rec:
            ms_lst = None

        if not ms_lst:
            while aux <= largo and not ms_lst:
                if self.cuf_hist_pag[aux - 1:aux] in mop_historicos:
                    mophist_x = float(self.cuf_hist_pag[aux - 1:aux])
                else:
                    mophist_x = 1

                if mophist_x > n:
                    ms_lst = self.fnc_dif_meses(self.cuf_fec_rec, self.fecha_buro) + int(aux) - 1
                aux = aux + 1

        if not ms_lst:
            ms_lst = None
        elif ms_lst < 0:
            ms_lst = None

        if not ms_lst:
            return None
        else:
            return float(ms_lst)

    @property
    def freq_factor(self) -> float:
        if self.cuf_fre_pag == 'Y':
            return float(1/12)
        elif self.cuf_fre_pag == 'B':
            return float(1/2)
        elif self.cuf_fre_pag == 'K':
            return float(2)
        elif self.cuf_fre_pag == 'S':
            return float(2)
        elif self.cuf_fre_pag == 'D':
            return float(30)
        elif self.cuf_fre_pag == 'W':
            return float(4)
        elif self.cuf_fre_pag == 'Q':
            return float(1/3)
        elif self.cuf_fre_pag == 'H':
            return float(1/6)
        else:
            return 1

    @property
    def usuario(self) -> str:
        if self.cuf_nom_oto in TIPOS_CUENTAS_BANCARIAS or \
                (self.cuf_nom_oto == 'CIA Q- OTORGA'
                 and self.cuf_tip_cue == 'O'
                 and self.cuf_tip_con == 'CC'):
            return 'BK'
        elif self.cuf_nom_oto in TIPOS_COMUNICACIONES_SERVICIOS:
            return 'C&S'
        else:
            return 'NBK'

    @property
    def producto(self) -> str:
        if self.cuf_nom_oto in TIPOS_COMUNICACIONES_SERVICIOS:
            return 'C&S'
        elif self.cuf_tip_cue == 'R':
            return 'R'
        elif self.cuf_tip_cue == 'M' or (self.cuf_tip_cue != 'R' and self.cuf_tip_con in ('HE', 'HI', 'RE')):
            return 'M'
        elif self.cuf_nom_oto == 'CIA Q- OTORGA' and self.cuf_tip_cue == 'O' and self.cuf_tip_con == 'CC':
            return 'AMX'
        elif (self.cuf_tip_cue in ('I', 'O') and self.cuf_tip_con in ('AL', 'AU')) or (
                self.cuf_tip_cue == 'I' and self.cuf_tip_con == 'LS'):
            return 'AU'
        elif (self.cuf_tip_cue == 'I' and self.cuf_tip_con in ('CC', 'PL', 'PN', 'PQ', 'SE', 'ST', 'TE', 'US')) or (
                self.cuf_tip_cue == 'O' and self.cuf_tip_con in ('PN', 'PQ', 'SE', 'ST', 'US')):
            return 'PL'
        else:
            return 'OTRO'

    @property
    def estado_actual(self) -> str:
        if self.cuf_fec_cie in (date(1901, 11, 7), date(1, 1, 1), date(552, 2, 24)) or not self.cuf_fec_cie:
            return 'OP_ACC'
        else:
            return 'CL_ACC'

    # banderas
    @property
    def bk_au_cl_acc(self):
        return self.usuario == 'BK' and self.producto == 'AU' and self.estado_actual == 'CL_ACC'

    @property
    def bk_au_op_acc(self):
        return self.usuario == 'BK' and self.producto == 'AU' and self.estado_actual == 'OP_ACC'

    @property
    def bk_au(self):
        return self.usuario == 'BK' and self.producto == 'AU'

    @property
    def bk_m_cl_acc(self):
        return self.usuario == 'BK' and self.producto == 'M' and self.estado_actual == 'CL_ACC'

    @property
    def bk_m_op_acc(self):
        return self.usuario == 'BK' and self.producto == 'M' and self.estado_actual == 'OP_ACC'

    @property
    def bk_m(self):
        return self.usuario == 'BK' and self.producto == 'M'

    @property
    def bk_pl_cl_acc(self):
        return self.usuario == 'BK' and self.producto == 'PL' and self.estado_actual == 'CL_ACC'

    @property
    def bk_pl_op_acc(self):
        return self.usuario == 'BK' and self.producto == 'PL' and self.estado_actual == 'OP_ACC'

    @property
    def bk_pl(self):
        return self.usuario == 'BK' and self.producto == 'PL'

    @property
    def bk_r_cl_acc(self):
        return self.usuario == 'BK' and self.producto == 'R' and self.estado_actual == 'CL_ACC'

    @property
    def bk_r_op_acc(self):
        return self.usuario == 'BK' and self.producto == 'R' and self.estado_actual == 'OP_ACC'

    @property
    def bk_r(self):
        return self.usuario == 'BK' and self.producto == 'R'

    @property
    def bk_cl_acc(self):
        return self.usuario == 'BK' and self.estado_actual == 'CL_ACC'

    @property
    def bk_op_acc(self):
        return self.usuario == 'BK' and self.estado_actual == 'OP_ACC'

    @property
    def bk(self):
        return self.usuario == 'BK'

    @property
    def nbk_au_cl_acc(self):
        return self.usuario == 'NBK' and self.producto == 'AU' and self.estado_actual == 'CL_ACC'

    @property
    def nbk_au_op_acc(self):
        return self.usuario == 'NBK' and self.producto == 'AU' and self.estado_actual == 'OP_ACC'

    @property
    def nbk_au(self):
        return self.usuario == 'NBK' and self.producto == 'AU'

    @property
    def nbk_m_cl_acc(self):
        return self.usuario == 'NBK' and self.producto == 'M' and self.estado_actual == 'CL_ACC'

    @property
    def nbk_m_op_acc(self):
        return self.usuario == 'NBK' and self.producto == 'M' and self.estado_actual == 'OP_ACC'

    @property
    def nbk_m(self):
        return self.usuario == 'NBK' and self.producto == 'M'

    @property
    def nbk_pl_cl_acc(self):
        return self.usuario == 'NBK' and self.producto == 'PL' and self.estado_actual == 'CL_ACC'

    @property
    def nbk_pl_op_acc(self):
        return self.usuario == 'NBK' and self.producto == 'PL' and self.estado_actual == 'OP_ACC'

    @property
    def nbk_pl(self):
        return self.usuario == 'NBK' and self.producto == 'PL'

    @property
    def nbk_r_cl_acc(self):
        return self.usuario == 'NBK' and self.producto == 'R' and self.estado_actual == 'CL_ACC'

    @property
    def nbk_r_op_acc(self):
        return self.usuario == 'NBK' and self.producto == 'R' and self.estado_actual == 'OP_ACC'

    @property
    def nbk_r(self):
        return self.usuario == 'NBK' and self.producto == 'R'

    @property
    def nbk_cl_acc(self):
        return self.usuario == 'NBK' and self.estado_actual == 'CL_ACC'

    @property
    def nbk_op_acc(self):
        return self.usuario == 'NBK' and self.estado_actual == 'OP_ACC'

    @property
    def nbk(self):
        return self.usuario == 'NBK'

    @property
    def nbk_tu(self):
        return self.usuario in ('NBK', 'C&S')

    @property
    def tu(self):
        return self.usuario == 'C&S'

    @property
    def amx_cl_acc(self):
        return self.usuario in ('BK', 'NBK') and self.producto == 'AMX' and self.estado_actual == 'CL_ACC'

    @property
    def amx_op_acc(self):
        return self.usuario in ('BK', 'NBK') and self.producto == 'AMX' and self.estado_actual == 'OP_ACC'

    @property
    def amx(self):
        return self.usuario in ('BK', 'NBK') and self.producto == 'AMX'

    @property
    def bk_amx(self):
        return self.usuario == 'BK' and self.producto == 'AMX'

    @property
    def nbk_amx(self):
        return self.usuario == 'NBK' and self.producto == 'AMX'

    @property
    def au_cl_acc(self):
        return self.usuario in ('BK', 'NBK') and self.producto == 'AU' and self.estado_actual == 'CL_ACC'

    @property
    def au_op_acc(self):
        return self.usuario in ('BK', 'NBK') and self.producto == 'AU' and self.estado_actual == 'OP_ACC'

    @property
    def au(self):
        return self.usuario in ('BK', 'NBK') and self.producto == 'AU'

    @property
    def m_cl_acc(self):
        return self.usuario in ('BK', 'NBK') and self.producto == 'M' and self.estado_actual == 'CL_ACC'

    @property
    def m_op_acc(self):
        return self.usuario in ('BK', 'NBK') and self.producto == 'M' and self.estado_actual == 'OP_ACC'

    @property
    def m(self):
        return self.usuario in ('BK', 'NBK') and self.producto == 'M'

    @property
    def pl_cl_acc(self):
        return self.usuario in ('BK', 'NBK') and self.producto == 'PL' and self.estado_actual == 'CL_ACC'

    @property
    def pl_op_acc(self):
        return self.usuario in ('BK', 'NBK') and self.producto == 'PL' and self.estado_actual == 'OP_ACC'

    @property
    def pl(self):
        return self.usuario in ('BK', 'NBK') and self.producto == 'PL'

    @property
    def r_cl_acc(self):
        return self.usuario in ('BK', 'NBK') and self.producto == 'R' and self.estado_actual == 'CL_ACC'

    @property
    def r_op_acc(self):
        return self.usuario in ('BK', 'NBK') and self.producto == 'R' and self.estado_actual == 'OP_ACC'

    @property
    def r(self):
        return self.usuario in ('BK', 'NBK') and self.producto == 'R'

    @property
    def cl_acc(self):
        return self.usuario in ('BK', 'NBK') and self.estado_actual == 'CL_ACC'

    @property
    def op_acc(self):
        return self.usuario in ('BK', 'NBK') and self.estado_actual == 'OP_ACC'

    @property
    def tu_cl_acc(self):
        return self.usuario in ('BK', 'NBK', 'C&S') and self.estado_actual == 'CL_ACC'

    @property
    def tu_op_acc(self):
        return self.usuario in ('BK', 'NBK', 'C&S') and self.estado_actual == 'OP_ACC'

    @property
    def all_acc(self):
        return self.usuario in ('BK', 'NBK')

    @property
    def tu_all_acc(self):
        return self.usuario in ('BK', 'NBK', 'C&S')

    @property
    def valido(self):
        if self.cuf_cve_mon == 'UD' and self.udi_fec_rep is None:
            return False
        elif self.cuf_cve_mon == 'US' and self.dlr_fec_rep is None:
            return False
        return True


class BuroScoreModel(BaseModel):
    scf_consec: int = Field(None, title='', alias='scfConsec')
    scf_nombre: str = Field(None, title='', alias='scfNombre')
    scf_codigo: str = Field(None, title='', alias='scfCodigo')
    scf_valor: int = Field(None, title='', alias='scfValor')
    scf_razon1: str = Field(None, title='', alias='scfRazon1')
    scf_razon2: str = Field(None, title='', alias='scfRazon2')
    scf_razon3: str = Field(None, title='', alias='scfRazon3')
    scf_err: str = Field(None, title='', alias='scfErr')
    scf_recal: int = Field(None, title='', alias='scfRecal')
    scf_fraude: bool = Field(None, title='', alias='scfFraude')
    icc_valor: int = Field(None, title='', alias='inpICCVal')


class VariablesBuroCuentasModel(BuroCuentasModel):

    @property
    def cred_max(self):
        return self.val_to_mon(self.cuf_max_cre)

    @property
    def pmt(self):
        if self.val_to_mon(self.cuf_monto) is None:
            return None
        else:
            return self.val_to_mon(self.cuf_monto) * self.freq_factor

    @property
    def cred_lim(self):
        return self.val_to_mon(self.cuf_lim_cre)

    @property
    def num_pmt(self):
        if self.cuf_num_pag is None:
            return None
        else:
            return self.cuf_num_pag / self.freq_factor

    @property
    def cur_bal(self):
        return self.val_to_mon(self.cuf_sal_act)

    @property
    def dlq_bal(self):
        return self.val_to_mon(self.cuf_sal_ven)

    @property
    def num_dlq_bal(self):
        if self.cuf_pag_ven is None:
            return None
        else:
            return self.cuf_pag_ven / self.freq_factor

    @property
    def max_mop_bal(self):
        return self.val_to_mon(self.cuf_imp_sal)

    @property
    def val_act(self):
        return self.val_to_mon(self.cuf_val_act)

    @property
    def rc(self):
        if self.cred_max is None and self.cuf_cve_obs not in ('FD', 'FR', 'GP', 'IM', 'RN', 'SG', 'UP', 'VR'):
            return None
        else:
            return self.cuf_cve_obs in ('FD', 'FR', 'GP', 'IM', 'RN', 'SG', 'UP', 'VR') \
               or (self.cred_max >= 500 * self.udi_fec_rep and self.cuf_cve_obs in ('CV', 'LC', 'NV')) \
               or (self.cuf_cve_obs == 'PC' and (self.cur_bal >= 500 * self.udi_fec_rep or
                                                 self.cur_bal >= 0.05 * self.cred_max))

    @property
    def apr(self):
        return self.fnc_interes_mensual(0.0001, self.cred_max, self.num_pmt, self.pmt)

    @property
    def max_mop(self):
        if self.cuf_mop_mor is None or int(self.cuf_mop_mor) == 0:
            return None
        elif self.cuf_mop_mor in ("96", "97", "99"):
            return 9
        else:
            return int(self.cuf_mop_mor)

    @property
    def m_mop(self):
        return self.fnc_moda()

    @property
    def avg_mop(self):
        return self.fnc_mop_promedio()

    @property
    def max_mop_hist_06m(self):
        return self.fnc_mopmaximo(6)

    @property
    def max_mop_hist_12m(self):
        return self.fnc_mopmaximo(12)

    @property
    def max_mop_hist_24m(self):
        return self.fnc_mopmaximo(24)

    @property
    def max_mop_hist_rel_06m(self):
        return self.fnc_mopmax_relevantes(6, self.cur_bal, self.cred_lim, self.cred_max)

    @property
    def max_mop_hist_rel_12m(self):
        return self.fnc_mopmax_relevantes(12, self.cur_bal, self.cred_lim, self.cred_max)

    @property
    def max_mop_hist_rel_24m(self):
        return self.fnc_mopmax_relevantes(24, self.cur_bal, self.cred_lim, self.cred_max)

    @property
    def max_mop_hist_rel_14m(self):
        return self.fnc_mopmax_relevantes(14, self.cur_bal, self.cred_lim, self.cred_max)

    @property
    def gd_acc(self):
        if not self.max_mop_hist_12m:
            return None
        else:
            return self.max_mop_hist_12m < 2

    @property
    def cred_max_gt_cur_bal(self):
        if self.cur_bal is None or (self.cred_max is None and self.cur_bal is None):
            return None
        else:
            if self.cred_max is None:
                return 0 > self.cur_bal
            else:
                return self.cred_max > self.cur_bal

    @property
    def t_mop(self):
        return self.fnc_t_mop()

    @property
    def peso_mop(self):
        return self.fnc_peso_mop()

    @property
    def mop_lt2(self):
        return self.fnc_lect_hispag('CONSECUTIVOS')

    @property
    def num_grw_mop(self):
        return self.fnc_lect_hispag('CRECIMIENTOS')

    @property
    def num_dec_mop(self):
        return self.fnc_lect_hispag('DECRECIMIENTOS')

    @property
    def log_base_mop_of_bal_mop(self):
        return self.fnc_log_basemop_saldo(self.max_mop_bal)

    @property
    def ms_lst_def_1(self):
        return self.fnc_ms_lst_def(1)

    @property
    def ms_lst_def_2(self):
        return self.fnc_ms_lst_def(2)

    @property
    def ms_lst_def_3(self):
        return self.fnc_ms_lst_def(3)

    @property
    def ms_op(self):
        return self.fnc_dif_meses(self.cuf_fec_ape, self.fecha_buro)

    @property
    def ms_act(self):
        return self.fnc_dif_meses(self.cuf_fec_act, self.fecha_buro)

    @property
    def d_ms_op_to_ms_cl(self):
        return self.fnc_dif_meses(self.cuf_fec_ape, self.cuf_fec_cie)

    @property
    def d_ms_op_to_ms_max_mop(self):
        return self.fnc_dif_meses(self.cuf_fec_ape, self.cuf_fec_mor)

    @property
    def d_ms_op_to_ms_re(self):
        return self.fnc_dif_meses(self.cuf_fec_ape, self.cuf_reestr)

    @property
    def ms_cl(self):
        return self.fnc_dif_meses(self.cuf_fec_cie, self.fecha_buro)

    @property
    def d_ms_max_mop_to_ms_zero_bal(self):
        return self.fnc_dif_meses(self.cuf_fec_mor, self.cuf_ult_sal)

    @property
    def ms_re(self):
        return self.fnc_dif_meses(self.cuf_reestr, self.fecha_buro)

    @property
    def d_ms_re_to_ms_zero_bal(self):
        return self.fnc_dif_meses(self.cuf_reestr, self.cuf_ult_sal)

    @property
    def d_ms_lst_buy_to_ms_lst_pay(self):
        return self.fnc_dif_meses(self.cuf_ult_com, self.cuf_ult_pag)

    @property
    def ms_zero_bal(self):
        return self.fnc_dif_meses(self.cuf_ult_sal, self.fecha_buro)

    @property
    def ms_lst_buy(self):
        return self.fnc_dif_meses(self.cuf_ult_com, self.fecha_buro)

    @property
    def ms_lst_pay(self):
        return self.fnc_dif_meses(self.cuf_ult_pag, self.fecha_buro)

    @property
    def r_cred_max_by_cred_lim(self):
        return self.ratio(self.cred_max, self.cred_lim)

    @property
    def r_cred_max_by_num_pmt(self):
        return self.ratio(self.cred_max, self.num_pmt)

    @property
    def r_pmt_by_cred_max(self):
        return self.ratio(self.pmt, self.cred_max)

    @property
    def r_pmt_by_cur_bal(self):
        return self.ratio(self.pmt, self.cur_bal)

    @property
    def r_cur_bal_by_cred_max(self):
        return self.ratio(self.cur_bal, self.cred_max)

    @property
    def r_dlq_bal_by_cred_max(self):
        return self.ratio(self.dlq_bal, self.cred_max)

    @property
    def util(self):
        return self.ratio(self.cur_bal, self.cred_lim)

    @property
    def d_pmt_to_dlq_bal(self):
        if self.pmt is None or self.dlq_bal is None:
            return None
        else:
            return self.pmt - self.dlq_bal

    @property
    def d_cur_bal_to_pmt(self):
        if self.cur_bal is None or self.pmt is None:
            return None
        else:
            return self.cur_bal - self.pmt

    @property
    def pct_dlq_bal(self):
        if self.dlq_bal is None:
            return 0
        else:
            return self.ratio(100 * self.dlq_bal, self.cur_bal)

    @property
    def r_mop_bal_by_cred_max(self):
        if self.max_mop_bal == 0 or (self.max_mop_bal is None and (self.cuf_mop_mor is None or int(self.cuf_mop_mor) > 1)):
            return 0
        elif self.cred_max is None or self.cred_max == 0:
            return None
        else:
            return self.max_mop_bal / self.cred_max

    @property
    def r_mop_bal_by_cred_lim(self):
        if self.max_mop_bal == 0 or (self.max_mop_bal is None and (self.cuf_mop_mor is None or int(self.cuf_mop_mor) > 1)):
            return 0
        elif self.cred_lim is None or self.cred_lim == 0:
            return None
        else:
            return self.max_mop_bal / self.cred_lim

    @property
    def pmt_sp(self):
        if self.cuf_nom_oto in ('AUTOREGIO', 'BANCO REGIONAL D', 'BANREGIO', 'BANREGIO, S.A.', 'TC BANREGIO') \
                and self.pmt is not None:
            return self.pmt
        else:
            return 0

    @property
    def pmt_op(self):
        if self.cuf_nom_oto not in ('AUTOREGIO', 'BANCO REGIONAL D', 'BANREGIO', 'BANREGIO, S.A.', 'TC BANREGIO') \
                and self.producto is not 'C&S' and self.pmt is not None:
            return self.pmt
        else:
            return 0

    @property
    def pmt_bk_op_acc(self):
        if self.usuario == 'BK' and self.estado_actual == 'OP_ACC' and self.pmt is not None:
            return self.pmt
        else:
            return 0

    @property
    def pmt_nbk_op_acc(self):
        if self.usuario == 'NBK' and self.estado_actual == 'OP_ACC' and self.pmt is not None:
            return self.pmt
        else:
            return 0

    @property
    def all_pmt(self):
        if self.usuario in ('BK', 'NBK') and self.estado_actual == 'OP_ACC' and self.pmt is not None:
            return self.pmt
        else:
            return 0

    @property
    def acc(self):
        return True

    @property
    def udis_vp(self):
        if self.udi_fec_ape is not None and self.udi_fec_buro is not None:
            return self.udi_fec_ape / self.udi_fec_buro
        else:
            return None

    @property
    def cred_bal(self):  # also called "saldos"
        if self.producto == 'R':
            if self.cred_max is None:
                return None
            else:
                return self.cred_lim if self.cred_lim > self.cred_max else self.cred_max
        else:
            return self.cred_max

    @property
    def vp_cur_bal(self):
        if self.cur_bal is not None and self.udis_vp is not None:
            return self.cur_bal * self.udis_vp
        else:
            return None

    @property
    def vp_cred_bal(self):
        if self.cred_bal is not None and self.udis_vp is not None:
            return self.cred_bal * self.udis_vp
        else:
            return None

    @property
    def cur_bal_mop_actual(self):
        if self.cuf_fma_pag in ('01', 'UR'):
            return self.cur_bal
        elif self.cuf_fma_pag == '02':
            return self.cur_bal / 2
        elif self.cuf_fma_pag == '03':
            return self.cur_bal / 3
        elif self.cuf_fma_pag == '04':
            return self.cur_bal / 4
        elif self.cuf_fma_pag == '05':
            return self.cur_bal / 5
        elif self.cuf_fma_pag == '06':
            return self.cur_bal / 6
        elif self.cuf_fma_pag == '07':
            return self.cur_bal / 7
        elif '9' in self.cuf_fma_pag:
            return self.cur_bal / 8
        else:
            return None

    @property
    def cur_bal_by_mop01(self):
        if self.cuf_fma_pag in ('01', 'UR'):
            return self.cur_bal
        else:
            return None

    @property
    def cur_bal_by_mop02(self):
        if self.cuf_fma_pag == '02':
            return self.cur_bal / 2
        else:
            return None

    @property
    def cur_bal_by_mop03(self):
        if self.cuf_fma_pag == '03':
            return self.cur_bal / 3
        else:
            return None

    @property
    def cur_bal_by_mop04(self):
        if self.cuf_fma_pag == '04':
            return self.cur_bal / 4
        else:
            return None

    @property
    def cur_bal_by_mop05(self):
        if self.cuf_fma_pag == '05':
            return self.cur_bal / 5
        else:
            return None

    @property
    def cur_bal_by_mop06(self):
        if self.cuf_fma_pag == '06':
            return self.cur_bal / 6
        else:
            return None

    @property
    def cur_bal_by_mop07(self):
        if self.cuf_fma_pag == '07':
            return self.cur_bal / 7
        else:
            return None

    @property
    def cur_bal_by_mop09(self):
        if '9' in self.cuf_fma_pag:
            return self.cur_bal / 8
        else:
            return None

    @property
    def dlq_bal_mop_actual(self):
        if self.cuf_fma_pag in ('01', 'UR'):
            return self.dlq_bal
        elif self.cuf_fma_pag == '02':
            return self.dlq_bal / 2
        elif self.cuf_fma_pag == '03':
            return self.dlq_bal / 3
        elif self.cuf_fma_pag == '04':
            return self.dlq_bal / 4
        elif self.cuf_fma_pag == '05':
            return self.dlq_bal / 5
        elif self.cuf_fma_pag == '06':
            return self.dlq_bal / 6
        elif self.cuf_fma_pag == '07':
            return self.dlq_bal / 7
        elif '9' in self.cuf_fma_pag:
            return self.dlq_bal / 8
        else:
            return None

    @property
    def dlq_bal_by_mop01(self):
        if self.cuf_fma_pag in ('01', 'UR'):
            return self.dlq_bal
        else:
            return None

    @property
    def dlq_bal_by_mop02(self):
        if self.cuf_fma_pag == '02':
            return self.dlq_bal / 2
        else:
            return None

    @property
    def dlq_bal_by_mop03(self):
        if self.cuf_fma_pag == '03':
            return self.dlq_bal / 3
        else:
            return None

    @property
    def dlq_bal_by_mop04(self):
        if self.cuf_fma_pag == '04':
            return self.dlq_bal / 4
        else:
            return None

    @property
    def dlq_bal_by_mop05(self):
        if self.cuf_fma_pag == '05':
            return self.dlq_bal / 5
        else:
            return None

    @property
    def dlq_bal_by_mop06(self):
        if self.cuf_fma_pag == '06':
            return self.dlq_bal / 6
        else:
            return None

    @property
    def dlq_bal_by_mop07(self):
        if self.cuf_fma_pag == '07':
            return self.dlq_bal / 7
        else:
            return None

    @property
    def dlq_bal_by_mop09(self):
        if '9' in self.cuf_fma_pag:
            return self.dlq_bal / 8
        else:
            return None

    @property
    def pmt_mop_actual(self):
        if self.cuf_fma_pag in ('01', 'UR'):
            return self.pmt
        elif self.cuf_fma_pag == '02':
            return self.pmt / 2
        elif self.cuf_fma_pag == '03':
            return self.pmt / 3
        elif self.cuf_fma_pag == '04':
            return self.pmt / 4
        elif self.cuf_fma_pag == '05':
            return self.pmt / 5
        elif self.cuf_fma_pag == '06':
            return self.pmt / 6
        elif self.cuf_fma_pag == '07':
            return self.pmt / 7
        elif '9' in self.cuf_fma_pag:
            return self.pmt / 8
        else:
            return None

    @property
    def pmt_by_mop01(self):
        if self.cuf_fma_pag in ('01', 'UR'):
            return self.pmt
        else:
            return None

    @property
    def pmt_by_mop02(self):
        if self.cuf_fma_pag == '02':
            return self.pmt / 2
        else:
            return None

    @property
    def pmt_by_mop03(self):
        if self.cuf_fma_pag == '03':
            return self.pmt / 3
        else:
            return None

    @property
    def pmt_by_mop04(self):
        if self.cuf_fma_pag == '04':
            return self.pmt / 4
        else:
            return None

    @property
    def pmt_by_mop05(self):
        if self.cuf_fma_pag == '05':
            return self.pmt / 5
        else:
            return None

    @property
    def pmt_by_mop06(self):
        if self.cuf_fma_pag == '06':
            return self.pmt / 6
        else:
            return None

    @property
    def pmt_by_mop07(self):
        if self.cuf_fma_pag == '07':
            return self.pmt / 7
        else:
            return None

    @property
    def pmt_by_mop09(self):
        if '9' in self.cuf_fma_pag:
            return self.pmt / 8
        else:
            return None

    @property
    def compromisos(self):
        if self.cuf_tip_cue == 'O' and self.cuf_nom_oto == 'CIA Q- OTORGA':
            return 0
        elif self.cuf_fec_cie is not None or self.cuf_tip_cue in ('I', 'M') or (
                self.cuf_tip_cue == 'O' and self.cuf_nom_oto != 'CIA Q- OTORGA'):
            return self.pmt
        elif self.cuf_tip_cue == 'R':
            return max(self.pmt, 0.03 * self.cred_lim)

    @property
    def hit_revolvente_relevante(self):
        ret = self.producto == 'R' and self.ms_op >= 12 and (self.cred_max >= 15000 or self.cred_lim >= 15000) \
              and self.estado_actual == 'OP_ACC'
        if self.ms_lst_buy is None and self.ms_lst_pay is None:
            return None
        elif self.ms_lst_buy is not None and self.ms_lst_pay is not None:
            return ret and (self.ms_lst_buy <= 24 or self.ms_lst_pay <= 24)
        elif self.ms_lst_buy is not None:
            return ret and self.ms_lst_buy <= 24
        else:
            return ret and self.ms_lst_pay <= 24

    @property
    def hit_revolvente_no_relevante(self):
        return not self.hit_revolvente_relevante and self.ms_op >= 12 \
               and (self.cred_max >= 15000 or self.cred_lim >= 15000) \
               and self.cuf_nom_oto not in ('SERVICIOS', 'SERVS. GRALES.', 'GUBERNAMENTALES', 'COMUNICACIONES')

    @property
    def cve_obs_relevante(self):
        return self.cuf_cve_obs in ('FD', 'FR', 'GP', 'IM', 'SG', 'VR') \
               or (self.cred_max >= 500 * self.udi_fec_rep and self.cuf_cve_obs in ('CV', 'LC', 'NV')) \
               or (self.cuf_cve_obs == 'UP' and (self.cur_bal >= 500 * self.udi_fec_rep or
                                                 self.cur_bal >= 0.05 * self.cred_max))

    @property
    def cve_obs_fd(self):
        return self.cuf_cve_obs == 'FD'

    @property
    def cve_obs_sg(self):
        return self.cuf_cve_obs == 'SG'

    @property
    def cve_obs_up(self):
        return self.cuf_cve_obs == 'UP'

    @property
    def cve_obs_rn(self):
        return self.cuf_cve_obs == 'RN'

    @property
    def cve_obs_gp(self):
        return self.cuf_cve_obs == 'GP'

    @property
    def cve_obs_fr(self):
        return self.cuf_cve_obs == 'FR'

    @property
    def cve_obs_vr(self):
        return self.cuf_cve_obs == 'VR'

    @property
    def cve_obs_lc(self):
        return self.cuf_cve_obs == 'LC'


class VariablesBuroConsultasModel(BuroConsultaModel):

    @property
    def iq_03m_bk(self):
        return self.iq_03m and self.bk

    @property
    def iq_03m_bk_au(self):
        return self.iq_03m and self.bk_au

    @property
    def iq_03m_bk_m(self):
        return self.iq_03m and self.bk_m

    @property
    def iq_03m_bk_pl(self):
        return self.iq_03m and self.bk_pl

    @property
    def iq_03m_bk_r(self):
        return self.iq_03m and self.bk_r

    @property
    def iq_03m_nbk(self):
        return self.iq_03m and self.nbk

    @property
    def iq_03m_nbk_au(self):
        return self.iq_03m and self.nbk_au

    @property
    def iq_03m_nbk_m(self):
        return self.iq_03m and self.nbk_m

    @property
    def iq_03m_nbk_pl(self):
        return self.iq_03m and self.nbk_pl

    @property
    def iq_03m_nbk_r(self):
        return self.iq_03m and self.nbk_r

    @property
    def iq_03m_amx(self):
        return self.iq_03m and self.amx and self.all_iq

    @property
    def iq_03m_au(self):
        return self.iq_03m and self.au and self.all_iq

    @property
    def iq_03m_m(self):
        return self.iq_03m and self.m and self.all_iq

    @property
    def iq_03m_pl(self):
        return self.iq_03m and self.pl and self.all_iq

    @property
    def iq_03m_r(self):
        return self.iq_03m and self.r and self.all_iq

    @property
    def iq_03m_fl(self):
        return self.iq_03m and self.all_iq

    @property
    def iq_03m_no_impl(self):
        return self.iq_03m and not self.implicito

    @property
    def iq_06m_bk(self):
        return self.iq_06m and self.bk

    @property
    def iq_06m_bk_au(self):
        return self.iq_06m and self.bk_au

    @property
    def iq_06m_bk_m(self):
        return self.iq_06m and self.bk_m

    @property
    def iq_06m_bk_pl(self):
        return self.iq_06m and self.bk_pl

    @property
    def iq_06m_bk_r(self):
        return self.iq_06m and self.bk_r

    @property
    def iq_06m_nbk(self):
        return self.iq_06m and self.nbk

    @property
    def iq_06m_nbk_au(self):
        return self.iq_06m and self.nbk_au

    @property
    def iq_06m_nbk_m(self):
        return self.iq_06m and self.nbk_m

    @property
    def iq_06m_nbk_pl(self):
        return self.iq_06m and self.nbk_pl

    @property
    def iq_06m_nbk_r(self):
        return self.iq_06m and self.nbk_r

    @property
    def iq_06m_amx(self):
        return self.iq_06m and self.amx and self.all_iq

    @property
    def iq_06m_au(self):
        return self.iq_06m and self.au and self.all_iq

    @property
    def iq_06m_m(self):
        return self.iq_06m and self.m and self.all_iq

    @property
    def iq_06m_pl(self):
        return self.iq_06m and self.pl and self.all_iq

    @property
    def iq_06m_r(self):
        return self.iq_06m and self.r and self.all_iq

    @property
    def iq_06m_fl(self):
        return self.iq_06m and self.all_iq

    @property
    def iq_12m_bk(self):
        return self.iq_12m and self.bk

    @property
    def iq_12m_bk_au(self):
        return self.iq_12m and self.bk_au

    @property
    def iq_12m_bk_m(self):
        return self.iq_12m and self.bk_m

    @property
    def iq_12m_bk_pl(self):
        return self.iq_12m and self.bk_pl

    @property
    def iq_12m_bk_r(self):
        return self.iq_12m and self.bk_r

    @property
    def iq_12m_nbk(self):
        return self.iq_12m and self.nbk

    @property
    def iq_12m_nbk_au(self):
        return self.iq_12m and self.nbk_au

    @property
    def iq_12m_nbk_m(self):
        return self.iq_12m and self.nbk_m

    @property
    def iq_12m_nbk_pl(self):
        return self.iq_12m and self.nbk_pl

    @property
    def iq_12m_nbk_r(self):
        return self.iq_12m and self.nbk_r

    @property
    def iq_12m_amx(self):
        return self.iq_12m and self.amx and self.all_iq

    @property
    def iq_12m_au(self):
        return self.iq_12m and self.au and self.all_iq

    @property
    def iq_12m_m(self):
        return self.iq_12m and self.m and self.all_iq

    @property
    def iq_12m_pl(self):
        return self.iq_12m and self.pl and self.all_iq

    @property
    def iq_12m_r(self):
        return self.iq_12m and self.r and self.all_iq

    @property
    def iq_12m_fl(self):
        return self.iq_12m and self.all_iq

    @property
    def iq_18m_bk(self):
        return self.iq_18m and self.bk

    @property
    def iq_18m_bk_au(self):
        return self.iq_18m and self.bk_au

    @property
    def iq_18m_bk_m(self):
        return self.iq_18m and self.bk_m

    @property
    def iq_18m_bk_pl(self):
        return self.iq_18m and self.bk_pl

    @property
    def iq_18m_bk_r(self):
        return self.iq_18m and self.bk_r

    @property
    def iq_18m_nbk(self):
        return self.iq_18m and self.nbk

    @property
    def iq_18m_nbk_au(self):
        return self.iq_18m and self.nbk_au

    @property
    def iq_18m_nbk_m(self):
        return self.iq_18m and self.nbk_m

    @property
    def iq_18m_nbk_pl(self):
        return self.iq_18m and self.nbk_pl

    @property
    def iq_18m_nbk_r(self):
        return self.iq_18m and self.nbk_r

    @property
    def iq_18m_amx(self):
        return self.iq_18m and self.amx and self.all_iq

    @property
    def iq_18m_au(self):
        return self.iq_18m and self.au and self.all_iq

    @property
    def iq_18m_m(self):
        return self.iq_18m and self.m and self.all_iq

    @property
    def iq_18m_pl(self):
        return self.iq_18m and self.pl and self.all_iq

    @property
    def iq_18m_r(self):
        return self.iq_18m and self.r and self.all_iq

    @property
    def iq_18m_fl(self):
        return self.iq_18m and self.all_iq

    @property
    def iq_24m_bk(self):
        return self.iq_24m and self.bk

    @property
    def iq_24m_bk_au(self):
        return self.iq_24m and self.bk_au

    @property
    def iq_24m_bk_m(self):
        return self.iq_24m and self.bk_m

    @property
    def iq_24m_bk_pl(self):
        return self.iq_24m and self.bk_pl

    @property
    def iq_24m_bk_r(self):
        return self.iq_24m and self.bk_r

    @property
    def iq_24m_nbk(self):
        return self.iq_24m and self.nbk

    @property
    def iq_24m_nbk_au(self):
        return self.iq_24m and self.nbk_au

    @property
    def iq_24m_nbk_m(self):
        return self.iq_24m and self.nbk_m

    @property
    def iq_24m_nbk_pl(self):
        return self.iq_24m and self.nbk_pl

    @property
    def iq_24m_nbk_r(self):
        return self.iq_24m and self.nbk_r

    @property
    def iq_24m_amx(self):
        return self.iq_24m and self.amx and self.all_iq

    @property
    def iq_24m_au(self):
        return self.iq_24m and self.au and self.all_iq

    @property
    def iq_24m_m(self):
        return self.iq_24m and self.m and self.all_iq

    @property
    def iq_24m_pl(self):
        return self.iq_24m and self.pl and self.all_iq

    @property
    def iq_24m_r(self):
        return self.iq_24m and self.r and self.all_iq

    @property
    def iq_24m_fl(self):
        return self.iq_24m and self.all_iq


class VariablesBuroScoreModel(BuroScoreModel):

    @property
    def score_recal(self):
        if bool(self.scf_recal):
            return self.scf_valor
        else:
            return int(round((0.9147 * self.scf_valor) + 19.369))

    @property
    def score_prod(self) -> int:
        if not bool(self.scf_recal):
            return self.scf_valor
        else:
            return int(round((1.0972 * self.scf_valor) - 24.2767))
