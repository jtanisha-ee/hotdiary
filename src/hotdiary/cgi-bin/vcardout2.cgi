#
# (C) Copyright 1998 HotDiary Inc.
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.  
#

#
# FileName: vcardout.cgi
# Purpose: it allows users to upload a file which is vcard compatible and saves the vcards
# as address records in the appropriate login files
# we support both vCard 2.1 and vCard 3.0 versions
# Creation Date: 05-27-99 
# Created by: Smitha Gudur
# 

#!/usr/local/bin/perl5

require "cgi-lib.pl";
require "flush.pl";
#use UNIVERSAL qw(isa);
use ParseTem::ParseTem;
use tp::tp;
use AsciiDB::TagFile;
use Time::Local;
use utils::utils;
#$cgi_lib'maxdata = 500000;

MAIN:
{
# Read in all the variables set by the form

#session timeout in secs


#public class Vcardin {
#   public String begin = null;
#   public String n = null;
#   public String title = null;  
#   public String email = null; 
#   public String pref = null;
#   public String internet = null;
#   public String ver = null; 
#   public String end = null;
#   public String type = null; 
#   public String fn = null;
#   public String nickname = null;
#  public String street = null;
#   public String city = null;
#   public String state = null;
#   public String zipcode = null;
#   public String country = null;
#   public String birthday = null;
#   /** Telephone type is specified as :
#      TEL;TYPE=work,voice,pref,msg:+1-213-555-1234
#    */
#   public String url = null;
#   public String home = null;
#   public String fax = null;
#   public String work = null;
#   public String pager = null;
#   public String cell = null;
#   public String emailtype = null;
#   public String org = null;
#   public String bday = null;
#   public String other = null;
#
#   /** photo can be PHOTO;VALUE=uri or PHOTO;ENCODING=b;TYPE=JPEG:<binary> */
#   public String Photo = null;
#}
#

   &ReadParse(*input);
   # fname has both first name and last name 
   $fname = "$ARGV[0]"; 
   $ver = "$ARGV[1]";
   $street =  "$ARGV[2]";

   $city =  "$ARGV[3]";
   $state =  "$ARGV[4]";
   $zipcode =  "$ARGV[5]";
   $country =  "$ARGV[6]";
   $homeph = "$ARGV[7]";
   $pager = "$ARGV[8]";
   $cell = "$ARGV[9]";
   $workph = "$ARGV[10]";
   $email = "$ARGV[11]";
   $url = "$ARGV[12]";
   $bday = "$ARGV[13]";
   $org = "$ARGV[14]";
   $fax = "$ARGV[15]";
   $other = "$ARGV[16]";

   #system "/bin/cat $input{"\name\"}";
   print "fname=  $fname \n";
   print "ver= $ver \n";
   print "street= $street \n";
   print "city= $city \n";
   print "state= $state \n";
   print "zipcode= $zipcode \n";
   print "country= $country \n";
   print "homeph= $homeph \n";
   print "pager= $pager \n";
   print "cell= $cell \n";
   print "fax= $fax \n";
   print "email= $email \n";
   print "url= $url \n";
   print "bday= $bday \n";
   print "org= $org \n";
   print "other= $other \n";


}
