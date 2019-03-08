import sys, glob, re, os, argparse

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



## Checks if previous report exists and retrieve most recent one if any.
pfound = 0
latest = ""

print("Lookup ref report:"+args.dir+'/report_*')

l=glob.glob(args.dir+'/report_*')
if l == []:
  pfound = 0
else:
  latest = max(glob.iglob(args.dir+'/report_*'), key=os.path.getctime)
  pfound = 1
  print("Found ref report:"+latest)
  

path=os.getcwd()
path=path.rsplit('/')
path.reverse()
job=path[2]


## List and dictionaries of tests per status category
## When _p_ is used, this is for list of tests from
## previous reports (used to detect broken or fixed tests)
l = {}
p_l = {}
 
for corner in args.corners:
  for testbench in args.testbenches:
      for status in ["started","fail","pass","timeout","disabled","duplicate","broken","fixed"]:
          l[status,corner,testbench] = []
          p_l[status,corner,testbench] = []

## Dictionnaries to hold information for each test

#   info is duration
disabled_time_d = {}
duplicate_time_d = {}
timeout_time_d = {}
fail_time_d = {}
pass_time_d = {}
started_time_d = {}

# info is start time/date
disabled_date_d = {}
duplicate_date_d = {}
timeout_date_d = {}
fail_date_d = {}
pass_date_d = {}
started_date_d = {}

# info is path to logfile
disabled_log_d = {}
duplicate_log_d = {}
timeout_log_d = {}
fail_log_d = {}
pass_log_d = {}
started_log_d = {}

# info is reason why test is disabled (user info)
# or why test has timed out (exec info)
# not relevant for pass, duplicate, started
disabled_reason_d = {}
duplicate_reason_d = {}
timeout_reason_d = {}
fail_reason_d = {}
pass_reason_d = {}
started_reason_d = {}

## Parse csv files

for status in ["started","fail","pass","timeout","disabled","duplicate"]:
    if os.path.isfile(args.dir+"/report/"+status+".csv"):
        with open(args.dir+"/report/"+status+".csv", "r") as f:
            for line in f:
                match = re.search('(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*)',line)
                if match:
                    target,seed,testbench,reason,corner,starttime,duration,logpath,violation=line.split(",")
                    l[status,corner,testbench].append(target+"__"+seed)
                    if status=="started":
                        started_date_d[target+"__"+seed] = starttime
                        started_log_d[target+"__"+seed] = logpath
                        started_time_d[target+"__"+seed] = duration
                        started_reason_d[target+"__"+seed] = reason
                    if status=="pass":
                        pass_date_d[target+"__"+seed] = starttime
                        pass_log_d[target+"__"+seed] = logpath
                        pass_time_d[target+"__"+seed] = duration
                        pass_reason_d[target+"__"+seed] = reason
                    if status=="fail":
                        fail_date_d[target+"__"+seed] = starttime
                        fail_log_d[target+"__"+seed] = logpath
                        fail_time_d[target+"__"+seed] = duration
                        fail_reason_d[target+"__"+seed] = reason
                    if status=="timeout":
                        timeout_date_d[target+"__"+seed] = starttime
                        timeout_log_d[target+"__"+seed] = logpath
                        timeout_time_d[target+"__"+seed] = duration
                        timeout_reason_d[target+"__"+seed] = reason
                    if status=="disabled":
                        disabled_date_d[target+"__"+seed] = starttime
                        disabled_log_d[target+"__"+seed] = logpath
                        disabled_time_d[target+"__"+seed] = duration
                        disabled_reason_d[target+"__"+seed] = reason
                    if status=="duplicate":
                        duplicate_date_d[target+"__"+seed] = starttime
                        duplicate_log_d[target+"__"+seed] = logpath
                        duplicate_time_d[target+"__"+seed] = duration
                        duplicate_reason_d[target+"__"+seed] = reason


