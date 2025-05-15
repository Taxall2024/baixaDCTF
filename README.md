# 📥 ECAC DCTF Downloader

Este projeto automatiza a navegação no portal e-CAC da Receita Federal para realizar o download das declarações DCTF (Declaração de Débitos e Créditos Tributários Federais), utilizando o SeleniumBase para automação web e uma API externa para resolução de CAPTCHA.

## ⚙️ Tecnologias Utilizadas

- **Python 3** (versão especificada em `.python-version`)
- **[SeleniumBase](https://github.com/seleniumbase/SeleniumBase)**: automação da navegação no portal e-CAC
- **API externa para CAPTCHA**: integração com serviço de resolução automática
- **AWS S3**: armazenamento dos arquivos baixados
- **Amazon SQS (FIFO Queue)**: recebimento de mensagens contendo CNPJ e nome da empresa
- **PostgreSQL**: conexão com base de dados
- **uv**: gerenciador de pacotes utilizado

## 📁 Organização dos arquivos

- `pyproject.toml`, `uv.lock` e `.python-version`: especificam as dependências e ambiente
- `.env`: arquivo de configuração sensível (não deve ser versionado)
- `downloads/`: pasta onde os arquivos são baixados
- `downloaded_files/`: pasta destino final dos arquivos

## 🧪 Requisitos

- Python 3 instalado
- Instalação das dependências com [uv](https://github.com/astral-sh/uv):

```bash
NUMBER_OF_TRIES=''
AWS_REGION=''
AWS_S3_BUCKET_NAME=''
FOLDER_PATH=''
CAPTCHA_SOLVER_API_KEY=''
DYNAMO_DB_TABLE_NAME=''
DOWNLOADS_PATH=''
CONSUMER_QUEUE=''
DB_CON_DEV=''
DB_CON_PROD=''
```

## 🚀 Como executar
A execução do script principal pode ser feita diretamente via terminal:
Por padrão, o processo realizará os seguintes passos:

Aguardar autenticação manual no e-CAC (30 segundos), caso a seleção automatica do certificado não esteja configurada do contrario basta retirar o '#' do codigo:
```bash
Login.loginEcac()
```

Alterar o perfil da empresa informada (CNPJ).

Navegar até a seção da DCTF.

Baixar os arquivos mês a mês.

Enviar os arquivos para a pasta configurada e/ou para um bucket S3 (se implementado).

Encerrar a sessão com segurança.

🧾 Exemplo de uso
```bash
EcacBaixaAndUploadPerdComps.get_and_upload_perdcomps(
    '17704522000177',
    'HORUS CENTRO MEDICO'
)

```