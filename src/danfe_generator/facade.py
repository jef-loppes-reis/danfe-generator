"""
Facade do gerador de DANFE.

Este módulo implementa o padrão Facade, fornecendo uma interface
simplificada para o sistema de geração de DANFE seguindo os
princípios da Clean Architecture.
"""

from typing import Union, Optional
from pathlib import Path

from .domain.entities.danfe import DANFE
from .use_cases.generate_danfe_from_xml import GenerateDANFEFromXMLUseCase
from .use_cases.save_danfe_to_file import SaveDANFEToFileUseCase
from .adapters.parsers.xml_nfe_parser import XMLNFeParser
from .adapters.generators.standard_zpl_generator import StandardZPLGenerator
from .infrastructure.file_system_writer import FileSystemWriter
from .use_cases.search_file_xml import SearchFileXMLUseCase
from .infrastructure.file_sytem_search_xml import FileSystemSearchXMLConfig


class DANFEGeneratorFacade:
    """
    Facade para o gerador de DANFE.
    
    Fornece uma interface simplificada para gerar DANFE a partir
    de arquivos XML da NFe, encapsulando a complexidade das camadas
    internas da Clean Architecture.
    
    Parameters
    ----------
    xml_file_path : Union[str, Path]
        Caminho para o arquivo XML da NFe
    
    Examples
    --------
    >>> generator = DANFEGeneratorFacade("nfe.xml")
    >>> danfe = generator.generate_danfe()
    >>> file_path = generator.save_danfe("minha_danfe.zpl")
    >>> print(f"DANFE salva em: {file_path}")
    DANFE salva em: minha_danfe.zpl
    """

    def __init__(self, xml_file_path: Optional[Union[str, Path]] = None, cod_invoice: Optional[str] = None):
        """
        Inicializa o gerador com o arquivo XML da NFe.
        
        Parameters
        ----------
        xml_file_path : Optional[Union[str, Path]], optional
            Caminho para o arquivo XML da NFe
        cod_invoice : Optional[str], optional
            Código da nota fiscal
        Examples
        --------
        >>> generator = DANFEGeneratorFacade("nfe.xml")
        >>> danfe = generator.generate_danfe()
        """
        self.file_system_search_xml = FileSystemSearchXMLConfig()
        self.xml_file_path = xml_file_path
        self.cod_invoice = cod_invoice
        self._danfe = None

        # Inicializa dependências
        self._xml_parser = XMLNFeParser()
        self._zpl_generator = StandardZPLGenerator()
        self._file_writer = FileSystemWriter()
        self._search_file_xml = SearchFileXMLUseCase()

        # Inicializa casos de uso
        self._generate_use_case = GenerateDANFEFromXMLUseCase(
            self._xml_parser,
            self._zpl_generator,
            self._search_file_xml
        )
        self._save_use_case = SaveDANFEToFileUseCase(self._file_writer)

    def generate_danfe(self) -> DANFE:
        """
        Gera DANFE a partir do XML da NFe.
        
        Returns
        -------
        DANFE
            DANFE gerado com código ZPL
        
        Raises
        ------
        ValueError
            Se o arquivo XML não for válido ou os dados estiverem incorretos
        FileNotFoundError
            Se o arquivo XML não for encontrado
        
        Examples
        --------
        >>> generator = DANFEGeneratorFacade("nfe.xml")
        >>> danfe = generator.generate_danfe()
        >>> print(danfe.get_info_summary())
        NFe 123/1 - Emitente: Empresa LTDA - Destinatário: João Silva
        """
        self._danfe = self._generate_use_case.execute(self.xml_file_path, self.cod_invoice)
        return self._danfe

    def get_zpl_code(self) -> str:
        """
        Retorna o código ZPL gerado.
        
        Returns
        -------
        str
            Código ZPL para impressão da etiqueta DANFE
        
        Raises
        ------
        RuntimeError
            Se o DANFE ainda não foi gerado
        
        Examples
        --------
        >>> generator = DANFEGeneratorFacade("nfe.xml")
        >>> generator.generate_danfe()
        >>> zpl_code = generator.get_zpl_code()
        >>> print(zpl_code[:10])
        ^XA^CI28^MCY
        """
        if self._danfe is None:
            self._danfe = self.generate_danfe()

        return self._danfe.codigo_zpl

    def save_danfe(self, output_file_path: Union[str, Path] = "danfe_generated.zpl") -> str:
        """
        Salva o código ZPL em um arquivo.
        
        Parameters
        ----------
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
        RuntimeError
            Se o DANFE ainda não foi gerado
        
        Examples
        --------
        >>> generator = DANFEGeneratorFacade("nfe.xml")
        >>> file_path = generator.save_danfe("minha_danfe.zpl")
        >>> print(f"DANFE salva em: {file_path}")
        DANFE salva em: minha_danfe.zpl
        """
        if self._danfe is None:
            self._danfe = self.generate_danfe()

        return self._save_use_case.execute(self._danfe, output_file_path)

    def print_nfe_info(self) -> None:
        """
        Exibe informações extraídas da NFe para debug.
        
        Raises
        ------
        RuntimeError
            Se o DANFE ainda não foi gerado
        
        Examples
        --------
        >>> generator = DANFEGeneratorFacade("nfe.xml")
        >>> generator.print_nfe_info()
        === INFORMAÇÕES DA NFe ===
        Número: 123
        Série: 1
        ...
        """
        if self._danfe is None:
            self._danfe = self.generate_danfe()

        nfe_data = self._danfe.nfe_data

        print("=== INFORMAÇÕES DA NFe ===")
        print(f"Número: {nfe_data.numero}")
        print(f"Série: {nfe_data.serie}")
        print(f"Data Emissão: {nfe_data.get_data_emissao_formatada()}")
        print(f"Chave de Acesso: {nfe_data.chave_acesso}")

        if nfe_data.protocolo:
            print(f"Protocolo: {nfe_data.protocolo.numero}")
            print(f"Data Autorização: {nfe_data.protocolo.get_data_formatada()}")

        print(f"Emitente: {nfe_data.emitente.nome}")
        print(f"CNPJ: {nfe_data.emitente.get_cnpj_formatado()}")
        print(f"Destinatário: {nfe_data.destinatario.nome}")
        print(f"{nfe_data.destinatario.tipo_documento.value}: {nfe_data.destinatario.get_documento_formatado()}")

    @property
    def danfe(self) -> DANFE:
        """
        Propriedade para acessar o DANFE gerado.
        
        Returns
        -------
        DANFE
            DANFE gerado ou None se ainda não foi gerado
        
        Examples
        --------
        >>> generator = DANFEGeneratorFacade("nfe.xml")
        >>> generator.generate_danfe()
        >>> print(generator.danfe.get_info_summary())
        NFe 123/1 - Emitente: Empresa LTDA - Destinatário: João Silva
        """
        return self._danfe
