<!--
title: 'AWS Simple HTTP Endpoint example in Python'
description: 'This template demonstrates how to make a simple HTTP API with Python running on AWS Lambda and API Gateway using the Serverless Framework.'
layout: Doc
framework: v4
platform: AWS
language: python
authorLink: 'https://github.com/serverless'
authorName: 'Serverless, Inc.'
authorAvatar: 'https://avatars1.githubusercontent.com/u/13742415?s=200&v=4'
-->

# Order Integration com Serverless Framework Python

Projeto para integrar dados de pedidos entre um ERP e um CRM utilizando AWS Lambda e S3 com Serverless Framework.


## Pré-requisitos
- [x] Serverless Framework


### Configurando o projeto

Clone o projeto Order Integration

```
$ cd pasta/onde/vc/guarda/seus/projetos
$ git https://github.com/evaristofm/order-integration.git

```

Adaptando o projeto:
- [] Vá no arquivo order-integration/serverless.yml
- [] Em Resource mude o ARN do bucket s3 para um endereço de bucket existente na aws Resource: "arn:aws:s3:::{seu-bucket-name}/*"
- [] Vá para order-integration/handler.py
- [] Altera a variavel S3_BUCKET = '{seu-bucket-name}' definindo o nome do seu bucket


Realizando o deploy do projeto

- [] Dentro da pasta order-integration/order-integration
- [] Execute o comando serverless deploy

```
serverless deploy

```
No final da execução sera fornecido o endpoint da Api Gateway e
será mostrado as funções lambdas que foram criadas na aws.

![deploy_lambdas](https://github.com/evaristofm/api-brasilprev/assets/46290279/9b4beec1-e421-45e6-a3c0-ed8c87cabecd)


### Invocando endpoint

Depois de realizar o deploy, você pode criar uma requisisão via HTTP
fornecendo como parametro o arquivo 'erp_data.json', para os dados serem transformados
em um bucket S3 

![postman_endpoint](https://github.com/evaristofm/api-brasilprev/assets/46290279/d75bb0d6-9329-4226-903d-701bd8b84e01)


Confira no seu Bucket se existe um arquivo chamado 'new_erp_data.json'

![bucket](https://github.com/evaristofm/api-brasilprev/assets/46290279/b98fe211-e090-4bd8-9fbe-394db0ab3bff)


A partir desse arquivo sera gerado um novo arquivo chamado 'crm_swagger.json',
onde o lambda 'crm_handler' a cada 10 min será responsável em ler o 'new_erp_data.json'
e gerar/atualizar o arquivo 'crm_swagger.json'.

![bucket_crm_swagger](https://github.com/evaristofm/api-brasilprev/assets/46290279/2abb5530-9b0b-47e8-af5c-3bbac8f9a1f2)


