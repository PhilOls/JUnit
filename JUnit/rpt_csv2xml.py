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


class Record:

  def __init__(self, duration, starttime, logpath, reason):
    self.duration = "0"
    self.starttime = "0"
    self.logpath = ""
    self.reason = ""


def parseFile(status, d):
  fn = args.dir + "/report/" + status + ".csv"
  if os.path.isfile(fn):
    with open(fn, "r") as fcsv:
      csvreader = csv.reader(fcsv, delimiter=',', quotechar='|')
      for line in csvreader:
        if len(line) == 9:
          test, seed, testbench, reason, corner, starttime, duration, logpath, violation = line
          l[status, corner, testbench].append(test + "__" + seed)
          d[test + "__" + seed] = Record(duration, starttime, logpath, reason)
        else:
          print("Formating error, file: " + fn)

# Dict


disabled_d = {}
duplicate_d = {}
timeout_d = {}
fail_d = {}
pass_d = {}
started_d = {}

# # Parse csv files

parseFile("started", started_d)
parseFile("fail", fail_d)
parseFile("pass", pass_d)
parseFile("timeout", timeout_d)
parseFile("disabled", disabled_d)
parseFile("duplicate", duplicate_d)

if pfound:
  for status in ["fail", "pass", "timeout"]:
    if os.path.isfile(latest + "/" + status + ".csv"):
      fn = latest + "/" + status + ".csv"
      with open(fn, "r") as fcsv:
        csvreader = csv.reader(fcsv, delimiter=',', quotechar='|')
        for line in csvreader:
          if len(line) == 9:
            target, seed, testbench, reason, corner, starttime, duration, logpath, violation = line
            p_l[status, corner, testbench].append(target + "__" + seed)
          else:
            print("Formating error, file: " + fn)

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
      if len(l["started", corner, testbench]) + len(l["disabled", corner, testbench]) > 0 :
        fo.write('  <testsuite  name="' + testbench + '@' + corner + 
          '" tests="' + str(len(l["started", corner, testbench]) + len(l["disabled", corner, testbench])) + 
          '" pass="' + str(len(l["pass", corner, testbench])) + 
          '" disabled="' + str(len(l["disabled", corner, testbench])) + 
          '" duplicate="' + str(len(l["duplicate", corner, testbench])) + 
          '" unknowns="' + str(unknowns_l[corner, testbench]) + 
          '" fixed="' + str(fixed) + 
          '" broken="' + str(broken) + 
          '" failures="' + str(len(l["started", corner, testbench]) - len(l["pass", corner, testbench])) + '">\n')
        for pass_i in l["pass", corner, testbench]:
          match = re.search('(.*)__(.*)', pass_i)
          tgt = match.group(1)
          seed = match.group(2)
          if pass_i in p_l["pass", corner, testbench]:
              classn = "pass.still"
          else:
              if pass_i in p_l["fail", corner, testbench]:
                  classn = "pass.fixed"
              else:
                  classn = "pass.tbd"
          fo.write('    <testcase name="' + tgt + '_' + seed + '" classname="' + classn + '" corner="' + corner + '" target="' + tgt + '" seed="' + seed + '" basename="' + testbench + '" time="' + pass_d[pass_i].starttime + '" log="' + pass_d[pass_i].logpath + '">\n')
          fo.write('    </testcase>\n')
        for fail_i in l["fail", corner, testbench]:
          match = re.search('(.*)__(.*)', fail_i)
          tgt = match.group(1)
          seed = match.group(2)
          if fail_i in p_l["pass", corner, testbench]:
              classn = "fail.broken"
          else:
              if fail_i in p_l["fail", corner, testbench]:
                  classn = "fail.still"
              else:
                  classn = "fail.tbd"
          fo.write('    <testcase name="' + tgt + '_' + seed + '" classname="' + classn + '" reason="' + fail_d[fail_i].reason + '" corner="' + corner + '" target="'
                   +tgt + '" seed="' + seed + '" basename="' + testbench + '" time="' + fail_d[fail_i].starttime + '" log="' + fail_d[fail_i].logpath + '">\n')        
          fo.write('      <failure message="Failed with fail status"/>\n')
          fo.write('  <system-out>\n')
          fo.write('  </system-out>\n')
          fo.write('</testcase>\n')
        for timeout_i in l["timeout", corner, testbench]:
          match = re.search('(.*)__(.*)', timeout_i)
          tgt = match.group(1)
          seed = match.group(2)
          fo.write('    <testcase name="' + tgt + '_' + seed + '" classname="fail.timeout" reason="' + timeout_d[timeout_i].reason + '" corner="' + corner + '" target="'
                   +tgt + '" seed="' + seed + '" basename="' + testbench + '" time="' + timeout_d[timeout_i].starttime + '" log="'
                   +timeout_d[timeout_i].logpath + '">\n')
          fo.write('      <failure message="Time out"/>\n')
          fo.write('    </testcase>\n')
        for disabled_i in l["disabled", corner, testbench]:
          match = re.search('(.*)__(.*)', disabled_i)
          tgt = match.group(1)
          seed = match.group(2)
          rn = disabled_d[disabled_i].reason
          fo.write('    <testcase name="' + tgt + '_' + seed + '" classname="disabled" reason="' + rn + '" corner="' + corner + '" target="' + tgt + '" seed="' + seed + '" basename="' + testbench + '" time="0">\n')
          fo.write('      <skipped/>\n')
          fo.write('    </testcase>\n')
        for duplicate_i in l["duplicate", corner, testbench]:
          match = re.search('(.*)__(.*)', duplicate_i)
          tgt = match.group(1)
          seed = match.group(2)
          rn = duplicate_d[duplicate_i].reason
          fo.write('    <testcase name="' + tgt + '_' + seed + '" classname="duplicate" reason="Skipped" corner="' + corner + '" target="' + tgt + '" seed="' + seed + '" basename="' + testbench + '" time="0">\n')
          fo.write('      <skipped/>\n')
          fo.write('    </testcase>\n')
        for started_i in l["started", corner, testbench]:
          if not started_i in l["fail", corner, testbench]:
            if not started_i in l["pass", corner, testbench]:
              if not started_i in l["timeout", corner, testbench]:
                if not started_i in l["disabled", corner, testbench]:
                  match = re.search('(.*)__(.*)', started_i)
                  tgt = match.group(1)
                  seed = match.group(2)
                  fo.write('    <testcase name="' + tgt + '_' + seed + '" classname="unknown" reason="started/not finished" corner="' + corner + '" target="' + tgt + '" seed="' + seed + '" basename="' + testbench + '" time="' + started_d[started_i].starttime + '" log="' + started_d[started_i].logpath + '">\n')
                  fo.write('      <failure message="Started but no pass/fail status found. Started at:' + started_d[started_i].starttime + '"/>\n')
                  fo.write('  <system-out>\n')
                  fo.write('  </system-out>\n')
                  fo.write('</testcase>\n')
        fo.write('  </testsuite>\n')
  fo.write('</testsuites>\n')
