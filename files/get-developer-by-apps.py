#!/usr/bin/env python3
"""
Nome do Script: get-developer-by-apps.py
Autor: Pedro Gomes  <pehgomess@gmail.com>
Data de Criação: set/2023
Descrição: Mostra o nome do developers de um app especifico
"""

import argparse
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

parser = argparse.ArgumentParser(description="Pesquisa o developer do Apigee pelo Apps e Organization.")
parser.add_argument("--service-account-env", required=True, help="Variável de ambiente com as informações do service Account.")
parser.add_argument("--org", required=True, help="Organization Apigee.")
parser.add_argument("--app-name", required=True, help="Nome do App do Apigee.")

args = parser.parse_args()

service_account_info = os.environ.get(args.service_account_env)

if not service_account_info:
    raise ValueError("As informações da conta de serviço não foram fornecidas nas variáveis de ambiente.")

credentials_info = json.loads(service_account_info)

credentials = service_account.Credentials.from_service_account_info(
    credentials_info,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

apigee_service = build('apigee', 'v1', credentials=credentials)

org = args.org
app_name = args.app_name

developers = apigee_service.organizations().developers().list(
    parent=f'organizations/{org}'
).execute()

developer_found = None

for developer in developers.get('developer', []):
    apps = apigee_service.organizations().developers().apps().list(
        parent=f'organizations/{org}/developers/{developer["email"]}'
    ).execute()
    for app in apps.get('app', []):
        if app['appId'] == app_name:
            developer_found = developer
            break

if developer_found:
    print(f'{developer_found["email"]}')
else:
    print(f'Nenhum desenvolvedor encontrado para o App {app_name}.')
