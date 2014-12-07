#!/usr/bin/perl
# 
# Calendar Admin Script
#
# Matt Kruse
# http://mkruse.netexpress.net/
#

$|=1;
print "Content-type: text/html\n\n";

# $base_dir = "";

&GetCwd;
&ReadParse;
&read_config;
$vars{"cgi"} = $ENV{'SCRIPT_NAME'};
&INITIALIZE;

# Routine to get working directory
# --------------------------------
sub GetCwd {
	if ($base_dir) { $vars{base_dir} = $base_dir; }
	return if $vars{base_dir};
	my $path =  $ENV{'PATH_TRANSLATED'} || $ENV{'SCRIPT_FILENAME'};
	unless ($path) {
		&Error("Your server does not provide the PATH_TRANSLATED or SCRIPT_FILENAME environment variables.");
		exit(0);
		}
	$path =~ s|[^/\\]*$||;
	$vars{base_dir} = $path;
	}

# Generate general variables
# --------------------------
$vars{'month'} = $in{'Month'} || $month;
$vars{'year'} = $in{'Year'} || $year;
$vars{'date'} = $in{'Date'};
if (!$vars{date} && $vars{month}==$month && $vars{year}==$year) {
	$vars{date} = $mday;
	}
$vars{'type'} = $DefaultType; 
$vars{'monthname'} = @months[int($vars{'month'})-1];
$vars{'datestamp'} = sprintf("%4.4d%2.2d%2.2d",$vars{year},$vars{month},$vars{date});

$vars{lastyear}  = $vars{year};
$vars{nextyear}  = $vars{year};
$vars{lastmonth} = $vars{month}-1;
$vars{nextmonth} = $vars{month}+1;
if ($vars{lastmonth} < 1) { $vars{lastmonth}=12; $vars{lastyear}--; }
if ($vars{nextmonth} > 12){ $vars{nextmonth}=1;  $vars{nextyear}++; }
$vars{lastmonthname} = @months[int($vars{lastmonth})-1];
$vars{nextmonthname} = @months[int($vars{nextmonth})-1];

#####################################################################
#
# Decide what to do based on the ACTION parameter
#
#####################################################################
if ($in{"ACTION"} eq "EVENTDETAILS") {
	&EVENTDETAILS;
	}
unless ($in{"OK"} eq "OK") { 
	&SPLASH;
	}
unless ( ($in{"username"} eq $vars{username}) && ($in{"password"} eq $vars{password})) {
	print "Username and/or password invalid";
	exit(0);
	}
if ($in{"ACTION"} eq "DO_UPDATE_FORMAT") {
	&DO_UPDATE_FORMAT;
	}

# Check file format before doing anything else
&read_cal_data;
	
if ($in{"ACTION"} eq "EDIT") {
	&EDIT;
	}
if ($in{"ACTION"} eq "DO_EDIT") {
	&DO_EDIT;
	}
if ($in{"ACTION"} eq "SAVE_EDIT") {
	&SAVE_EDIT;
	}
elsif ($in{"ACTION"} eq "ADD") {
	&ADD;
	}
elsif ($in{"ACTION"} eq "DO_ADD") {
	&DO_ADD;
	}
elsif ($in{"ACTION"} eq "UPDATE") {
	&UPDATE;
	}
elsif ($in{"ACTION"} eq "OPTIONS") {
	&OPTIONS;
	}
else {
	&ADMIN;
	}
exit(0);

#####################################################################
#
# SPLASH()
#
# Splash Screen
#
#####################################################################
sub SPLASH {
	print <<"END";
<HTML>
<HEAD><TITLE>Calendar Administration</TITLE></HEAD>
<BODY BGCOLOR=white onLoad="document.forms[0].username.focus();">
<BR><BR>
<CENTER>
<TABLE BORDER=1 BORDERCOLOR="#333333" CELLSPACING=0 WIDTH=400 CELLPADDING=3>
<TR>
	<TD ALIGN=CENTER BGCOLOR="#000080"><FONT COLOR="white" SIZE="+1"><B>Calendar Administration</B></FONT></TD>
</TR>
<TR>
	<TD BGCOLOR="#CCCCCC">
	<B>Author</B>: <A HREF="mailto:mkruse\@netexpress.net">Matt Kruse</A><br>
	<B>Web Site</B>: <A HREF="http://mkruse.netexpress.net/scripts/calendar/">http://mkruse.netexpress.net/scripts/calendar/</A><br>
	<CENTER>
	<BR>
	<B><U>THIS PROGRAM IS FREE SOFTWARE</U></B>
	</CENTER>
	<UL>However...
		<LI>It may not be re-distributed
		<LI>It may not be sold
		<LI>Please put a link to my site on your site
	</UL>
	<CENTER>
	<B><U>THE POSTCARD INITIATIVE</U></B><br>
	</CENTER>
	This program is free, but I would appreciate receiving a postcard from you as a Thank-You for my time. If used for company purposes, a \$50 donation is appreciated.<br><br>
	<CENTER>
	<TABLE BORDER=1>
	<TR><TD>Matt Kruse<br>5510 31st Ave Ct.<br>Moline, IL 61265</TD></TR>
	</TABLE>
	<BR>
	<form action="$vars{cgi}" method=post><input type="hidden" name="OK" value="OK"><tt>
		<b>&nbsp;&nbsp;&nbsp;Login:&nbsp;</b><input name="username" value="" size=10><br>
		<b>Password:&nbsp;</b><input type="password" name="password" value="" size=10><br><br>
		<input type="submit" value="     OK     ">
	</tt></form>
	</CENTER>
	
	</TD>
</TR>
</TABLE>
</BODY>
</HTML>
END
	exit(0);
	}

