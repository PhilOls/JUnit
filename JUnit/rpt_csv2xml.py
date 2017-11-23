import sys, glob, re, os
import os
import argparse

import sys, glob, re, os
import os
import argparse

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

pfound = 0
latest = ""

l=glob.glob(args.dir+'report_*')
if l == []:
  pfound = 0
else:
  latest = max(glob.iglob(args.dir+'report_*'), key=os.path.getctime)
  pfound = 1
  

started_l = {}
disabled_l = {}
pass_l = {}
pass_p_l = {}
fail_l = {}
fail_p_l = {}
timeout_l = {}
duplicate_l = {}
fixed_l = {}
broken_l = {}

path=os.getcwd()
path=path.rsplit('/')
path.reverse()
job=path[2]


## List of tests per status category
## When _p_ is used, this is for list of tests from
## previous reports (used to detect broken or fixed tests)

for corner in args.corners:
  for testbench in args.testbenches:
    started_l[corner,testbench] = []
    disabled_l[corner,testbench] = []
    pass_l[corner,testbench] = []
    pass_p_l[corner,testbench] = []
    fail_l[corner,testbench] = []
    fail_p_l[corner,testbench] = []
    timeout_l[corner,testbench] = []
    duplicate_l[corner,testbench] = []
    broken_l[corner,testbench] = []
    fixed_l[corner,testbench] = []

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

for status in ["started","fail","pass","timeout","disabled","duplicate"]:
    if os.path.isfile(args.dir+"/"+status+".csv"):
        with open(args.dir+"/"+status+".csv", "r") as f:
            for line in f:
                match = re.search('(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*)',line)
                if match:
                    target,seed,testbench,reason,corner,starttime,duration,logpath,violation=line.split(",")
                    if status=="started":
                        started_l[corner,testbench].append(target+"__"+seed)
                        started_date_d[target+"__"+seed] = starttime
                        started_log_d[target+"__"+seed] = logpath
                        started_time_d[target+"__"+seed] = duration
                        started_reason_d[target+"__"+seed] = reason
                    if status=="pass":
                        pass_l[corner,testbench].append(target+"__"+seed)
                        pass_date_d[target+"__"+seed] = starttime
                        pass_log_d[target+"__"+seed] = logpath
                        pass_time_d[target+"__"+seed] = duration
                        pass_reason_d[target+"__"+seed] = reason
                    if status=="fail":
                        fail_l[corner,testbench].append(target+"__"+seed)
                        fail_date_d[target+"__"+seed] = starttime
                        fail_log_d[target+"__"+seed] = logpath
                        fail_time_d[target+"__"+seed] = duration
                        fail_reason_d[target+"__"+seed] = reason
                    if status=="timeout":
                        timeout_l[corner,testbench].append(target+"__"+seed)
                        timeout_date_d[target+"__"+seed] = starttime
                        timeout_log_d[target+"__"+seed] = logpath
                        timeout_time_d[target+"__"+seed] = duration
                        timeout_reason_d[target+"__"+seed] = reason
                    if status=="disabled":
                        disabled_l[corner,testbench].append(target+"__"+seed)
                        disabled_date_d[target+"__"+seed] = starttime
                        disabled_log_d[target+"__"+seed] = logpath
                        disabled_time_d[target+"__"+seed] = duration
                        disabled_reason_d[target+"__"+seed] = reason
                    if status=="duplicate":
                        duplicate_l[corner,testbench].append(target+"__"+seed)
                        duplicate_date_d[target+"__"+seed] = starttime
                        duplicate_log_d[target+"__"+seed] = logpath
                        duplicate_time_d[target+"__"+seed] = duration
                        duplicate_reason_d[target+"__"+seed] = reason
  
fo = open(args.dir+"/report.xml", "w")  
fo.write('<?xml-stylesheet href="../../../shared/utils/report.xsl" type="text/xsl"?>\n')

tests = 0
passed = 0
disabled = 0
duplicate = 0
failures = 0

for corner in args.corners:
  for testbench in args.testbenches:
    tests=tests+len(started_l[corner,testbench]+disabled_l[corner,testbench])
    passed=passed+len(pass_l[corner,testbench])
    disabled=disabled+len(disabled_l[corner,testbench])
    duplicate=duplicate+len(duplicate_l[corner,testbench])
    failures=failures+len(started_l[corner,testbench])-len(pass_l[corner,testbench])

unknowns = 0    
unknowns_l = {}
for corner in args.corners:
  for testbench in args.testbenches:
    unknowns_l[corner,testbench] = 0
    if len(started_l[corner,testbench])+len(disabled_l[corner,testbench])>0 :
      for started_i in started_l[corner,testbench]:
        if not started_i in fail_l[corner,testbench]:
          if not started_i in pass_l[corner,testbench]:
            if not started_i in timeout_l[corner,testbench]:
              if not started_i in disabled_l[corner,testbench]:
                unknowns = unknowns + 1
                unknowns_l[corner,testbench] = unknowns_l[corner,testbench] + 1


