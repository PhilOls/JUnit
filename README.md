# JUnit

Creation of a custom test report in JUnit xml format from csv delimited files.
Upload of test results to an sql database.
A Grafana dashboard generation is available as well.

![alt text](https://raw.githubusercontent.com/PhilOls/JUnit/master/grafana/dashboard.png)

Direct access to test log is provided by clicking on the testname.

For an example of generated report:
http://htmlpreview.github.io/?https://github.com/PhilOls/JUnit/blob/master/example/report/report.html

JUnit can be used with continuous integration tools like Jenkins, Bamboo and point to stored artifacts for each build

The format of each csv file is the same.

Each line corresponds to a testcase and consists in:
target,seed,testbench,reason,corner,starttime,duration,logpath,violation

where:

| Field | Description |
| --- | --- |
| target |  test name
| seed |  integer reflecting seed used
| testbench |  testbench in which test was run
| reason |  multiple usage <br> timeout  :  can indicate what timeout fired (UVM phase timeout, Ant exec timeout,...) <br> disabled :  user information to indficate whyb test is currently disabled
| corner |  corner used, most commonly rtl (can also be best, typ, worst, etc....)
| starttime |  start time+date when test kicked
| duration |  duration of test in sec
| logpath |  path to test logfile
| violation |  counts of violation (mostly relevant for gate-level)

## Getting Started


### Prerequisites

#### Python packages 
| Package | Pip install name |
| --- | --- |
| cryptography  | cryptography
| base64        | pybase64
| PyMySQL       | PyMySQL
| SQLAlchemy    | SQLAlchemy
| requests      | requests

#### Windows
* [MSXSL] (https://www.microsoft.com/en-us/download/details.aspx?displaylang=en&id=21714) - MSXSL

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Ant](http://www.tbd.org) - The web framework used

## Authors

* **Philippe Olszewski** - *Initial work*
