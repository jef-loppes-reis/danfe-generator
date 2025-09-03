"""
Caso de uso para buscar arquivos XML no sistema de arquivos.
"""
from typing import Optional
from ..infrastructure.file_sytem_search_xml import FileSystemSearchXML, FileSystemSearchXMLConfig


class SearchFileXMLUseCase():
    """
    Caso de uso para buscar arquivos XML no sistema de arquivos.

    Parameters
    ----------
    file_search_xml : FileSearchXMLInterface
        Interface para buscar arquivos XML no sistema de arquivos.
    """
    def __init__(self):
        """
        Inicializa o caso de uso com as dependências necessárias.
        """
        self.file_search_xml = FileSystemSearchXML(FileSystemSearchXMLConfig())

    def execute(self, cod_invoice: Optional[str] = None) -> Optional[str] | list[str]:
        """
        Executa o caso de uso para buscar arquivos XML no sistema de arquivos.
        """
        return self.file_search_xml.listing_files_xml(cod_invoice=cod_invoice)
