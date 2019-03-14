#Standard packages
import argparse, json

#Non-standard packages (install via pip)
import requests, base64

#Project package
from grafana import panels

parser = argparse.ArgumentParser(description='Uploads xml to sql database')
parser.add_argument('-grafana.user', action="store", dest="user")
parser.add_argument('-grafana.pwd', action="store", dest="pwd")
parser.add_argument('-grafana.server', action="store", dest="server")
parser.add_argument('-grafana.port', action="store", dest="port")
args = parser.parse_args()

encoded = str(base64.b64encode (bytes(args.user+':'+args.pwd, "utf-8")))
url = 'http://'+args.server+':'+args.port+'/api/dashboards/db'
headers = {'content-type': 'application/json', 'accept': 'application/json', 'authorization' :  'Basic '+ encoded[2:-1]}

#with open('grafana/TestSuites.json') as fp:
#  data = fp.read()

data = {
  "dashboard": {
    "id": None,
    "uid": None,
    "title": "Production Overview",
    #"tags": [ "templated" ],
    "timezone": "browser",
    "schemaVersion": 16,
    "version": 0,
    "panels": [ panels.passrate('passrate') , panels.status('status')]
  },
  "folderId": 0,
  "overwrite": True,
}

response = requests.post(url, data=json.dumps(data), headers=headers)

if response.status_code!=200:
  print('Status:'+str(response.status_code))
  print(response.text)

