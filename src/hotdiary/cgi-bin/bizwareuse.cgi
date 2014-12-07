#!/usr/bin/perl

require "cgi-lib.pl";
use AsciiDB::TagFile;
use utils::utils;
use MIME::Base64;

&ReadParse(*input);

$var = decode_base64 $input{whoami};

$ip = $ENV{REMOTE_ADDR};

tie %bizwaretab, 'AsciiDB::TagFile',
 DIRECTORY => "$ENV{HDDATA}/bizwaretab",
 SUFIX => '.rec',
 SCHEMA => {
 ORDER => ['ip', 'use', 'license'] };

$bizwaretab{$ip}{ip} = $ip;
$bizwaretab{$ip}{use} = $bizwaretab{$ip}{use} + 1;
$bizwaretab{$ip}{license} = $var;

hddebug "Redbasin E-Business Server Started on host with IP $ENV{REMOTE_ADDR} With License $var";

status("You have used Redbasin E-Business Server $bizwaretab{$ip}{use} times");

tied(%bizwaretab)->sync();
