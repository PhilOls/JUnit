#Standard packages
import argparse, json

#Non-standard packages (install via pip)
import requests, base64

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
  "panels": [
    {
      "cacheTimeout": None,
      "datasource": "MySQL",
      "gridPos": {
        "h": 6,
        "w": 8,
        "x": 0,
        "y": 0
      },
      "id": 4,
      "links": [],
      "options": {
        "maxValue": 100,
        "minValue": 0,
        "showThresholdLabels": False,
        "showThresholdMarkers": True,
        "thresholds": [
          {
            "color": "#F2495C",
            "index": 0,
            "value": None
          },
          {
            "color": "#FADE2A",
            "index": 1,
            "value": 50
          },
          {
            "color": "#5794F2",
            "index": 2,
            "value": 75
          },
          {
            "color": "#C8F2C2",
            "index": 3,
            "value": 87.5
          },
          {
            "color": "#96D98D",
            "index": 4,
            "value": 95
          },
          {
            "color": "#56A64B",
            "index": 5,
            "value": 97.5
          },
          {
            "color": "#37872D",
            "index": 6,
            "value": 98.75
          }
        ],
        "valueMappings": [],
        "valueOptions": {
          "decimals": 1,
          "prefix": "",
          "stat": "current",
          "suffix": "",
          "unit": "percent"
        }
      },
      "targets": [
        {
          "format": "time_series",
          "group": [],
          "metricColumn": "none",
          "rawQuery": False,
          "rawSql": "SELECT\n  timestamp AS \"time\",\n  passrate\nFROM testsuites\nORDER BY timestamp",
          "refId": "A",
          "select": [
            [
              {
                "params": [
                  "passrate"
                ],
                "type": "column"
              }
            ]
          ],
          "table": "testsuites",
          "timeColumn": "timestamp",
          "timeColumnType": "timestamp",
          "where": []
        }
      ],
      "timeFrom": None,
      "timeShift": None,
      "title": "Pass Rate",
      "type": "gauge"
    }
  ]
  },
  "folderId": 0,
  "overwrite": True,
}

response = requests.post(url, data=json.dumps(data), headers=headers)

if response.status_code!=200:
  print('Status:'+str(response.status_code))
  print(response.text)

