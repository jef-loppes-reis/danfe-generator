"""
Classe para buscar arquivos XML no sistema de arquivos.
"""

from dataclasses import dataclass, field
import os
from datetime import datetime
from typing import Optional

from ..domain.interfaces.file_search_xml import FileSearchXMLInterface


@dataclass
class FileSystemSearchXMLConfig:
    """
    Configuração para buscar arquivos XML no sistema de arquivos.
    """
    xml_dir_path: str = field(
        default_factory=lambda: f'S:/0_ecommerce_XML/{datetime.today().strftime("%Y-%m")}'
        )


class FileSystemSearchXML(FileSearchXMLInterface):
    """
    Classe para buscar arquivos XML no sistema de arquivos.
    """

    def __init__(self, config: FileSystemSearchXMLConfig):
        """
        Inicializa a classe com a configuração necessária.
        """
        self.config = config

    def get_file_m_datetime(self, path: str) -> datetime:
        """
        Retorna a data de modificação do arquivo.
        """
        return datetime.fromtimestamp(os.path.getmtime(path))

    def listing_files_xml(self, cod_invoice: Optional[str] = None) -> Optional[str] | list[str]:
        """
        Lista os arquivos XML no diretório.
        """
        if cod_invoice:
            files = [
                self.config.xml_dir_path + '/' + file for file in os.listdir(self.config.xml_dir_path)
                if self.get_file_m_datetime(path=f'{self.config.xml_dir_path}/{file}')
                and cod_invoice in file
                and file.endswith('.xml')
            ]
            if files:
                return files[0]
            return None
        return [
            file for file in os.listdir(self.config.xml_dir_path)
            if self.get_file_m_datetime(path=f'{self.config.xml_dir_path}/{file}')
            and file.endswith('.xml')
        ]
