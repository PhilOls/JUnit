#Standard packages
import sys, glob, re, os, argparse

#Non-standard packages (install via pip)
import sqlalchemy, pymysql

parser = argparse.ArgumentParser(description='Uploads xml to sql database')
parser.add_argument('-db', action="store", dest="db")

args = parser.parse_args()

def sql_out():
  metadata = sqlalchemy.MetaData()
  engine = sqlalchemy.create_engine('mysql://mysql:mysql@localhost:3306') # connect to server
  engine.execute("CREATE DATABASE IF NOT EXISTS "+ args.db)
  engine.execute("USE " + args.db)
  engine.execute("CREATE TABLE IF NOT EXISTS testsuites (\
    tests INT, \
    passed INT, \
    failures INT, \
    disabled INT, \
    duplicate INT, \
    unknowns INT, \
    fixed INT, \
    broken INT) ")
  table = sqlalchemy.Table('testsuites', metadata, autoload=True, autoload_with=engine)
  tests    = 0
  passed   = 0
  failures = 0
  disabled = 0
  duplicate= 0
  unknowns = 0
  fixed    = 0
  broken   = 0
  q = table.insert().values(
    tests=tests,
    passed=passed,
    failures=failures,
    disabled=disabled,
    duplicate=duplicate,
    unknowns=unknowns,
    fixed=fixed,
    broken=broken)
  connection = engine.connect()
  connection.execute(q)

sql_out()