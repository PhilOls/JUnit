import sys, glob, re, os
import os

corners_l = sys.argv[2].split(",")
tbs_l     = sys.argv[3].split(",")

pfound = 0
latest = ""

l=glob.glob('report_*')
if l == []:
  pfound = 0
else:
  latest = max(glob.iglob('report_*'), key=os.path.getctime)
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

#print str(sys.argv[1])

for corner in corners_l:
  for bn in bns_l:
    started_l[corner,bn] = []
    disabled_l[corner,bn] = []
    pass_l[corner,bn] = []
    pass_p_l[corner,bn] = []
    fail_l[corner,bn] = []
    fail_p_l[corner,bn] = []
    timeout_l[corner,bn] = []
    duplicate_l[corner,bn] = []
    broken_l[corner,bn] = []
    fixed_l[corner,bn] = []

disabled_time_d = {}
duplicate_time_d = {}
timeout_time_d = {}
fail_time_d = {}
fail_p_time_d = {}
pass_time_d = {}
pass_p_time_d = {}
fail_reason_d = {}
started_date_d = {}
reason_d = {}
log_d = {}
log_p_d = {}
started_log_d = {}

timeout_tv_d = {}
fail_tv_d = {}
pass_tv_d = {}

if os.path.isfile("report/started.csv"):
  fis = open("report/started.csv", "r")
  lines = fis.read().split("\n")
  for line in lines:
    match = re.search('(.*),(.*),(.*),(.*),(.*),(.*),STARTED,(.*),(.*)',line)
    if match:
      id = match.group(1)+"__"+match.group(2)
      corner=match.group(6)
      bn=match.group(3)
      started_l[corner,bn].append(id)
      started_date_d[id] = match.group(7)
      started_log_d[id] = match.group(8)
  fis.close()

if os.path.isfile("report/pass.csv"):
  fip = open("report/pass.csv", "r")
  lines = fip.read().split("\n")
  for line in lines:
    match = re.search('(.*),(.*),(.*),(.*),(.*),(.*),PASS,(.*),(.*),(.*),(.*)',line)
    if match:
      id = match.group(1)+"__"+match.group(2)
      corner=match.group(6)
      bn=match.group(3)
      pass_l[corner,bn].append(id)
      duration = match.group(8)
      pass_tv_d[id] = match.group(9)
      log_d[id] = match.group(10)
      match = re.search('(.*):(.*)\.(.*) sec',duration)
      if match:
        pass_time_d[id] = str(float(match.group(1))*60+float(match.group(2)))
      else:
        match = re.search('(.*)\.(.*) sec',duration)
        if match:
          pass_time_d[id] = str(float(match.group(1)))
        else:
          pass_time_d[id] = 0  
  fip.close()

if pfound:
  if os.path.isfile(latest+"/pass.csv"):
    fip = open(latest+"/pass.csv", "r")
    lines = fip.read().split("\n")
    for line in lines:
      match = re.search('(.*),(.*),(.*),(.*),(.*),(.*),PASS,(.*),(.*),(.*),(.*)',line)
      if match:
        id = match.group(1)+"__"+match.group(2)
        corner=match.group(6)
        bn=match.group(3)
        pass_p_l[corner,bn].append(id)
        duration = match.group(8)
        match = re.search('(.*):(.*)\.(.*) sec',duration)
        if match:
          pass_p_time_d[id] = str(float(match.group(1))*60+float(match.group(2)))
        else:
          match = re.search('(.*)\.(.*) sec',duration)
          if match:
            pass_p_time_d[id] = str(float(match.group(1)))
          else:
            pass_p_time_d[id] = 0  
    fip.close()



  
if os.path.isfile("report/fail.csv"):
  fif = open("report/fail.csv", "r")
  lines = fif.read().split("\n")
  for line in lines:
    match = re.search('(.*),(.*),(.*),(.*),(.*),(.*),FAIL,(.*),(.*).(.*),(.*)',line)
    if match:
      #hermes_top,testcase016 ,${rrrunargs},rtl,FAIL,1:13.812 sec,${errmsg},
      id = match.group(1)+"__"+match.group(2)
      bn=match.group(3)
      corner = match.group(6)
      duration = match.group(7)
      reason_d[id] = match.group(8)
      fail_tv_d[id] = match.group(9)
      log_d[id] = match.group(10)
      fail_l[corner,bn].append(id)
      match = re.search('(.*):(.*)\.(.*) sec',duration)
      if match:
        fail_time_d[id] = str(float(match.group(1))*60+float(match.group(2)))
      else:
        match = re.search('(.*)\.(.*) sec',duration)
        if match:
          fail_time_d[id] = str(float(match.group(1)))
        else:
          fail_time_d[id] = 0  
  fif.close()

