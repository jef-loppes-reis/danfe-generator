"""
Classe para buscar arquivos XML no sistema de arquivos.
"""

from dataclasses import dataclass, field
import os
from datetime import datetime
from typing import Optional, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from ..domain.interfaces.file_search_xml import FileSearchXMLInterface


@dataclass
class FileSystemSearchXMLConfig:
    """
    Configuração para buscar arquivos XML no sistema de arquivos.
    """
    xml_dir_path: str = field(
        default_factory=lambda: f'//10.4.1.2/DRIVE-D/0_ecommerce_XML/{datetime.today().strftime("%Y-%m")}'
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
        self._mtime_cache: Dict[str, datetime] = {}

    def get_file_m_datetime(self, path: str) -> datetime:
        """
        Retorna a data de modificação do arquivo com cache.
        
        Parameters
        ----------
        path : str
            Caminho completo para o arquivo
            
        Returns
        -------
        datetime
            Data de modificação do arquivo
            
        Examples
        --------
        >>> fs = FileSystemSearchXML(config)
        >>> mtime = fs.get_file_m_datetime("/path/to/file.xml")
        >>> isinstance(mtime, datetime)
        True
        """
        if path not in self._mtime_cache:
            self._mtime_cache[path] = datetime.fromtimestamp(os.path.getmtime(path))
        return self._mtime_cache[path]

    def clear_cache(self) -> None:
        """
        Limpa o cache de datas de modificação de arquivos.
        
        Útil quando arquivos podem ter sido modificados externamente
        e é necessário forçar uma nova leitura das datas.
        
        Examples
        --------
        >>> fs = FileSystemSearchXML(config)
        >>> fs.clear_cache()
        """
        self._mtime_cache.clear()

    def _process_file_batch(self, files_batch: list[str], cod_invoice: Optional[str] = None) -> list[str]:
        """
        Processa um lote de arquivos de forma concorrente.
        
        Parameters
        ----------
        files_batch : list[str]
            Lista de nomes de arquivos para processar
        cod_invoice : Optional[str], optional
            Código da nota fiscal para filtrar
            
        Returns
        -------
        list[str]
            Lista de caminhos completos de arquivos XML válidos
        """
        valid_files = []
        base_path = Path(self.config.xml_dir_path)

        for filename in files_batch:
            # Filtro rápido: extensão .xml primeiro
            if not filename.endswith('.xml'):
                continue

            # Filtro de código se especificado
            if cod_invoice and cod_invoice not in filename:
                continue

            full_path = str(base_path / filename)
            try:
                # Verifica se arquivo existe e tem data de modificação válida
                if self.get_file_m_datetime(full_path):
                    valid_files.append(full_path)
            except (OSError, FileNotFoundError):
                # Ignora arquivos que não podem ser acessados
                continue

        return valid_files

    def listing_files_xml(self, cod_invoice: Optional[str] = None) -> Optional[str] | list[str]:
        """
        Lista os arquivos XML no diretório de forma otimizada e concorrente.
        
        Parameters
        ----------
        cod_invoice : Optional[str], optional
            Código da nota fiscal para filtrar arquivos específicos
            
        Returns
        -------
        Optional[str] | list[str]
            Se cod_invoice fornecido: primeiro arquivo encontrado ou None
            Se cod_invoice não fornecido: lista de todos os arquivos XML válidos
            
        Raises
        ------
        OSError
            Se o diretório não puder ser acessado
            
        Examples
        --------
        >>> fs = FileSystemSearchXML(config)
        >>> # Buscar arquivo específico
        >>> arquivo = fs.listing_files_xml("12345")
        >>> # Listar todos os XMLs
        >>> todos_xmls = fs.listing_files_xml()
        """
        try:
            all_files = os.listdir(self.config.xml_dir_path)
        except OSError as e:
            raise OSError(f"Não foi possível acessar o diretório: {self.config.xml_dir_path}") from e

        # Pre-filtro rápido para arquivos .xml
        xml_files = [f for f in all_files if f.endswith('.xml')]

        if not xml_files:
            return None if cod_invoice else []

        # Para poucos arquivos, processamento sequencial é mais eficiente
        if len(xml_files) <= 10:
            valid_files = self._process_file_batch(xml_files, cod_invoice)
        else:
            # Processamento concorrente para muitos arquivos
            batch_size = max(1, len(xml_files) // 4)  # 4 threads
            batches = [xml_files[i:i + batch_size] for i in range(0, len(xml_files), batch_size)]

            valid_files = []
            with ThreadPoolExecutor(max_workers=4) as executor:
                # Submete tarefas concorrentemente
                future_to_batch = {
                    executor.submit(self._process_file_batch, batch, cod_invoice): batch
                    for batch in batches
                }

                # Coleta resultados
                for future in as_completed(future_to_batch):
                    try:
                        batch_results = future.result()
                        valid_files.extend(batch_results)

                        # Se buscando arquivo específico e encontrou, retorna imediatamente
                        if cod_invoice and batch_results:
                            return batch_results[0]
                    except (OSError, FileNotFoundError):
                        # Ignora erros de arquivo e continua processamento
                        continue

        # Retorna resultado baseado no tipo de busca
        if cod_invoice:
            return valid_files[0] if valid_files else None
        return valid_files
