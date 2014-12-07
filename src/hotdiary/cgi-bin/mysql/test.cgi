#!/usr/local/bin/perl5

##
##   In other words: DBD::mSQL and DBD::mysql are an interface between the
##   Perl programming language and the mSQL or mysql programming API 
##   that come with the mSQL any mysql relational database management systems.
##   Most functions provided by the respective programming API's are
##   supported. 
##
##
#
# Architecture of a DBI Application
#
#                    |<- Scope of DBI ->|
#                         .-.   .--------------.   .-------------.
#         .-------.       | |---| XYZ Driver   |---| XYZ Engine  |
#         | Perl  |       | |   `--------------'   `-------------'
#         | script|  |A|  |D|   .--------------.   .-------------.
#         | using |--|P|--|B|---|Oracle Driver |---|Oracle Engine|
#         | DBI   |  |I|  |I|   `--------------'   `-------------'
#         | API   |       | |...
#         |methods|       | |... Other drivers
#         `-------'       | |...
#                         `-'
#

require "cgi-lib.pl";
use utils::utils;
use DBI::*;

{

   &ReadParse(*input};

 # Connect to the database.
      $hd_driver = "mysql";
      $dsn = "DBI:$hd_driver:database=$database;host=$hostname;port=$port";
      $user =  "anonymous";
      $password = "";
      $dbh = DBI->connect($dsn, $user, $password);

      # Drop table 'foo'. This may fail, if 'foo' doesn't exist.
      # Thus we put an eval around it.
      #eval { $dbh->do("DROP TABLE logtab") };

      #print "Dropping foo failed: $@\n" if $@;

      # Create a new table 'logtab'. This must not fail, thus we don't
      # catch errors.
      $dbh->do("CREATE TABLE logtab (logid INTEGER, login VARCHAR(20)");

      # INSERT some data into 'logtab'. We are using $dbh->quote() for
      # quoting the name.
      $dbh->do("INSERT INTO logtab VALUES (1, " . $dbh->quote("Tim") . ")");


 # Same thing, but using placeholders
      $dbh->do("INSERT INTO logtab VALUES (?, ?)", undef, 2, "Jochen");

      # Now retrieve data from the table.
      my $sth = $dbh->prepare("SELECT * FROM logtab");
      $sth->execute();
      while (my $ref = $sth->fetchrow_hashref()) {
        print "Found a row: id = $ref->{'id'}, name = $ref->{'name'}\n";
      }
      $sth->finish();
  # Disconnect from the database.
      $dbh->disconnect();



}
