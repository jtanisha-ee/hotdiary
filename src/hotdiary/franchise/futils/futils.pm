package futils::futils;

# (C) Copyright 1998-1999 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.


require Exporter;

@ISA = qw(Exporter);
@EXPORT = qw(trim badwebstr status goodwebstr normalizeurlparmvalue multselkeys multsel);

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

sub badwebstr {
   my($str) = @_;
   return ((index($str, '=') >= 0) ||
           (index($str, '&') >= 0) ||
           (index($str, '?') >= 0) );
}

sub status {
   my($str) = @_;
   $str =~ s/\"/\\"/g;
   $str =~ s/\n//g;
   system "cat $ENV{HDHOME}/content.html";
   print "<HTML><BODY BGCOLOR=ffffff><h2><FONT FACE=\"Verdana\"><P VALIGN=CENTER>$str</FONT></h2></BODY></HTML>";
}

sub goodwebstr {
   my($str) = @_;

   #if (badwebstr $str) {
   #   status "The field \"$str\" contains invalid characters (one of '=, &, ?'). Please correct these errors and try again.";
   #   exit;
   #}
   
   $str = normalizeurlparmvalue($str);
# replacing space below also damages CRLF (\r\n). Hence we first
# replace those with %0d%0a in upper function.
   $str =~ s/ /%20/g;
   return $str;
}

sub normalizeurlparmvalue {
   my($ur) = @_;
   $ur =~ s/\&/%26/g;
   $ur =~ s/\|/%7c/g;
   $ur =~ s/\'/%27/g;
   $ur =~ s/\=/%3d/g;
   $ur =~ s/\?/%3f/g;
   $ur =~ s/\;/%3b/g;
   $ur =~ s/\#/%23/g;
   $ur =~ s/\:/%3a/g;
   $ur =~ s/\//%2f/g;
   $ur =~ s/\r\n/%0d%0a/g;
# extra stuff
   $ur =~ s/\)/%29/g;
   $ur =~ s/\(/%28/g;
   $ur =~ s/\#/%2a/g;
   $ur =~ s/\+/%2b/g;
   $ur =~ s/\,/%2c/g;
   $ur =~ s/\-/%2d/g;
   $ur =~ s/\./%2e/g;
   $ur =~ s/\>/%3e/g;
   $ur =~ s/\</%3c/g;
   $ur =~ s/\"/%22/g;
   $ur =~ s/\!/%21/g;
   $ur =~ s/\~/%7e/g;
   $ur =~ s/\{/%7b/g;
   $ur =~ s/\}/%7d/g;
   $ur =~ s/\[/%5b/g;
   $ur =~ s/\\/%5c/g;
   $ur =~ s/\]/%5d/g;
   $ur =~ s/\_/%5f/g;
   $ur =~ s/\^/%5e/g;
   return $ur;
}

sub multselkeys {
   my($input, $argmatch) = @_;
   $option = "";
   (@pairs) = split '&', $input;
   foreach $pair (@pairs) {
     ($name, $value) = split '=', $pair;
     if ($name eq $argmatch) {
        $option .= ' ' . $value;
     }
   }
   return $option;
}


sub multsel {
   my(%arginput, $argmatch) = @_;
   $output = "";
   foreach $key (sort keys(%arginput)) {
      if ((index $key, $argmatch) == 0) {
        foreach (split("\0", $arginput{$key})) {
          ($out = $_) =~ s/\n//g;
          $output .=  " $out";
        }
      }
   }
   return $output;
}


1;

__END__
