#Standard packages
import sys, glob, re, os, argparse, csv

parser = argparse.ArgumentParser(description='Converts csv to JUnit XML file')
parser.add_argument('-dir', action="store", dest="dir")
args = parser.parse_args()

status_l =["started", "failures", "passed", "timeout", "disabled", "duplicate"]

class TestCase:
  '''Doc - object storing all required data for a single testcase'''

  def __init__(self, status, line):
    self.test, self.seed, self.testbench, self.reason, self.corner, self.time, self.duration, self.log, self.violation = line
    self.status = status
    self.regress = "tbd"

  def testname(self):
    '''Doc - JUnit testname attribute'''
    return(self.test+"_"+self.seed)
  
  def classname(self):
    '''Doc - JUnit classname attribute'''
    return(self.status+"."+self.regress)
  
  def xml_out(self):
    indent = "    "
    xml = (indent+
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
    if self.status=="failures":
      xml += indent + '  <failure message="Failed with failures status"/>\n'
      xml += indent + '  <system-out>\n'
      #TBD
      xml += indent +'  </system-out>\n'
    elif self.status=="timeout":
      xml += indent+  '  <failure message="Time out"/>\n'
    elif self.status=="disable":
      xml += indent+  '  <skipped/>\n'
    elif self.status=="duplicate":
      xml += indent+  '  <skipped/>\n'
    xml += indent+'</testcase>\n'
    return (xml)

class TestSuite:
  '''Doc - object storing all required data for a single testsuite'''

  def __init__(self,corner,testbench):
    self.tc_l = []
    self.corner = corner
    self.testbench = testbench
    
  def add(self, testcase):
    '''Doc - add a testcase to testsuite. If testcase already exists with status=started, remove it'''
    for tc in self.tc_l:
      if tc.testname() == testcase.testname() and tc.status == "started":
        self.tc_l.remove(tc)
    self.tc_l.append(testcase)
    
  def xml_out(self):
    indent = "  "
    xml = indent  + '<testsuite  name="' + self.testbench + '@' + self.corner +'"' 
    xml += ' tests="'      + str(len([i for i in self.tc_l if i.status in ["started","passed","failures","timeout"]]))                + '"'
    xml += ' passed="'       + str(len([i for i in self.tc_l if i.status == "passed"]))                                             + '"'
    xml += ' disabled="'   + str(len([i for i in self.tc_l if i.status == "disabled"]))                                         + '"'
    xml += ' duplicate="'  + str(len([i for i in self.tc_l if i.status == "duplicate"]))                                        + '"'
    xml += ' unknowns="'   + str(len([i for i in self.tc_l if i.status == "started"]))                                          + '"'
    xml += ' fixed="'      + str(len([i for i in self.tc_l if i.regress == "fixed"]))                                           + '"'
    xml += ' broken="'     + str(len([i for i in self.tc_l if i.regress == "broken"]))                                          + '"'
    xml += ' failures="'   + str(len([i for i in self.tc_l if i.status in ["started","failures","timeout"]]))                       + '"'
    xml += '>\n'
    for tc in self.tc_l:
      xml+= tc.xml_out()
    xml += indent  + '</testsuite>\n' 

    return (xml)

class TestSuites:
  '''Doc - object storing all required data for a single testsuite'''

  def __init__(self):
    self.ts_l = []
  
  def xml_out(self):
    indent = ""
    xml = indent + '<testsuites name="testsuites"'
    tests = 0
    passed = 0
    fails = 0
    disabled = 0
    duplicates = 0
    fixed = 0
    broken = 0
    unknowns = 0
    for ts in self.ts_l:
      tests      += len([i for i in ts.tc_l if i.status  in ["passed","failures","started","timeout"]])
      passed     += len([i for i in ts.tc_l if i.status  in ["passed"]])
      fails      += len([i for i in ts.tc_l if i.status  in ["failures","timeout"]])
      unknowns   += len([i for i in ts.tc_l if i.status  in ["started"]])
      disabled   += len([i for i in ts.tc_l if i.status  in ["disabled"]])
      duplicates += len([i for i in ts.tc_l if i.status  in ["duplicates"]])
      fixed      += len([i for i in ts.tc_l if i.regress in ["fixed"]])
      broken     += len([i for i in ts.tc_l if i.regress in ["broken"]])
    xml += ' tests="'     + str(tests)      +'"'
    xml += ' passed="'    + str(passed)     +'"'
    xml += ' failures="'  + str(fails)      +'"'
    xml += ' disabled="'  + str(disabled)   +'"'
    xml += ' duplicate="' + str(duplicates) +'"'
    xml += ' unknowns="'  + str(unknowns)    +'"'
    xml += ' fixed="'     + str(fixed)      +'"'
    xml += ' broken="'    + str(broken)     +'"'
    xml += '>\n'
    for ts in self.ts_l:
      xml += ts.xml_out()
    xml += '</testsuites>\n'
    return (xml)

def parseFile(file, status, tss):
  if os.path.isfile(file):
    with open(file, "r") as fcsv:
      csvreader = csv.reader(fcsv, delimiter=',', quotechar='|')
      for line in csvreader:
        if len(line) == 9:
          testbench = line[2]
          corner = line[4]
          if len([i for i in tss.ts_l if i.corner == corner and i.testbench == testbench])<1:
            tss.ts_l.append(TestSuite(corner,testbench))
          for i in [i for i in tss.ts_l if i.corner == corner and i.testbench == testbench]:
            i.add(TestCase(status, line))
        else:
          print("Formating error, file: " + fn)

prev_tss = TestSuites()

if glob.glob(args.dir + '/report_*'):
  latest = max(glob.iglob(args.dir + '/report_*'), key=os.path.getctime)
  print("Found ref report:" + latest)
  for status in status_l:
    parseFile(latest + "/" + status + ".csv", status, prev_tss)

tss = TestSuites()
    
for status in status_l:
  parseFile(args.dir + "/report/" + status + ".csv", status, tss)

for prev_ts in prev_tss.ts_l:
  for ts in [i for i in tss.ts_l if i.testbench == prev_ts.testbench and i.corner == prev_ts.corner]:
    for prev_tc in prev_ts.tc_l:
      for tc in [i for i in ts.tc_l if i.test == prev_tc.test and i.seed == prev_tc.seed]:
        if (tc.status == prev_tc.status):
          tc.regress = "unchanged"
        elif tc.status == "passed" and prev_tc.status in ["failures", "timeout"] :
          tc.regress = "fixed"
        elif tc.status in ["failures","timeout"] and prev_tc.status == "passed" :
          tc.regress = "broken"

with open(args.dir + "/report/report.xml", "w") as fo: 
  fo.write(tss.xml_out())
