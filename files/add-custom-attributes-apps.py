#!/usr/bin/env python3
"""
Nome do Script: add-CustomAttributes-apps.py
Autor: Pedro Gomes  <pehgomess@gmail.com>
Data de Criação: out/2023
Descrição: Adiciona um custom attributes no Apps do apigee
"""

import argparse
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

parser = argparse.ArgumentParser(description="Atualiza ou cria Custom Attributes em um Apps do Apigee.")
parser.add_argument("--service-account-env", required=True, help="Variável de ambiente com as informações do service Account.")
parser.add_argument("--app-name", required=True, help="Nome do App do Apigee.")
parser.add_argument("--org", required=True, help="Organization Apigee")
parser.add_argument("--developer-email", required=True, help="Endereço de e-mail do developer.")
parser.add_argument("--attribute-name", required=True, help="Nome do Custom Attribute a ser atualizado/criado.")
parser.add_argument("--attribute-value", required=True, help="Valor do Custom Attributes")

args = parser.parse_args()

service_account_info = os.environ.get(args.service_account_env)

if not service_account_info:
    raise ValueError("As informações da conta de serviço não foram fornecidas nas variáveis de ambiente.")

credentials_info = json.loads(service_account_info)

credentials = service_account.Credentials.from_service_account_info(
    credentials_info,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# credentials = service_account.Credentials.from_service_account_file(
#     args.service_account_file,
#     scopes=['https://www.googleapis.com/auth/cloud-platform']
# )

apigee_service = build('apigee', 'v1', credentials=credentials)

app_name = args.app_name
org = args.org
developer_email = args.developer_email

app_details = apigee_service.organizations().developers().apps().get(
    name=f'organizations/{org}/developers/{developer_email}/apps/{app_name}'
).execute()

new_attribute = {
    'name': args.attribute_name,
    'value': args.attribute_value
}

if 'attributes' not in app_details:
    app_details['attributes'] = []

attribute_exists = False
for attribute in app_details['attributes']:
    if attribute['name'] == new_attribute['name']:
        attribute['value'] = new_attribute['value']
        attribute_exists = True
        break

if not attribute_exists:
    app_details['attributes'].append(new_attribute)

response = apigee_service.organizations().developers().apps().update(
    name=f'organizations/{org}/developers/{developer_email}/apps/{app_name}',
    body=app_details
).execute()

print(f'Custom Attributes: "{new_attribute["name"]}" atualizado/criado com sucesso no App: "{app_name}".')


#python seu_script.py --service-account-file caminho/para/arquivo-de-credenciais.json --app-name acesoftware --org dock-apigee-nonprod --developer-email acesoftware@dock.tech --attribute-name cloud --attribute-value cloud2
