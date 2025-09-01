"""
Entidade Destinatário do domínio.

Esta entidade representa o destinatário de uma Nota Fiscal Eletrônica (NFe),
contendo todas as informações necessárias para identificar o receptor
do documento fiscal.
"""

from dataclasses import dataclass
from enum import Enum


class TipoDocumento(Enum):
    """
    Enumera os tipos de documento do destinatário.
    
    Attributes
    ----------
    CPF : str
        Cadastro de Pessoa Física
    CNPJ : str
        Cadastro Nacional de Pessoa Jurídica
    """
    CPF = "CPF"
    CNPJ = "CNPJ"


@dataclass
class Destinatario:
    """
    Representa o destinatário de uma NFe.
    
    Esta entidade encapsula todas as informações relacionadas ao destinatário
    da nota fiscal, incluindo dados de identificação e localização.
    
    Parameters
    ----------
    documento : str
        CPF ou CNPJ do destinatário (somente números)
    tipo_documento : TipoDocumento
        Tipo do documento (CPF ou CNPJ)
    nome : str
        Nome/razão social do destinatário
    uf : str
        Unidade federativa do destinatário
    
    Examples
    --------
    >>> destinatario = Destinatario(
    ...     documento="12345678901",
    ...     tipo_documento=TipoDocumento.CPF,
    ...     nome="João da Silva",
    ...     uf="RJ"
    ... )
    >>> print(destinatario.nome)
    João da Silva
    """

    documento: str
    tipo_documento: TipoDocumento
    nome: str
    uf: str

    def __post_init__(self):
        """
        Valida os dados do destinatário após a inicialização.
        
        Raises
        ------
        ValueError
            Se algum campo obrigatório estiver vazio ou inválido
        """
        if not self.documento:
            raise ValueError("Documento é obrigatório")

        if self.tipo_documento == TipoDocumento.CPF and len(self.documento) != 11:
            raise ValueError("CPF deve ter exatamente 11 dígitos")

        if self.tipo_documento == TipoDocumento.CNPJ and len(self.documento) != 14:
            raise ValueError("CNPJ deve ter exatamente 14 dígitos")

        if not self.nome:
            raise ValueError("Nome do destinatário é obrigatório")

        if not self.uf or len(self.uf) != 2:
            raise ValueError("UF deve ter exatamente 2 caracteres")

    def get_documento_formatado(self) -> str:
        """
        Retorna o documento formatado com máscara.
        
        Returns
        -------
        str
            CPF no formato XXX.XXX.XXX-XX ou CNPJ no formato XX.XXX.XXX/XXXX-XX
        
        Examples
        --------
        >>> dest_cpf = Destinatario("12345678901", TipoDocumento.CPF, "João", "RJ")
        >>> dest_cpf.get_documento_formatado()
        '123.456.789-01'
        
        >>> dest_cnpj = Destinatario("12345678000195", TipoDocumento.CNPJ, "Empresa", "SP")
        >>> dest_cnpj.get_documento_formatado()
        '12.345.678/0001-95'
        """
        if self.tipo_documento == TipoDocumento.CPF:
            return f"{self.documento[:3]}.{self.documento[3:6]}.{self.documento[6:9]}-{self.documento[9:11]}"
        # CNPJ
        return f"{self.documento[:2]}.{self.documento[2:5]}.{self.documento[5:8]}/{self.documento[8:12]}-{self.documento[12:14]}"
