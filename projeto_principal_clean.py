"""
Exemplo de uso do gerador de DANFE com Clean Architecture.

Este arquivo demonstra como usar o novo sistema organizados em
camadas seguindo os princípios da Clean Architecture.
"""

from src.danfe_generator import DANFEGenerator


def main():
    """
    Exemplo principal de uso do gerador de DANFE.
    
    Este exemplo demonstra como usar a nova estrutura para gerar
    uma DANFE a partir de um arquivo XML da NFe.
    """
    try:
        # Cria o gerador com base no XML
        generator = DANFEGenerator("nfe.xml")

        # Exibe informações extraídas
        generator.print_nfe_info()

        # Gera e salva o código ZPL
        output_file = generator.save_danfe("danfe_from_xml_clean.zpl")
        print(f"\nCódigo ZPL da DANFE gerado e salvo em: {output_file}")

        # Exibe o código ZPL gerado
        print("\n=== CÓDIGO ZPL GERADO ===")
        print(generator.get_zpl_code())

        # Também é possível acessar o objeto DANFE diretamente
        danfe = generator.danfe
        if danfe:
            print("\n=== RESUMO ===")
            print(danfe.get_info_summary())

    except (ValueError, FileNotFoundError) as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()
