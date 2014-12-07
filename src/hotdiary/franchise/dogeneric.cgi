#!/usr/bin/perl

# (C) Copyright 1998-1999 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.

require "cgi-lib.pl";
use futils::futils;
use MIME::Base64;
use HTTP::Request::Common qw(POST);
use LWP::UserAgent;
use HTML::TreeBuilder;
use URI::URL;
use LWP::UserAgent;
use HTTP::Request;
use HTTP::Request::Common;
use HTTP::Request::Form;

&ReadParse(*input);

$pnum = $input{'pnum'};
if ($pnum eq "") {
   status "No programs to execute. Please check the configuration.";
   exit;
}
#system "echo \"pnum = $pnum\" > /tmp/generic";
system "echo \"cookie = $ENV{HTTP_COOKIE}\" > /tmp/generic";
$p0 = $input{p0};
$p0 =~ s/aaaa/=/g;
#system "echo \"p0 = $p0\" > /tmp/generic";
$p0 = decode_base64 $p0;
$parms = "/cgi-bin/$p0?";
#$parms = "/jsp/$p0?";
#$var = encode_base64 "p0", "";
#$var =~ s/=/aaaa/g;
#$parms = "/cgi-bin/$input{$var}?";
$lwptemplate = $input{lwptemplate};
   #system "echo \"lwptemplate = $lwptemplate\" >> /tmp/generic";
if ($lwptemplate ne "") {
   $lwppress = $input{lwppress};
   #system "echo \"lwppress = $lwppress\" >> /tmp/generic";
   $ua = LWP::UserAgent->new;
   my $url = url $lwptemplate;
   my $res = $ua->request(GET $url);
   my $tb = HTML::TreeBuilder->new;
   $tb->parse($res->content);
   my @forms = @{$tb->extract_links(qw(FORM))};
   $f = HTTP::Request::Form->new($forms[0][1], $url);
}

$i = 0;
for ($i = 1; $i < $pnum; $i = $i + 1) {
    $var = "p" . $i;
    $p = goodwebstr $input{$var};
    #system "echo \"p = $p\" >> /tmp/generic";
    $valattr = "pattr" . $i;
    $valattr = $input{$valattr};
    #system "echo \"valattr = $valattr\" >> /tmp/generic";
    if ($valattr eq "multsel") {
       #system "echo \"input = $input\" >> /tmp/generic";
       $v = goodwebstr multselkeys $input, "$p";
    } else {
       $v = goodwebstr $input{$p};
    }
    #system "echo \"v = $v\" >> /tmp/generic";
    if ($i == 1) {
       $parms .= "$p=$v";
    } else {
       $parms .= "&$p=$v";
    }
    if ($lwptemplate ne "") {
       $f->field($p, $input{$input{$var}});
    }
}

$enum = $input{'enum'};
#system "echo \"enum = $enum\" >> /tmp/generic";
for ($j = 0; $j < $enum; $j = $j + 1) {
    $rhs = "re" . $j;
    $lhs = "le" . $j;
    $rp = $input{$rhs};
    #system "echo \"rp = $rp\" >> /tmp/generic";
    $lp = $input{$lhs};
    #system "echo \"lp = $lp\" >> /tmp/generic";
    $v = goodwebstr $ENV{$rp};
    if ($i == 0) {
       $parms .= "$lp=$v";
    } else {
       $parms .= "&$lp=$v";
    }
    if ($lwptemplate ne "") {
       $f->field($lp, $ENV{$rp});
    }
}

$firewall = $ENV{FIREWALL};
$proxyPort = $ENV{proxyPort};
$proxyHost = $ENV{proxyHost};
$proxySet = $ENV{proxySet};

#system "echo \"before parms \" >> /tmp/generic";
#system "echo \"parms = $parms\" >> /tmp/generic";

$ip = qx{nslookup `hostname` | tail -2 | awk '{print \$2}'};
$ip =~ s/\n//g;
#print "System down for maintenance.";
system "cat $ENV{HDHOME}/content.html";
if ($lwptemplate eq "") {
   system "/usr/local/java/jdk118_v1/bin/java -ms32m -mx128m COM.hotdiary.franchise.FetchCal '$parms' '$firewall' '$proxyPort' '$proxyHost' '$proxySet' \'$ip\'";
   #system "/usr/local/java/jdk118_v1/bin/java COM.hotdiary.franchise.FetchCal '$parms' '$firewall' '$proxyPort' '$proxyHost' '$proxySet' \'$ip\'";
   #system "java COM.hotdiary.calmgmtserver.CalAppClient \"$parms\" \"$firewall\" \"$proxyPort\" \"$proxyHost\" \"$proxySet\"";
} else {
   my $response = $ua->request($f->press($lwppress));
   print $response->content;
}
