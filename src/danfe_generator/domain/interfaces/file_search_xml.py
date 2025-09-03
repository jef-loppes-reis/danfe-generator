from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

class FileSearchXMLInterface(ABC):
    """
    Interface para buscar arquivos XML no sistema de arquivos.
    """
    @abstractmethod
    def listing_files_xml(self, cod_invoice: Optional[str] = None) -> Optional[str] | list[str]:
        """
        Lista os arquivos XML no diretório.
        """
        pass

    @abstractmethod
    def get_file_m_datetime(self, path: str) -> datetime:
        """
        Retorna a data de modificação do arquivo.
        """
        pass
