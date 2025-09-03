"""
Caso de uso para geração de DANFE a partir de XML.

Este módulo implementa o caso de uso principal do sistema:
gerar um DANFE a partir de um arquivo XML da NFe.
"""

from typing import Union, Optional
from pathlib import Path

from ..domain.entities.danfe import DANFE
from ..domain.interfaces.nfe_parser import NFeParserInterface
from ..domain.interfaces.zpl_generator import ZPLGeneratorInterface
from ..use_cases.search_file_xml import SearchFileXMLUseCase


class GenerateDANFEFromXMLUseCase:
    """
    Caso de uso para geração de DANFE a partir de XML da NFe.
    
    Este caso de uso coordena o processo de extração de dados
    de um XML da NFe e a geração do código ZPL correspondente.
    
    Parameters
    ----------
    nfe_parser : NFeParserInterface
        Parser responsável por extrair dados do XML
    zpl_generator : ZPLGeneratorInterface
        Gerador responsável por criar o código ZPL
    Examples
    --------
    >>> use_case = GenerateDANFEFromXMLUseCase(xml_parser, zpl_gen)
    >>> danfe = use_case.execute("nfe.xml")
    >>> print(danfe.get_info_summary())
    NFe 123/1 - Emitente: Empresa LTDA - Destinatário: João Silva
    """

    def __init__(
        self,
        nfe_parser: NFeParserInterface,
        zpl_generator: ZPLGeneratorInterface,
        search_file_xml: SearchFileXMLUseCase
    ):
        """
        Inicializa o caso de uso com as dependências necessárias.
        
        Parameters
        ----------
        nfe_parser : NFeParserInterface
            Parser para extração de dados do XML
        zpl_generator : ZPLGeneratorInterface
            Gerador de código ZPL
        search_file_xml: SearchFileXMLUseCase
            Caso de uso para buscar arquivos XML
        """
        self._nfe_parser = nfe_parser
        self._zpl_generator = zpl_generator
        self._search_file_xml = search_file_xml

    def execute(self, xml_file_path: Optional[Union[str, Path]] = None, cod_invoice: Optional[str] = None) -> DANFE:
        """
        Executa o caso de uso de geração de DANFE.
        
        Parameters
        ----------
        xml_file_path : Optional[Union[str, Path]], optional
            Caminho para o arquivo XML da NFe
        cod_invoice : Optional[str], optional
            Código da nota fiscal
        
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
        >>> danfe = use_case.execute("path/to/nfe.xml")
        >>> print(danfe.codigo_zpl[:10])
        ^XA^CI28^MCY
        """
        if xml_file_path is None and cod_invoice is not None:
            search_result = self._search_file_xml.execute(cod_invoice=cod_invoice)
            if isinstance(search_result, list):
                xml_file_path = search_result[0] if search_result else None
            else:
                xml_file_path = search_result
        if xml_file_path is None:
            raise ValueError("Caminho do arquivo XML ou código da nota fiscal não fornecido")
        # Extrai dados da NFe do XML
        nfe_data = self._nfe_parser.parse(xml_file_path)

        # Gera o DANFE com código ZPL
        danfe = self._zpl_generator.generate(nfe_data)

        return danfe
