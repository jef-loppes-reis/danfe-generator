import xml.etree.ElementTree as ET
from datetime import datetime

class DANFEGenerator:
    """
    Gerador de código ZPL para DANFE Simplificado a partir de XML da NFe.
    
    Esta classe extrai informações de um arquivo XML da NFe e gera código ZPL
    no mesmo padrão da etiqueta DANFE existente.
    """
    
    def __init__(self, xml_file_path):
        """
        Inicializa o gerador com o arquivo XML da NFe.
        
        Parameters
        ----------
        xml_file_path : str
            Caminho para o arquivo XML da NFe
        
        Examples
        --------
        >>> generator = DANFEGenerator("nfe.xml")
        >>> zpl_code = generator.generate_zpl()
        """
        self.xml_file_path = xml_file_path
        self.nfe_data = {}
        self._extract_nfe_data()
    
    def _extract_nfe_data(self):
        """
        Extrai dados relevantes do XML da NFe.
        
        Returns
        -------
        None
            Os dados são armazenados em self.nfe_data
        
        Raises
        ------
        FileNotFoundError
            Se o arquivo XML não for encontrado
        ET.ParseError
            Se o XML estiver malformado
        """
        try:
            # Parse do XML
            tree = ET.parse(self.xml_file_path)
            root = tree.getroot()
            
            # Define namespace
            ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
            
            # Extrai dados da identificação
            ide = root.find('.//nfe:ide', ns)
            if ide is None:
                raise ValueError("Elemento 'ide' não encontrado no XML")
            
            numero_elem = ide.find('nfe:nNF', ns)
            serie_elem = ide.find('nfe:serie', ns)
            data_elem = ide.find('nfe:dhEmi', ns)
            
            self.nfe_data['numero'] = numero_elem.text if numero_elem is not None else ""
            self.nfe_data['serie'] = serie_elem.text if serie_elem is not None else ""
            self.nfe_data['data_emissao'] = data_elem.text if data_elem is not None else ""
            
            # Extrai chave de acesso do atributo Id
            inf_nfe = root.find('.//nfe:infNFe', ns)
            if inf_nfe is None:
                raise ValueError("Elemento 'infNFe' não encontrado no XML")
            
            chave_completa = inf_nfe.get('Id', '')
            self.nfe_data['chave_acesso'] = chave_completa.replace('NFe', '') if chave_completa else ""
            
            # Extrai dados do emitente
            emit = root.find('.//nfe:emit', ns)
            if emit is None:
                raise ValueError("Elemento 'emit' não encontrado no XML")
            
            cnpj_emit = emit.find('nfe:CNPJ', ns)
            nome_emit = emit.find('nfe:xNome', ns)
            fantasia_emit = emit.find('nfe:xFant', ns)
            ie_emit = emit.find('nfe:IE', ns)
            uf_emit = emit.find('.//nfe:UF', ns)
            
            self.nfe_data['emit_cnpj'] = cnpj_emit.text if cnpj_emit is not None else ""
            self.nfe_data['emit_nome'] = nome_emit.text if nome_emit is not None else ""
            self.nfe_data['emit_fantasia'] = fantasia_emit.text if fantasia_emit is not None else ""
            self.nfe_data['emit_ie'] = ie_emit.text if ie_emit is not None else ""
            self.nfe_data['emit_uf'] = uf_emit.text if uf_emit is not None else ""
            
            # Extrai dados do destinatário
            dest = root.find('.//nfe:dest', ns)
            if dest is None:
                raise ValueError("Elemento 'dest' não encontrado no XML")
            
            cpf_elem = dest.find('nfe:CPF', ns)
            cnpj_elem = dest.find('nfe:CNPJ', ns)
            nome_dest = dest.find('nfe:xNome', ns)
            uf_dest = dest.find('.//nfe:UF', ns)
            
            self.nfe_data['dest_doc'] = cpf_elem.text if cpf_elem is not None else (cnpj_elem.text if cnpj_elem is not None else "")
            self.nfe_data['dest_tipo_doc'] = 'CPF' if cpf_elem is not None else 'CNPJ'
            self.nfe_data['dest_nome'] = nome_dest.text if nome_dest is not None else ""
            self.nfe_data['dest_uf'] = uf_dest.text if uf_dest is not None else ""
            
            # Extrai protocolo de autorização
            prot = root.find('.//nfe:protNFe/nfe:infProt', ns)
            if prot is not None:
                prot_num = prot.find('nfe:nProt', ns)
                prot_data = prot.find('nfe:dhRecbto', ns)
                self.nfe_data['protocolo'] = prot_num.text if prot_num is not None else ""
                self.nfe_data['data_autorizacao'] = prot_data.text if prot_data is not None else ""
            else:
                self.nfe_data['protocolo'] = ""
                self.nfe_data['data_autorizacao'] = ""
                
        except (ET.ParseError, FileNotFoundError, AttributeError) as e:
            raise ValueError(f"Erro ao processar XML da NFe: {e}") from e
    
    def _format_date(self, iso_date):
        """
        Formata data ISO para formato brasileiro.
        
        Parameters
        ----------
        iso_date : str
            Data no formato ISO (2025-09-01T08:55:05-03:00)
        
        Returns
        -------
        str
            Data formatada (01/09/2025)
        """
        try:
            # Remove timezone e parse
            date_part = iso_date.split('T')[0]
            dt = datetime.strptime(date_part, '%Y-%m-%d')
            return dt.strftime('%d/%m/%Y')
        except (ValueError, AttributeError):
            return iso_date
    
    def _format_datetime(self, iso_datetime):
        """
        Formata data/hora ISO para formato brasileiro.
        
        Parameters
        ----------
        iso_datetime : str
            Data/hora no formato ISO
        
        Returns
        -------
        str
            Data/hora formatada (01/09/2025 08:55:07)
        """
        try:
            # Remove timezone e parse
            datetime_part = iso_datetime.split('-03:00')[0] if '-03:00' in iso_datetime else iso_datetime.split('T')[0]
            if 'T' in datetime_part:
                dt = datetime.strptime(datetime_part, '%Y-%m-%dT%H:%M:%S')
                return dt.strftime('%d/%m/%Y %H:%M:%S')
            else:
                dt = datetime.strptime(datetime_part, '%Y-%m-%d')
                return dt.strftime('%d/%m/%Y')
        except (ValueError, AttributeError):
            return iso_datetime
    
    def _format_cnpj_cpf(self, documento):
        """
        Formata CNPJ ou CPF com máscara.
        
        Parameters
        ----------
        documento : str
            Número do documento sem formatação
        
        Returns
        -------
        str
            Documento formatado
        """
        if len(documento) == 14:  # CNPJ
            return f"{documento[:2]}.{documento[2:5]}.{documento[5:8]}/{documento[8:12]}-{documento[12:14]}"
        elif len(documento) == 11:  # CPF
            return f"{documento[:3]}.{documento[3:6]}.{documento[6:9]}-{documento[9:11]}"
        return documento
    
    def generate_zpl(self):
        """
        Gera código ZPL para DANFE Simplificado.
        
        Returns
        -------
        str
            Código ZPL formatado para impressão da etiqueta DANFE
        
        Examples
        --------
        >>> generator = DANFEGenerator("nfe.xml")
        >>> zpl_code = generator.generate_zpl()
        >>> print(zpl_code)
        """
        # Formata dados para exibição
        data_emissao = self._format_date(self.nfe_data['data_emissao'])
        data_autorizacao = self._format_datetime(self.nfe_data['data_autorizacao'])
        cnpj_formatado = self._format_cnpj_cpf(self.nfe_data['emit_cnpj'])
        
        # Gera código ZPL baseado no padrão da DANFE existente
        zpl_code = f"""^XA
^CI28
^MCY
^FO30,20^GB265,130,3^FS
^FO40,40^A0N,20,20^FD1 - Saida^FS
^FO40,70^A0N,20,20^FH^FDNumero {self.nfe_data['numero']}/Serie {self.nfe_data['serie']}^FS
^FO40,100^A0N,20,20^FH^FDEmissao {data_emissao}^FS
^FO440,40^A0N,30,30^FDChave de acesso^FS
^FO320,70^A0N,20,20^FD{self.nfe_data['chave_acesso']}^FS
^FO340,100^A0N,30,30^FH^FDProtocolo de Autorizacao de uso^FS
^FO395,130^A0N,20,20^FD{self.nfe_data['protocolo']} {data_autorizacao}^FS
^FO135,190^BY2,,0^BCN,150,Y,N,N^FD>;{self.nfe_data['chave_acesso']}^FS
^FO0,355^A0N,25,25^FB675,1,0,R^FD^FS
^FO0,380^GB800,1,3^FS
^FO40,400^A0N,20,20^FH^FDREMETENTE: {self.nfe_data['emit_nome']}^FS
^FO40,430^A0N,20,20^FDCNPJ: {cnpj_formatado}^FS
^FO310,430^A0N,20,20^FH^FDINSCRICAO ESTADUAL: {self.nfe_data['emit_ie']}^FS
^FO690,430^A0N,20,20^FDUF: {self.nfe_data['emit_uf']}^FS
^FO40,500^A0N,20,20^FH^FDDESTINATARIO: {self.nfe_data['dest_nome']}^FS
^FO40,530^A0N,20,20^FD{self.nfe_data['dest_tipo_doc']}: {self._format_cnpj_cpf(self.nfe_data['dest_doc'])}^FS
^FO690,530^A0N,20,20^FDUF: {self.nfe_data['dest_uf']}^FS
^FO40,560^A0N,20,20^FDDANFE SIMPLIFICADO^FS
^FO0,600^GB800,1,3^FS
^FO0,1000^GB800,1,3^FS
^FO40,1020^A0N,25,25^FDDADOS ADICIONAIS^FS
^FO40,1050^A0N,20,20^FB740,8,3,L^FH^FD^FS
^XZ"""
        
        return zpl_code
    
    def save_zpl(self, output_file_param="danfe_generated.zpl"):
        """
        Salva o código ZPL em um arquivo.
        
        Parameters
        ----------
        output_file_param : str, optional
            Nome do arquivo de saída (default: "danfe_generated.zpl")
        
        Returns
        -------
        str
            Caminho do arquivo salvo
        
        Examples
        --------
        >>> generator = DANFEGenerator("nfe.xml")
        >>> file_path = generator.save_zpl("minha_danfe.zpl")
        >>> print(f"DANFE salva em: {file_path}")
        """
        zpl_code = self.generate_zpl()
        
        with open(output_file_param, 'w', encoding='utf-8') as f:
            f.write(zpl_code)
        
        return output_file_param
    
    def print_nfe_info(self):
        """
        Exibe informações extraídas da NFe para debug.
        
        Returns
        -------
        None
        """
        print("=== INFORMAÇÕES DA NFe ===")
        print(f"Número: {self.nfe_data['numero']}")
        print(f"Série: {self.nfe_data['serie']}")
        print(f"Data Emissão: {self._format_date(self.nfe_data['data_emissao'])}")
        print(f"Chave de Acesso: {self.nfe_data['chave_acesso']}")
        print(f"Protocolo: {self.nfe_data['protocolo']}")
        print(f"Emitente: {self.nfe_data['emit_nome']}")
        print(f"CNPJ: {self._format_cnpj_cpf(self.nfe_data['emit_cnpj'])}")
        print(f"Destinatário: {self.nfe_data['dest_nome']}")
        print(f"{self.nfe_data['dest_tipo_doc']}: {self._format_cnpj_cpf(self.nfe_data['dest_doc'])}")

# Exemplo de uso
if __name__ == "__main__":
    try:
        # Cria o gerador com base no XML
        generator = DANFEGenerator("nfe.xml")
        
        # Exibe informações extraídas
        generator.print_nfe_info()
        
        # Gera e salva o código ZPL
        output_file = generator.save_zpl("danfe_from_xml.zpl")
        print(f"\nCódigo ZPL da DANFE gerado e salvo em: {output_file}")
        
        # Exibe o código ZPL gerado
        print("\n=== CÓDIGO ZPL GERADO ===")
        print(generator.generate_zpl())
        
    except (ValueError, FileNotFoundError) as e:
        print(f"Erro: {e}")