if pfound:
    for status in ["fail","pass","timeout"]:
        if os.path.isfile(latest+"/"+status+".csv"):
            with open(latest+"/"+status+".csv", "r") as f:
                for line in f:
                    match = re.search('(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*)',line)
                    if match:
                        target,seed,testbench,reason,corner,starttime,duration,logpath,violation=line.split(",")
                        p_l[status,corner,testbench].append(target+"__"+seed)

## Generates XML file
  
fo = open(args.dir+"/report/report.xml", "w")  
fo.write('<?xml-stylesheet href="../../../shared/utils/report.xsl" type="text/xsl"?>\n')

tests = 0
passed = 0
disabled = 0
duplicate = 0
failures = 0

for corner in args.corners:
  for testbench in args.testbenches:
    tests=tests+len(l["started",corner,testbench]+l["disabled",corner,testbench])
    passed=passed+len(l["pass",corner,testbench])
    disabled=disabled+len(l["disabled",corner,testbench])
    duplicate=duplicate+len(l["duplicate",corner,testbench])
    failures=failures+len(l["started",corner,testbench])-len(l["pass",corner,testbench])

unknowns = 0    
unknowns_l = {}
for corner in args.corners:
  for testbench in args.testbenches:
    unknowns_l[corner,testbench] = 0
    if len(l["started",corner,testbench])+len(l["disabled",corner,testbench])>0 :
      for started_i in l["started",corner,testbench]:
        if not started_i in l["fail",corner,testbench]:
          if not started_i in l["pass",corner,testbench]:
            if not started_i in l["timeout",corner,testbench]:
              if not started_i in l["disabled",corner,testbench]:
                unknowns = unknowns + 1
                unknowns_l[corner,testbench] = unknowns_l[corner,testbench] + 1


fixed = 0
broken = 0
for corner in args.corners:
  for testbench in args.testbenches:
    for pass_i in l["pass",corner,testbench]:
      if pass_i in p_l["fail",corner,testbench]:
        fixed = fixed + 1
    for fail_i in l["fail",corner,testbench]:
      if fail_i in p_l["pass",corner,testbench]:
        broken = broken + 1

fo.write(
  '<testsuites name="testsuites"'
  +' size="'+args.size
  +'" machine="'+args.machine
  +'" job="'+job
  +'" build="'+args.build
  +'" cover="'+args.cover
  +'" urlroot="'+args.urlroot
  +'" version="'+args.version
  +'" tests="'+str(tests)
  +'" pass="'+str(passed)
  +'" disabled="'+str(disabled)
  +'" duplicate="'+str(duplicate)
  +'" unknowns="'+str(unknowns)
  +'" fixed="'+str(fixed)
  +'" broken="'+str(broken))

if tests-duplicate > 0:
  fo.write('" passrate="'+str(passed*100/(tests))
  +'" failures="'+str(failures)+'">\n')
else:
  fo.write('" failures="'+str(failures)+'">\n')


