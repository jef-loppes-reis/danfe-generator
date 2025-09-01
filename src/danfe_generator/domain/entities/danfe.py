"""
Entidade DANFE do domínio.

Esta entidade representa o Documento Auxiliar da Nota Fiscal Eletrônica (DANFE),
contendo os dados formatados e prontos para geração do código ZPL.
"""

from dataclasses import dataclass
from .nfe_data import NFeData


@dataclass
class DANFE:
    """
    Representa um DANFE Simplificado.
    
    Esta entidade encapsula os dados formatados de uma NFe
    prontos para serem utilizados na geração do código ZPL.
    
    Parameters
    ----------
    nfe_data : NFeData
        Dados da NFe que originou este DANFE
    codigo_zpl : str
        Código ZPL gerado para impressão da etiqueta
    
    Examples
    --------
    >>> danfe = DANFE(nfe_data=nfe_dados, codigo_zpl="^XA...^XZ")
    >>> print(len(danfe.codigo_zpl))
    1234
    """

    nfe_data: NFeData
    codigo_zpl: str

    def __post_init__(self):
        """
        Valida os dados do DANFE após a inicialização.
        
        Raises
        ------
        ValueError
            Se algum campo obrigatório estiver vazio ou inválido
        """
        if not isinstance(self.nfe_data, NFeData):
            raise ValueError("nfe_data deve ser uma instância de NFeData")

        if not self.codigo_zpl:
            raise ValueError("Código ZPL é obrigatório")

        if not self.codigo_zpl.startswith('^XA'):
            raise ValueError("Código ZPL deve começar com ^XA")

        if not self.codigo_zpl.endswith('^XZ'):
            raise ValueError("Código ZPL deve terminar com ^XZ")

    def save_to_file(self, file_path: str) -> None:
        """
        Salva o código ZPL em um arquivo.
        
        Parameters
        ----------
        file_path : str
            Caminho do arquivo onde salvar o código ZPL
        
        Raises
        ------
        IOError
            Se houver erro ao escrever o arquivo
        
        Examples
        --------
        >>> danfe.save_to_file("minha_danfe.zpl")
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.codigo_zpl)
        except Exception as e:
            raise IOError(f"Erro ao salvar arquivo: {e}") from e

    def get_info_summary(self) -> str:
        """
        Retorna um resumo das informações do DANFE.
        
        Returns
        -------
        str
            Resumo formatado das informações principais
        
        Examples
        --------
        >>> summary = danfe.get_info_summary()
        >>> print(summary)
        NFe 123/1 - Emitente: Empresa LTDA - Destinatário: João Silva
        """
        return (f"NFe {self.nfe_data.numero}/{self.nfe_data.serie} - "
                f"Emitente: {self.nfe_data.emitente.nome} - "
                f"Destinatário: {self.nfe_data.destinatario.nome}")
