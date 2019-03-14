def passrate(title):
  return {
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
    "title": title,
    "type": "gauge"
  }
  
def status(title):
  return {
    "aliasColors": {},
    "bars": False,
    "dashLength": 10,
    "dashes": False,
    "datasource": "MySQL",
    "description": "TestSuites status, time is UTC",
    "fill": 1,
    "gridPos": {
      "h": 5,
      "w": 20,
      "x": 0,
      "y": 6
    },
    "id": 2,
    "interval": "1mn",
    "legend": {
      "alignAsTable": True,
      "avg": True,
      "current": True,
      "max": True,
      "min": True,
      "rightSide": True,
      "show": True,
      "total": False,
      "values": True
    },
    "lines": True,
    "linewidth": 1,
    "links": [],
    "nullPointMode": "null",
    "paceLength": 10,
    "percentage": False,
    "pointradius": 2,
    "points": False,
    "renderer": "flot",
    "seriesOverrides": [],
    "stack": False,
    "steppedLine": False,
    "targets": [
      {
        "format": "time_series",
        "group": [],
        "metricColumn": "none",
        "rawQuery": False,
        "rawSql": "SELECT\n  timestamp AS \"time\",\n  tests,\n  passed,\n  failures,\n  fixed,\n  broken\nFROM testsuites\nORDER BY timestamp",
        "refId": "A",
        "select": [
          [
            {
              "params": [
                "tests"
              ],
              "type": "column"
            }
          ],
          [
            {
              "params": [
                "passed"
              ],
              "type": "column"
            }
          ],
          [
            {
              "params": [
                "failures"
              ],
              "type": "column"
            }
          ],
          [
            {
              "params": [
                "fixed"
              ],
              "type": "column"
            }
          ],
          [
            {
              "params": [
                "broken"
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
    "thresholds": [],
    "timeFrom": None,
    "timeRegions": [],
    "timeShift": None,
    "title": "TestSuites",
    "tooltip": {
      "shared": True,
      "sort": 0,
      "value_type": "individual"
    },
    "type": "graph",
    "xaxis": {
      "buckets": None,
      "mode": "time",
      "name": None,
      "show": True,
      "values": []
    },
    "yaxes": [
      {
        "format": "short",
        "label": None,
        "logBase": 1,
        "max": None,
        "min": None,
        "show": True
      },
      {
        "format": "short",
        "label": None,
        "logBase": 1,
        "max": None,
        "min": None,
        "show": True
      }
    ],
    "yaxis": {
      "align": False,
      "alignLevel": None
    }
  }

