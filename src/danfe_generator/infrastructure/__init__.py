"""
Infraestrutura do gerador de DANFE.

Este módulo contém as implementações de infraestrutura que
lidam com recursos externos como sistema de arquivos,
banco de dados, etc.
"""

from .file_system_writer import FileSystemWriter

__all__ = ['FileSystemWriter']
