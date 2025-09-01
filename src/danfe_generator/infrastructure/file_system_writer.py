"""
Escritor de arquivos no sistema de arquivos.

Este módulo implementa a interface FileWriterInterface para
escrever arquivos diretamente no sistema de arquivos local.
"""

from typing import Union
from pathlib import Path

from ..domain.interfaces.file_writer import FileWriterInterface


class FileSystemWriter(FileWriterInterface):
    """
    Implementação de FileWriterInterface para sistema de arquivos.
    
    Esta classe implementa a escrita de arquivos diretamente
    no sistema de arquivos local.
    
    Examples
    --------
    >>> writer = FileSystemWriter()
    >>> writer.write("conteúdo", "arquivo.txt")
    >>> writer.exists("arquivo.txt")
    True
    """

    def write(self, content: str, file_path: Union[str, Path]) -> None:
        """
        Escreve conteúdo em um arquivo no sistema de arquivos.
        
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
        
        Examples
        --------
        >>> writer = FileSystemWriter()
        >>> writer.write("Hello World", "hello.txt")
        """
        try:
            path = Path(file_path)

            # Cria diretórios pai se não existirem
            path.parent.mkdir(parents=True, exist_ok=True)

            # Escreve o arquivo
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

        except PermissionError as e:
            raise PermissionError(f"Sem permissão para escrever em '{file_path}': {e}") from e
        except Exception as e:
            raise IOError(f"Erro ao escrever arquivo '{file_path}': {e}") from e

    def exists(self, file_path: Union[str, Path]) -> bool:
        """
        Verifica se um arquivo existe no sistema de arquivos.
        
        Parameters
        ----------
        file_path : Union[str, Path]
            Caminho do arquivo a verificar
        
        Returns
        -------
        bool
            True se o arquivo existir, False caso contrário
        
        Examples
        --------
        >>> writer = FileSystemWriter()
        >>> writer.exists("arquivo_existente.txt")
        True
        >>> writer.exists("arquivo_inexistente.txt")
        False
        """
        try:
            return Path(file_path).exists()
        except Exception:
            return False
