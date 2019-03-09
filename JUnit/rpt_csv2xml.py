import sys, glob, re, os, argparse, csv

parser = argparse.ArgumentParser(description='Converts csv to JUnit XML file')

parser.add_argument('-dir', action="store", dest="dir")
parser.add_argument('-size', action="store", dest="size")
parser.add_argument('-machine', action="store", dest="machine")
parser.add_argument('-build', action="store", dest="build")
parser.add_argument('-cover', action="store", dest="cover")
parser.add_argument('-version', action="store", dest="version")
parser.add_argument('-corners', action="store", dest="corners")
parser.add_argument('-testbenches', action="store", dest="testbenches")
parser.add_argument('-urlroot', action="store", dest="urlroot")

args = parser.parse_args()
args.corners = args.corners.split(",")
args.testbenches = args.testbenches.split(",")

# # Checks if previous report exists and retrieve most recent one if any.
pfound = 0
latest = ""

print("Lookup ref report:" + args.dir + '/report_*')

l = glob.glob(args.dir + '/report_*')
if l == []:
  pfound = 0
else:
  latest = max(glob.iglob(args.dir + '/report_*'), key=os.path.getctime)
  pfound = 1
  print("Found ref report:" + latest)

path = os.getcwd()
path = path.rsplit('/')
path.reverse()
print("path=")
print(path)
# job=path[2]

# # List and dictionaries of tests per status category
# # When _p_ is used, this is for list of tests from
# # previous reports (used to detect broken or fixed tests)
l = {}
p_l = {}
 
for corner in args.corners:
  for testbench in args.testbenches:
      for status in ["started", "fail", "pass", "timeout", "disabled", "duplicate", "broken", "fixed"]:
          l[status, corner, testbench] = []
          p_l[status, corner, testbench] = []

# # Dictionnaries to hold information for each test


class Testcase:
  '''Doc - object storing all required data for a single testcase'''

  def __init__(self, corner, testbench, test, seed, status, duration, time, log, reason, regress = None):
    self.corner = corner
    self.testbench = testbench
    self.test = test
    self.seed = seed
    self.status = status
    self.duration = duration
    self.time = time
    self.log = log
    self.reason = reason
    if regress is None:
      self.regress = "tbd"
    else:
      self.regress = regress
      
  def testname(self):
    '''Doc - JUnit testname attribute'''
    return(self.test+"_"+self.seed)
  
  def classname(self):
    '''Doc - JUnit classname attribute'''
    return(self.status+"."+self.regress)
  
  def as_pass(self):
    self.status = "pass"

  def as_fail(self):
    self.status = "pass"
    
  def xml_out(self,f):
    indent = "  "
    f.write(indent+
            '<testcase' +
            ' name="'       + self.testname()  + '"' +
            ' classname="'  + self.classname() + '"' +
            ' corner="'     + self.corner      + '"' +
            ' target="'     + self.test        + '"' +
            ' seed="'       + self.seed        + '"' +
            ' basename="'   + self.testbench   + '"' +
            ' time="'       + self.time        + '"' +
            ' log="'        + self.log         + '"' +
            '>\n')
    
    if self.status=="fail":
      f.write(indent + '  <failure message="Failed with fail status"/>\n')
      f.write(indent + '  <system-out>\n')
      #TBD
      f.write(indent +'  </system-out>\n')
    elif self.status=="timeout":
      f.write(indent+  '  <failure message="Time out"/>\n')
    elif self.status=="disable":
      f.write(indent+  '  <skipped/>\n')
    elif self.status=="duplicate":
      f.write(indent+  '  <skipped/>\n')

    f.write(indent+'</testcase>\n')

tc_l = []

def parseFile(status):
  fn = args.dir + "/report/" + status + ".csv"
  if os.path.isfile(fn):
    with open(fn, "r") as fcsv:
      csvreader = csv.reader(fcsv, delimiter=',', quotechar='|')
      for line in csvreader:
        if len(line) == 9:
          test, seed, testbench, reason, corner, time, duration, log, violation = line
          tn = test + "__" + seed
          l[status, corner, testbench].append(tn)
          regress = None
          if status == "pass":
            if tn in p_l["pass", corner, testbench]:
              regress = "unchanged"
            elif tn in p_l["fail", corner, testbench]:
              regress = "fixed"
            elif tn in p_l["timeout", corner, testbench]:
              regress = "fixed"
          elif status == "fail":
            if tn in p_l["fail", corner, testbench]:
              regress = "unchanged"
            elif tn in p_l["pass", corner, testbench]:
              regress = "broken"
          elif status == "timeout":
            if tn in p_l["timeout", corner, testbench]:
              regress = "unchanged"
            elif tn in p_l["pass", corner, testbench]:
              regress = "broken"
          tc_l.append(Testcase(corner, testbench, test, seed, status, duration, time, log, reason, regress))
        else:
          print("Formating error, file: " + fn)

