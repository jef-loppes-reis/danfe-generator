"""
Parser de XML para NFe.

Este módulo implementa o parser responsável por extrair
dados de arquivos XML da NFe seguindo o padrão SEFAZ.
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Union, Optional
from pathlib import Path

from ...domain.entities.nfe_data import NFeData
from ...domain.entities.emitente import Emitente
from ...domain.entities.destinatario import Destinatario, TipoDocumento
from ...domain.entities.protocolo import Protocolo
from ...domain.interfaces.nfe_parser import NFeParserInterface


class XMLNFeParser(NFeParserInterface):
    """
    Parser para arquivos XML da NFe.
    
    Implementa a interface NFeParserInterface para extrair dados
    de arquivos XML da NFe seguindo o padrão da SEFAZ.
    
    Examples
    --------
    >>> parser = XMLNFeParser()
    >>> nfe_data = parser.parse("nfe.xml")
    >>> print(nfe_data.numero)
    123
    """

    def __init__(self):
        """Inicializa o parser XML."""
        self._namespace = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

    def parse(self, source: Union[str, Path]) -> NFeData:
        """
        Extrai dados de uma NFe a partir de arquivo XML.
        
        Parameters
        ----------
        source : Union[str, Path]
            Caminho para o arquivo XML da NFe
        
        Returns
        -------
        NFeData
            Dados estruturados da NFe
        
        Raises
        ------
        ValueError
            Se o XML não for válido ou estiver malformado
        FileNotFoundError
            Se o arquivo não for encontrado
        
        Examples
        --------
        >>> parser = XMLNFeParser()
        >>> nfe_data = parser.parse("path/to/nfe.xml")
        >>> print(nfe_data.emitente.nome)
        Empresa Exemplo LTDA
        """
        try:
            # Parse do XML
            tree = ET.parse(source)
            root = tree.getroot()

            # Extrai dados principais
            identificacao = self._extract_identificacao(root)
            emitente = self._extract_emitente(root)
            destinatario = self._extract_destinatario(root)
            protocolo = self._extract_protocolo(root)

            # Monta objeto NFeData
            return NFeData(
                numero=identificacao['numero'],
                serie=identificacao['serie'],
                chave_acesso=identificacao['chave_acesso'],
                data_emissao=identificacao['data_emissao'],
                emitente=emitente,
                destinatario=destinatario,
                protocolo=protocolo
            )

        except ET.ParseError as e:
            raise ValueError(f"XML malformado: {e}") from e
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Arquivo XML não encontrado: {source}") from e
        except Exception as e:
            raise ValueError(f"Erro ao processar XML da NFe: {e}") from e

    def _extract_identificacao(self, root: ET.Element) -> dict:
        """
        Extrai dados de identificação da NFe.
        
        Parameters
        ----------
        root : ET.Element
            Elemento raiz do XML
        
        Returns
        -------
        dict
            Dados de identificação extraídos
        """
        ide = root.find('.//nfe:ide', self._namespace)
        if ide is None:
            raise ValueError("Elemento 'ide' não encontrado no XML")

        numero_elem = ide.find('nfe:nNF', self._namespace)
        serie_elem = ide.find('nfe:serie', self._namespace)
        data_elem = ide.find('nfe:dhEmi', self._namespace)

        numero = numero_elem.text if numero_elem is not None else ""
        serie = serie_elem.text if serie_elem is not None else ""
        data_emissao_str = data_elem.text if data_elem is not None else ""

        # Converte data de emissão
        data_emissao = self._parse_iso_datetime(data_emissao_str)

        # Extrai chave de acesso
        inf_nfe = root.find('.//nfe:infNFe', self._namespace)
        if inf_nfe is None:
            raise ValueError("Elemento 'infNFe' não encontrado no XML")

        chave_completa = inf_nfe.get('Id', '')
        chave_acesso = chave_completa.replace('NFe', '') if chave_completa else ""

        return {
            'numero': numero,
            'serie': serie,
            'data_emissao': data_emissao,
            'chave_acesso': chave_acesso
        }

    def _extract_emitente(self, root: ET.Element) -> Emitente:
        """
        Extrai dados do emitente.
        
        Parameters
        ----------
        root : ET.Element
            Elemento raiz do XML
        
        Returns
        -------
        Emitente
            Dados do emitente
        """
        emit = root.find('.//nfe:emit', self._namespace)
        if emit is None:
            raise ValueError("Elemento 'emit' não encontrado no XML")

        cnpj_elem = emit.find('nfe:CNPJ', self._namespace)
        nome_elem = emit.find('nfe:xNome', self._namespace)
        fantasia_elem = emit.find('nfe:xFant', self._namespace)
        ie_elem = emit.find('nfe:IE', self._namespace)
        uf_elem = emit.find('.//nfe:UF', self._namespace)

        cnpj = cnpj_elem.text if cnpj_elem is not None else ""
        nome = nome_elem.text if nome_elem is not None else ""
        fantasia = fantasia_elem.text if fantasia_elem is not None else None
        ie = ie_elem.text if ie_elem is not None else ""
        uf = uf_elem.text if uf_elem is not None else ""

        return Emitente(
            cnpj=cnpj,
            nome=nome,
            fantasia=fantasia,
            inscricao_estadual=ie,
            uf=uf
        )

    def _extract_destinatario(self, root: ET.Element) -> Destinatario:
        """
        Extrai dados do destinatário.
        
        Parameters
        ----------
        root : ET.Element
            Elemento raiz do XML
        
        Returns
        -------
        Destinatario
            Dados do destinatário
        """
        dest = root.find('.//nfe:dest', self._namespace)
        if dest is None:
            raise ValueError("Elemento 'dest' não encontrado no XML")

        cpf_elem = dest.find('nfe:CPF', self._namespace)
        cnpj_elem = dest.find('nfe:CNPJ', self._namespace)
        nome_elem = dest.find('nfe:xNome', self._namespace)
        uf_elem = dest.find('.//nfe:UF', self._namespace)

        # Determina tipo e valor do documento
        if cpf_elem is not None:
            documento = cpf_elem.text
            tipo_documento = TipoDocumento.CPF
        elif cnpj_elem is not None:
            documento = cnpj_elem.text
            tipo_documento = TipoDocumento.CNPJ
        else:
            documento = ""
            tipo_documento = TipoDocumento.CPF  # Default

        nome = nome_elem.text if nome_elem is not None else ""
        uf = uf_elem.text if uf_elem is not None else ""

        return Destinatario(
            documento=documento,
            tipo_documento=tipo_documento,
            nome=nome,
            uf=uf
        )

    def _extract_protocolo(self, root: ET.Element) -> Optional[Protocolo]:
        """
        Extrai dados do protocolo de autorização.
        
        Parameters
        ----------
        root : ET.Element
            Elemento raiz do XML
        
        Returns
        -------
        Optional[Protocolo]
            Dados do protocolo ou None se não encontrado
        """
        prot = root.find('.//nfe:protNFe/nfe:infProt', self._namespace)
        if prot is None:
            return None

        prot_num_elem = prot.find('nfe:nProt', self._namespace)
        prot_data_elem = prot.find('nfe:dhRecbto', self._namespace)

        if prot_num_elem is None or prot_data_elem is None:
            return None

        numero = prot_num_elem.text
        data_autorizacao = self._parse_iso_datetime(prot_data_elem.text)

        return Protocolo(
            numero=numero,
            data_autorizacao=data_autorizacao
        )

    def _parse_iso_datetime(self, iso_datetime: str) -> datetime:
        """
        Converte string ISO para datetime.
        
        Parameters
        ----------
        iso_datetime : str
            Data/hora no formato ISO
        
        Returns
        -------
        datetime
            Objeto datetime correspondente
        """
        try:
            # Remove timezone se presente
            datetime_part = iso_datetime.split('-03:00')[0] if '-03:00' in iso_datetime else iso_datetime

            if 'T' in datetime_part:
                return datetime.strptime(datetime_part, '%Y-%m-%dT%H:%M:%S')
            date_part = datetime_part.split('T')[0]
            return datetime.strptime(date_part, '%Y-%m-%d')
        except ValueError:
            # Se não conseguir fazer parse, retorna data atual
            return datetime.now()
