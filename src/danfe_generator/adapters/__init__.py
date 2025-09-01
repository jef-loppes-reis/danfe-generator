"""
Adaptadores do gerador de DANFE.

Este módulo contém os adaptadores que implementam as interfaces
do domínio, fazendo a ponte entre as regras de negócio e
as tecnologias específicas utilizadas.
"""

from .parsers import XMLNFeParser
from .formatters import BrazilianDateFormatter, BrazilianDocumentFormatter
from .generators import StandardZPLGenerator

__all__ = [
    'XMLNFeParser',
    'BrazilianDateFormatter',
    'BrazilianDocumentFormatter', 
    'StandardZPLGenerator'
]