# Parse csv files

if pfound:
  for status in ["fail", "pass", "timeout"]:
    if os.path.isfile(latest + "/" + status + ".csv"):
      fn = latest + "/" + status + ".csv"
      with open(fn, "r") as fcsv:
        csvreader = csv.reader(fcsv, delimiter=',', quotechar='|')
        for line in csvreader:
          if len(line) == 9:
            target, seed, testbench, reason, corner, time, duration, log, violation = line
            p_l[status, corner, testbench].append(target + "__" + seed)
          else:
            print("Formating error, file: " + fn)

parseFile("started")
parseFile("fail")
parseFile("pass")
parseFile("timeout")
parseFile("disabled")
parseFile("duplicate")

# # Generates XML file
  
with open(args.dir + "/report/report.xml", "w") as fo: 

  tests = 0
  passed = 0
  disabled = 0
  duplicate = 0
  failures = 0
  
  for corner in args.corners:
    for testbench in args.testbenches:
      tests = tests + len(l["started", corner, testbench] + l["disabled", corner, testbench])
      passed = passed + len(l["pass", corner, testbench])
      disabled = disabled + len(l["disabled", corner, testbench])
      duplicate = duplicate + len(l["duplicate", corner, testbench])
      failures = failures + len(l["started", corner, testbench]) - len(l["pass", corner, testbench])
  
  unknowns = 0    
  unknowns_l = {}
  for corner in args.corners:
    for testbench in args.testbenches:
      unknowns_l[corner, testbench] = 0
      if len(l["started", corner, testbench]) + len(l["disabled", corner, testbench]) > 0 :
        for started_i in l["started", corner, testbench]:
          if not started_i in l["fail", corner, testbench]:
            if not started_i in l["pass", corner, testbench]:
              if not started_i in l["timeout", corner, testbench]:
                if not started_i in l["disabled", corner, testbench]:
                  unknowns = unknowns + 1
                  unknowns_l[corner, testbench] = unknowns_l[corner, testbench] + 1
  
  fixed = 0
  broken = 0
  for corner in args.corners:
    for testbench in args.testbenches:
      for pass_i in l["pass", corner, testbench]:
        if pass_i in p_l["fail", corner, testbench]:
          fixed = fixed + 1
      for fail_i in l["fail", corner, testbench]:
        if fail_i in p_l["pass", corner, testbench]:
          broken = broken + 1
  
  fo.write(
    '<testsuites name="testsuites"'
    +' size="' + args.size
    +'" machine="' + args.machine
  #  +'" job="'+job
    +'" build="' + args.build
    +'" cover="' + args.cover
    +'" urlroot="' + args.urlroot
    +'" version="' + args.version
    +'" tests="' + str(tests)
    +'" pass="' + str(passed)
    +'" disabled="' + str(disabled)
    +'" duplicate="' + str(duplicate)
    +'" unknowns="' + str(unknowns)
    +'" fixed="' + str(fixed)
    +'" broken="' + str(broken))
  
  if tests - duplicate > 0:
    fo.write('" passrate="' + str(passed * 100 / (tests))
    +'" failures="' + str(failures) + '">\n')
  else:
    fo.write('" failures="' + str(failures) + '">\n')
  
  for corner in args.corners:
    for testbench in args.testbenches:
      started  = [i for i in tc_l if i.status == "started" and i.testbench == testbench and i.corner == corner]
      disabled = [i for i in tc_l if i.status == "disabled" and i.testbench == testbench and i.corner == corner]
      if len(l["started", corner, testbench]) + len(l["disabled", corner, testbench]) > 0 :
        fo.write('  <testsuite  name="' + testbench + '@' + corner + 
          '" tests="'     + str(len(started) + len(disabled)) + 
          '" pass="'      + str(len(l["pass", corner, testbench])) + 
          '" disabled="'  + str(len(l["disabled", corner, testbench])) + 
          '" duplicate="' + str(len(l["duplicate", corner, testbench])) + 
          '" unknowns="'  + str(unknowns_l[corner, testbench]) + 
          '" fixed="'     + str(fixed) + 
          '" broken="'    + str(broken) + 
          '" failures="'  + str(len(l["started", corner, testbench]) - len(l["pass", corner, testbench])) + '">\n')
        for i in tc_l:
          if not i.status == "started":
            i.xml_out(fo)
          else:
            if not i in l["fail", corner, testbench]:
              if not i in l["pass", corner, testbench]:
                if not i in l["timeout", corner, testbench]:
                  if not i in l["disabled", corner, testbench]:
                    i.xml_out(fo)
            
        fo.write('  </testsuite>\n')
  fo.write('</testsuites>\n')