#####################################################################
#
# ADMIN()
#
# Main Admin page
#
#####################################################################
sub ADMIN {

	if ($vars{viewday_style} eq "popup") { $popup_style = " CHECKED "; }
	else { $inline_style = " CHECKED "; }

	if ($vars{html_heading} eq "yes") { $html_heading = " CHECKED "; }
	if ($vars{html_description} eq "yes") { $html_description= " CHECKED "; }
	
	print <<"END";
<HTML>
<HEAD><TITLE>Calendar Administration</TITLE>
<SCRIPT LANGUAGE="JavaScript">
function showmessage(msg) {
	if (msg != "") {
		alert(msg);
		}
	}
</SCRIPT>
</HEAD>
<BODY BGCOLOR=white onLoad='showmessage("$vars{message}")'>
<BR><BR>
<CENTER>
<TABLE BORDER=1 BORDERCOLOR="#333333" CELLSPACING=0 CELLPADDING=3 WIDTH=500>
<TR>
	<TD ALIGN=CENTER BGCOLOR="#000080"><FONT COLOR="white" SIZE="+1"><B>Calendar Administration</B></FONT></TD>
</TR>
<TR>
	<TD BGCOLOR="#CCCCCC">

	<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=5>
	
	<!-- General Options -->	
	<FORM ACTION=$vars{cgi} METHOD=POST>
	<INPUT TYPE="HIDDEN" NAME="OK" VALUE="OK">
	<INPUT TYPE="HIDDEN" NAME="username" VALUE="$in{username}">
	<INPUT TYPE="HIDDEN" NAME="password" VALUE="$in{password}">
	<INPUT TYPE="HIDDEN" NAME="ACTION" VALUE="OPTIONS">
	<TR>
		<TD ALIGN=RIGHT><B>General&nbsp;Options</B></TD>
		<TD WIDTH=100%><HR SIZE=1></TD>
	</TR>
	<TR>
		<TD COLSPAN=2>
		<BLOCKQUOTE>
			View selected day: <INPUT TYPE="RADIO" NAME="viewday_style" VALUE="inline" $inline_style> On monthly view <INPUT TYPE="RADIO" NAME="viewday_style" VALUE="popup" $popup_style> In pop-up window<br>
			<INPUT TYPE="checkbox" name="html_heading" VALUE="yes" $html_heading> Allow HTML tags in headings<br>
			<INPUT TYPE="checkbox" name="html_description" VALUE="yes" $html_description> Allow HTML tags in descriptions<br>
			Highlight today using <INPUT NAME="bgcolor_today" VALUE="$vars{bgcolor_today}" SIZE=25><br>
			Highlight selected day using <INPUT NAME="bgcolor_current" VALUE="$vars{bgcolor_current}" SIZE=25><br>
			Highlight other days using <INPUT NAME="bgcolor_day" VALUE="$vars{bgcolor_day}" SIZE=25><br>
			<CENTER><INPUT TYPE="submit" value="   Save Options   "></CENTER>
		</BLOCKQUOTE>
		</TD>
	</TR>
	</FORM>
	<TR>
		<TD COLSPAN=2><HR SIZE=1></TD>
	</TR>
	</TABLE>
	
	<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=5 WIDTH=100%>
	<TR>
		<TD ALIGN=CENTER WIDTH=50%>
			<FORM ACTION="$vars{cgi}" METHOD=POST>
			<INPUT TYPE="hidden" NAME="ACTION" VALUE="ADD">
			<INPUT TYPE="HIDDEN" NAME="OK" VALUE="OK">
			<INPUT TYPE="HIDDEN" NAME="username" VALUE="$in{username}">
			<INPUT TYPE="HIDDEN" NAME="password" VALUE="$in{password}">
			<INPUT TYPE="SUBMIT" VALUE="Add Event">
			</FORM>
		</TD>
		<TD ALIGN=CENTER WIDTH=50%>
			<FORM ACTION="$vars{cgi}" METHOD=POST>
			<INPUT TYPE="hidden" NAME="ACTION" VALUE="EDIT">
			<INPUT TYPE="HIDDEN" NAME="OK" VALUE="OK">
			<INPUT TYPE="HIDDEN" NAME="username" VALUE="$in{username}">
			<INPUT TYPE="HIDDEN" NAME="password" VALUE="$in{password}">
			<INPUT TYPE="SUBMIT" VALUE="Edit Events">
			</FORM>
		</TD>
	</TR>
	<TR>
		<TD ALIGN=CENTER COLSPAN=2>
			<FORM METHOD=get ACTION="http://mkruse.netexpress.net/scripts/calendar/feedback/">
			<INPUT TYPE="submit" VALUE="Feedback, Bug Reports, Feature Requests">
			</FORM>
		</TD>
	</TR>
	</TABLE>
	
	</TD>
</TR>
</TABLE>
</BODY>
</HTML>
END
	exit(0);
	} #end of ADMIN

#####################################################################
#
# OPTIONS()
#
# Save Options
#
#####################################################################
sub OPTIONS {
	my $config_file = $vars{base_dir} . "calendar.cfg";
	open(IN,$config_file) || &Error("Can't open $config_file. Does this file even exist?");
	undef $/;
	my $cfg = <IN>;
	close(IN);
	
	foreach (	'viewday_style',
				'html_heading',
				'html_description',
				'bgcolor_today',
				'bgcolor_current',
				'bgcolor_day'			
				) {
		$cfg =~ s|^$_=.*|$_=$in{$_}|mg;
		}

	open(OUT,"> $config_file") || &Error( "Can't open $config_file for writing.");
	flock OUT,2;
	print OUT $cfg;
	close(OUT);
	
	$/ = "\n";
	&read_config;
	$vars{message} = "Options Saved";
	&ADMIN;
	
	} # end of OPTIONS

