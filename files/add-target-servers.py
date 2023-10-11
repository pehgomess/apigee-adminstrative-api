#!/usr/bin/env python3
"""
Nome do Script: add-target-servers.py
Autor: Pedro Gomes  <pehgomess@gmail.com>
Data de Criação: out/2023
Descrição: Cadastra novos target servers no apigee
"""

import argparse
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

def create_target_server(apigee_org, apigee_env, target_server_name, target_server_host, target_server_port, service_account_info):

    if not service_account_info:
        raise ValueError("As informações da conta de serviço não foram fornecidas nas variáveis de ambiente.")

    credentials_info = json.loads(service_account_info)

    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )

    apigee_service = build('apigee', 'v1', credentials=credentials)

    target_server_data = {
        "name": target_server_name,
        "host": target_server_host,
        "port": target_server_port,
        "isEnabled": True,
        "sSLInfo": { 
            "enabled": True,
        },
        "protocol": "HTTP"

    }

    response = apigee_service.organizations().environments().targetservers().create(
        parent=f'organizations/{apigee_org}/environments/{apigee_env}',
        body=target_server_data
    ).execute()

    print(f'Success: Target Server "{response["name"]}" created.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cria um Target Server no Apigee.")
    parser.add_argument("--service-account-env", required=True, help="Variável de ambiente com as informações do service Account.")
    parser.add_argument("--org", required=True, help="Nome da organização Apigee.")
    parser.add_argument("--env", required=True, help="Nome do ambiente Apigee. Ex: prd, dev, qa, hml")
    parser.add_argument("--name", required=True, help="Nome do Target Server.")
    parser.add_argument("--host", required=True, help="Host do Target Server.")
    parser.add_argument("--port", required=True, help="Port do Target Server")

    args = parser.parse_args()

    apigee_org = args.org
    apigee_env = args.env
    target_server_name = args.name
    target_server_host = args.host
    target_server_port = args.port
    service_account_info = os.environ.get(args.service_account_env)



    create_target_server(apigee_org, apigee_env, target_server_name, target_server_host, target_server_port, service_account_info)
