import re
import json
import boto3
import requests
import logging
from datetime import datetime, date


S3_BUCKET = '{seu-bucket-name}'

s3_client = boto3.client("s3")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def transforma_dados(dados):
    pedido_final = []
    for pedido in dados:
        pedido_final.append({
                "id": pedido['id'],
                "origem": "nome_ferramenta",
                "valor": float(pedido['valor']),
                "data_fato": datetime.strptime(pedido['data'], '%d/%m/%Y').strftime("%Y-%m-%d"),
                "frete": float(pedido['frete']),
                "desconto": int(re.sub(r'[^0-9]', '', pedido['desconto'])) if isinstance(pedido['desconto'], str) else None,
                "status": 'finalizado' if pedido['status'] in ('finished', 'in progress') else pedido['status']
        })
    return pedido_final
            
def json_serial(obj):
        """JSON serializador para objetos de data não serializaveis por padrão para json"""

        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError ("Type %s not serializable" % type(obj))


def erp_handler(event, context):

    try:
        body = event.get('body')
        body_pedidos_dict = json.loads(body)

        pedidos = transforma_dados(body_pedidos_dict)
        #TODO: Pesquisar o erro de runtime ao utilizar a dunção map para transformar os dados. https://docs.aws.amazon.com/lambda/latest/dg/runtimes-update.html

        filename = 'new_erp_data' + '.json'
        uploadByteStream = bytes(json.dumps(
            pedidos,
            indent=4,
            default=json_serial).encode('UTF-8'))

        s3_client.put_object(Bucket=S3_BUCKET, Key=filename, Body=uploadByteStream)

        print(pedidos)

        return {
             "statusCode": 200,
             "body": json.dumps("Dados processados e armazenados com sucesso no S3")
            }

    except Exception as e:
        logger.error(f"Error ao processar ERP data: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps("Internal Server Error")
        }
    

def crm_handler(event, context):
    """Ler arquivo com os dados transformados no s3"""
    try:
         
        object_key = 'new_erp_data' + '.json'

        file_content = json.loads(s3_client.get_object(
            Bucket=S3_BUCKET, Key=object_key)['Body'].read())
        
        print("FILE CONTENT", file_content)

        """Envio dos dados para o CRM"""
        url = "http://httpbin.org/post"
        payload = json.dumps(file_content)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        print("Retorno do CRM", response.json())

        return {
            "statusCode": 200,
             "body": json.dumps("Dados enviados com sucesso para CRM")
        }
    
    except Exception as e:
        logger.error(f"Error ao processar CRM data: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps("Internal Server Error")
        }