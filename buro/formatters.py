from dataclasses import dataclass, fields
from datetime import date, datetime


@dataclass
class BuroCuentasFormatter:
    cufFolio: str
    cufConsec: int
    cufFecAct: date
    cufRegImp: str
    cufCveOto: str
    cufNomOto: str
    cufNumTel: str  # added
    cufNumCue: str
    cufTipRes: str
    cufTipCue: str
    cufTipCon: str
    cufCveMon: str
    cufValAct: int
    cufNumPag: int
    cufFrePag: str
    cufMonto: float
    cufFecApe: date
    cufUltPag: date
    cufUltCom: date
    cufFecCie: date
    cufFecRep: date
    cufFmaRep: str
    cufUltSal: date
    cufGarant: str
    cufMaxCre: float
    cufSalAct: float
    cufLimCre: float
    cufSalVen: float
    cufPagVen: float
    cufFmaPag: str
    cufHisPag: str
    cufFecRec: date
    cufFecAnt: date
    cufCveObs: str
    cufTotPag: int
    cufMop02: int
    cufMop03: int
    cufMop04: int
    cufMop05: int
    cufImpSal: int
    cufFecMor: date
    cufMopMor: str
    cufReestr: date

    # variables economicas
    fecFecBur: date
    fecRepDol: float = None
    fecRepUdi: float = None
    fecApeUdi: float = None
    fecConUdi: float = None

    def __post_init__(self):
        self.emitir_variables()

    def emitir_variables(self):
        for f in fields(self):
            value = getattr(self, f.name)
            if value is None:
                continue
            elif value == '' or value == ' ':
                if f.name in ('cufImpSal', 'cufMop05', 'cufMop04', 'cufMop03',
                              'cufMop02', 'cufTotPag', 'cufPagVen', 'cufSalVen',
                              'cufLimCre', 'cufSalAct', 'cufMaxCre', 'cufMonto'):
                    setattr(self, f.name, 0)
                else:
                    setattr(self, f.name, None)
            # elif f.name == 'cufSalAct':
            #     value = value.rstrip('+').rstrip('-')
            #     setattr(self, f.name, f.type(value))
            elif f.name == 'fecFecBur':
                value = value.rstrip('+').rstrip('-')
                setattr(self, f.name, datetime.strptime(value, '%Y-%m-%d').date())
            elif f.type == date:
                setattr(self, f.name, datetime.strptime(value, '%Y-%m-%d').date())

            elif not isinstance(value, f.type):
                try:
                    setattr(self, f.name, f.type(value))
                except Exception as e:
                    print(e)


@dataclass
class BuroConsultaFormatter:
    cofFolio: str
    cofConsec: int
    cofFecCon: date
    cofBuroId: str
    cofCveOto: str
    cofNomOto: str
    cofNumTel: str
    cofTipCon: str
    cofCveMon: str
    cofImport: str
    cofTipRes: str
    cofConsum: str
    cofResult: int
    cofFecBur: date

    def __post_init__(self):
        self.emitir_variables()

    def emitir_variables(self):
        for f in fields(self):
            value = getattr(self, f.name)
            if value is None:
                continue
            elif value == '' or value == ' ':
                setattr(self, f.name, None)
            elif f.name == 'cofFecBur':
                value = value.rstrip('+').rstrip('-')
                setattr(self, f.name, datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f').date())
            elif f.type == date:
                setattr(self, f.name, datetime.strptime(value, '%Y-%m-%d').date())
            elif not isinstance(value, f.type):
                try:
                    setattr(self, f.name, f.type(value))
                except Exception as e:
                    print(e)


@dataclass
class BuroScoreFormatter:
    scfFolio: str
    scfConsec: int
    scfNombre: str
    scfCodigo: str
    scfValor: str
    scfRazon1: str
    scfRazon2: str
    scfRazon3: str
    scfCodErr: str
    scfRecal: int
    scfFraude: bool
    inpICCVal: int = 0

    def __post_init__(self):
        self.emitir_variables()

    def emitir_variables(self):
        for f in fields(self):
            value = getattr(self, f.name)
            if value is None:
                continue
            elif value == '' or value == ' ':
                if f.name == 'scfValor':
                    self.scfValor = 0
                else:
                    setattr(self, f.name, None)
            elif not isinstance(value, f.type):
                try:
                    setattr(self, f.name, f.type(value))
                except Exception as e:
                    print(e)
