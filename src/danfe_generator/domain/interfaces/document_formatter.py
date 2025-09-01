"""
Interface para formatador de documentos.

Esta interface define o contrato para implementações de formatadores
que aplicam máscaras em documentos como CPF e CNPJ.
"""

from abc import ABC, abstractmethod


class DocumentFormatterInterface(ABC):
    """
    Interface para formatadores de documento.
    
    Define o contrato que deve ser implementado por classes
    responsáveis por formatar documentos (CPF, CNPJ) com máscaras.
    
    Examples
    --------
    >>> class BrazilianDocumentFormatter(DocumentFormatterInterface):
    ...     def format_cpf(self, cpf):
    ...         return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
    """

    @abstractmethod
    def format_cpf(self, cpf: str) -> str:
        """
        Formata um CPF com máscara.
        
        Parameters
        ----------
        cpf : str
            CPF sem formatação (11 dígitos)
        
        Returns
        -------
        str
            CPF formatado (XXX.XXX.XXX-XX)
        
        Raises
        ------
        ValueError
            Se o CPF não tiver o formato correto
        """
        pass

    @abstractmethod
    def format_cnpj(self, cnpj: str) -> str:
        """
        Formata um CNPJ com máscara.
        
        Parameters
        ----------
        cnpj : str
            CNPJ sem formatação (14 dígitos)
        
        Returns
        -------
        str
            CNPJ formatado (XX.XXX.XXX/XXXX-XX)
        
        Raises
        ------
        ValueError
            Se o CNPJ não tiver o formato correto
        """
        pass

    @abstractmethod
    def format_document(self, document: str) -> str:
        """
        Formata um documento (CPF ou CNPJ) automaticamente.
        
        Parameters
        ----------
        document : str
            Documento sem formatação
        
        Returns
        -------
        str
            Documento formatado
        
        Raises
        ------
        ValueError
            Se o documento não tiver um formato reconhecido
        """
        pass