#####################################################################
#
# ADD()
#
# Form to add an entry
#
#####################################################################
sub ADD {	
	print <<"END";
<HTML>
<HEAD><TITLE>Calendar Administration</TITLE>
<SCRIPT LANGUAGE="JavaScript">
function verifyform() {
	if (document.forms[0].month.value<1 || document.forms[0].month.value>12) {
		alert("Month is invalid");
		return false;
		}
	if (document.forms[0].date.value<1 || document.forms[0].date.value>31) {
		alert("Date is invalid");
		return false;
		}
	if (document.forms[0].year.value<0 || document.forms[0].year.value == "") {
		alert("Year is invalid");
		return false;
		}
	if (document.forms[0].heading.value == "") {
		alert("Heading is required");
		return false;
		}
	if (document.forms[0].description.value == "") { 
		alert("Description is required");
		return false;
		}
	return true;
	} // end of function
function showmessage(msg) {
	if (msg != "") {
		alert(msg);
		}
	}
</SCRIPT>
</HEAD>
<BODY BGCOLOR=white onLoad='showmessage("$vars{message}")'>
<BR><BR>
<CENTER>
<TABLE BORDER=1 BORDERCOLOR="#333333" CELLSPACING=0 CELLPADDING=3 WIDTH=500>
<TR>
	<TD ALIGN=CENTER BGCOLOR="#000080"><FONT COLOR="white" SIZE="+1"><B>Calendar Administration</B></FONT></TD>
</TR>
<TR>
	<TD BGCOLOR="#CCCCCC">

		<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=3>
			<form action="$vars{cgi}" method=post onSubmit="return verifyform();">
			<INPUT TYPE="HIDDEN" NAME="OK" VALUE="OK">
			<INPUT TYPE="HIDDEN" NAME="username" VALUE="$in{username}">
			<INPUT TYPE="HIDDEN" NAME="password" VALUE="$in{password}">
			<input type="hidden" name="ACTION" value="DO_ADD">
			<TR>
				<TD ALIGN=RIGHT><B>Add&nbsp;Event</B></TD>
				<TD WIDTH=100%><HR SIZE=1></TD>
			</TR>			
			<TR>
				<TH BGCOLOR="#CCCCCC">Date</TH>
				<TD BGCOLOR="#CCCCCC">
					<input name="month" size=2 maxlength=2 value="$vars{month}"> / <input name="date" size=2 maxlength=2 value="$vars{date}"> / <input name="year" size=4 maxlength=4 value="$vars{year}">&nbsp;&nbsp;
					<input type="checkbox" name="annual" value="1" onClick="if(form.annual.checked == true){form.year.value='0000'}else{form.year.value=''}"> Every Year
				</TD>
			</TR>
			<TR>
				<TH BGCOLOR="#CCCCCC">Heading</TH>
				<TD BGCOLOR="#CCCCCC"><input name="heading" size=30></TD>
			</TR>
			<TR>
				<TH BGCOLOR="#CCCCCC">Description</TH>
				<TD BGCOLOR="#CCCCCC" COLSPAN=3><textarea name="description" cols=50 rows=3></textarea></TD>
			</TR>
			<TR>
				<TD COLSPAN=2 ALIGN=RIGHT BGCOLOR="#CCCCCC"><input type="reset" value="Clear">&nbsp;&nbsp;&nbsp;<input type="submit" value="Save">
				</form>
				</TD>
			</TR>
			<TR>
				<TD COLSPAN=2><HR SIZE=1></TD>
			</TR>
			<form action="$vars{cgi}" method=post>
			<INPUT TYPE="HIDDEN" NAME="OK" VALUE="OK">
			<INPUT TYPE="HIDDEN" NAME="username" VALUE="$in{username}">
			<INPUT TYPE="HIDDEN" NAME="password" VALUE="$in{password}">
			<TR>
				<TD COLSPAN=2 ALIGN=CENTER><input type="submit" value="Main Menu"></TD>
			</TR>
			</form>
		</TABLE>
	</TD>
</TR>
</TABLE>
</CENTER>
</BODY>
</HTML>
END
	exit(0);
	} #end of ADD

#####################################################################
#
# DO_ADD()
#
# Add an entry
#
#####################################################################
sub DO_ADD {	
	$in{description} =~ s|[\r\n]+|<BR>|gs;
	$in{month} =~ s|^(\d)$|0$1|;
	$in{date}  =~ s|^(\d)$|0$1|;
	my $datestamp = $in{year} . $in{month} . $in{date};
	
	if ($datestamp =~ /^\d\d\d\d\d\d\d\d$/) {
		open(OUT,">> $vars{calendar_file}") || &Error( "Can't open $calendar_file for writing!");
		flock OUT,2;
		print OUT "$vars{new_id}|$datestamp|$in{heading}|$in{description}\n";
		close(OUT);
		$vars{'message'} = "Event Added";
		}
	else {
		$vars{'message'} = "ERROR: Event not added";
		}
	&ADD;
	exit(0);
	} # end of DO_ADD
	
