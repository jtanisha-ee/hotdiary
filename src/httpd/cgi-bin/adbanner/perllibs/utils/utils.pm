# (C) Copyright 2000 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.

package utils::utils;
require Exporter;
use Time::Local;
use tparser::tparser;
use AsciiDB::TagFile;
use MIME::Base64;

@ISA = qw(Exporter);
@EXPORT = qw(trim adjusturl status hddebug getkeys);

sub trim {
   my($ts) = @_;
   $ts =~ s/[\s]+/ /g;
   @hsh = split(" ", $ts);
   #print $#hsh;
   #print @hsh[0];
   $ts = "";
   #@hsh[0] = "\b@hsh[0]";
   foreach $i (@hsh) {
      if ($ts eq "") {
        $ts = "$i";
      } else {
        $ts = "$ts $i";
      }
   }
   return $ts;
}

sub adjusturl {
   my($ur) = @_;
   $ur =~ s/\=/\-\-\-/g;
   return $ur;
}

sub hddebug {
   my($msg) = @_;
   $msg =~ s/\"/\\"/g;
   $msg =~ s/\n//g;
   $msg = localtime(time()) . " $msg";
   #system "echo \"$msg\" >> /tmp/hddebug.log";
   system "echo \"$msg\" >> /usr/local/hotdiary/logs/hddebug.log";
   return;
}

sub status {
   my($msg) = @_;

   $somefile = "$$.html";

   $prml = "";
   $prml = strapp $prml, "template=templates/statusTemplate.html";
   $prml = strapp $prml, "templateout=/tmp/$somefile";
   $msg = adjusturl $msg;
   $prml = strapp $prml, "label=$msg";
   parseIt $prml;

   system "/bin/cat /tmp/$somefile";
   system "/bin/rm -f /tmp/$somefile";
   $msg =~ s/\"/\\"/g;
   $msg =~ s/\n//g;
   $msg = localtime(time()) . " $msg";
   system "echo \"$msg\" >> /tmp/hdstatus.log";
   return;
}

sub getkeys {
   $tt = time();
   $sessionid = "$tt$$";
   return $sessionid;
}


1;

__END__
