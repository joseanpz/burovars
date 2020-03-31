from dataclasses import dataclass, field

from agregadores.buro import cuentas, consultas, score
from caracteristicas.buro import FeaturesBuro


@dataclass
class ControladorBuro:
    features_buro: FeaturesBuro

    # types
    subcontrolador_cuentas: type = field(init=False)
    subcontrolador_vector_fecha_cuentas: type = field(init=False)
    controlador_cuentas: type = field(init=False)

    controlador_consultas: type = field(init=False)

    controlador_score: type = field(init=False)

    def __post_init__(self):
        self.configura_controlador_cuentas()
        self.configura_controlador_consultas()
        self.configura_controlador_score()

    def configura_controlador_consultas(self):
        self.controlador_consultas = type(
            'ControladorConsultas',
            (consultas.CtrlVariablesConsultas,),
            {
                'subcampos': self.features_buro.subcampos_consultas,
                'campos': self.features_buro.campos_consultas,
                'clase_subcampo': self.features_buro.subvariables_consultas,
                'clase_variables': self.features_buro.variables_consultas
            }
        )

    def configura_controlador_score(self):
        self.controlador_score = type(
            'ControladorScore',
            (score.CtrlVariablesScore,),
            {
                'subcampos': self.features_buro.subcampos_score,
                'campos': self.features_buro.campos_score,
                'clase_subcampo': self.features_buro.subvariables_score,
                'clase_variables': self.features_buro.variables_score
            }
        )

    def configura_controlador_cuentas(self):
        self.subcontrolador_cuentas = type(
            'SubControladorCuentas',
            (cuentas.VariablesCuentas,),
            {
                'subcampos': self.features_buro.subcampos_cuentas,
                'clase_subcampo': self.features_buro.subvariables_cuentas
            }
        )

        self.subcontrolador_vector_fecha_cuentas = type(
            'SubControladorVectorFechaCuentas',
            (cuentas.VariablesVectorFechaCuentas,),
            {
                'subcampos': self.features_buro.subcampos_vector_cuentas,
                'clase_subcampos': self.features_buro.subvariables_vector_cuentas
            }
        )

        self.controlador_cuentas = type(
            'ControladorCuentas',
            (cuentas.ConstructorVariablesAgregadasCuentas,),
            {
                'campos': self.features_buro.campos_cuentas,
                'clase_variables': self.features_buro.variables_cuentas,
                'clase_subvar': self.subcontrolador_cuentas,
                'clase_subvar_vec': self.subcontrolador_vector_fecha_cuentas
            }
        )