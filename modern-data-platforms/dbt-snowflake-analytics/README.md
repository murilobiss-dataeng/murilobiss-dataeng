# dbt_snow_demo

## Descrição do Projeto

Este projeto é uma demonstração de como usar o [dbt (data build tool)](https://www.getdbt.com/) com o Snowflake para transformar dados em um ambiente de Data Engineering. O objetivo deste projeto é ilustrar as melhores práticas de modelagem de dados, transformação e documentação usando dbt.

## Estrutura do Projeto

O projeto segue a estrutura recomendada pelo dbt e contém os seguintes diretórios e arquivos:


dbt_snow_demo/
├── analyses/            # Análises SQL não incluídas em modelos 
├── data_sources/        # Fonte de dados utilizadas 
├── dbt_project.yml      # Configurações do projeto dbt 
├── macros/              # Macros personalizadas do dbt 
├── models/              # Modelos dbt (tabelas e views) 
│   ├── staging/         # Modelos de staging 
│   ├── marts/           # Modelos de dados finais 
│   └── intermediate/     # Modelos intermediários
├── seeds/               # Dados de entrada em formato CSV 
├── snapshots/           # Snapshots para capturar o estado dos dados 
├── tests/               # Testes para validar modelos 
└── profiles.yml         # Configurações do perfil de conexão


## Requisitos

Antes de começar, certifique-se de ter os seguintes pré-requisitos instalados:

- [Python](https://www.python.org/downloads/) (versão 3.7 ou superior)
- [dbt](https://docs.getdbt.com/dbt-cli/installation) (versão compatível com o Snowflake)
- Acesso a uma conta do Snowflake

## Configuração

1. Clone o repositório:

   ```bash
   git clone https://github.com/murilobiss/dbt_snow_demo.git