#####################################################################
#
# EDIT()
#
# Edit/Delete Entries
#
#####################################################################
sub EDIT {	
	$monthselected{$vars{month}} = " SELECTED ";
	$yearselected{$vars{year}} = " SELECTED ";
	print <<"END";
<HTML>
<HEAD><TITLE>Calendar Administration</TITLE>
<SCRIPT LANGUAGE="JavaScript">
function eventdetails(id) {
	window.open('$vars{cgi}?ACTION=EVENTDETAILS&id=' + id,'EVENTDETAILS','scrollbars,resizable,height=250,width=400');
	}
function verify() {
	return confirm("Are you sure?");
	}
function showmessage(msg) {
	if (msg != "") {
		alert(msg);
		}
	}
</SCRIPT>
<style>
<!--
 A { text-decoration:none; }
-->
</style>
</HEAD>
<BODY BGCOLOR="#ffffff" LINK="#000080" ALINK="#000080" VLINK="#000080" onLoad='showmessage("$vars{message}");'>
<BR><BR>
<CENTER>
<TABLE BORDER=1 BORDERCOLOR="#333333" CELLSPACING=0 CELLPADDING=3 WIDTH=500>
<TR>
	<TD ALIGN=CENTER BGCOLOR="#000080"><FONT COLOR="white" SIZE="+1"><B>Calendar Administration</B></FONT></TD>
</TR>
<TR>
	<TD BGCOLOR="#CCCCCC">
		<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=3>
			<TR>
				<TD ALIGN=RIGHT><B>Edit&nbsp;Events</B></TD>
				<TD WIDTH=100%><HR SIZE=1></TD>
			</TR>	
		</TABLE>	
		<CENTER>
		<form action="$vars{cgi}" method=post>
		<INPUT TYPE="HIDDEN" NAME="OK" VALUE="OK">
		<INPUT TYPE="HIDDEN" NAME="ACTION" VALUE="EDIT">
		<INPUT TYPE="HIDDEN" NAME="username" VALUE="$in{username}">
		<INPUT TYPE="HIDDEN" NAME="password" VALUE="$in{password}">
		<INPUT TYPE="HIDDEN" NAME="month" VALUE="$vars{lastmonth}">
		<INPUT TYPE="HIDDEN" NAME="year" VALUE="$vars{lastyear}">
		<select name="Month" size=1>
			<option value="1" $monthselected{1}>January
			<option value="2" $monthselected{2}>February
			<option value="3" $monthselected{3}>March
			<option value="4" $monthselected{4}>April
			<option value="5" $monthselected{5}>May
			<option value="6" $monthselected{6}>June
			<option value="7" $monthselected{7}>July
			<option value="8" $monthselected{8}>August
			<option value="9" $monthselected{9}>September
			<option value="10" $monthselected{10}>October
			<option value="11" $monthselected{11}>November
			<option value="12" $monthselected{12}>December
		</select>
		<select name="Year" size=1>
			<option value="1997" $yearselected{1997}>1997
			<option value="1998" $yearselected{1998}>1998
			<option value="1999" $yearselected{1999}>1999
			<option value="2000" $yearselected{2000}>2000
			<option value="2001" $yearselected{2001}>2001
			<option value="2002" $yearselected{2002}>2002
			<option value="2003" $yearselected{2003}>2003
		</select>
		<input type="submit" value="Go"><br>
		</FORM>
		</CENTER>

		<TABLE BORDER=1 CELLSPACING=0 CELLPADDING=3 WIDTH=100%> 
		<form action="$vars{cgi}" method=post onSubmit="return verify();">
		<INPUT TYPE="HIDDEN" NAME="OK" VALUE="OK">
		<INPUT TYPE="HIDDEN" NAME="ACTION" VALUE="DO_EDIT">
		<INPUT TYPE="HIDDEN" NAME="username" VALUE="$in{username}">
		<INPUT TYPE="HIDDEN" NAME="password" VALUE="$in{password}">
		<TR>
			<TD VALIGN=BOTTOM ALIGN=CENTER><B>Date</B></TD>
			<TD VALIGN=BOTTOM ALIGN=CENTER WIDTH=100%><B>Heading</B><br><FONT COLOR=red SIZE=+1>*</FONT> = Annual Event</TD>
			<TD VALIGN=BOTTOM ALIGN=CENTER><B>Action</B></TD>
		</TR>
END
	foreach $datestamp ( sort keys %events ) {
		($year,$month,$date) = ($datestamp =~ /(\d\d\d\d)(\d\d)(\d\d)/o);
		next unless ($month==$vars{month} && ($year==$vars{year}||$year eq "0000"));
		foreach $i ( sort keys %{$events{$datestamp}} ) {
			if ($year eq "0000") { $annual = "<FONT COLOR=red SIZE=+1>*</FONT>"; }
				else { $annual=""; }			
			print "<TR><TD ALIGN=CENTER>${month}/${date}</TD><TD>$annual <A HREF=\"javascript:eventdetails('${$events{$datestamp}}{$i}{id}');\">${$events{$datestamp}}{$i}{label}</A></TD>\n";
			print "    <TD><input type=\"submit\" name=\"ID${$events{$datestamp}}{$i}{id}\" VALUE=\"Edit\">&nbsp;&nbsp;<input type=\"submit\" name=\"ID${$events{$datestamp}}{$i}{id}\" VALUE=\"Delete\"></TD>\n";
			print "</TR>\n";
			}
		}
	print <<"END";
		</form>
		</TABLE>

		<CENTER>
		<form action="$vars{cgi}" method=post>
		<BR>
		<HR SIZE=1>
		<INPUT TYPE="HIDDEN" NAME="OK" VALUE="OK">
		<INPUT TYPE="HIDDEN" NAME="username" VALUE="$in{username}">
		<INPUT TYPE="HIDDEN" NAME="password" VALUE="$in{password}">
			<input type="submit" value="Main Menu">
		</form>
		</CENTER>

	</TD>
</TR>
</TABLE>
</BODY>
</HTML>
END
	exit(0);
	} #end of EDIT

