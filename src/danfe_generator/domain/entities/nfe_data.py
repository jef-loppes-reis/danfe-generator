"""
Entidade NFe Data do domínio.

Esta entidade representa os dados principais de uma Nota Fiscal Eletrônica (NFe),
agregando todas as informações necessárias para a geração do DANFE.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .emitente import Emitente
from .destinatario import Destinatario
from .protocolo import Protocolo


@dataclass
class NFeData:
    """
    Representa os dados principais de uma NFe.
    
    Esta entidade agrega todas as informações essenciais de uma NFe
    necessárias para a geração do DANFE Simplificado.
    
    Parameters
    ----------
    numero : str
        Número da NFe
    serie : str
        Série da NFe
    chave_acesso : str
        Chave de acesso da NFe (44 dígitos)
    data_emissao : datetime
        Data de emissão da NFe
    emitente : Emitente
        Dados do emitente
    destinatario : Destinatario
        Dados do destinatário
    protocolo : Optional[Protocolo]
        Dados do protocolo de autorização
    
    Examples
    --------
    >>> from datetime import datetime
    >>> emitente = Emitente("12345678000195", "Empresa", None, "123", "SP")
    >>> destinatario = Destinatario("12345678901", TipoDocumento.CPF, "João", "RJ")
    >>> nfe = NFeData(
    ...     numero="123",
    ...     serie="1",
    ...     chave_acesso="12345678901234567890123456789012345678901234",
    ...     data_emissao=datetime(2025, 9, 1),
    ...     emitente=emitente,
    ...     destinatario=destinatario,
    ...     protocolo=None
    ... )
    >>> print(nfe.numero)
    123
    """

    numero: str
    serie: str
    chave_acesso: str
    data_emissao: datetime
    emitente: Emitente
    destinatario: Destinatario
    protocolo: Optional[Protocolo] = None

    def __post_init__(self):
        """
        Valida os dados da NFe após a inicialização.
        
        Raises
        ------
        ValueError
            Se algum campo obrigatório estiver vazio ou inválido
        """
        if not self.numero:
            raise ValueError("Número da NFe é obrigatório")

        if not self.serie:
            raise ValueError("Série da NFe é obrigatória")

        if not self.chave_acesso or len(self.chave_acesso) != 44:
            raise ValueError("Chave de acesso deve ter exatamente 44 dígitos")

        if not isinstance(self.data_emissao, datetime):
            raise ValueError("Data de emissão deve ser um objeto datetime")

    def get_data_emissao_formatada(self) -> str:
        """
        Retorna a data de emissão formatada para exibição.
        
        Returns
        -------
        str
            Data no formato brasileiro (dd/mm/aaaa)
        
        Examples
        --------
        >>> nfe = NFeData("123", "1", "1"*44, datetime(2025, 9, 1), emitente, destinatario)
        >>> nfe.get_data_emissao_formatada()
        '01/09/2025'
        """
        return self.data_emissao.strftime('%d/%m/%Y')

    def get_chave_formatada(self) -> str:
        """
        Retorna a chave de acesso formatada para exibição.
        
        Returns
        -------
        str
            Chave de acesso formatada em grupos de 4 dígitos
        
        Examples
        --------
        >>> nfe = NFeData("123", "1", "1234567890123456789012345678901234567890123", emitente, destinatario)
        >>> nfe.get_chave_formatada()
        '1234 5678 9012 3456 7890 1234 5678 9012 3456 7890 123'
        """
        # Formata a chave em grupos de 4 dígitos
        grupos = [self.chave_acesso[i:i+4] for i in range(0, len(self.chave_acesso), 4)]
        return ' '.join(grupos)
