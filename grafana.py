#Standard packages
import argparse,json

#Non-standard packages (install via pip)
import requests

parser = argparse.ArgumentParser(description='Uploads xml to sql database')
parser.add_argument('-grafana.authentication', action="store", dest="authentication")
parser.add_argument('-grafana.server', action="store", dest="server")
parser.add_argument('-grafana.port', action="store", dest="port")
args = parser.parse_args()

url = 'http://'+args.server+':'+args.port+'/api/dashboards/db'
headers = {'content-type': 'application/json', 'accept': 'application/json', 'authorization' :  'Basic YWRtaW46YWRtaW4='}

with open('grafana/TestSuites.json') as fp:
  v = fp.read()

print(v)

data = {
  "dashboard": {
    "id": None,
    "uid": None,
    "title": "Production Overview",
    #"tags": [ "templated" ],
    "timezone": "browser",
    "schemaVersion": 16,
    "version": 0
  },
  "folderId": 0,
  "overwrite": True
}

response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.status_code)
print(response.text)

#POST /api/dashboards/db HTTP/1.1
#Accept: application/json
#Content-Type: application/json
#Authorization: Bearer eyJrIjoiT0tTcG1pUlY2RnVKZTFVaDFsNFZXdE9ZWmNrMkZYbk

