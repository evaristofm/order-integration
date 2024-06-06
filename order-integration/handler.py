import re
import json
import boto3
from datetime import datetime, date


s3_client = boto3.client("s3")
S3_BUCKET = 'seu-bucket-name'

def transforma_dados(dados):
    pedido_final = []
    for pedido in dados:
        pedido_final.append({
                "id": pedido['id'],
                "valor": float(pedido['valor']),
                "data": datetime.strptime(pedido['data'], '%d/%m/%Y'),
                "frete": float(pedido['frete']),
                "desconto": int(re.sub(r'[^0-9]', '', pedido['desconto'])) if isinstance(pedido['desconto'], str) else None,
                "status": pedido['status']
        })
    return pedido_final
            
def json_serial(obj):
        """JSON serializador para objetos de data não serializaveis por padrão para json"""

        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError ("Type %s not serializable" % type(obj))


def erp_handler(event, context):

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

    return {'statusCode': 200}


def crm_handler(event, context):
    """Ler arquivo com os dados transformados no s3"""
    
    object_key = 'new_erp_data' + '.json'

    file_content = json.loads(s3_client.get_object(
        Bucket=S3_BUCKET, Key=object_key)['Body'].read())
    
    print(file_content)

    """Envio dos dados para s3 com o arquivo crm_swagger.json"""
    filename = 'crm_swagger' + '.json'

    uploadByteStream = bytes(json.dumps(
        file_content,
        indent=4,
        default=str).encode('UTF-8'))

    s3_client.put_object(Bucket=S3_BUCKET, Key=filename, Body=uploadByteStream)

    return {'statusCode': 200}