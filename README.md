# Automação Apigee X

Repositorio com os codigos **"playbook"** ansible **(AWX)** para consumir os recursos da API do Apigee X
A playbook faz referencias aos scripts contidos no diretorio files.
<br>

## Diretorio files

- [`add-access-control-ip-list.py`](files/add-access-control-ip-list.py): <tr>
*Este script tem como objetivo efetuar o cadastro de um ou mais IPs mantendo o atual e não deixando duplicidade, tambem pode adicionar o CIDR como no exemplo, **sempre separando por virgula em caso de mais de um CIDR ou IP**.* ```Ex: python3 add-access-control-ip-list.py --org dock-apigee-nonprod --app-name acesoftware --developer-email acesoftware@dock.tech --service-account-env service_account_nonprod_apigee --ips-to-add "150.10.10.0/24,151.10.1.0/18,190.190.190.190"```
<br>

- [`add-custom-attributes-apps.py`](files/add-custom-attributes-apps.py): <tr> 
*Esse script adiciona um novo atributo customizado no Apps, **caso exista ele sobrescreve a chave com o valor passado no parametro**.* ```Ex: python3 add-custom-attributes-apps.py --org dock-apigee-nonprod --app-name acesoftware --developer-email acesoftware@dock.tech --service-account-env service_account_nonprod_apigee --attribute-name novoatt --attribute-value valueatt```
<br>

- [`get-access-control-ip-list.py`](files/get-access-control-ip-list.py): <tr>
*Este faz um get no app passado no parametro e tras apenas os IPs da chave access-control-ip-list.* ```Ex: python3 get-access-control-ip-list.py --org dock-apigee-nonprod --app-name acesoftware --developer-email acesoftware@dock.tech --service-account-env service_account_nonprod_apigee```
<br>

- [`get-custom-attributes-uniq-app.py`](files/get-custom-attributes-uniq-app.py): <tr>
*Mostra todos os custom attributes de um unico app.* ```Ex: python3 get-developer-by-apps.py --org dock-apigee-nonprod --app-name acesoftware --developer-email acesoftware@dock.tech --service-account-env service_account_nonprod_apigee```
<br>

- [`get-developer-by-apps.py`](files/get-developer-by-apps.py): <tr>
*Mostra o nome do developer pelo App.* ```Ex: python3 get-developer-by-apps.py --org dock-apigee-nonprod --app-name acesoftware --service-account-env service_account_nonprod_apigee```
<br>

---

## Info para execução local dos scripts

Para conseguir consumir o script é necessario utilizar o usuario de servico da GCP, geralmente baixando o arquivo de json do usuario de servico e atribuino o mesmo como uma variavel de ambiente, um dos parametros de todos os scripts ```--service-account-env``` passando o nome da variavel.
Um exemplo de como gerar essa variavel de ambiente pelo arquivo.

```bash
cat files/credentials-file.json | jq -c .
```

Para utilizar tambem pode se fazer desta forma 

```bash
#fish
export service_account_nonprod_apigee=(cat credentials-file.json | jq -c .)
```
---

## Arquivo de playbook 

- [`consume-apigee-add-custom-attributes.yml`](consume-apigee-add-custom-attributes.yml): <tr>
*Faz uso dos scripts get-developer-by-apps.py e add-custom-attributes-apps.py para gerar o atributo usando a interface do AWX*
<br>

- [`consume-apigee-add-attribute-access-control-ip-list.yml`](consume-apigee-add-attribute-access-control-ip-list.yml): <tr>
*Faz uso dos scripts get-developer-by-apps.py e add-access-control-ip-list.py exclusivo para criar o atributo access-control-ip-list para gerar o atributo de IPs/CIDR usando a interface do AWX*
<br>

>**Nota**: *Abaixo algumas opções ainda em analise para o desenvolvimento.*

- [`consume-apigee-get-access-control-ip-list.yml`](consume-apigee-get-access-control-ip-list.yml): <tr>
*Faz uso dos scripts get-developer-by-apps.py e get-access-control-ip-list.py exclusivo parar gerar as informações de get do access-control-ip-list do app*
<br>

- [`consume-apigee-get-custom-attributes-uniq-app.yml`](consume-apigee-get-custom-attributes-uniq-app.yml): <tr>
*Faz uso dos scripts get-developer-by-apps.py e get-custom-attributes-uniq-app.py gera o valor de todos os atributos de um app especifico*
<br>

---

