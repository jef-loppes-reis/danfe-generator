"""
Interfaces do domínio do gerador de DANFE.

Este módulo contém as interfaces (contratos) que definem os comportamentos
esperados pelos diferentes componentes do sistema, seguindo o princípio
da inversão de dependência da Clean Architecture.
"""

from .nfe_parser import NFeParserInterface
from .date_formatter import DateFormatterInterface
from .document_formatter import DocumentFormatterInterface
from .zpl_generator import ZPLGeneratorInterface
from .file_writer import FileWriterInterface

__all__ = [
    'NFeParserInterface',
    'DateFormatterInterface', 
    'DocumentFormatterInterface',
    'ZPLGeneratorInterface',
    'FileWriterInterface'
]
