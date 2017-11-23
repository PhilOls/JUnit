JUnit allows creation of a custom test report in JUnit xml format from csv delimited files
Direct access to test log is provided by clicking on the testname.

For an example of generated report:
http://htmlpreview.github.io/?https://github.com/PhilOls/JUnit/blob/master/JUnit/example/report/report.html

JUnit can be used with continuous integration tools like Jenkins, Bamboo and point to stored artifacts for each build

----------------------------------
The format of each csv file is the same.Each line consists in:
target,seed,testbench,reason,corner,starttime,duration,logpath,violation

where:
	- target: test name
	- seed: integer reflecting seed used
	- testbench: testbench in which test was run
	- reason: multiple usage. 
		> timeout: can indicate what timeout fired (UVM phase timeout, Ant exec timeout,...) 
		> disabled: user information to indficate whyb test is currently disabled
	- corner: corner used, most commonly rtl (can also be best, typ, worst, etc....)
	- starttime: start time+date when test kicked
	- duration: duration of test in sec
	- logpath: path to test logfile
	- violation: counts of violation (mostly relevant for gate-level)
	
-------
Recommended tooling
	Shell-based
		> cd JUnit 
		> ant
	

