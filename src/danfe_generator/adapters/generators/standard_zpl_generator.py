"""
Gerador padrão de código ZPL.

Este módulo implementa o gerador de código ZPL para DANFE
seguindo o layout padrão estabelecido.
"""

from ...domain.entities.nfe_data import NFeData
from ...domain.entities.danfe import DANFE
from ...domain.interfaces.zpl_generator import ZPLGeneratorInterface
from ..formatters.brazilian_date_formatter import BrazilianDateFormatter
from ..formatters.brazilian_document_formatter import BrazilianDocumentFormatter


class StandardZPLGeneratorConfig:
    """
    Configuração para o gerador padrão de código ZPL.
    """
    cpf_dest: bool = False


class StandardZPLGenerator(ZPLGeneratorInterface):
    """
    Gerador padrão de código ZPL para DANFE.
    
    Implementa a interface ZPLGeneratorInterface para gerar
    código ZPL seguindo o layout padrão da DANFE Simplificada.
    
    Examples
    --------
    >>> generator = StandardZPLGenerator()
    >>> danfe = generator.generate(nfe_data)
    >>> print(danfe.codigo_zpl[:10])
    ^XA^CI28^MCY
    """

    def __init__(self):
        """Inicializa o gerador com formatadores padrão."""
        self._date_formatter = BrazilianDateFormatter()
        self._doc_formatter = BrazilianDocumentFormatter()
        self.config = StandardZPLGeneratorConfig()

    def generate(self, nfe_data: NFeData) -> DANFE:
        """
        Gera código ZPL a partir dos dados da NFe.
        
        Parameters
        ----------
        nfe_data : NFeData
            Dados da NFe para geração do DANFE
        
        Returns
        -------
        DANFE
            Objeto DANFE com código ZPL gerado
        
        Raises
        ------
        ValueError
            Se os dados da NFe não forem válidos para geração
        
        Examples
        --------
        >>> generator = StandardZPLGenerator()
        >>> danfe = generator.generate(nfe_data)
        >>> print(danfe.get_info_summary())
        NFe 123/1 - Emitente: Empresa LTDA - Destinatário: João Silva
        """
        if not isinstance(nfe_data, NFeData):
            raise ValueError("nfe_data deve ser uma instância de NFeData")

        # Formata dados para exibição
        data_emissao = self._date_formatter.format_date(nfe_data.data_emissao)
        cnpj_formatado = self._doc_formatter.format_cnpj(nfe_data.emitente.cnpj)
        doc_dest_formatado = self._doc_formatter.format_document(nfe_data.destinatario.documento) if self.config.cpf_dest else '-'

        # Formata protocolo se existir
        protocolo_info = ""
        if nfe_data.protocolo:
            data_autorizacao = self._date_formatter.format_datetime(nfe_data.protocolo.data_autorizacao)
            protocolo_info = f"{nfe_data.protocolo.numero} {data_autorizacao}"

        # Gera código ZPL baseado no padrão estabelecido
        zpl_code = f"""^XA
^CI28
^MCY
^FO30,20^GB265,130,3^FS
^FO40,40^A0N,20,20^FD1 - Saida^FS
^FO40,70^A0N,20,20^FH^FDNumero {nfe_data.numero}/Serie {nfe_data.serie}^FS
^FO40,100^A0N,20,20^FH^FDEmissao {data_emissao}^FS
^FO440,40^A0N,30,30^FDChave de acesso^FS
^FO320,70^A0N,20,20^FD{nfe_data.chave_acesso}^FS
^FO340,100^A0N,30,30^FH^FDProtocolo de Autorizacao de uso^FS
^FO395,130^A0N,20,20^FD{protocolo_info}^FS
^FO135,190^BY2,,0^BCN,150,Y,N,N^FD>;{nfe_data.chave_acesso}^FS
^FO0,355^A0N,25,25^FB675,1,0,R^FD^FS
^FO0,380^GB800,1,3^FS
^FO40,400^A0N,20,20^FH^FDREMETENTE: {nfe_data.emitente.nome}^FS
^FO40,430^A0N,20,20^FDCNPJ: {cnpj_formatado}^FS
^FO310,430^A0N,20,20^FH^FDINSCRICAO ESTADUAL: {nfe_data.emitente.inscricao_estadual}^FS
^FO690,430^A0N,20,20^FDUF: {nfe_data.emitente.uf}^FS
^FO40,500^A0N,20,20^FH^FDDESTINATARIO: {nfe_data.destinatario.nome}^FS
^FO40,530^A0N,20,20^FD{nfe_data.destinatario.tipo_documento.value}: {doc_dest_formatado}^FS
^FO690,530^A0N,20,20^FDUF: {nfe_data.destinatario.uf}^FS
^FO40,560^A0N,20,20^FDDANFE SIMPLIFICADO^FS
^FO0,600^GB800,1,3^FS
^FO0,1000^GB800,1,3^FS
^FO40,1020^A0N,25,25^FDDADOS ADICIONAIS^FS
^FO40,1050^A0N,20,20^FB740,8,3,L^FH^FD^FS
^XZ"""

        return DANFE(nfe_data=nfe_data, codigo_zpl=zpl_code)