#####################################################################
#
# EVENTDETAILS()
#
# Show details of an event in pop-up window
#
#####################################################################
sub EVENTDETAILS {	
	open(IN,"$vars{calendar_file}") || &Error( "Can't open $vars{calendar_file}");
	my $header = <IN>;
	while (<IN>) {
		chomp;
		($id,$xdatestamp,$label,$description) = split(/\|/,$_,4);
		next unless ($id == $in{id});
		($year,$month,$date) = ($xdatestamp =~ /(\d\d\d\d)(\d\d)(\d\d)/);
		if ($year eq "0000") {
			$year = " (Annual)";
			}
		else {
			$year = ", $year";
			}
		last;
		}
	close(IN);
	print <<"END";	
<HTML>
<HEAD>
	<TITLE>$label</TITLE>
</HEAD>
<BODY BGCOLOR="#ffffff" LINK="#000080" ALINK="#000080" VLINK="#000080" LEFTMARGIN=3 RIGHTMARGIN=3 TOPMARGIN=3 MARGINWIDTH=3 MARGINHEIGHT=3>
<font size="+1" face="verdana,arial">$label</font><br>
<HR WIDTH=75% ALIGN=LEFT SIZE=1 NOSHADE>
<DL>
<DT><B>When</B>
	<DD>$month/$date$year
<DT><B>Description</B>
	<DD>$description
</DL>
<HR>
<CENTER><FORM><INPUT TYPE="button" VALUE="Close" onClick="window.close();"></FORM></CENTER>
</BODY>
</HTML>
END
	exit(0);
	} # end	

#####################################################################
#
# DO_EDIT()
#
# Edit/Delete Entries
#
#####################################################################
sub DO_EDIT {	
	# Get ID of button pressed
	foreach (keys %in) { if (/^ID(\d+)/) { $id = $1; } }
	if ($in{"ID$id"} eq "Edit") {
		&EDITFORM($id);
		}
	elsif ($in{"ID$id"} eq "Delete") {
		&DELETE($id);
		}
	else { &ADMIN; }
	exit(0);
	}

#####################################################################
#
# EDITFORM()
#
# Form to edit an entry
#
#####################################################################
sub EDITFORM {
	$vars{id} = shift;
	open(IN,"$vars{calendar_file}") || &Error( "Can't open $vars{calendar_file}");
	my $header = <IN>;
	while (<IN>) {
		chomp;
		($id,$xdatestamp,$label,$description) = split(/\|/,$_,4);
		next unless ($id == $vars{id});
		($year,$month,$date) = ($xdatestamp =~ /(\d\d\d\d)(\d\d)(\d\d)/);
		$description =~ s|<BR>|\n|gis;
		last;
		}
	close(IN);
	print <<"END";
<HTML>
<HEAD><TITLE>Calendar Administration</TITLE>
<SCRIPT LANGUAGE="JavaScript">
function verifyform() {
	if (document.forms[0].month.value<1 || document.forms[0].month.value>12) {
		alert("Month is invalid");
		return false;
		}
	if (document.forms[0].date.value<1 || document.forms[0].date.value>31) {
		alert("Date is invalid");
		return false;
		}
	if (document.forms[0].year.value<0 || document.forms[0].year.value == "") {
		alert("Year is invalid");
		return false;
		}
	if (document.forms[0].heading.value == "") {
		alert("Heading is required");
		return false;
		}
	if (document.forms[0].description.value == "") { 
		alert("Description is required");
		return false;
		}
	return true;
	} // end of function
</SCRIPT>
</HEAD>
<BODY BGCOLOR=white>
<BR><BR>
<CENTER>
<TABLE BORDER=1 BORDERCOLOR="#333333" CELLSPACING=0 CELLPADDING=3 WIDTH=500>
<TR>
	<TD ALIGN=CENTER BGCOLOR="#000080"><FONT COLOR="white" SIZE="+1"><B>Calendar Administration</B></FONT></TD>
</TR>
<TR>
	<TD BGCOLOR="#CCCCCC">

		<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=3>
			<form action="$vars{cgi}" method=post onSubmit="return verifyform();">
			<INPUT TYPE="HIDDEN" NAME="OK" VALUE="OK">
			<INPUT TYPE="HIDDEN" NAME="username" VALUE="$in{username}">
			<INPUT TYPE="HIDDEN" NAME="password" VALUE="$in{password}">
			<INPUT TYPE="HIDDEN" NAME="id" VALUE="$id">
			<input type="hidden" name="ACTION" value="SAVE_EDIT">
			<TR>
				<TD ALIGN=RIGHT><B>Edit&nbsp;Event</B></TD>
				<TD WIDTH=100%><HR SIZE=1></TD>
			</TR>			
			<TR>
				<TH BGCOLOR="#CCCCCC">Date</TH>
				<TD BGCOLOR="#CCCCCC">
					<input name="month" size=2 maxlength=2 value="$month"> / <input name="date" size=2 maxlength=2 value="$date"> / <input name="year" size=4 maxlength=4 value="$year">&nbsp;&nbsp;
					<input type="checkbox" name="annual" value="1" onClick="if(form.annual.checked == true){form.year.value='0000'}else{form.year.value=''}"> Every Year
				</TD>
			</TR>
			<TR>
				<TH BGCOLOR="#CCCCCC">Heading</TH>
				<TD BGCOLOR="#CCCCCC"><input name="heading" size=30 value="$label"></TD>
			</TR>
			<TR>
				<TH BGCOLOR="#CCCCCC">Description</TH>
				<TD BGCOLOR="#CCCCCC" COLSPAN=3><textarea name="description" cols=50 rows=3>$description</textarea></TD>
			</TR>
			<TR>
				<TD COLSPAN=2 ALIGN=RIGHT BGCOLOR="#CCCCCC"><input type="reset" value="Clear">&nbsp;&nbsp;&nbsp;<input type="submit" value="Save">
				</form>
				</TD>
			</TR>
			<TR>
				<TD COLSPAN=2><HR SIZE=1></TD>
			</TR>
			<form action="$vars{cgi}" method=post>
			<INPUT TYPE="HIDDEN" NAME="OK" VALUE="OK">
			<INPUT TYPE="HIDDEN" NAME="username" VALUE="$in{username}">
			<INPUT TYPE="HIDDEN" NAME="password" VALUE="$in{password}">
			<TR>
				<TD COLSPAN=2 ALIGN=CENTER><input type="submit" value="Main Menu"></TD>
			</TR>
			</form>
		</TABLE>
	</TD>
</TR>
</TABLE>
</CENTER>
</BODY>
</HTML>
END
	exit(0);
	}

