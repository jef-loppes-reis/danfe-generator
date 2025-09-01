"""
Caso de uso para geração de DANFE a partir de XML.

Este módulo implementa o caso de uso principal do sistema:
gerar um DANFE a partir de um arquivo XML da NFe.
"""

from typing import Union
from pathlib import Path

from ..domain.entities.danfe import DANFE
from ..domain.interfaces.nfe_parser import NFeParserInterface
from ..domain.interfaces.zpl_generator import ZPLGeneratorInterface


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
        zpl_generator: ZPLGeneratorInterface
    ):
        """
        Inicializa o caso de uso com as dependências necessárias.
        
        Parameters
        ----------
        nfe_parser : NFeParserInterface
            Parser para extração de dados do XML
        zpl_generator : ZPLGeneratorInterface
            Gerador de código ZPL
        """
        self._nfe_parser = nfe_parser
        self._zpl_generator = zpl_generator

    def execute(self, xml_file_path: Union[str, Path]) -> DANFE:
        """
        Executa o caso de uso de geração de DANFE.
        
        Parameters
        ----------
        xml_file_path : Union[str, Path]
            Caminho para o arquivo XML da NFe
        
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
        # Extrai dados da NFe do XML
        nfe_data = self._nfe_parser.parse(xml_file_path)

        # Gera o DANFE com código ZPL
        danfe = self._zpl_generator.generate(nfe_data)

        return danfe