if pfound:
  if os.path.isfile(latest+"/fail.csv"):
    fif = open(latest+"/fail.csv", "r")
    lines = fif.read().split("\n")
    for line in lines:
      match = re.search('(.*),(.*),(.*),(.*),(.*),(.*),FAIL,(.*),(.*),(.*)',line)
      if match:
        id = match.group(1)+"__"+match.group(2)
        bn=match.group(3)
        duration = match.group(7)
        reason_d[id] = match.group(8)
        log_p_d[id] = match.group(9)
        fail_p_l[corner,bn].append(id)
        match = re.search('(.*):(.*)\.(.*) sec',duration)
        if match:
          fail_p_time_d[id] = str(float(match.group(1))*60+float(match.group(2)))
        else:
          match = re.search('(.*)\.(.*) sec',duration)
          if match:
            fail_p_time_d[id] = str(float(match.group(1)))
          else:
            fail_p_time_d[id] = 0  
    fif.close()

if os.path.isfile("report/timeout.csv"):
  fif = open("report/timeout.csv", "r")
  lines = fif.read().split("\n")
  for line in lines:
    match = re.search('(.*),(.*),(.*),(.*),(.*),(.*),TIMEOUT,(.*),(.*),(.*),(.*)',line)
    if match:
      id = match.group(1)+"__"+match.group(2)
      corner=match.group(6)
      bn=match.group(3)
      duration = match.group(8)
      log_d[id] = match.group(9)
      timeout_l[corner,bn].append(id)
      timeout_tv_d[id] = match.group(9)
      match = re.search('(.*):(.*)\.(.*) sec',duration)
      if match:
        timeout_time_d[id] = str(float(match.group(1))*60+float(match.group(2)))
      else:
        match = re.search('(.*)\.(.*) sec',duration)
        if match:
          timeout_time_d[id] = str(float(match.group(1)))
        else:
          timeout_time_d[id] = str(0)  
  fif.close()

if os.path.isfile("report/disabled.csv"):
  f = open("report/disabled.csv", "r")
  lines = f.read().split("\n")
  for line in lines:  
    match = re.search('(.*),(.*),(.*),(.*),(.*),(.*),DISABLED,(.*),(.*),(.*)',line)
    if match:
      id = match.group(1)+"__"+match.group(2)
      corner=match.group(6)
      bn=match.group(3)
      duration = match.group(8)
      reason_d[id] = match.group(7)
      disabled_l[corner,bn].append(id)
      log_d[id] = match.group(8)
      match = re.search('(.*):(.*)\.(.*) sec',duration)
      if match:
        disabled_time_d[id] = str(float(match.group(1))*60+float(match.group(2)))
      else:
        match = re.search('(.*)\.(.*) sec',duration)
        if match:
          disabled_time_d[id] = str(float(match.group(1)))
        else:
          disabled_time_d[id] = 0  
  f.close()

if os.path.isfile("report/duplicate.csv"):
  f = open("report/duplicate.csv", "r")
  lines = f.read().split("\n")
  for line in lines:  
    #hermes_top_uvm_tb,pass_detect_test ,_octaveon_iteration2_seed0,rtl,DUPLICATE,20170323_080222
    match = re.search('(.*),(.*),(.*),(.*),(.*),(.*),DUPLICATE,(.*)',line)
    if match:
      id = match.group(1)+"__"+match.group(2)
      corner=match.group(6)
      bn=match.group(3)
      duration = 0
      reason_d[id] = match.group(7)
      duplicate_l[corner,bn].append(id)
      duplicate_time_d[id] = 0 
  f.close()
  
fo = open("report/report.xml", "w")  
fo.write('<?xml-stylesheet href="../../../shared/utils/report.xsl" type="text/xsl"?>\n')

tests = 0
passed = 0
disabled = 0
duplicate = 0
failures = 0

for corner in corners_l:
  for bn in bns_l:
    tests=tests+len(started_l[corner,bn]+disabled_l[corner,bn])
    passed=passed+len(pass_l[corner,bn])
    disabled=disabled+len(disabled_l[corner,bn])
    duplicate=duplicate+len(duplicate_l[corner,bn])
    failures=failures+len(started_l[corner,bn])-len(pass_l[corner,bn])
    
    

