"""
Interface para formatador de datas.

Esta interface define o contrato para implementações de formatadores
que convertem datas entre diferentes formatos.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class DateFormatterInterface(ABC):
    """
    Interface para formatadores de data.
    
    Define o contrato que deve ser implementado por classes
    responsáveis por formatar datas para exibição.
    
    Examples
    --------
    >>> class BrazilianDateFormatter(DateFormatterInterface):
    ...     def format_date(self, date):
    ...         return date.strftime('%d/%m/%Y')
    """

    @abstractmethod
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
        """
        pass

    @abstractmethod
    def format_date(self, date: datetime) -> str:
        """
        Formata uma data para exibição.
        
        Parameters
        ----------
        date : datetime
            Data a ser formatada
        
        Returns
        -------
        str
            Data formatada
        """
        pass

    @abstractmethod
    def format_datetime(self, date: datetime) -> str:
        """
        Formata uma data/hora para exibição.
        
        Parameters
        ----------
        date : datetime
            Data/hora a ser formatada
        
        Returns
        -------
        str
            Data/hora formatada
        """
        pass
