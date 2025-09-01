"""
DANFE Generator.

Gerador de código ZPL para DANFE Simplificado a partir de XML da NFe
seguindo os princípios da Clean Architecture.

Este módulo fornece uma interface simples para gerar DANFEs a partir
de arquivos XML da NFe, organizando o código em camadas bem definidas.
"""

from .facade import DANFEGeneratorFacade

# Facilita o uso da biblioteca
DANFEGenerator = DANFEGeneratorFacade

__version__ = "1.0.0"
__author__ = "Sistema DANFE Generator"

__all__ = [
    'DANFEGenerator',
    'DANFEGeneratorFacade'
]
