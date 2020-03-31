from dataclasses import dataclass, field

from agregadores.buro import cuentas
from features import FeaturesBuro


@dataclass
class VariablesBuro:
    features_buro: FeaturesBuro

    # types
    subcontrolador_cuentas: type = field(init=False)
    subcontrolador_vector_fecha_cuentas: type = field(init=False)
    controlador_cuentas: type = field(init=False)

    def __post_init__(self):
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