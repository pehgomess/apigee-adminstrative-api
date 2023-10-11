#!/usr/bin/env python3
"""
Nome do Script: get-customAttributes-uniqueApp.py
Autor: Pedro Gomes  <pehgomess@gmail.com>
Data de Criação: out/2023
Descrição: Mostra todos os attributo de um especifico Apps do apigee
"""

import argparse
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

parser = argparse.ArgumentParser(description="Obtém todos os Custom Attributes de um Apps Apigee.")
parser.add_argument("--service-account-env", required=True, help="Variável de ambiente com as informações do service Account.")
parser.add_argument("--org", required=True, help="Nome da organização Apigee.")
parser.add_argument("--app-name", required=True, help="Nome do aplicativo Apigee.")
parser.add_argument("--developer-email", required=True, help="Endereço de e-mail do desenvolvedor.")

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

org = args.org
app_name = args.app_name
developer_email = args.developer_email

app_details = apigee_service.organizations().developers().apps().get(
    name=f'organizations/{org}/developers/{developer_email}/apps/{app_name}'
).execute()

if 'attributes' in app_details:
    print("Custom Attributes do aplicativo:")
    for attribute in app_details['attributes']:
        attribute_name = attribute['name']
        attribute_value = attribute['value']
        print(f"Nome: {attribute_name}, Valor: {attribute_value}")
else:
    print("O aplicativo não possui Custom Attributes.")
