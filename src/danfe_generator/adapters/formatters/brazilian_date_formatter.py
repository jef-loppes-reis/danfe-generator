"""
Formatador de datas brasileiro.

Este módulo implementa formatação de datas seguindo
os padrões brasileiros (dd/mm/aaaa).
"""

from datetime import datetime

from ...domain.interfaces.date_formatter import DateFormatterInterface


class BrazilianDateFormatter(DateFormatterInterface):
    """
    Formatador de datas seguindo padrões brasileiros.
    
    Implementa a interface DateFormatterInterface para formatar
    datas no padrão brasileiro (dd/mm/aaaa e dd/mm/aaaa hh:mm:ss).
    
    Examples
    --------
    >>> formatter = BrazilianDateFormatter()
    >>> date = datetime(2025, 9, 1, 8, 55, 5)
    >>> formatter.format_date(date)
    '01/09/2025'
    >>> formatter.format_datetime(date)
    '01/09/2025 08:55:05'
    """

    def parse_iso_date(self, iso_date: str) -> datetime:
        """
        Converte uma data ISO para objeto datetime.
        
        Parameters
        ----------
        iso_date : str
            Data no formato ISO (ex: 2025-09-01T08:55:05-03:00)
        
        Returns
        -------
        datetime
            Objeto datetime correspondente
        
        Raises
        ------
        ValueError
            Se a data não puder ser convertida
        
        Examples
        --------
        >>> formatter = BrazilianDateFormatter()
        >>> dt = formatter.parse_iso_date("2025-09-01T08:55:05-03:00")
        >>> dt.year
        2025
        """
        try:
            # Remove timezone se presente
            datetime_part = iso_date.split('-03:00')[0] if '-03:00' in iso_date else iso_date

            if 'T' in datetime_part:
                return datetime.strptime(datetime_part, '%Y-%m-%dT%H:%M:%S')
            # Apenas data
            date_part = datetime_part.split('T')[0]
            return datetime.strptime(date_part, '%Y-%m-%d')
        except ValueError as e:
            raise ValueError(f"Não foi possível converter a data '{iso_date}': {e}") from e

    def format_date(self, date: datetime) -> str:
        """
        Formata uma data para exibição brasileira.
        
        Parameters
        ----------
        date : datetime
            Data a ser formatada
        
        Returns
        -------
        str
            Data formatada (dd/mm/aaaa)
        
        Examples
        --------
        >>> formatter = BrazilianDateFormatter()
        >>> date = datetime(2025, 9, 1)
        >>> formatter.format_date(date)
        '01/09/2025'
        """
        return date.strftime('%d/%m/%Y')

    def format_datetime(self, date: datetime) -> str:
        """
        Formata uma data/hora para exibição brasileira.
        
        Parameters
        ----------
        date : datetime
            Data/hora a ser formatada
        
        Returns
        -------
        str
            Data/hora formatada (dd/mm/aaaa hh:mm:ss)
        
        Examples
        --------
        >>> formatter = BrazilianDateFormatter()
        >>> date = datetime(2025, 9, 1, 8, 55, 5)
        >>> formatter.format_datetime(date)
        '01/09/2025 08:55:05'
        """
        return date.strftime('%d/%m/%Y %H:%M:%S')
