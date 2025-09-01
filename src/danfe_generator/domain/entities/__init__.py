"""
Entidades do domínio do gerador de DANFE.

Este módulo contém as entidades centrais do domínio, representando
os conceitos fundamentais do sistema de geração de DANFE.
"""

from .nfe_data import NFeData
from .emitente import Emitente
from .destinatario import Destinatario
from .protocolo import Protocolo
from .danfe import DANFE

__all__ = [
    'NFeData',
    'Emitente', 
    'Destinatario',
    'Protocolo',
    'DANFE'
]
