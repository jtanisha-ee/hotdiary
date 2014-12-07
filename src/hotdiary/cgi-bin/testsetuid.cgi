#!/usr/bin/perl
##!/usr/bin/suidperl -wT

#$ARGV[0] =~ /^-P(\w+)$/;
print "Running as UID $> GID $) \n";
#$> = $<;
#$ENV{PATH} = "";
#$ENV{BASH_ENV} = "";
system "echo \"Helo\" > /u3/testsetuid";
exit 100;
