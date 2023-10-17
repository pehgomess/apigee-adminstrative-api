#!/usr/bin/env python3
"""
Nome do Script: add-access-control-ip-list.py
Autor: Pedro Gomes <pehgomess@gmail.com>
Data de Criação: out/2023
Descrição: Atualiza o atributo custom attributes "access-control-ip-list", ele mantem a lista e adiciona novos IPS e caso adicione um repetido ele nao deixa replicar 
"""

import argparse
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

parser = argparse.ArgumentParser(description="Atualiza o Custom Attribute 'access-control-ip-list' de um Apps Apigee.")
parser.add_argument("--service-account-env", required=True, help="Variável de ambiente com as informações do service Account.")
parser.add_argument("--org", required=True, help="Nome da organização Apigee.")
parser.add_argument("--app-name", required=True, help="Nome do aplicativo Apigee.")
parser.add_argument("--developer-email", required=True, help="Endereço de e-mail do desenvolvedor.")
parser.add_argument("--ips-to-add", required=True, help="IPs a serem adicionados à lista access-control-ip-list ou CIDR, um ou mais, se houver mais de 1 separados por vírgula. Ex: --ips-to-add \"150.10.10.0/24,151.10.1.0/18,190.190.190.190\"")

args = parser.parse_args()

service_account_info = os.environ.get(args.service_account_env)

if not service_account_info:
    raise ValueError("As informações da service account não foram fornecidas nas variáveis de ambiente.")

credentials_info = json.loads(service_account_info)

credentials = service_account.Credentials.from_service_account_info(
    credentials_info,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# usando arquivo
# credentials = service_account.Credentials.from_service_account_file(
#     args.service_account_file,
#     scopes=['https://www.googleapis.com/auth/cloud-platform']
# )

apigee_service = build('apigee', 'v1', credentials=credentials)

org = args.org
app_name = args.app_name
developer_email = args.developer_email
ips_to_add = args.ips_to_add.split(',') 

app_details = apigee_service.organizations().developers().apps().get(
    name=f'organizations/{org}/developers/{developer_email}/apps/{app_name}'
).execute()

if 'attributes' in app_details:
    for attribute in app_details['attributes']:
        if attribute['name'] == 'access-control-ip-list':
            current_ip_list = attribute['value'].split(',')
            
            current_ip_list = list(set(current_ip_list))
            
            added_ips = [] 
            duplicate_ips = [] 
            
            for ip in ips_to_add:
                if ip.strip() not in current_ip_list:
                    added_ips.append(ip.strip())
                else:
                    duplicate_ips.append(ip.strip())
            
            current_ip_list.extend(added_ips)
            
            updated_attribute_value = ','.join(current_ip_list)

            attribute['value'] = updated_attribute_value

            response = apigee_service.organizations().developers().apps().update(
                name=f'organizations/{org}/developers/{developer_email}/apps/{app_name}',
                body=app_details
            ).execute()

            if added_ips:
                print(f"IPs adicionados à lista access-control-ip-list: {', '.join(added_ips)}")
            else:
                print("Nenhum IP novo adicionado à lista access-control-ip-list.")
            
            if duplicate_ips:
                print(f"IPs que já estão na lista access-control-ip-list: {', '.join(duplicate_ips)}")
            else:
                print("Nenhum IP duplicado encontrado.")
            
            print(f"IPs atuais na lista access-control-ip-list: {', '.join(current_ip_list)}")
                
            break
    else:
        print("O App não possui um Custom Attribute 'access-control-ip-list'.")
else:
    print("O App não possui Custom Attributes.")
