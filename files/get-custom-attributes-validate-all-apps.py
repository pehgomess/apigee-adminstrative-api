import json
import argparse
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

def check_custom_attribute(app, attribute_name):
    if 'attributes' in app:
        custom_attributes = app['attributes']
        if attribute_name in custom_attributes:
            return True
    return False

def get_apps_by_developer(apigee_service, organization, developer_email, attribute_name):
    count = 100
    startKey = None
    while True:
        response = apigee_service.organizations().developers().apps().list(
            parent=f'organizations/{organization}/developers/{developer_email}',
            startKey=startKey,
            count=count
        ).execute()

        if 'app' not in response:
            break

        apps = response['app']
        attribute_found = False

        for app in apps:
            app_id = app['appId']
            app_details = apigee_service.organizations().developers().apps().get(
                name=f'organizations/{organization}/developers/{developer_email}/apps/{app_id}'
            ).execute()

            if 'attributes' in app_details:
                for attribute in app_details['attributes']:
                    if attribute['name'] == attribute_name:
                        attribute_value = attribute['value']
                        print(f'O atributo personalizado "{attribute_name}" está definido no aplicativo "{app_id}" do desenvolvedor "{developer_email}". Valor: {attribute_value}')
                        attribute_found = True
                        continue

                #print(f'O atributo personalizado "{attribute_name}" NÃO está definido no aplicativo "{app_id}" do desenvolvedor "{developer_email}".')
        if not attribute_found:
            print(f'O atributo personalizado "{attribute_name}" NÃO está definido no aplicativo "{app_id}" do desenvolvedor "{developer_email}".')

        if len(apps) == count:
            # Se o número de aplicativos obtidos for igual a count, aumente count para um valor maior
            count *= 2
        else:
            # Caso contrário, defina startKey como o nome do último aplicativo obtido na chamada anterior
            last_app = apps[-1]
            startKey = last_app['appId']

        if 'next' not in response:
            break


def main():
    parser = argparse.ArgumentParser(description="Verifica Custom Attributes de um Apps no Apigee.")
    parser.add_argument("--service-account-env", required=True, help="Variável de ambiente com as informações do service Account.")
    parser.add_argument("--org", required=True, help="Organização Apigee")
    parser.add_argument("--attribute-name", required=True, help="Nome do Custom Attributes a verificar")
    args = parser.parse_args()

    apigee_org = args.org
    attribute_name_to_check = args.attribute_name

    auth = os.environ.get(args.service_account_env)

    if not auth:
        raise ValueError(f'A variável de ambiente {auth} não foi definida.')

    credentials_info = json.loads(auth)

    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )

    apigee_service = build('apigee', 'v1', credentials=credentials)

    developers = apigee_service.organizations().developers().list(
        parent=f'organizations/{apigee_org}'
    ).execute()

    for developer in developers.get('developer', []):
        developer_email = developer["email"]
        get_apps_by_developer(apigee_service, apigee_org, developer_email, attribute_name_to_check)

if __name__ == "__main__":
    main()