fixed = 0
broken = 0
for corner in args.corners:
  for testbench in args.testbenches:
    fixed_l[corner,testbench] = 0
    for pass_i in pass_l[corner,testbench]:
      if pass_i in fail_p_l[corner,testbench]:
        fixed_l[corner,testbench] = fixed_l[corner,testbench] + 1
        fixed = fixed + 1
    broken_l[corner,testbench] = 0
    for fail_i in fail_l[corner,testbench]:
      if fail_i in pass_p_l[corner,testbench]:
        broken_l[corner,testbench] = broken_l[corner,testbench] + 1
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
    if len(started_l[corner,testbench])+len(disabled_l[corner,testbench])>0 :
      if len(started_l[corner,testbench]) > 0:
        fo.write('  <testsuite  name="'+testbench+'@'+corner+
        '" tests="'+str(len(started_l[corner,testbench])+len(disabled_l[corner,testbench]))+ 
        '" pass="'+str(len(pass_l[corner,testbench]))+ 
        '" passrate="'+str(len(pass_l[corner,testbench])*100/len(started_l[corner,testbench]))+ 
        '" disabled="'+str(len(disabled_l[corner,testbench]))+ 
        '" duplicate="'+str(len(duplicate_l[corner,testbench]))+ 
        '" unknowns="'+str(unknowns_l[corner,testbench])+ 
        '" fixed="'+str(fixed_l[corner,testbench])+ 
        '" broken="'+str(broken_l[corner,testbench])+ 
        '" failures="'+str(len(started_l[corner,testbench])-len(pass_l[corner,testbench]))+'">\n')
      else:
        fo.write('  <testsuite  name="'+testbench+'@'+corner+
        '" tests="'+str(len(started_l[corner,testbench])+len(disabled_l[corner,testbench]))+ 
        '" pass="'+str(len(pass_l[corner,testbench]))+ 
        '" disabled="'+str(len(disabled_l[corner,testbench]))+ 
        '" duplicate="'+str(len(duplicate_l[corner,testbench]))+ 
        '" unknowns="'+str(unknowns_l[corner,testbench])+ 
        '" fixed="'+str(fixed_l[corner,testbench])+ 
        '" broken="'+str(broken_l[corner,testbench])+ 
        '" failures="'+str(len(started_l[corner,testbench])-len(pass_l[corner,testbench]))+'">\n')      
      for pass_i in pass_l[corner,testbench]:
        match = re.search('(.*)__(.*)',pass_i)
        tgt = match.group(1)
        seed = match.group(2)
        if pass_i in pass_p_l[corner,testbench]:
          fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="pass.still" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+testbench+'" time="'+pass_time_d[pass_i]+'" log="'+pass_log_d[pass_i]+'">\n')
        else:
          if pass_i in fail_p_l[corner,testbench]:
            fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="pass.fixed" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+testbench+'" time="'+pass_time_d[pass_i]+'" log="'+pass_log_d[pass_i]+'">\n')
          else:
            fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="pass.tbd" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+testbench+'" time="'+pass_time_d[pass_i]+'" log="'+pass_log_d[pass_i]+'">\n')
        #fo.write('      <system-out>\n')
        #fo.write('      </system-out>\n')
        fo.write('    </testcase>\n')
      for fail_i in fail_l[corner,testbench]:
        match = re.search('(.*)__(.*)',fail_i)
        tgt = match.group(1)
        seed = match.group(2)
        if fail_i in pass_p_l[corner,testbench]:
          fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="fail.broken" reason="'+fail_reason_d[fail_i]+'" corner="'+corner+'" target="'
                   +tgt+'" seed="'+seed+'" basename="'+testbench+'" time="'+fail_time_d[fail_i]+'" log="'
                   +fail_log_d[fail_i]+'">\n')
        else:
          if fail_i in fail_p_l[corner,testbench]:
            fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="fail.still" reason="'+fail_reason_d[fail_i]+'" corner="'+corner+'" target="'
                     +tgt+'" seed="'+seed+'" basename="'+testbench+'" time="'+fail_time_d[fail_i]+'" tv="'+'" log="'
                     +fail_log_d[fail_i]+'">\n')
          else:
            fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="fail.tbd" reason="'+fail_reason_d[fail_i]+'" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+testbench+'" time="'+fail_time_d[fail_i]+'" log="'+fail_log_d[fail_i]+'">\n')
        fo.write('      <failure message="Failed with fail status"/>\n')
        fo.write('  <system-out>\n')
        fo.write('  </system-out>\n')
        fo.write('</testcase>\n')
      for timeout_i in timeout_l[corner,testbench]:
        match = re.search('(.*)__(.*)',timeout_i)
        tgt = match.group(1)
        seed = match.group(2)
        fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="fail.timeout" reason="'+timeout_reason_d[timeout_i]+'" corner="'+corner+'" target="'
                 +tgt+'" seed="'+seed+'" basename="'+testbench+'" time="'+timeout_time_d[timeout_i]+'" log="'
                 +timeout_log_d[timeout_i]+'">\n')
        fo.write('      <failure message="Time out"/>\n')
        fo.write('    </testcase>\n')
      for disabled_i in disabled_l[corner,testbench]:
        match = re.search('(.*)__(.*)',disabled_i)
        tgt = match.group(1)
        seed = match.group(2)
        rn = disabled_reason_d[disabled_i]
        fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="disabled" reason="'+rn+'" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+testbench+'" time="0">\n')
        fo.write('      <skipped/>\n')
        fo.write('    </testcase>\n')
      for duplicate_i in duplicate_l[corner,testbench]:
        match = re.search('(.*)__(.*)',duplicate_i)
        tgt = match.group(1)
        seed = match.group(2)
        rn = duplicate_reason_d[duplicate_i]
        fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="duplicate" reason="Skipped" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+testbench+'" time="0">\n')
        fo.write('      <skipped/>\n')
        fo.write('    </testcase>\n')
      for started_i in started_l[corner,testbench]:
        if not started_i in fail_l[corner,testbench]:
          if not started_i in pass_l[corner,testbench]:
            if not started_i in timeout_l[corner,testbench]:
              if not started_i in disabled_l[corner,testbench]:
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