#####################################################################
#
# SAVE_EDIT()
#
# Save edits
#
#####################################################################
sub SAVE_EDIT {
	my %events;
	
	$in{description} =~ s|[\r\n]+|<BR>|gs;
	$in{month} =~ s|^(\d)$|0$1|;
	$in{date}  =~ s|^(\d)$|0$1|;
	my $datestamp = $in{year} . $in{month} . $in{date};

	open(IN,"$vars{calendar_file}") || &Error( "Can't open $vars{calendar_file}");
	my $header = <IN>;
	while (<IN>) {
		chomp;
		($id,$xdatestamp,$label,$description) = split(/\|/,$_,4);
		$events{$id}{datestamp} = $xdatestamp;
		$events{$id}{label} = $label;
		$events{$id}{description} = $description;
		}
	close(IN);

	$events{$in{id}}{datestamp} = $datestamp;
	$events{$in{id}}{label} = $in{heading};
	$events{$in{id}}{description} = $in{description};
	
	open(OUT,"> $vars{calendar_file}") || &Error( "Can't open $calendar_file for writing!");
	flock OUT,2;
	print OUT "#id|datestamp|label|description\n";
	foreach $id ( sort {$a <=> $b} keys %events ) {
		print OUT "$id|$events{$id}{datestamp}|$events{$id}{label}|$events{$id}{description}\n";
		}
	close(OUT);
	$vars{'message'} = "Changes Saved";
	undef %events;
	
	&read_cal_data;
	&EDIT;	
	exit(0);
	}
	
#####################################################################
#
# DELETE()
#
# Delete an entry
#
#####################################################################
sub DELETE {
	$in{id} = shift;
	my %events;
	open(IN,"$vars{calendar_file}") || &Error( "Can't open $vars{calendar_file}");
	my $header = <IN>;
	while (<IN>) {
		chomp;
		($id,$xdatestamp,$label,$description) = split(/\|/,$_,4);
		next if ($id == $in{id});
		$events{$id}{datestamp} = $xdatestamp;
		$events{$id}{label} = $label;
		$events{$id}{description} = $description;
		}
	close(IN);

	open(OUT,"> $vars{calendar_file}") || &Error( "Can't open $calendar_file for writing!");
	flock OUT,2;
	print OUT "#id|datestamp|label|description\n";
	foreach $id ( sort {$a <=> $b} keys %events ) {
		print OUT "$id|$events{$id}{datestamp}|$events{$id}{label}|$events{$id}{description}\n";
		}
	close(OUT);
	$vars{'message'} = "Event Deleted";
	undef %events;
	
	&read_cal_data;
	&EDIT;	
	exit(0);
	}
	
#####################################################################
#
# UPDATE_FORMAT()
#
# Display confirmation screen to update file format
#
#####################################################################
sub UPDATE_FORMAT {
	print <<"END";
<HTML>
<HEAD><TITLE>Calendar Administration</TITLE></HEAD>
<BODY BGCOLOR=white>
<BR><BR>
<CENTER>
<TABLE BORDER=1 BORDERCOLOR="#333333" CELLSPACING=0 WIDTH=400 CELLPADDING=3>
<TR>
	<TD ALIGN=CENTER BGCOLOR="#000080"><FONT COLOR="white" SIZE="+1"><B>Calendar Administration</B></FONT></TD>
</TR>
<TR>
	<TD BGCOLOR="#CCCCCC">
	<CENTER>
	<B><U>EVENTS FILE UPDATE</U></B>
	</CENTER>
	<BR>
	The file format of your events file needs to be updated for the new version. If you still want to use your events file with the old version of this application, please make a manual backup of the file.
	<BR><BR>
	Press OK to update the file format and return to the main Administration screen.
	<BR><BR>
	<CENTER>
	<FORM ACTION="$vars{cgi}" method=post>
		<INPUT TYPE="hidden" name="OK" VALUE="OK">
		<INPUT TYPE="hidden" name="username" VALUE="$in{username}">	
		<INPUT TYPE="hidden" name="password" VALUE="$in{password}">
		<INPUT TYPE="hidden" name="ACTION" VALUE="DO_UPDATE_FORMAT">
		<INPUT TYPE="submit" VALUE="    OK    ">
	</FORM>
	</CENTER>
	</TD>
</TR>
</TABLE>
</BODY>
</HTML>
END
	exit(0);
	} # end of UPDATE_FORMAT	

#####################################################################
#
# DO_UPDATE_FORMAT()
#
# Update the events file to new format
#
#####################################################################
sub DO_UPDATE_FORMAT {
	open(IN,"$vars{calendar_file}") || &Error( "Can't open $vars{calendar_file}");
	while (<IN>) {
		chomp;
		next unless /^\d/;
		($xdatestamp,$label,$desc) = split(/\|/,$_,3);
		$total_events{$xdatestamp}++;
		${$events{$xdatestamp}}{$total_events{$xdatestamp}}{description} = $desc;
		${$events{$xdatestamp}}{$total_events{$xdatestamp}}{label} = $label;
		}
	close(IN);
	$i = 1;
	open(OUT,"> $vars{calendar_file}") || &Error( "Can't open $vars{calendar_file} for writing!}");
	flock OUT,2;
	print OUT "#id|datestamp|label|description\n";
	foreach $xdatestamp (sort keys %events) {
		foreach (sort keys %{$events{$xdatestamp}}) {
			print OUT "$i|$xdatestamp|${$events{$xdatestamp}}{$_}{label}|${$events{$xdatestamp}}{$_}{description}\n";
			$i++;
			}
		}
	close(OUT);
		
	&ADMIN;
	exit(0);
	} # end DO_FORMAT_UPDATE
	
