"""
Entidade Emitente do domínio.

Esta entidade representa o emitente de uma Nota Fiscal Eletrônica (NFe),
contendo todas as informações necessárias para identificar a empresa
emissora do documento fiscal.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Emitente:
    """
    Representa o emitente de uma NFe.
    
    Esta entidade encapsula todas as informações relacionadas ao emitente
    da nota fiscal, incluindo dados de identificação e localização.
    
    Parameters
    ----------
    cnpj : str
        CNPJ do emitente (somente números)
    nome : str
        Razão social do emitente
    fantasia : Optional[str]
        Nome fantasia do emitente
    inscricao_estadual : str
        Inscrição estadual do emitente
    uf : str
        Unidade federativa do emitente
    
    Examples
    --------
    >>> emitente = Emitente(
    ...     cnpj="12345678000195",
    ...     nome="Empresa Exemplo LTDA",
    ...     fantasia="Exemplo",
    ...     inscricao_estadual="123456789",
    ...     uf="SP"
    ... )
    >>> print(emitente.nome)
    Empresa Exemplo LTDA
    """

    cnpj: str
    nome: str
    fantasia: Optional[str]
    inscricao_estadual: str
    uf: str

    def __post_init__(self):
        """
        Valida os dados do emitente após a inicialização.
        
        Raises
        ------
        ValueError
            Se algum campo obrigatório estiver vazio ou inválido
        """
        if not self.cnpj or len(self.cnpj) != 14:
            raise ValueError("CNPJ deve ter exatamente 14 dígitos")

        if not self.nome:
            raise ValueError("Nome do emitente é obrigatório")

        if not self.inscricao_estadual:
            raise ValueError("Inscrição estadual é obrigatória")

        if not self.uf or len(self.uf) != 2:
            raise ValueError("UF deve ter exatamente 2 caracteres")

    def get_cnpj_formatado(self) -> str:
        """
        Retorna o CNPJ formatado com máscara.
        
        Returns
        -------
        str
            CNPJ no formato XX.XXX.XXX/XXXX-XX
        
        Examples
        --------
        >>> emitente = Emitente("12345678000195", "Empresa", None, "123", "SP")
        >>> emitente.get_cnpj_formatado()
        '12.345.678/0001-95'
        """
        return f"{self.cnpj[:2]}.{self.cnpj[2:5]}.{self.cnpj[5:8]}/{self.cnpj[8:12]}-{self.cnpj[12:14]}"
