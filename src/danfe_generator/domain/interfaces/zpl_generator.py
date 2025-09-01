"""
Interface para gerador de código ZPL.

Esta interface define o contrato para implementações de geradores
que criam código ZPL a partir dos dados da NFe.
"""

from abc import ABC, abstractmethod
from danfe_generator.domain.entities.nfe_data import NFeData
from danfe_generator.domain.entities.danfe import DANFE


class ZPLGeneratorInterface(ABC):
    """
    Interface para geradores de código ZPL.
    
    Define o contrato que deve ser implementado por classes
    responsáveis por gerar código ZPL para impressão de DANFE.
    
    Examples
    --------
    >>> class StandardZPLGenerator(ZPLGeneratorInterface):
    ...     def generate(self, nfe_data):
    ...         # Implementação específica
    ...         pass
    """

    @abstractmethod
    def generate(self, nfe_data: NFeData) -> DANFE:
        """
        Gera código ZPL a partir dos dados da NFe.
        
        Parameters
        ----------
        nfe_data : NFeData
            Dados da NFe para geração do DANFE
        
        Returns
        -------
        DANFE
            Objeto DANFE com código ZPL gerado
        
        Raises
        ------
        ValueError
            Se os dados da NFe não forem válidos para geração
        """
        pass