unknowns = 0    
unknowns_l = {}
for corner in corners_l:
  for bn in bns_l:
    unknowns_l[corner,bn] = 0
    if len(started_l[corner,bn])+len(disabled_l[corner,bn])>0 :
      for started_i in started_l[corner,bn]:
        if not started_i in fail_l[corner,bn]:
          if not started_i in pass_l[corner,bn]:
            if not started_i in timeout_l[corner,bn]:
              if not started_i in disabled_l[corner,bn]:
                unknowns = unknowns + 1
                unknowns_l[corner,bn] = unknowns_l[corner,bn] + 1


fixed = 0
broken = 0
for corner in corners_l:
  for bn in bns_l:
    fixed_l[corner,bn] = 0
    for pass_i in pass_l[corner,bn]:
      if pass_i in fail_p_l[corner,bn]:
        fixed_l[corner,bn] = fixed_l[corner,bn] + 1
        fixed = fixed + 1
    broken_l[corner,bn] = 0
    for fail_i in fail_l[corner,bn]:
      if fail_i in pass_p_l[corner,bn]:
        broken_l[corner,bn] = broken_l[corner,bn] + 1
        broken = broken + 1

if tests-duplicate > 0:
  fo.write('<testsuites name="testsuites" size="'+sys.argv[1]
    +'" machine="'+sys.argv[2]
    +'" job="'+job
    +'" build="'+sys.argv[3]
    +'" cover="'+sys.argv[4]
    +'" svn="'+sys.argv[5]
    +'" tests="'+str(tests)
    +'" pass="'+str(passed)
    +'" passrate="'+str(passed*100/(tests))
    +'" disabled="'+str(disabled)
    +'" duplicate="'+str(duplicate)
    +'" unknowns="'+str(unknowns)
    +'" fixed="'+str(fixed)
    +'" broken="'+str(broken)
    +'" failures="'+str(failures)+'">\n')
else:
  fo.write('<testsuites name="testsuites" size="'+sys.argv[1]
    +'" machine="'+sys.argv[2]
    +'" job="'+job
    +'" build="'+sys.argv[3]
    +'" cover="'+sys.argv[4]
    +'" tests="'+str(tests)
    +'" pass="'+str(passed)
    +'" disabled="'+str(disabled)
    +'" duplicate="'+str(duplicate)
    +'" unknowns="'+str(unknowns)
    +'" fixed="'+str(fixed)
    +'" broken="'+str(broken)
    +'" failures="'+str(failures)+'">\n')


