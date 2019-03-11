<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE xsl:stylesheet  [
	<!ENTITY nbsp   "&#160;">
]>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="utf-8"/>
<xsl:template match="/">
<html>&nbsp;
<head>&nbsp;
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>&nbsp;
<title>Test report</title>&nbsp;
<link type="text/css" rel="stylesheet" href="css/.urg.css"/>&nbsp;
<link type="text/css" rel="stylesheet" href="css/.layout.css"/>&nbsp;
<script type="text/javascript" src="js/jquery-latest.js"></script>&nbsp;
<script type="text/javascript" src="js/jquery.tablesorter.min.js"></script>&nbsp;
<!-- script type="text/javascript">
	$(function() {
		$("#summary").tablesorter({sortList:[[0,0],[2,1]], widgets: ['zebra']});
		$("#detail").tablesorter({sortList:[[0,0],[2,1]], widgets: ['zebra']});
		$("#options").tablesorter({sortList: [[0,0]], headers: { 3:{sorter: false}, 4:{sorter: false}}});
	});
</script-->
<script type="text/javascript" src="js/.colResizable.js"></script>&nbsp;
<script type="text/javascript" src="js/.layout.js"></script>&nbsp;
<script type="text/javascript">&nbsp;
$(document).ready(function() 
    { 
        $("#detail").tablesorter( {sortList: [[0,0], [1,0]]} ); 
    } 
); 
</script>&nbsp;
</head>&nbsp;
<style>&nbsp;
.cl { width: 3.2em; }
.rt { text-align: right }
.lf { text-align: left }
.ct { text-align: center }
.code { font-size: larger; font-weight: bold }
.sortablehead{ color: #222222; font-size: .7em; font-weight: bold; height: 23px; }
.sortablehead, .sortablehead td, .sortablehead:hover td { background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAABkEAAAAAAy19n/AAAAAmJLR0T//xSrMc0AAAAJcEhZcwAAAEgAAABIAEbJaz4AAABaSURBVBjTY3h8jYFOaAPDo/cMj/QYHu
YyPGhjuF/BcC+L4W4swx0NhltfGG7uZ7jRzXA9nOGaEsOV4wyXdzJcamW4WM5wYQLD+SaGcwcZzt5iOOvAcObMACIAsZae6pVZewYAAAAldEVYdGRhdGU6Y3JlYXRlADIwMTQtMDItMjNUMTg6NTU6MTQtMDg6MDDU4lRpAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDE0LTAyLTIzVDE4OjU1OjE0LTA4OjAwpb
/s1QAAAABJRU5ErkJggg==); background-repeat: repeat-x; background-size: 100% 100%; -moz-background-size: 100% 100%; -o-background-size: 100% 100%; -webkit-background-size: 100% 100%; }
.sortablehead td A:link { color: #222222; }
.sortablehead td A:visited { color: #222222; }
.sortablehead td A:hover { color: red; }
.pagetitle { font-weight: bold; font-size: 22pt }
.clr { color: 000000; background-color: #ffffff }
.wht { color: 000000; background-color: #f0f0f0 }
.uGreen { color: #00ff00 }
.uRed { color: #ff0000 }
.fvGreen { color: 000000; background-color: #00ff00 }
.fvYellow { color: 000000; background-color: #ffff00 }
.fvRed { color: 000000; background-color: #ff0000 }
.s0 { color: ffffff; background-color: #FF0033 }
.s1 { color: ffffff; background-color: #FF0033 }
.s2 { color: 000000; background-color: #FFB5A1 }
.s3 { color: 000000; background-color: #FFB5A1 }
.s4 { color: 000000; background-color: #FFE680 }
.s5 { color: 000000; background-color: #FFE680 }
.s6 { color: 000000; background-color: #FFFF52 }
.s7 { color: 000000; background-color: #FFFF52 }
.s8 { color: 000000; background-color: #B8FFB8 }
.s9 { color: 000000; background-color: #B8FFB8 }
.s10 { color: 000000; background-color: #52FF52 }
</style>&nbsp;
<body>&nbsp;
<br/>
Machine      : <xsl:value-of select="testsuites/@machine"/>
<br/>
Jenkins build:<xsl:value-of select="testsuites/@build"/>
<br/>
SVN revision :<xsl:value-of select="testsuites/@svn"/>
<br/>
Coverage     :<xsl:value-of select="testsuites/@cover"/>
<xsl:for-each select="testsuites">
<br/>Full sortable report :<a href="{concat(@urlroot,'/job/',@job,'/ws/testbench/all/report_',@build,'/report.html')}">Here</a>&nbsp;
<xsl:choose>
<xsl:when test="@cover='on'">
<br/>Coverage report      :<a href="{concat(@urlroot,'/job/',@job,'/ws/testbench/all/cov/rpt/')}">Here</a>&nbsp;
</xsl:when>
</xsl:choose>
<br/>Trend chart          :<a href="{concat(@urlroot,'/job/',@job,'/test/trend')}">Here</a>&nbsp;
<br/>
</xsl:for-each>
<table id="summary" style="border-width:1px; border-style:solid; border-color:black">&nbsp;
  <thead>&nbsp;
  <tr style="border-width:1px; border-style:solid; border-color:black">&nbsp;
    <th scope="col">Name</th>&nbsp;
    <th scope="col">Passrate</th>&nbsp;
    <th scope="col">Total</th>&nbsp;
    <th scope="col">Pass</th>&nbsp;
    <th scope="col">Disabled</th>&nbsp;
    <th scope="col">Failure</th>&nbsp;
    <th scope="col">Unknown</th>&nbsp;
    <th scope="col">Duplicate</th>&nbsp;
    <th scope="col">Fixed</th>&nbsp;
    <th scope="col">Broken</th>&nbsp;
  </tr>&nbsp;
  </thead>&nbsp;
  <tbody>&nbsp;
  <tr style="border-width:1px; border-style:solid; border-color:black">&nbsp;
    <td align="right"><xsl:value-of select="All"/></td>&nbsp;
    <td align="right"><xsl:value-of select="testsuites/@passrate"/>%</td>&nbsp;
    <td align="right"><xsl:value-of select="testsuites/@tests"/></td>&nbsp;
    <td align="right"><xsl:value-of select="testsuites/@pass"/></td>&nbsp;
    <td align="right"><xsl:value-of select="testsuites/@disabled"/></td>&nbsp;
    <td align="right"><xsl:value-of select="testsuites/@failures"/></td>&nbsp;
    <td align="right"><xsl:value-of select="testsuites/@unknowns"/></td>&nbsp;
    <td align="right"><xsl:value-of select="testsuites/@duplicate"/></td>&nbsp;
    <td align="right"><xsl:value-of select="testsuites/@fixed"/></td>&nbsp;
    <td align="right"><xsl:value-of select="testsuites/@broken"/></td>&nbsp;
  </tr>&nbsp;
  <xsl:for-each select="testsuites/testsuite">
  <xsl:choose>
  <xsl:when test="@failures &gt; 0">
  <tr style="width: 3.2em; color: #ffffff; background-color: #FF0033; border-width:1px; border-style:solid; border-color:black">&nbsp;
    <td align="right"><xsl:value-of select="@name"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@passrate"/>%</td>&nbsp;
    <td align="right"><xsl:value-of select="@tests"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@pass"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@disabled"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@failures"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@unknowns"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@duplicate"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@fixed"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@broken"/></td>&nbsp;
  </tr>&nbsp;
  </xsl:when>
  <xsl:when test="@disabled &gt; 0">
  <tr style="width: 3.2em; background-color: #FFE680; border-width:1px; border-style:solid; border-color:black">&nbsp;
    <td align="right"><xsl:value-of select="@name"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@passrate"/>%</td>&nbsp;
    <td align="right"><xsl:value-of select="@tests"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@pass"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@disabled"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@failures"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@unknowns"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@duplicate"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@fixed"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@broken"/></td>&nbsp;
  </tr>&nbsp;
  </xsl:when>
  <xsl:otherwise>
  <tr style="width: 3.2em; background-color: #B8FFB8; border-width:1px; border-style:solid; border-color:black">&nbsp;
    <td align="right"><xsl:value-of select="@name"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@passrate"/>%</td>&nbsp;
    <td align="right"><xsl:value-of select="@tests"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@pass"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@disabled"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@failures"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@unknowns"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@duplicate"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@fixed"/></td>&nbsp;
    <td align="right"><xsl:value-of select="@broken"/></td>&nbsp;
  </tr>&nbsp;
  </xsl:otherwise>
  </xsl:choose>
  </xsl:for-each>
  </tbody>&nbsp;
</table>&nbsp;
<p>Make sure to scroll down....</p>
<table id="detail" class="tablesorter" style="border-width:1px; border-style:solid; border-color:black">&nbsp;
  <thead>&nbsp;
  <tr style="border-width:1px; border-style:solid; border-color:black; width:50%">&nbsp;
    <th scope="col" align="right" style="white-space:nowrap" width="400">Target</th>&nbsp;
    <th scope="col" align="right" style="white-space:nowrap" width="60">Seed</th>&nbsp;
    <th scope="col" align="right" style="white-space:nowrap" width="100">Basename</th>&nbsp;
    <th scope="col" align="right" style="white-space:nowrap" width="60">Corner</th>&nbsp;
    <th scope="col" align="right" style="white-space:nowrap" width="60">Violation</th>&nbsp;
    <th scope="col" align="right" style="white-space:nowrap" width="100">Status</th>&nbsp;
    <th scope="col" align="right" style="white-space:nowrap" width="40">Duration</th>&nbsp;
    <th scope="col" align="right" style="white-space:nowrap" width="150">Log/Message</th>&nbsp;
  </tr>&nbsp;
  </thead>&nbsp;
  <tbody>&nbsp;
  <xsl:for-each select="testsuites/testsuite/testcase">
  <xsl:choose>
  <xsl:when test="@classname='pass'">
  <tr style="width: 3.2em; color: 000000; background-color: #B8FFB8; border-width:1px; border-style:solid; border-color:black">&nbsp;
  <td align="left">
    <a href="{concat(@log,'.html')}"><xsl:value-of select="@target"/></a>&nbsp;
  </td>&nbsp;
  <td align="right"><xsl:value-of select="@seed"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@basename"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@corner"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@tv"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@classname"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@time"/></td>&nbsp;
  <td align="right">Success</td>&nbsp;
  </tr>&nbsp;
  </xsl:when>
  <xsl:when test="@classname='pass.fixed'">
  <tr style="font-weight: bold; width: 3.2em; color: 000000; background-color: #B8FFB8; border-width:1px; border-style:solid; border-color:black">&nbsp;
  <td align="left">
    <a href="{concat(@log,'.html')}"><xsl:value-of select="@target"/></a>&nbsp;
  </td>&nbsp;
  <td align="right"><xsl:value-of select="@seed"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@basename"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@corner"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@tv"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@classname"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@time"/></td>&nbsp;
  <td align="right">Fixed</td>&nbsp;
  </tr>&nbsp;
  </xsl:when>
  <xsl:when test="@classname='pass.unchanged'">
  <tr style="width: 3.2em; color: 000000; background-color: #B8FFB8; border-width:1px; border-style:solid; border-color:black">&nbsp;
  <td align="left">
    <a href="{concat(@log,'.html')}"><xsl:value-of select="@target"/></a>&nbsp;
  </td>&nbsp;
  <td align="right"><xsl:value-of select="@seed"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@basename"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@corner"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@tv"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@classname"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@time"/></td>&nbsp;
  <td align="right">Success</td>&nbsp;
  </tr>&nbsp;
  </xsl:when>
  <xsl:when test="@classname='pass.tbd'">
  <tr style="width: 3.2em; color: 000000; background-color: #B8FFB8; border-width:1px; border-style:solid; border-color:black">&nbsp;
  <td align="left">
    <a href="{concat(@log,'.html')}"><xsl:value-of select="@target"/></a>&nbsp;
  </td>&nbsp;
  <td align="right"><xsl:value-of select="@seed"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@basename"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@corner"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@tv"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@classname"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@time"/></td>&nbsp;
  <td align="right">Success</td>&nbsp;
  </tr>&nbsp;
  </xsl:when>
  <xsl:when test="@classname='fail.tbd'">
  <tr style="width: 3.2em; color: #ffffff; background-color: #FF0033; border-width:1px; border-style:solid; border-color:black">&nbsp;
  <td align="left">
  <a href="{concat(@log,'.html')}"><xsl:value-of select="@target"/></a>&nbsp;
  </td>&nbsp;
  <td align="right"><xsl:value-of select="@seed"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@basename"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@corner"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@tv"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@classname"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@time"/></td>&nbsp;
  <td align="right">Fail</td>&nbsp;
  </tr>&nbsp;
  </xsl:when>
  <xsl:when test="@classname='fail.unchanged'">
  <xsl:variable name="color" select="ffffff" />
  <tr color="$color" style="width: 3.2em; background-color: #FF0033; border-width:1px; border-style:solid; border-color:black">&nbsp;
  <td align="left">
  <a href="{concat(@log,'.html')}"><xsl:value-of select="@target"/></a>&nbsp;
  </td>&nbsp;
  <td align="right"><xsl:value-of select="@seed"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@basename"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@corner"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@tv"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@classname"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@time"/></td>&nbsp;
  <td align="right">
  </td>&nbsp;
  </tr>&nbsp;
  </xsl:when>
  <xsl:when test="@classname='fail.broken'">
  <tr style="font-weight: bold; width: 3.2em; color: #ffffff; background-color: #FF0033; border-width:1px; border-style:solid; border-color:black">&nbsp;
  <td align="left">
  <a href="{concat(@log,'.html')}"><xsl:value-of select="@target"/></a>&nbsp;
  </td>&nbsp;
  <td align="right"><xsl:value-of select="@seed"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@basename"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@corner"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@tv"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@classname"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@time"/></td>&nbsp;
  <td align="right">Broken</td>&nbsp;
  </tr>&nbsp;
  </xsl:when>
  <xsl:when test="@classname='timeout.tbd'">
  <tr style="width: 3.2em; color: #000000; background-color: #FFB5A1; border-width:1px; border-style:solid; border-color:black">&nbsp;
  <td align="left">
  <a href="{concat(@log,'.html')}"><xsl:value-of select="@target"/></a>&nbsp;
  </td>&nbsp;
  <td align="right"><xsl:value-of select="@seed"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@basename"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@corner"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@tv"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@classname"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@time"/></td>&nbsp;
  <td align="right">Timeout</td>&nbsp;
  </tr>&nbsp;
  </xsl:when>
  <xsl:when test="@classname='timeout.unchanged'">
  <tr style="width: 3.2em; color: #000000; background-color: #FFB5A1; border-width:1px; border-style:solid; border-color:black">&nbsp;
  <td align="left">
  <a href="{concat(@log,'.html')}"><xsl:value-of select="@target"/></a>&nbsp;
  </td>&nbsp;
  <td align="right"><xsl:value-of select="@seed"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@basename"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@corner"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@tv"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@classname"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@time"/></td>&nbsp;
  <td align="right">Timeout</td>&nbsp;
  </tr>&nbsp;
  </xsl:when>
  <xsl:when test="@classname='disabled'">
  <tr style="width: 3.2em; color: #000000; background-color: #FFE680; border-width:1px; border-style:solid; border-color:black">&nbsp;
  <td align="left"><xsl:value-of select="@target"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@seed"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@basename"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@corner"/></td>&nbsp;
  <td align="right">N/A</td>&nbsp;
  <td align="right"><xsl:value-of select="@classname"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@time"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@reason"/></td>&nbsp;
  </tr>&nbsp;
  </xsl:when>
  <xsl:when test="@classname='duplicate'">
  <tr style="width: 3.2em; color: #ffffff; background-color: #606060; border-width:1px; border-style:solid; border-color:black">&nbsp;
  <td align="left"><xsl:value-of select="@target"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@seed"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@basename"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@corner"/></td>&nbsp;
  <td align="right">N/A</td>&nbsp;
  <td align="right"><xsl:value-of select="@classname"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@time"/></td>&nbsp;
  <td align="right">Skipped</td>&nbsp;
  </tr>&nbsp;
  </xsl:when>
  <xsl:otherwise>
  <tr style="width: 3.2em; color: #000000; background-color: #f0f0f0; border-width:1px; border-style:solid; border-color:black">&nbsp;
  <td align="left">
  <a href="{concat(@log,'.log')}"><xsl:value-of select="@target"/></a>&nbsp;
  </td>&nbsp;
  <td align="right"><xsl:value-of select="@seed"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@basename"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@corner"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@tv"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@classname"/></td>&nbsp;
  <td align="right"><xsl:value-of select="@time"/></td>&nbsp;
  <td align="right">Unknown</td>&nbsp;
  </tr>&nbsp;
  </xsl:otherwise>
  </xsl:choose>
  </xsl:for-each>
  </tbody>&nbsp;
</table>&nbsp;
</body>&nbsp;
</html>&nbsp;
</xsl:template>
</xsl:stylesheet>