#####################################################################
#
# INITIALIZE()
#
# Initialize variables
#
#####################################################################
sub INITIALIZE {
	@months = (January,February,March,April,May,June,July,August,September,October,November,December);
	@shortmonths = (Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec);
	@days =(Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday);
	@shortdays = (Sun,Mon,Tue,Wed,Thu,Fri,Sat);

	# Current date and stuff

	$time = time;
	($mday,$month,$year) = (localtime($time))[3,4,5];
	$month = $month+1;
	$year = $year+1900;
	$datestamp = sprintf("%4.4d%2.2d%2.2d",$year,$month,$mday);
	
	}

#####################################################################
#
# Read in calendar data file
#
#####################################################################
sub read_cal_data {
	undef %events;
	my $id,$xdatestamp, $xmonth;
	$vars{new_id} = 0;
	open(IN,"$vars{calendar_file}") || &Error( "Can't open $vars{calendar_file}");
	my $header = <IN>;

	# If file isnt in right format, prompt to update it.
	unless ($header =~ m/^#id\|datestamp\|label\|description/) {
		close(IN);
		&UPDATE_FORMAT;
		}

	while (<IN>) {
		chomp;
		next unless /^\d/;
		($id,$xdatestamp,$label,$desc) = split(/\|/,$_,4);

		if ($id > $vars{new_id}) { $vars{new_id} = $id; }
				
		$total_events{$xdatestamp}++;
		${$events{$xdatestamp}}{$total_events{$xdatestamp}}{description} = $desc;
		${$events{$xdatestamp}}{$total_events{$xdatestamp}}{label} = $label;
		${$events{$xdatestamp}}{$total_events{$xdatestamp}}{id} = $id;
		
		}
	close(IN);
	$vars{new_id}++;
	}

#####################################################################
#
# Read in config file
#
#####################################################################
sub read_config {
	if ($in{config}) {
		$vars{config} = $in{config};
		}
	else {
		$vars{config} = $vars{base_dir} . "calendar.cfg";;
		}
	my $key,$val;
	open(IN,$vars{config}) || &Error("Can't open config file $vars{config}.");
	while(<IN>) {
		next if /^#/;
		chomp;
		($key,$val) = ( /([^=]+)=(.*)/ );
		$key = lc($key);
		$val =~ s|\[(\S+)\]|$vars{$1}|g;
		$val =~ s|\s*$||;
		$vars{$key} = $val;
		}
	close(IN);
	}

