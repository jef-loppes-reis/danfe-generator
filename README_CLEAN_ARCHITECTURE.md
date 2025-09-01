# DANFE Generator - Clean Architecture

Gerador de código ZPL para DANFE Simplificado a partir de XML da NFe seguindo os princípios da Clean Architecture.

## 🏗️ Arquitetura

Este projeto foi refatorado seguindo os princípios da **Clean Architecture**, organizando o código em camadas bem definidas com responsabilidades específicas.

### Estrutura do Projeto

```
src/danfe_generator/
├── domain/                     # Camada de Domínio
│   ├── entities/              # Entidades de negócio
│   │   ├── nfe_data.py       # Dados principais da NFe
│   │   ├── emitente.py       # Dados do emitente
│   │   ├── destinatario.py   # Dados do destinatário
│   │   ├── protocolo.py      # Protocolo de autorização
│   │   └── danfe.py          # DANFE gerado
│   └── interfaces/           # Contratos/Interfaces
│       ├── nfe_parser.py     # Interface para parsers
│       ├── zpl_generator.py  # Interface para geradores ZPL
│       ├── file_writer.py    # Interface para escrita
│       ├── date_formatter.py # Interface para formatação de datas
│       └── document_formatter.py # Interface para formatação de docs
├── use_cases/                 # Camada de Aplicação
│   ├── generate_danfe_from_xml.py # Gerar DANFE do XML
│   └── save_danfe_to_file.py     # Salvar DANFE em arquivo
├── adapters/                  # Camada de Adaptadores
│   ├── parsers/              # Implementações de parsers
│   │   └── xml_nfe_parser.py # Parser de XML da NFe
│   ├── formatters/           # Implementações de formatadores
│   │   ├── brazilian_date_formatter.py    # Formatador de datas BR
│   │   └── brazilian_document_formatter.py # Formatador de docs BR
│   └── generators/           # Implementações de geradores
│       └── standard_zpl_generator.py # Gerador ZPL padrão
├── infrastructure/           # Camada de Infraestrutura
│   └── file_system_writer.py # Escritor de arquivos
└── facade.py                 # Facade principal
```

### Camadas da Arquitetura

#### 1. **Domínio** (Core/Business)
- **Entidades**: Objetos de negócio que encapsulam dados e regras fundamentais
- **Interfaces**: Contratos que definem comportamentos esperados
- **Características**: Independente de frameworks, bancos de dados ou UI

#### 2. **Casos de Uso** (Application)
- Coordenam o fluxo de dados entre as camadas externas e o domínio
- Implementam regras de negócio específicas da aplicação
- Dependem apenas das interfaces do domínio

#### 3. **Adaptadores** (Interface Adapters)
- Convertem dados entre formatos externos e internos
- Implementam as interfaces definidas no domínio
- Fazem a ponte entre casos de uso e infraestrutura

#### 4. **Infraestrutura** (Frameworks & Drivers)
- Implementações concretas de recursos externos
- Sistema de arquivos, APIs, bancos de dados, etc.
- Camada mais externa, pode ser facilmente substituída

## 🚀 Como Usar

### Uso Básico

```python
from src.danfe_generator import DANFEGenerator

# Instancia o gerador com o arquivo XML
generator = DANFEGenerator("nfe.xml")

# Gera o DANFE
danfe = generator.generate_danfe()

# Salva o código ZPL
file_path = generator.save_danfe("minha_danfe.zpl")
print(f"DANFE salva em: {file_path}")

# Exibe informações da NFe
generator.print_nfe_info()
```

### Uso Avançado (Injeção de Dependência)

```python
from src.danfe_generator.use_cases.generate_danfe_from_xml import GenerateDANFEFromXMLUseCase
from src.danfe_generator.adapters.parsers.xml_nfe_parser import XMLNFeParser
from src.danfe_generator.adapters.generators.standard_zpl_generator import StandardZPLGenerator

# Configuração manual das dependências
xml_parser = XMLNFeParser()
zpl_generator = StandardZPLGenerator()

use_case = GenerateDANFEFromXMLUseCase(xml_parser, zpl_generator)
danfe = use_case.execute("nfe.xml")
```

## 🔧 Benefícios da Clean Architecture

### 1. **Testabilidade**
- Cada camada pode ser testada isoladamente
- Fácil criação de mocks para interfaces
- Testes unitários rápidos e confiáveis

### 2. **Flexibilidade**
- Troca de implementações sem afetar o core
- Suporte a múltiplos formatos de entrada/saída
- Extensão facilitada para novos requisitos

### 3. **Manutenibilidade**
- Separação clara de responsabilidades
- Baixo acoplamento entre camadas
- Código mais legível e organizizado

### 4. **Independência**
- Core de negócio independente de frameworks
- Regras de negócio centralizadas
- Facilita migrações tecnológicas

## 📝 Exemplos de Extensão

### Adicionando Novo Parser (JSON)

```python
from src.danfe_generator.domain.interfaces.nfe_parser import NFeParserInterface

class JSONNFeParser(NFeParserInterface):
    def parse(self, source):
        # Implementação para JSON
        pass
```

### Adicionando Novo Gerador (PDF)

```python
from src.danfe_generator.domain.interfaces.zpl_generator import ZPLGeneratorInterface

class PDFGenerator(ZPLGeneratorInterface):
    def generate(self, nfe_data):
        # Implementação para PDF
        pass
```

## 📋 Comparação: Antes vs Depois

| Aspecto | Antes (Monolítico) | Depois (Clean Architecture) |
|---------|-------------------|----------------------------|
| **Estrutura** | Uma classe com tudo | Camadas separadas por responsabilidade |
| **Testabilidade** | Difícil de testar | Fácil teste de unidade por camada |
| **Extensibilidade** | Modificações complexas | Extensões simples via interfaces |
| **Reutilização** | Baixa | Alta (componentes independentes) |
| **Manutenção** | Complexa | Simples e localizada |
| **Acoplamento** | Alto | Baixo |

## 🎯 Princípios Aplicados

- **Single Responsibility Principle**: Cada classe tem uma responsabilidade
- **Open/Closed Principle**: Aberto para extensão, fechado para modificação
- **Liskov Substitution Principle**: Substituição de implementações
- **Interface Segregation Principle**: Interfaces específicas e coesas
- **Dependency Inversion Principle**: Dependência de abstrações, não de concretizações

## 🧪 Executando

```bash
# Versão com Clean Architecture
python projeto_principal_clean.py

# Versão original (para comparação)
python projeto_principal.py
```

## 📖 Documentação Adicional

Cada módulo possui documentação detalhada no estilo NumPy, incluindo:
- Descrição da funcionalidade
- Parâmetros com tipos e descrições
- Valores de retorno
- Exemplos de uso
- Exceções que podem ser lançadas

Esta organização garante que o código seja maintível, testável e extensível, seguindo as melhores práticas da engenharia de software moderna.
