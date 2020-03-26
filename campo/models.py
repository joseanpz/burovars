from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Campo:
    segmento: str
    variable: str
    sufijo: str = None

    @property
    def nombre(self):
        if self.sufijo:
            return f'{self.variable}_{self.sufijo}'
        else:
            return self.variable


@dataclass(unsafe_hash=True)
class CampoAgregado:
    campo: Any = field(init=False)
    segmento: str
    agregacion: str
    variable: Any
    sufijo: str = None

    def __post_init__(self):
        if isinstance(self.variable, self.__class__):
            self.campo = self.variable
        elif isinstance(self.variable, str):
            self.campo = Campo(
                self.segmento,
                self.variable,
                self.sufijo
            )

    @property
    def nombre(self) -> str:
        if isinstance(self.variable, self.__class__):
            if self.sufijo:
                return f'{self.agregacion}_{self.variable.nombre}_{self.sufijo}'
            else:
                return f'{self.agregacion}_{self.variable.nombre}'

        elif isinstance(self.variable, str):
            if self.sufijo:
                return f'{self.agregacion}_{self.variable}_{self.sufijo}'
            else:
                return f'{self.agregacion}_{self.variable}'
