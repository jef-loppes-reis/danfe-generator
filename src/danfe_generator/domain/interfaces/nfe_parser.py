"""
Interface para parser de NFe.

Esta interface define o contrato para implementações de parsers
que extraem dados de arquivos XML de NFe.
"""

from abc import ABC, abstractmethod
from typing import Union
from pathlib import Path

from danfe_generator.domain.entities.nfe_data import NFeData


class NFeParserInterface(ABC):
    """
    Interface para parsers de NFe.
    
    Define o contrato que deve ser implementado por classes
    responsáveis por extrair dados de arquivos XML da NFe.
    
    Examples
    --------
    >>> class XMLNFeParser(NFeParserInterface):
    ...     def parse(self, source):
    ...         # Implementação específica
    ...         pass
    """

    @abstractmethod
    def parse(self, source: Union[str, Path]) -> NFeData:
        """
        Extrai dados de uma NFe a partir da fonte fornecida.
        
        Parameters
        ----------
        source : Union[str, Path]
            Fonte dos dados da NFe (ex: caminho do arquivo XML)
        
        Returns
        -------
        NFeData
            Dados estruturados da NFe
        
        Raises
        ------
        ValueError
            Se a fonte não for válida ou os dados não puderem ser extraídos
        FileNotFoundError
            Se o arquivo não for encontrado
        """
        pass
