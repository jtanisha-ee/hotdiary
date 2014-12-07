#!/usr/local/bin/perl5

# $Header: /cys/people/brenner/http/docs/web/RCS/simple-form.cgi,v 1.4 1996/03/29 22:07:56 brenner Exp $
# Copyright (C) 1994 Steven E. Brenner
# This is a small demonstration script to demonstrate the use of
# the cgi-lib.pl library
# this file is invoked from execservice.cgi.
# the pathname for metasend is required otherwise it will not work.

require "cgi-lib.pl";

# When writing files, several options can be set... here we just set one
# Limit upload size to avoid using too much memory
#$cgi_lib'maxdata = 500000; 

MAIN:
{

  # Read in all the variables set by the form
  &ReadParse(*input);

  # Print the header
  print &PrintHeader;
  print &HtmlTop ("search button example");

   $action = $input{'action'};
#  ($delete = $input{'Delete'}) =~ s/\n/\n/g;
  

  print $action;

  if  ($action eq "update") 
  {
      print "update button is pressed";

  } else {
      print "delete button is pressed";
  }


  # Close the document cleanly.
  print &HtmlBot;
}
