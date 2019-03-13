#Standard packages
import sys, glob, re, os, argparse, datetime, xml.etree.ElementTree

#Non-standard packages (install via pip)
import sqlalchemy, pymysql

parser = argparse.ArgumentParser(description='Uploads xml to sql database')
parser.add_argument('-db', action="store", dest="db")
parser.add_argument('-p', '--purge', help="purge database")
args = parser.parse_args()

root = xml.etree.ElementTree.parse('example/report/report.xml').getroot()

metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine('mysql://mysql:mysql@localhost:3306') # connect to server
engine.execute("CREATE DATABASE IF NOT EXISTS "+ args.db)
engine.execute("USE " + args.db)
if args.purge:
  engine.execute("DROP TABLE IF EXISTS testsuites")
engine.execute("CREATE TABLE IF NOT EXISTS testsuites (\
  timestamp TIMESTAMP, \
  tests INT, \
  passed INT, \
  failures INT, \
  disabled INT, \
  duplicate INT, \
  unknowns INT, \
  fixed INT, \
  broken INT, \
  passrate FLOAT(5,2)) ")
table = sqlalchemy.Table('testsuites', metadata, autoload=True, autoload_with=engine)
for child in root:
  try:
    passrate = 100*int(child.attrib['passed'])/int(child.attrib['tests'])
  except ZeroDivisionError:
    passrate = 0
  q = table.insert().values(
    timestamp=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
    tests=child.attrib['tests'],
    passed=child.attrib['passed'],
    failures=child.attrib['failures'],
    disabled=child.attrib['disabled'],
    duplicate=child.attrib['duplicate'],
    unknowns=child.attrib['unknowns'],
    fixed=child.attrib['fixed'],
    broken=child.attrib['broken'],
    passrate=passrate)
  connection = engine.connect()
  connection.execute(q)
