"""
Casos de uso do gerador de DANFE.

Este módulo contém os casos de uso da aplicação, que coordenam
as operações necessárias para executar as funcionalidades principais
do sistema seguindo os princípios da Clean Architecture.
"""

from .generate_danfe_from_xml import GenerateDANFEFromXMLUseCase
from .save_danfe_to_file import SaveDANFEToFileUseCase

__all__ = [
    'GenerateDANFEFromXMLUseCase',
    'SaveDANFEToFileUseCase'
]
