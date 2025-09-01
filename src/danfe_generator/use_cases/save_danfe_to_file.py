"""
Caso de uso para salvar DANFE em arquivo.

Este módulo implementa o caso de uso para persistir
o código ZPL do DANFE em um arquivo.
"""

from typing import Union
from pathlib import Path

from ..domain.entities.danfe import DANFE
from ..domain.interfaces.file_writer import FileWriterInterface


class SaveDANFEToFileUseCase:
    """
    Caso de uso para salvar DANFE em arquivo.
    
    Este caso de uso coordena o processo de escrita do código ZPL
    do DANFE em um arquivo no sistema de arquivos.
    
    Parameters
    ----------
    file_writer : FileWriterInterface
        Escritor responsável por salvar o arquivo
    
    Examples
    --------
    >>> use_case = SaveDANFEToFileUseCase(file_writer)
    >>> file_path = use_case.execute(danfe, "output.zpl")
    >>> print(f"DANFE salvo em: {file_path}")
    DANFE salvo em: output.zpl
    """

    def __init__(self, file_writer: FileWriterInterface):
        """
        Inicializa o caso de uso com as dependências necessárias.
        
        Parameters
        ----------
        file_writer : FileWriterInterface
            Escritor para salvar arquivos
        """
        self._file_writer = file_writer

    def execute(
        self,
        danfe: DANFE,
        output_file_path: Union[str, Path] = "danfe_generated.zpl"
    ) -> str:
        """
        Executa o caso de uso de salvamento do DANFE.
        
        Parameters
        ----------
        danfe : DANFE
            DANFE a ser salvo
        output_file_path : Union[str, Path], optional
            Caminho do arquivo de saída (default: "danfe_generated.zpl")
        
        Returns
        -------
        str
            Caminho do arquivo salvo
        
        Raises
        ------
        IOError
            Se houver erro ao escrever o arquivo
        ValueError
            Se o DANFE não for válido
        
        Examples
        --------
        >>> file_path = use_case.execute(danfe, "meu_danfe.zpl")
        >>> print(f"Arquivo criado: {file_path}")
        Arquivo criado: meu_danfe.zpl
        """
        if not isinstance(danfe, DANFE):
            raise ValueError("O objeto fornecido deve ser uma instância de DANFE")

        # Converte para string se necessário
        file_path_str = str(output_file_path)

        # Escreve o código ZPL no arquivo
        self._file_writer.write(danfe.codigo_zpl, file_path_str)

        return file_path_str
