#!/usr/bin/perl

require "cgi-lib.pl";
require "flush.pl";

MAIN:
{
  &ReadParse(*input);
  #open thandle, ">/tmp/manoj";
  #printf thandle time();
  #printf thandle "   ";
  #printf thandle $input{"outputfile"};
  #printf thandle "\n";
  #&flush(thandle);
  #close thandle;
  #print $input{"outputfile"};
  system "/bin/cat $input{\"outputfile\"}";
}
