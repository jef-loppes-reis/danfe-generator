"""
Entidade Protocolo do domínio.

Esta entidade representa o protocolo de autorização de uma NFe,
contendo as informações sobre a autorização do documento fiscal
pela SEFAZ.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Protocolo:
    """
    Representa o protocolo de autorização de uma NFe.
    
    Esta entidade encapsula as informações relacionadas à autorização
    da nota fiscal pelos órgãos competentes.
    
    Parameters
    ----------
    numero : str
        Número do protocolo de autorização
    data_autorizacao : datetime
        Data e hora da autorização
    
    Examples
    --------
    >>> from datetime import datetime
    >>> protocolo = Protocolo(
    ...     numero="123456789012345",
    ...     data_autorizacao=datetime(2025, 9, 1, 8, 55, 5)
    ... )
    >>> print(protocolo.numero)
    123456789012345
    """

    numero: str
    data_autorizacao: datetime

    def __post_init__(self):
        """
        Valida os dados do protocolo após a inicialização.
        
        Raises
        ------
        ValueError
            Se algum campo obrigatório estiver vazio ou inválido
        """
        if not self.numero:
            raise ValueError("Número do protocolo é obrigatório")

        if not isinstance(self.data_autorizacao, datetime):
            raise ValueError("Data de autorização deve ser um objeto datetime")

    def get_data_formatada(self) -> str:
        """
        Retorna a data de autorização formatada para exibição.
        
        Returns
        -------
        str
            Data no formato brasileiro (dd/mm/aaaa hh:mm:ss)
        
        Examples
        --------
        >>> protocolo = Protocolo("123", datetime(2025, 9, 1, 8, 55, 5))
        >>> protocolo.get_data_formatada()
        '01/09/2025 08:55:05'
        """
        return self.data_autorizacao.strftime('%d/%m/%Y %H:%M:%S')
