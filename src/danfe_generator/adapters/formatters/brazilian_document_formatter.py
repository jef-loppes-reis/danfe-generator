"""
Formatador de documentos brasileiro.

Este módulo implementa formatação de documentos brasileiros
(CPF e CNPJ) com suas respectivas máscaras.
"""

from ...domain.interfaces.document_formatter import DocumentFormatterInterface


class BrazilianDocumentFormatter(DocumentFormatterInterface):
    """
    Formatador de documentos brasileiros.
    
    Implementa a interface DocumentFormatterInterface para formatar
    CPF e CNPJ com suas respectivas máscaras.
    
    Examples
    --------
    >>> formatter = BrazilianDocumentFormatter()
    >>> formatter.format_cpf("12345678901")
    '123.456.789-01'
    >>> formatter.format_cnpj("12345678000195")
    '12.345.678/0001-95'
    """

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
        
        Examples
        --------
        >>> formatter = BrazilianDocumentFormatter()
        >>> formatter.format_cpf("12345678901")
        '123.456.789-01'
        """
        if not cpf or len(cpf) != 11:
            raise ValueError(f"CPF deve ter exatamente 11 dígitos, recebido: '{cpf}'")

        if not cpf.isdigit():
            raise ValueError(f"CPF deve conter apenas dígitos, recebido: '{cpf}'")

        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"

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
        
        Examples
        --------
        >>> formatter = BrazilianDocumentFormatter()
        >>> formatter.format_cnpj("12345678000195")
        '12.345.678/0001-95'
        """
        if not cnpj or len(cnpj) != 14:
            raise ValueError(f"CNPJ deve ter exatamente 14 dígitos, recebido: '{cnpj}'")

        if not cnpj.isdigit():
            raise ValueError(f"CNPJ deve conter apenas dígitos, recebido: '{cnpj}'")

        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"

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
        
        Examples
        --------
        >>> formatter = BrazilianDocumentFormatter()
        >>> formatter.format_document("12345678901")
        '123.456.789-01'
        >>> formatter.format_document("12345678000195")
        '12.345.678/0001-95'
        """
        if not document:
            return document

        if len(document) == 11:
            return self.format_cpf(document)
        if len(document) == 14:
            return self.format_cnpj(document)
        raise ValueError(f"Documento deve ter 11 (CPF) ou 14 (CNPJ) dígitos, recebido: '{document}' com {len(document)} dígitos")