#####################################################################
#
# Convert old calendar file to new format
#
#####################################################################
sub convert_file {
	open(IN,"$vars{calendar_file}") || &Error( "Can't open $vars{calendar_file}");
	while (<IN>) {
		chomp;
		next unless /^\d/;
		($xdatestamp,$label,$desc) = split(/\|/,$_,3);
		$xdatestamp =~ s|^0000|$vars{year}|;

		$desc =~ s|(http://\S+)|<a href="$1" target="_new">$1</a>|g;

		$total_events{$xdatestamp}++;
		${$events{$xdatestamp}}{$total_events{$xdatestamp}}{description} = $desc;
		${$events{$xdatestamp}}{$total_events{$xdatestamp}}{label} = $label;
		}
	close(IN);
	}

#####################################################################
#
# Return an error screen
#
#####################################################################
sub Error {
	$message = shift;
	print <<"END";
<HTML>
<HEAD><TITLE>Error</TITLE>
</HEAD>
<BODY BGCOLOR=white>
<BR><BR>
<CENTER>
<TABLE BORDER=1 BORDERCOLOR="#333333" CELLSPACING=0 CELLPADDING=3 WIDTH=500>
<TR>
	<TD ALIGN=CENTER BGCOLOR="#000080"><FONT COLOR="white" SIZE="+1"><B>ERROR</B></FONT></TD>
</TR>
<TR>
	<TD BGCOLOR="#CCCCCC">
	<br><B>Error Message:</B><br>
	$message
	<br><br>
	<B>Please check the documentation for how to fix this problem.</B>
	</TD>
</TR>
</TABLE>
</BODY>
</HTML>
END
	exit(0);
	}

#####################################################################
#
# Parse input
#
#####################################################################
sub ReadParse {
 local (*in) = @_ if @_;  local ($i, $loc, $key, $val);
 if ($ENV{'REQUEST_METHOD'} eq "GET") { $in = $ENV{'QUERY_STRING'};} 
 elsif ($ENV{'REQUEST_METHOD'} eq "POST")
      {read(STDIN,$in,$ENV{'CONTENT_LENGTH'});}
 @in = split(/&/,$in);
 foreach $i (0 .. $#in) {
  $in[$i] =~ s/\+/ /g;    ($key, $val) = split(/=/,$in[$i],2);
  $key =~ s/%(..)/pack("c",hex($1))/ge;
  $val =~ s/%(..)/pack("c",hex($1))/ge;
  $in{$key} .= "\0" if (defined($in{$key})); 
  $in{$key} .= $val;  
  }  
 return 1; 
 }


#####################################################################
#
# Calendar logic
#
#####################################################################
sub PerpetualCalendar {
	# This perpetual calendar routine provides accurate day/date
	# correspondences for dates from 1601 to 2899 A.D.  It is based on
	# the Gregorian calendar, so be aware that early correspondences
	# may not always be historically accurate.  The Gregorian calendar
	# was adopted by the Italian states, Portugal and Spain in 1582,
	# and by the Catholic German states in 1583.  However, it was not
	# adopted by the Protestant German states until 1699, by England
	# and its colonies until 1752, by Sweden until 1753, by Japan
	# until 1873, by China until 1912, by the Soviet Union until 1918,
	# and by Greece until 1923.
	($perp_mon,$perp_day,$perp_year) = @_;
	%day_counts =
	  (1,0,2,31,3,59,4,90,5,120,6,151,7,181,
	  8,212,9,243,10,273,11,304,12,334);
	$perp_days = (($perp_year-1601)*365)+(int(($perp_year-1601)/4));
	$perp_days += $day_counts{$perp_mon};
	$perp_days += $perp_day;
	$perp_sofar = $day_counts{$perp_mon};
	$perp_sofar += $perp_day;
	$perp_togo = 365-$perp_sofar;
	if (int(($perp_year-1600)/4) eq (($perp_year-1600)/4)) {
		$perp_togo++;
		if ($perp_mon > 2) {
			$perp_days++;
			$perp_sofar++;
			$perp_togo -= 1;
		}
	}
	foreach $key (1700,1800,1900,2100,2200,2300,2500,2600,2700) {
		if ((($perp_year == $key) && ($perp_mon > 2))
		  || ($perp_year > $key)) {
			$perp_days -= 1;
		}
	}
	$perp_dow = $perp_days - (int($perp_days/7)*7);
	if ($perp_dow == 7) { $perp_dow = 0; }
	if ($MonSunWeek) {
		$perp_dow -= 1;
		if ($perp_dow == -1) { $perp_dow = 6; }
	}
	$perp_eom = 31;
	if (($perp_mon == 4) || ($perp_mon == 6)
	  || ($perp_mon == 9) || ($perp_mon == 11)) {
		$perp_eom = 30;
	}
	if (($perp_mon == 2)) {
		$perp_eom = 28;
	}
	if ((int(($perp_year-1600)/4) eq (($perp_year-1600)/4))
	  && ($perp_mon == 2)) {
		$perp_eom = 29;
	}
	foreach $key (1700,1800,1900,2100,2200,2300,2500,2600,2700) {
		if ($perp_year == $key) {
			if ($perp_mon == 1) {
				$perp_togo -= 1;
			}
			elsif ($perp_mon == 2) {
				$perp_togo -= 1;
				$perp_eom = 28;
			}
			else {
				$perp_sofar -= 1;
			}
		}
	}
}

#####################################################################
# load_template
# 
# load_template( "filename" )
#
# load a file and return it
#
#####################################################################
sub load_template {
	my($filename) = shift;
	undef $/;
	open(IN,"$filename") || &Error( "Couldn't open file $filename in load_template: $!\n");
	my($template) = <IN>;
	close(IN);
	$/="\n";
	return $template;
	}

#####################################################################
# parse_template
# 
# parse_template( $template_string , \%value_array )
#
# Replace <%=TAGS%> in template with values
#
#####################################################################
sub parse_template {
	my ($template) = shift;
	my ($data) = shift;

	# Replace <%TAG%> <%/TAG%>
	foreach (keys %$data) {
		if (defined ${$data}{$_}) {
			$template =~ s|<%$_%>(.+?)<%/$_%>|
							my($tmp2) = $1; 
							$tmp2 =~ s!<%=VALUE%>!${$data}{$_}!s;
							"$tmp2";
						 |esgx;
			}
		else {
			$template =~ s|<%$_%>(.*?)<%/$_%>||sg;
			}
		}

	# Replace <%=TAG%>
	foreach (keys %$data) {
		$template =~ s|<%=$_%>|${$data}{$_}|sg;
		}

	# Replace <%=ENCODE TAG%>
	foreach (keys %$data) {
		$temp = ${$data}{$_};
		$temp =~ s/([^a-zA-Z0-9_.-])/uc sprintf("%%%02x",ord($1))/eg;
		$template =~ s|<%=ENCODE $_%>|$temp|sg;
		}

	# Pass back parsed template
	return $template;
	
	}

#####################################################################
# parse_output
# 
# parse_output( $tag , $template_string , \%value_array )
#
# Loop through values array and replace <%OUTPUT $tag%> </%OUTPUT%>
# 
#####################################################################
sub parse_output {
	my ($tag) = shift;
	my ($template) = shift;
	my ($data) = shift;

	# Parse the <%OUTPUT%> <%/OUTPUT%> tags for record format
	my ($format) = ($template =~ m|<%OUTPUT $tag%>(.+?)<%/OUTPUT%>|si);
	my($output) = "";
	my($key,$tmp,$tmp2);
	# Loop through data and create output data
	foreach $key ( sort keys %$data ) {
		$tmp = $format;
		foreach (keys %{$$data{$key}}) {
			if ($$data{$key}{$_} =~ /\S/) {
				$tmp =~ s|<%$_%>(.+?)<%/$_%>|
							$tmp2 = $1; 
							$tmp2 =~ s!<%=VALUE%>!$$data{$key}{$_}!s;
							"$tmp2";
						 |esgx;
				}
			else {
				$tmp =~ s|<%$_%>(.+?)<%/$_%>||sg;
				}
			}
		foreach (keys %{$$data{$key}}) {
			$tmp =~ s|<%=($_)%>|$$data{$key}{$1}|sg;
			}
		$output .= $tmp;
		}

	# Replace OUTPUT in template with generated output
	$template =~ s|<%OUTPUT $tag%>.+?<%/OUTPUT%>|$output|s;

	return $template;
	}

#####################################################################
# html_escape
# 
# html_escape ( $string )
#
# Escape a string for display in HTML forms, etc.
# 
#####################################################################
sub html_escape {
	my ($string) = shift;
	$string =~ s|"|&quot;|sg;
	$string =~ s|<|&lt;|sg;
	$string =~ s|>|&gt;|sg;
	
	return $string;
	}
