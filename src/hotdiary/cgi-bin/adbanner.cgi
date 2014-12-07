#!/usr/bin/perl

require "cgi-lib.pl";
use AsciiDB::TagFile;
use utils::utils;
use tparser::tparser;

&ReadParse(*input);

tie %adtab, 'AsciiDB::TagFile',
 DIRECTORY => "$ENV{HDDATA}/adtab",
 SUFIX => '.rec',
 SCHEMA => {
 ORDER => ['login', 'clickbalance', 'impressionbalance', 'impressions', 'accbalance', 'rate', 'acctype', 'business'] };


$acc = $input{acc};
$url = $input{url};
$business = $adtab{$acc}{business};
hddebug "url = \"$url\"";

if (!exists $adtab{$acc}) {
   status("Invalid account");
   exit;
}

$clickbalance = $adtab{$acc}{clickbalance};
$clickbalance = $clickbalance - 1;
$adtab{$acc}{clickbalance} = $clickbalance;
$adtab{$acc}{accbalance} = $adtab{$acc}{accbalance} - $adtab{$acc}{rate};
hddebug "acc = $acc, login = $adtab{$acc}{login}, accbalance = $accbalance, clickbalance = $clickbalance";
tied(%adtab)->sync();
if ($clickbalance == 0) {
   $msg = "WARNING! Member $adtab{$acc}{login} has ZERO clickbalance!!";
   system "echo \"$msg\" > /var/tmp/adbanner$$";
   system "/bin/mail -s \"$adtab{$acc}{login} ZERO clickbalance\" rhsup\@hotdiary.com < /var/tmp/adbanner$$";
}

$login = $adtab{$acc}{login};
$rtime = getkeys();
$prml = "";
$prml = strapp $prml, "template=$ENV{HDTMPL}/redirectad.html";
$prml = strapp $prml, "templateout=/var/tmp/adbanner-$rtime-$$";
$prml = strapp $prml, "sponsor=This advertisement sponsored by $business.";
$url = adjusturl $url;
$prml = strapp $prml, "redirecturl=$url";
parseIt $prml;

system "cat $ENV{HDTMPL}/content.html";
#system "java COM.hotdiary.main.ExecURLPrint \"$url\"";
system "cat /var/tmp/adbanner-$rtime-$$";