for corner in args.corners:
  for testbench in args.testbenches:
    if len(l["started",corner,testbench])+len(l["disabled",corner,testbench])>0 :
      if len(l["started",corner,testbench]) > 0:
        fo.write('  <testsuite  name="'+testbench+'@'+corner+
        '" tests="'+str(len(l["started",corner,testbench])+len(l["disabled",corner,testbench]))+ 
        '" pass="'+str(len(l["pass",corner,testbench]))+ 
        '" disabled="'+str(len(l["disabled",corner,testbench]))+ 
        '" duplicate="'+str(len(l["duplicate",corner,testbench]))+ 
        '" unknowns="'+str(unknowns_l[corner,testbench])+ 
        '" fixed="'+str(fixed)+ 
        '" broken="'+str(broken)+ 
        '" failures="'+str(len(l["started",corner,testbench])-len(l["pass",corner,testbench]))+'">\n')
      else:
        fo.write('  <testsuite  name="'+testbench+'@'+corner+
        '" tests="'+str(len(l["started",corner,testbench])+len(l["disabled",corner,testbench]))+ 
        '" pass="'+str(len(l["pass",corner,testbench]))+ 
        '" disabled="'+str(len(l["disabled",corner,testbench]))+ 
        '" duplicate="'+str(len(l["duplicate",corner,testbench]))+ 
        '" unknowns="'+str(unknowns_l[corner,testbench])+ 
        '" fixed="'+str(fixed)+ 
        '" broken="'+str(broken)+ 
        '" failures="'+str(len(l["started",corner,testbench])-len(l["pass",corner,testbench]))+'">\n')      
      for pass_i in l["pass",corner,testbench]:
        match = re.search('(.*)__(.*)',pass_i)
        tgt = match.group(1)
        seed = match.group(2)
        if pass_i in p_l["pass",corner,testbench]:
            classn="pass.still"
        else:
            if pass_i in p_l["fail",corner,testbench]:
                classn="pass.fixed"
            else:
                classn="pass.tbd"
        fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="'+classn+'" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+testbench+'" time="'+pass_time_d[pass_i]+'" log="'+pass_log_d[pass_i]+'">\n')
        fo.write('    </testcase>\n')
      for fail_i in l["fail",corner,testbench]:
        match = re.search('(.*)__(.*)',fail_i)
        tgt = match.group(1)
        seed = match.group(2)
        if fail_i in p_l["pass",corner,testbench]:
            classn="fail.broken"
        else:
            if fail_i in p_l["fail",corner,testbench]:
                classn="fail.still"
            else:
                classn="fail.tbd"
        fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="'+classn+'" reason="'+fail_reason_d[fail_i]+'" corner="'+corner+'" target="'
                 +tgt+'" seed="'+seed+'" basename="'+testbench+'" time="'+fail_time_d[fail_i]+'" log="'+fail_log_d[fail_i]+'">\n')        
        fo.write('      <failure message="Failed with fail status"/>\n')
        fo.write('  <system-out>\n')
        fo.write('  </system-out>\n')
        fo.write('</testcase>\n')
      for timeout_i in l["timeout",corner,testbench]:
        match = re.search('(.*)__(.*)',timeout_i)
        tgt = match.group(1)
        seed = match.group(2)
        fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="fail.timeout" reason="'+timeout_reason_d[timeout_i]+'" corner="'+corner+'" target="'
                 +tgt+'" seed="'+seed+'" basename="'+testbench+'" time="'+timeout_time_d[timeout_i]+'" log="'
                 +timeout_log_d[timeout_i]+'">\n')
        fo.write('      <failure message="Time out"/>\n')
        fo.write('    </testcase>\n')
      for disabled_i in l["disabled",corner,testbench]:
        match = re.search('(.*)__(.*)',disabled_i)
        tgt = match.group(1)
        seed = match.group(2)
        rn = disabled_reason_d[disabled_i]
        fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="disabled" reason="'+rn+'" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+testbench+'" time="0">\n')
        fo.write('      <skipped/>\n')
        fo.write('    </testcase>\n')
      for duplicate_i in l["duplicate",corner,testbench]:
        match = re.search('(.*)__(.*)',duplicate_i)
        tgt = match.group(1)
        seed = match.group(2)
        rn = duplicate_reason_d[duplicate_i]
        fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="duplicate" reason="Skipped" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+testbench+'" time="0">\n')
        fo.write('      <skipped/>\n')
        fo.write('    </testcase>\n')
      for started_i in l["started",corner,testbench]:
        if not started_i in l["fail",corner,testbench]:
          if not started_i in l["pass",corner,testbench]:
            if not started_i in l["timeout",corner,testbench]:
              if not started_i in l["disabled",corner,testbench]:
                match = re.search('(.*)__(.*)',started_i)
                tgt = match.group(1)
                seed = match.group(2)
                fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="unknown" reason="started/not finished" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+testbench+'" time="'+started_date_d[started_i]+'" log="'+started_log_d[started_i]+'">\n')
                fo.write('      <failure message="Started but no pass/fail status found. Started at:'+started_date_d[started_i]+'"/>\n')
                fo.write('  <system-out>\n')
                fo.write('  </system-out>\n')
                fo.write('</testcase>\n')
      fo.write('  </testsuite>\n')
fo.write('</testsuites>\n')
fo.close()