for corner in corners_l:
  for bn in bns_l:
    if len(started_l[corner,bn])+len(disabled_l[corner,bn])>0 :
      if len(started_l[corner,bn]) > 0:
        fo.write('  <testsuite  name="'+bn+'@'+corner+
        '" tests="'+str(len(started_l[corner,bn])+len(disabled_l[corner,bn]))+ 
        '" pass="'+str(len(pass_l[corner,bn]))+ 
        '" passrate="'+str(len(pass_l[corner,bn])*100/len(started_l[corner,bn]))+ 
        '" disabled="'+str(len(disabled_l[corner,bn]))+ 
        '" duplicate="'+str(len(duplicate_l[corner,bn]))+ 
        '" unknowns="'+str(unknowns_l[corner,bn])+ 
        '" fixed="'+str(fixed_l[corner,bn])+ 
        '" broken="'+str(broken_l[corner,bn])+ 
        '" failures="'+str(len(started_l[corner,bn])-len(pass_l[corner,bn]))+'">\n')
      else:
        fo.write('  <testsuite  name="'+bn+'@'+corner+
        '" tests="'+str(len(started_l[corner,bn])+len(disabled_l[corner,bn]))+ 
        '" pass="'+str(len(pass_l[corner,bn]))+ 
        '" disabled="'+str(len(disabled_l[corner,bn]))+ 
        '" duplicate="'+str(len(duplicate_l[corner,bn]))+ 
        '" unknowns="'+str(unknowns_l[corner,bn])+ 
        '" fixed="'+str(fixed_l[corner,bn])+ 
        '" broken="'+str(broken_l[corner,bn])+ 
        '" failures="'+str(len(started_l[corner,bn])-len(pass_l[corner,bn]))+'">\n')      
      for pass_i in pass_l[corner,bn]:
        match = re.search('(.*)__(.*)',pass_i)
        tgt = match.group(1)
        seed = match.group(2)
        if pass_i in pass_p_l[corner,bn]:
          fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="pass.still" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+bn+'" time="'+pass_time_d[pass_i]+'" tv="'+pass_tv_d[pass_i]+'" log="'+log_d[pass_i]+'">\n')
        else:
          if pass_i in fail_p_l[corner,bn]:
            fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="pass.fixed" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+bn+'" time="'+pass_time_d[pass_i]+'" tv="'+pass_tv_d[pass_i]+'" log="'+log_d[pass_i]+'">\n')
          else:
            fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="pass.tbd" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+bn+'" time="'+pass_time_d[pass_i]+'" tv="'+pass_tv_d[pass_i]+'" log="'+log_d[pass_i]+'">\n')
        #fo.write('      <system-out>\n')
        #fo.write('      </system-out>\n')
        fo.write('    </testcase>\n')
      for fail_i in fail_l[corner,bn]:
        match = re.search('(.*)__(.*)',fail_i)
        tgt = match.group(1)
        seed = match.group(2)
        rn = reason_d[fail_i]
        if fail_i in pass_p_l[corner,bn]:
          fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="fail.broken" reason="'+rn+'" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+bn+'" time="'+fail_time_d[fail_i]+'" tv="'+fail_tv_d[fail_i]+'" log="'+log_d[fail_i]+'">\n')
        else:
          if fail_i in fail_p_l[corner,bn]:
            fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="fail.still" reason="'+rn+'" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+bn+'" time="'+fail_time_d[fail_i]+'" tv="'+fail_tv_d[fail_i]+'" log="'+log_d[fail_i]+'">\n')
          else:
            fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="fail.tbd" reason="'+rn+'" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+bn+'" time="'+fail_time_d[fail_i]+'" tv="'+fail_tv_d[fail_i]+'" log="'+log_d[fail_i]+'">\n')
        fo.write('      <failure message="Failed with fail status"/>\n')
        fo.write('  <system-out>\n')
        fo.write('  </system-out>\n')
        fo.write('</testcase>\n')
      for timeout_i in timeout_l[corner,bn]:
        match = re.search('(.*)__(.*)',timeout_i)
        tgt = match.group(1)
        seed = match.group(2)
        fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="fail.timeout" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+bn+'" time="'+timeout_time_d[timeout_i]+'" tv="'+timeout_tv_d[timeout_i]+'" log="'+log_d[timeout_i]+'">\n')
        fo.write('      <failure message="Time out"/>\n')
        fo.write('    </testcase>\n')
      for disabled_i in disabled_l[corner,bn]:
        match = re.search('(.*)__(.*)',disabled_i)
        tgt = match.group(1)
        seed = match.group(2)
        rn = reason_d[disabled_i]
        fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="disabled" reason="'+rn+'" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+bn+'" time="0">\n')
        fo.write('      <skipped/>\n')
        fo.write('    </testcase>\n')
      for duplicate_i in duplicate_l[corner,bn]:
        match = re.search('(.*)__(.*)',duplicate_i)
        tgt = match.group(1)
        seed = match.group(2)
        rn = reason_d[duplicate_i]
        fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="duplicate" reason="Skipped" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+bn+'" time="0">\n')
        fo.write('      <skipped/>\n')
        fo.write('    </testcase>\n')
      for started_i in started_l[corner,bn]:
        if not started_i in fail_l[corner,bn]:
          if not started_i in pass_l[corner,bn]:
            if not started_i in timeout_l[corner,bn]:
              if not started_i in disabled_l[corner,bn]:
                match = re.search('(.*)__(.*)',started_i)
                tgt = match.group(1)
                seed = match.group(2)
                fo.write('    <testcase name="'+tgt+'_'+seed+'" classname="unknown" reason="started/not finished" corner="'+corner+'" target="'+tgt+'" seed="'+seed+'" basename="'+bn+'" time="'+started_date_d[started_i]+'" log="'+started_log_d[started_i]+'">\n')
                fo.write('      <failure message="Started but no pass/fail status found. Started at:'+started_date_d[started_i]+'"/>\n')
                fo.write('  <system-out>\n')
                fo.write('  </system-out>\n')
                fo.write('</testcase>\n')
      fo.write('  </testsuite>\n')
fo.write('</testsuites>\n')
fo.close()
