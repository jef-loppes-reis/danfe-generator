"""
Interface para escrita de arquivos.

Esta interface define o contrato para implementações que
gerenciam a escrita de arquivos no sistema de arquivos.
"""

from abc import ABC, abstractmethod
from typing import Union
from pathlib import Path


class FileWriterInterface(ABC):
    """
    Interface para escritores de arquivo.
    
    Define o contrato que deve ser implementado por classes
    responsáveis por escrever conteúdo em arquivos.
    
    Examples
    --------
    >>> class TextFileWriter(FileWriterInterface):
    ...     def write(self, content, file_path):
    ...         # Implementação específica
    ...         pass
    """

    @abstractmethod
    def write(self, content: str, file_path: Union[str, Path]) -> None:
        """
        Escreve conteúdo em um arquivo.
        
        Parameters
        ----------
        content : str
            Conteúdo a ser escrito
        file_path : Union[str, Path]
            Caminho do arquivo de destino
        
        Raises
        ------
        IOError
            Se houver erro ao escrever o arquivo
        PermissionError
            Se não houver permissão para escrever no local
        """
        pass

    @abstractmethod
    def exists(self, file_path: Union[str, Path]) -> bool:
        """
        Verifica se um arquivo existe.
        
        Parameters
        ----------
        file_path : Union[str, Path]
            Caminho do arquivo a verificar
        
        Returns
        -------
        bool
            True se o arquivo existir, False caso contrário
        """
        pass
