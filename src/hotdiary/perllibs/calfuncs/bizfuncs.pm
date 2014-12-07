package calfuncs::bizfuncs;
require Exporter;
require "flush.pl";
use Time::Local;
use tparser::tparser;
use utils::utils;
use AsciiDB::TagFile;
use calfuncs::calfuncs;


@ISA = qw(Exporter);
@EXPORT = qw(updateMeetingEvent updatePcal updateTeamcal updateGroupcal updateResource getbiz dupBusinesses getbusinesses cleanupmeetingtab);

sub updateMeetingEvent {

   ## bizpeople excludes people from the teams.
   ## teams are not being used anymore.
   my($people, $peoplevals, $bizteamvals, $bizteams, $bizmemvals, $bizmem, $bizresourcevals, $bizresource, $bizpeoplevals, $bizpeople, $groups, $groupvals, $entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $group, $econtact, $update, $businesses) = @_; 

   hddebug "updateMeetingEvent, day=$eday";
   hddebug "groups = $groups, groupvals = $groupvals, people = $people, peoplevals = $peoplevals, bizteams = $bizteams, bizteamvals = $bizteamvals, businesses = $businesses";

   hddebug "bizmem = $bizmem, bizmemvals = $bizmemvals";

   ### businesses indicates which business this user belongs to has been
   ## used to update or add a meeting. this is picked up from surveytab
   ## in future.
   ## currently from the business selection 
  
   (@hshpeoplevals) = split("-", $peoplevals);
   (@hshpeople) = split(" ", $people);

   (@hshbizteamvals) = split("-", $bizteamvals);
   (@hshbizteams) = split(" ", $bizteams);

   (@hshgroupvals) = split("-", $groupvals);
   (@hshgroups) = split(" ", $groups);

   ## when we use business-to-business calendaring, businessname
   ## will be very useful.
   (@hshbizmemvals) = split("-", $bizmemvals);
   (@hshbizmem) = split(" ", $bizmem);

   (@hshbizresourcevals) = split("-", $bizresourcevals);
   (@hshbizresource) = split(" ", $bizresource);

   ## exclude these members from team meeting.
   (@hshbizpeoplevals) = split("-", $bizpeoplevals);
   (@hshbizpeople) = split(" ", $bizpeople);

   ## if the values are man  add it to their personal calendar
   ## if rsvp show it as an rsvp event which they need to confirm 

   ## from personal address book
   $ppeople = "";
   $peoplecntr = 0;
   $rescntr = 0;

   ## stick similar teams and teampeople together in one index.
   ## include business-team in bxx.
   ## bizpeople has business-team-memberlogin
   $num = $#hshbizpeople;
   for ($k =0; $k <= $num; $k = $k + 1) {
       ($rem, $bxx) = split ("-", $hshbizpeople[$k]);
       ($bxxteam, $teampeople) = split("-", $bxx); 
       $found = 0;
       for ($i = 0; $i <= $#hshbteams; $i = $i + 1) {
	  if ($hshbteams[$i] eq $bxx) {
	     $hshbizpeopleteam[$i] .= " $teampeople";
	     $hshbizpeopleteamvals[$i] .= " $hshbizpeoplevals[$k]";
	     $found = 1;
	  }
       }
       if ($found == 0) {
	  $hshbteams[$#hshbteams + 1] = $bxx;
	  $hshbizpeopleteam[$#hshbteams + 1] = $teampeople;
	  $hshbizpeopleteamvals[$#hshbteams +1] = $hshbizpeopleteamvals[$k];
       }
   }

   $bbusinesses = "";
   $bbizteam = "";

   $bbusinesses = getbusinesses($hshbizteamvals, $hshbizteams, $hshbizmemvals, $hshbizmem, $hshbizresourcevals, $hshbizresource);
   #hddebug "bbusinesses = $bbusinesses";

   if ($update == 1) {
      if ($bbusinesses ne "") {
         $businesses = $bbusinesses;
      }
   }
   ### for debugging purposes
   $xbusinesses = $businesses;
   $businesses = dupBusinesses($businesses);

   # delete existing meetingtab info as we should not keep invitees who are not
   # selected before.
   (@hshbusiness) = split(" ", $businesses);
    if ($update == 1) {
      for ($i = 0; $i <= $#hshbusiness; $i = $i + 1) {
          $ret = cleanupmeetingtab($entryno, $hshbusiness[$i]);
          if ($ret == 1) {
	     last; 
	  }
      }
   }

   ## exclude members in $bizpeople team
   $num = $#hshbizteamvals;
   for ($i = 0; $i <= $num; $i = $i + 1) {
       #hddebug "hshbizteams = $hshbizteams[$i]";
       if ($hshbizteamvals[$i] ne "") {
	  $bizpeopleteam = "";
	  $bizpeopleteamvals = "";
	
	  for ($k =0; $k < $#hshbteams; $k = $k + 1) {
	     if ($hshbizteams[$i] eq $hshbteams[$k]) {
		$bizpeopleteam = $hshbizpeopleteam[$k];
		$bizpeopleteamvals = $hshbizpeopleteamvals[$k];
	     } 
	  } 
	  ($business, $teamname) = split("-", $hshbizteams[$i]);
          updateTeamcal($hshbizteamvals[$i], $teamname, $entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $group, $econtact, $bizpeopleteam, $bizpeopleteamvals, $businesses);
	  $bbizteam .= "$hshbizteams[$i] ";
       }
   }

   hddebug "bbizteam = $bbizteam";

   ## already invited contacts list
   $num = $#hshpeoplevals;
   for ($i = 0; $i <= $num; $i = $i + 1) {
      if ($hshpeoplevals[$i] ne "") {
          updatePcal($entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $group, $econtact, $hshpeople[$i], $hshpeoplevals[$i], $businesses); 
	  $ppeople .= "$hshpeople[$i] ";
	  $peoplecntr = $peoplecntr + 1;
      }
   }

   $bbizmem = "";
   $num = $#hshbizmemvals;
   for ($i = 0; $i <= $num; $i = $i + 1) {
      if ($hshbizmemvals[$i] ne "") {
	  ($business, $mem) = split("-", $hshbizmem[$i]);
          updatePcal($entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $group, $econtact, $mem, $hshbizmemvals[$i], $businesses); 
	  $bbizmem .= "$hshbizmem[$i] ";
      }
   }
   hddebug "bbizmem = $bbizmem, num = $num";


   $ggroups = "";
   $num = $#hshgroups;
   for ($i = 0; $i <= $num; $i = $i + 1) {
      if ($hshgroupvals[$i] ne "") {
         updateGroupcal($etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $hshgroups[$i], $econtact, $businesses);
	 $ggroups = "$hshgroups[$i] ";
      }
   }

   $rresource = "";
   $num = $#hshbizresource;
   for ($i = 0; $i <= $num; $i = $i + 1) {
      if ($hshbizresourcevals[$i] ne "") {
         ($rem, $bizres) = split ("Resource-", $hshbizresource[$i]);
         ($biz, $res) = split ("-", $bizres);
         updateResource($res, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $bizres, $lg, $entryno, $biz, $hshbizresourcevals[$i], $businesses);
	  $rresource .= "$bizres ";
	  $rescntr = $rescntr + 1;
      }
   }

   #hddebug "bbizmem = $bbizmem, ggroups = $ggroups, rresource=$rresource, bbizteam = $bbizteam, businesses = $businesses, bbusinesses = $bbusinesses";
  hddebug "bbusinesses = $bbusinesses";

  $num = $#hshbusiness;

   for ($i = 0; $i <= $num; $i = $i + 1) {
       updateMeeting($hshbusiness[$i], $entryno, $ppeople, $lg, $rresource, $ggroups, $bbizteam, $bbizmem, $rescntr, $peoplecntr, $businesses);
   }

} 
   
sub updateResource {

   my($resname, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $bizres, $organizer, $entryno, $biz, $val, $businesses) = @_;

  $biz = trim $biz;

  if (-d("$ENV{HDDATA}/business/business/$biz/restab")) {
      system "mkdir -p $ENV{HDDATA}/business/business/$biz/resources/$resname";
      system "chmod 755 $ENV{HDDATA}/business/business/$biz/resources/$resname";

      if (-d("$ENV{HDDATA}/business/business/$biz/resources/$resname")) {
         tie %appttab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$biz/resources/$resname/appttab",
         SUFIX => '.rec',
         SCHEMA => {
            ORDER => ['entryno', 'login', 'month', 'day', 'year',
                 'hour', 'min', 'meridian', 'dhour', 'dmin',
                 'dtype', 'atype', 'desc', 'zone', 'recurtype',
                 'share', 'free', 'subject', 'street', 'city', 'state',
                 'zipcode', 'country', 'venue', 'person', 'phone', 'banner',
                 'confirm', 'id', 'type'] };

        #$appttab{$entryno}{'login'} = trim $login;
        $appttab{$entryno}{'month'} = $grouptab{$en}{month};
        $appttab{$entryno}{'day'} = $grouptab{$en}{day};
        $appttab{$entryno}{'year'} = $grouptab{$en}{year};
        $appttab{$entryno}{'hour'} = $grouptab{$en}{hour};
        $appttab{$entryno}{'min'} = $grouptab{$en}{min};
        $appttab{$entryno}{'meridian'} = $grouptab{$en}{meridian};
        $appttab{$entryno}{'dhour'} = $grouptab{$en}{dhour};
        $appttab{$entryno}{'dmin'} = $grouptab{$en}{dmin};
        $appttab{$entryno}{'dtype'} = $grouptab{$en}{dtype};
        $appttab{$entryno}{'atype'} = $grouptab{$en}{atype};
        $appttab{$entryno}{'desc'} = $grouptab{$en}{desc};
        $appttab{$entryno}{'zone'} = $grouptab{$en}{zone};
        $appttab{$entryno}{'recurtype'} = $grouptab{$en}{recurtype};
        $appttab{$entryno}{'share'} = $grouptab{$en}{share};
        $appttab{$entryno}{'free'} = $grouptab{$en}{free};
        $appttab{$entryno}{'subject'} = $grouptab{$en}{subject};
        $appttab{$entryno}{'entryno'} = $entryno;
        $appttab{$entryno}{'id'} = $businesses;
        ## organizer
        $appttab{$entryno}{'person'} = $organizer;

        if ($val eq "man") {
           $appttab{$entryno}{'confirm'} = "yes";
	} 
        if ($val eq "rsvp") { 
           $appttab{$entryno}{'confirm'} = "no";
	}
        $appttab{$entryno}{'type'} = "meeting";
        tied(%appttab)->sync();
      }
   }
}

sub updatePcal {

    my($entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $group, $econtact, $person, $val, $businesses) = @_; 

   if (!-d "$ENV{HDDATA}/$person/appttab") {
      return;
   }

    # bind personal appointment table vars
    tie %appttab, 'AsciiDB::TagFile',
    DIRECTORY => "$ENV{HDDATA}/$person/appttab",
    SUFIX => '.rec',
    SCHEMA => {
    ORDER => ['entryno', 'login', 'month', 'day', 'year',
             'hour', 'min', 'meridian', 'dhour', 'dmin',
             'dtype', 'atype', 'desc', 'zone', 'recurtype',
             'share', 'free', 'subject', 'street', 'city', 'state',
             'zipcode', 'country', 'venue', 'person', 'phone', 'banner',
             'confirm', 'id', 'type'] };

    ## id and type don't change
    $appttab{$entryno}{'month'} = trim $emonth;
    $appttab{$entryno}{'day'} = trim $eday;
    $appttab{$entryno}{'year'} = trim $eyear;
    $appttab{$entryno}{'hour'} = trim $ehour;
    $appttab{$entryno}{'min'} = trim $emin;
    $appttab{$entryno}{'meridian'} = trim $emeridian;
    $appttab{$entryno}{'dhour'} = trim $edhour;
    $appttab{$entryno}{'dmin'} = trim $edmin;
    $appttab{$entryno}{'dtype'} = trim $edtype;
    $appttab{$entryno}{'atype'} = trim $eatype;
    $appttab{$entryno}{'desc'} = $edesc;
    $appttab{$entryno}{'zone'} = trim $ezone;
    $appttab{$entryno}{'recurtype'} = trim $erecurtype;
    $appttab{$entryno}{'share'} = trim $eshare;
    $appttab{$entryno}{'free'} = trim $efree;
    $appttab{$entryno}{'subject'} = trim $etitle;
    $appttab{$entryno}{'type'} = "meeting";
    $appttab{$entryno}{'id'} = $businesses;
    $appttab{$entryno}{'entryno'} = $entryno;

    ## organizer
    $appttab{$entryno}{'person'} = $lg; 

    if ($val eq "man") {
       $appttab{$entryno}{'confirm'} = "yes";
    } else {
        $appttab{$entryno}{'confirm'} = "no";
    }
    tied(%appttab)->sync();
    if ($econtact ne "") {
       calfuncs::calfuncs::regEmailContacts($econtact, $lg, $eventdetails, $entryno, $group);
    }
}

sub updateTeamcal {

    my($teamval, $teamname, $entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $group, $econtact, $bizpeople, $bizpeoplevals, $business, $businesses) = @_;

  $business = trim $business;

    if ($team eq "AllTeams") {
       if (-d("$ENV{HDDATA}/business/business/$business/teams/teamtab")) {
          # bind teamtab table vars
          tie %teamtab, 'AsciiDB::TagFile',
          DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/teamtab",
          SUFIX => '.rec',
          SCHEMA => {
              ORDER => ['teamname', 'teamtitle', 'teamdesc', 'password', 'cpublish' ] };

          foreach $team (sort keys %teamtab) {
              updateEachTeam($teamval, $team, $entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $group, $econtact, $bizpeople, $bizpeoplevals, $business, $businesses);
	  }
       } else {
	  ## when there are no teams setup at all. we need to make this like company
	  ## wide event maybe.
	 
       }
    } else {
       updateEachTeam($teamval, $teamname, $entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $group, $econtact, $bizpeople, $bizpeoplevals, $business, $businesses);
    }
}


sub updateEachTeam {

    my($teamval, $team, $entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $group, $econtact, $bizpeople, $bizpeoplevals, $business, $businesses) = @_;

  $business = trim $business;
  $team = trim $team;

    if (-d ("$ENV{HDDATA}/business/business/$business/teams/$team/teampeopletab")) {
       # bind manager table vars
       tie %teampeopletab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$team/teampeopletab",
       SUFIX => '.rec',
       SCHEMA => {
       ORDER => ['login']};

       (@hshbizpeoplevals) = split(" ", $bizpeoplevals);
       (@hshbizpeople) = split(" ", $bizpeople);

       foreach $mem (sort keys %teampeopletab) {
	  ## remove the meeting from this team member
	  $found = 0;
          for ($i = 0; $i <= $#hshbizpeoplevals; $i = $i + 1) {
	      if ($mem eq $hshbizpeople[$i]) {
		 $found = 1;
   	         if ($hshbizpeoplevals[$i] ne "") {
  	            tie %appttab, 'AsciiDB::TagFile',
                    DIRECTORY => "$ENV{HDDATA}/$mem/appttab",
                    SUFIX => '.rec',
                    SCHEMA => {
                       ORDER => ['entryno', 'login', 'month', 'day', 'year',
                      'hour', 'min', 'meridian', 'dhour', 'dmin',
                      'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
                      'subject', 'street', 'city', 'state', 'zipcode', 'country',
                      'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type']};

		    if (exists ($appttab{$entryno})) {
	                delete $appttab{$entryno};
	                tied(%appttab)->sync();
		    }
		 }
	      }
	  }
	  if ($found == 0) {
             updatePcal($entryno, $etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $group, $econtact, $mem, $teamval, $businesses); 
	  }
      }
   }

   if ((!(-d "$ENV{HDDATA}/business/business/$business/teams")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$team")) ||
      (!(-d "$ENV{HDDATA}/business/business/$business/teams/$team/busappttab"))) {
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$team";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$team";
       system "mkdir -p $ENV{HDDATA}/business/business/$business/teams/$team/busappttab";
       system "chmod 755 $ENV{HDDATA}/business/business/$business/teams/$teamname/busappttab";
   }

   # bind personal appt table vars
   tie %busappttab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$team/busappttab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['entryno', 'login', 'month', 'day', 'year',
            'hour', 'min', 'meridian', 'dhour', 'dmin',
            'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
           'subject', 'street', 'city', 'state', 'zipcode', 'country',
            'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };
    

   #$busappttab{$entryno}{'login'} = trim $lg;
   $busappttab{$entryno}{'month'} = trim $emonth;
   $busappttab{$entryno}{'day'} = trim $eday;
   $busappttab{$entryno}{'year'} = trim $eyear;
   $busappttab{$entryno}{'hour'} = trim $ehour;
   $busappttab{$entryno}{'min'} = trim $emin;
   $busappttab{$entryno}{'meridian'} = trim $emeridian;
   $busappttab{$entryno}{'dhour'} = trim $edhour;
   $busappttab{$entryno}{'dmin'} = trim $edmin;
   $busappttab{$entryno}{'dtype'} = trim $edtype;
   $busappttab{$entryno}{'atype'} = trim $eatype;
   $busappttab{$entryno}{'desc'} = $edesc;
   $busappttab{$entryno}{'zone'} = trim $ezone;
   $busappttab{$entryno}{'recurtype'} = trim $erecurtype;
   $busappttab{$entryno}{'share'} = trim $eshare;
   $busappttab{$entryno}{'free'} = trim $efree;
   $busappttab{$entryno}{'subject'} = trim $etitle;
   $busappttab{$entryno}{'entryno'} = trim $entryno;
   $busappttab{$entryno}{'type'} = "meeting";
   $busappttab{$entryno}{'person'} = $lg;
   $busappttab{$entryno}{'id'} = $businesses;
   if ($teamval eq "man") {
       $busappttab{$entryno}{'confirm'} = "yes"; 
   } else {
       $busappttab{$entryno}{'confirm'} = "no"; 
   }

   tied(%busappttab)->sync();
} 
  
sub updateGroupcal {

   my($etitle, $edtype, $edesc, $emonth, $eday, $eyear, $erecurtype, $ehour, $emin, $emeridian, $ezone, $eshare, $efree, $eatype, $edhour, $edmin, $lg, $group, $econtact, $val, $businesses) = @_;

   if ($group ne "") {
      system "mkdir -p $ENV{HDDATA}/listed/groups/$group/appttab";
      system "chmod 755 $ENV{HDDATA}/listed/groups/$group/appttab";

      # bind group appt table vars
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$group/appttab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };
  }

   $appttab{$entryno}{'login'} = trim $lg;
   $appttab{$entryno}{'month'} = trim $emonth;
   $appttab{$entryno}{'day'} = trim $eday;
   $appttab{$entryno}{'year'} = trim $eyear;
   $appttab{$entryno}{'hour'} = trim $ehour;
   $appttab{$entryno}{'min'} = trim $emin;
   $appttab{$entryno}{'meridian'} = trim $emeridian;
   $appttab{$entryno}{'dhour'} = trim $edhour;
   $appttab{$entryno}{'dmin'} = trim $edmin;
   $appttab{$entryno}{'dtype'} = trim $edtype;
   $appttab{$entryno}{'atype'} = trim $eatype;
   $appttab{$entryno}{'desc'} = $edesc;
   $appttab{$entryno}{'zone'} = trim $ezone;
   $appttab{$entryno}{'recurtype'} = trim $erecurtype;
   $appttab{$entryno}{'share'} = trim $eshare;
   $appttab{$entryno}{'free'} = trim $efree;
   $appttab{$entryno}{'subject'} = trim $etitle;
   $appttab{$entryno}{'entryno'} = trim $entryno;
   $appttab{$entryno}{'person'} = $lg;
   $appttab{$entryno}{'id'} = $businesses;

   if ($val eq "man") {
      $appttab{$entryno}{'confirm'} = "yes";
   } 
   if ($val eq "rsvp") {
      $appttab{$entryno}{'confirm'} = "no";
   } 

   $appttab{$entryno}{'type'} = "meeting";
   if ($econtact ne "") {
      $eventdetails .= "Event: $etitle \n";
      $eventdetails .= "Event Type: $edtype \n";
      $eventdetails .= "Date:  $emonth-$eday-$eyear \n";
      $eventdetails .= "Time: $ehour:$emin:$emeridian \n";
      $eventdetails .= "Description: $edesc \n";
      $eventdetails .= "Frequency: $erecurtype \n";
   }

   tied(%appttab)->sync();
   if ($econtact ne "") {
      calfuncs::calfuncs::regEmailContacts($econtact, $lg, $eventdetails, $entryno, $group);
   }
}

sub updateMeeting {

   my($business, $entryno, $people, $login, $bizresources, $groups, $bizteams, $bizmem, $numresources, $numpeople, $businesses) = @_;

   (@bizs, @rems) = split("-", $bizmem);

   hddebug "bizfuncs::updateMeeting(), entryno = $entryno";

   hddebug "people = $people, bizresources=$bizresources, groups=$groups, teams= $bizteams, businesses = $businesses, bizmem = $bizmem, business=$business login=$login";

   $business = trim $business;

   if ($business ne "") {
     tie %businesstab, 'AsciiDB::TagFile',
     DIRECTORY => "$ENV{HDDATA}/business/businesstab",
     SUFIX => '.rec',
     SCHEMA => {
     ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
            'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
            'fax', 'url', 'email', 'other', 'list'] };


     if (exists $businesstab{$business}) {
        system "mkdir -p $ENV{HDDATA}/business/business/$business/meetingtab";
        system "chmod 755 $ENV{HDDATA}/business/business/$business/meetingtab";

        tie %meetingtab, 'AsciiDB::TagFile',
        DIRECTORY => "$ENV{HDDATA}/business/business/$business/meetingtab",
        SUFIX => '.rec',
        SCHEMA => {
        ORDER => ['entryno', 'invitees', 'numinvitees', 'organizer',
                 'numresources', 'resources', 'teams', 'groups', 'mem',
  	       'businesses'] };

        if (!exists($meetingtab{$entryno})) {
           $meetingtab{$entryno}{entryno} = $entryno;
        } 

        if ($people eq "") {
	   $numpeople = 0;
        } 
        if ($bizresources eq "") {
	   $numresources = 0;
        } 
        $meetingtab{$entryno}{invitees} = $people;
        $meetingtab{$entryno}{numinvitees} = $numpeople;
        $meetingtab{$entryno}{organizer} = $login;
        $meetingtab{$entryno}{businesses} = $businesses;

        ## resources in the form of business-resource
        $meetingtab{$entryno}{resources} = $bizresources;

        $meetingtab{$entryno}{numresources} = $numresources;
        $meetingtab{$entryno}{groups} = $groups;

        ## teams in the form of business-teamname
        $meetingtab{$entryno}{teams} = $bizteams;
   
        ## teams in the form of business-mem
        $meetingtab{$entryno}{mem} = $bizmem;
   	#hddebug "done, entryno = $entryno, bizmem = $meetingtab{$entryno}{mem}, bizmem from = $bizmem";  
         tied(%meetingtab)->sync();
      }
   }
}
 
sub getmeminfo {

   my($bizmems, $entryno) = @_;

   (@hshbizmems) = split(" ", $bizmems);

   # bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 'remoteaddr', 
	'informme', 'cserver', 'zone', 'calpublish'] };
   for ($i = 0; $i <= $nummem; $i = $i + 1) {
       ($biz, $mem) = split("-", $bizmems);
     if (-d "$ENV{HDDATA}/$mem/appttab") {
       tie %appttab, 'AsciiDB::TagFile',
       DIRECTORY => "$ENV{HDDATA}/$mem/appttab",
       SUFIX => '.rec',
       SCHEMA => {
           ORDER => ['entryno', 'login', 'month', 'day', 'year',
                   'hour', 'min', 'meridian', 'dhour', 'dmin',
                   'dtype', 'atype', 'desc', 'zone', 'recurtype',
                   'share', 'free', 'subject', 'street', 'city', 'state',
                   'zipcode', 'country', 'venue', 'person', 'phone', 'banner',
                   'confirm', 'id', 'type'] };

       if (exists($appttab{$entryno} )) {
          if ($appttab{$entryno}{confirm} eq "no") {
             $no .= "$logtab{$mem}{fname}$logtab{$mem}{lname}($mem)";
           } else {
             $yes .= "$logtab{$mem}{fname}$logtab{$mem}{lname}($mem) ";
           }
       }
     }
   }

   hddebug "no = $no";
   hddebug "yes = $yes";
   hddebug "nummem = $#hshbizmems";
   
   ($no, $yes, $nummem) = (@values);
   return (@values);
}


sub getbiz {

   my($entryno, $login) = @_;

   tie %businesstab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/businesstab",
   SUFIX => '.rec',
   SCHEMA => {
     ORDER => ['business', 'businessmaster', 'password', 'businesstitle',
            'street', 'suite', 'city', 'state', 'zipcode', 'country', 'phone',
            'fax', 'url', 'email', 'other', 'list'] };

   (@hshbiz) = (sort keys %businesstab);

   for ($i = 0; $i <= $#hshbiz; $i = $i + 1) {
      tie %peopletab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$hshbiz[$i]/peopletab",
      SUFIX => '.rec',
      SCHEMA => {
      ORDER => ['login', 'business']};
      if (exists($peopletab{$login})) {
	 if (!-d "$ENV{HDDATA}/business/business/$hshbiz[$i]/meetingtab") {
	    next;
	 }
         tie %meetingtab, 'AsciiDB::TagFile',
         DIRECTORY => "$ENV{HDDATA}/business/business/$hshbiz[$i]/meetingtab",
         SUFIX => '.rec',
         SCHEMA => {
         ORDER => ['entryno', 'invitees', 'numinvitees', 'organizer',
            'numresources', 'resources', 'teams', 'groups', 'mem',
            'businesses'] };
	 if (exists $meetingtab{$entryno}) {
	    return($hshbiz[$i]);
	 }
      }	 
   } 
   return "";

}

sub dupBusinesses {
   my($businesses) = @_;

   (@hshbusiness) = split(" ", $businesses);

   $hshbusiness[$#hshbusiness + 1] = $business;
   (@cleanup) = "";
   $nodups = "";  
   $cleanup[0] = $hshbusiness[0];
   $nodups = "$hshbusiness[0] ";
   $m = 0;
   $num = $#hshbusiness;
   for ($i = 0; $i <= $num; $i = $i + 1){
      $cntr = 1;
      for ($k = 0; $k <= $m; $k = $k + 1){
         if ($cleanup[$k] eq $hshbusiness[$i]) {
            $cntr = $cntr + 1;
	 }
      }
      if ($cntr == 1) {
         $m = $m + 1;
         $cleanup[$m] = $hshbusiness[$i];
	 $nodups .= $hshbusiness[$i] . " "; 
      }
   }
   return $nodups;
}

sub getbusinesses {

   my($hshbizteamvals, $hshbizteams, $hshbizmemvals, $hshbizmem, $hshbizresourcevals, $hshbizresource) = @_;

  $bbusinesses = "";

  for ($i = 0; $i <= $num; $i = $i + 1) {
     if ($hshbizteamvals[$i] ne "") {
        ($business, $teamname) = split("-", $hshbizteams[$i]);
        $bbusinesses .= "$business ";	
     }
  }

  $num = $#hshbizmemvals;
  for ($i = 0; $i <= $num; $i = $i + 1) {
      if ($hshbizmemvals[$i] ne "") {
	 ($business, $mem) = split("-", $hshbizmem[$i]);
         $bbusinesses .= "$business ";	
      }
  }

  $num = $#hshbizresource;
  for ($i = 0; $i <= $num; $i = $i + 1) {
     if ($hshbizresourcevals[$i] ne "") {
	($rem, $bizres) = split ("Resource-", $hshbizresource[$i]);
        ($biz, $res) = split ("-", $bizres);
         $bbusinesses .= "$biz ";	
     }
  }

  return $bbusinesses;
}

sub cleanupmeetingtab {

   my($entryno, $business) = @_;

   $business = trim $business;

   if (!-d "$ENV{HDDATA}/business/business/$business/meetingtab") {
      return 0;
   }

   tie %meetingtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/business/business/$business/meetingtab",
   SUFIX => '.rec',
   SCHEMA => {
      ORDER => ['entryno', 'invitees', 'numinvitees', 'organizer',
               'numresources', 'resources', 'teams', 'groups', 'mem',
               'businesses'] };

   if (!exists($meetingtab{$entryno})){
      return 0;
   }

   # bind login table vars
   tie %logtab, 'AsciiDB::TagFile',
   DIRECTORY => "$ENV{HDDATA}/logtab",
   SUFIX => '.rec',
   SCHEMA => {
   ORDER => ['login', 'password', 'fname', 'lname', 'street',
        'city', 'state', 'zipcode', 'country', 'phone', 'pager', 'pagertype',
        'fax', 'cphone', 'bphone', 'email', 'url', 'checkid', 'winner', 'remoteaddr',
        'informme', 'cserver', 'zone', 'calpublish'] };


   (@hshinvitees) = split(" ", $meetingtab{$entryno}{invitees});
   $num = $#hshinvitees;
   for ($i = 0; $i <= $num; $i = $i + 1) {
       $mem = trim $hshinvitees[$i];
       if (exists $logtab{$mem}) {
         if (-d("$ENV{HDDATA}/$mem/appttab")) {
            tie %appttab, 'AsciiDB::TagFile',
            DIRECTORY => "$ENV{HDDATA}/$mem/appttab",
            SUFIX => '.rec',
            SCHEMA => {
               ORDER => ['entryno', 'login', 'month', 'day', 'year',
                 'hour', 'min', 'meridian', 'dhour', 'dmin',
                 'dtype', 'atype', 'desc', 'zone', 'recurtype',
                 'share', 'free', 'subject', 'street', 'city', 'state',
                 'zipcode', 'country', 'venue', 'person', 'phone', 'banner',
                 'confirm', 'id', 'type'] };

             if (exists($appttab{$entryno})) {
	        delete $appttab{$entryno};
	        tied(%appttab)->sync();
	     }
          }
       } 
   }

   (@hshmembers) = split(" ", $meetingtab{$entryno}{mem});
   $num = $#hshhmembers;
   for ($i = 0; $i <= $num; $i = $i + 1) {
       ($biz, $mem) = split("-", $hshmembers[$i]);
       $mem = trim $mem;
       if (exists $logtab{$mem}) {
         if (-d("$ENV{HDDATA}/$mem/appttab")) {
            tie %appttab, 'AsciiDB::TagFile',
            DIRECTORY => "$ENV{HDDATA}/$mem/appttab",
            SUFIX => '.rec',
            SCHEMA => {
               ORDER => ['entryno', 'login', 'month', 'day', 'year',
                 'hour', 'min', 'meridian', 'dhour', 'dmin',
                 'dtype', 'atype', 'desc', 'zone', 'recurtype',
                 'share', 'free', 'subject', 'street', 'city', 'state',
                 'zipcode', 'country', 'venue', 'person', 'phone', 'banner',
                 'confirm', 'id', 'type'] };

             if (exists($appttab{$entryno})) {
                delete $appttab{$entryno};
	        tied(%appttab)->sync();
             }
          }
       }
   }

   (@hshresources) = split(" ", $meetingtab{$entryno}{resources});
   $num = $#hshresources;
   for ($i = 0; $i <= $num; $i = $i + 1) {
       ($biz, $resname) = split("-", $hshresources[$i]);
       $resname = trim $resname;
       $biz = trim $biz;
       if (-d("$ENV{HDDATA}/business/business/$biz/restab")) {
          system "mkdir -p $ENV{HDDATA}/business/business/$biz/resources/$resname";
          system "chmod 755 $ENV{HDDATA}/business/business/$biz/resources/$resname";

          if (-d("$ENV{HDDATA}/business/business/$biz/resources/$resname")) {
             tie %appttab, 'AsciiDB::TagFile',
             DIRECTORY => "$ENV{HDDATA}/business/business/$biz/resources/$resname/appttab",
             SUFIX => '.rec',
             SCHEMA => {
                ORDER => ['entryno', 'login', 'month', 'day', 'year',
                 'hour', 'min', 'meridian', 'dhour', 'dmin',
                 'dtype', 'atype', 'desc', 'zone', 'recurtype',
                 'share', 'free', 'subject', 'street', 'city', 'state',
                 'zipcode', 'country', 'venue', 'person', 'phone', 'banner',
                 'confirm', 'id', 'type'] };
             if (exists($appttab{$entryno})) {
                delete $appttab{$entryno};
	        tied(%appttab)->sync();
             }
          }
       }
   }


   (@hshteams) = split(" ", $meetingtab{$entryno}{teams});
   $num = $#hshteams;
   for ($i = 0; $i <= $num; $i = $i + 1) {
       ($business, $team) = split("-", $hshteams[$i]);
       $team = trim $team;
       $business = trim $business;
       if ((-d "$ENV{HDDATA}/business/business/$business/teams") && 
          (-d "$ENV{HDDATA}/business/business/$business/teams/$team") &&
          (-d "$ENV{HDDATA}/business/business/$business/teams/$team/busappttab")) {
           # bind personal appt table vars
          tie %busappttab, 'AsciiDB::TagFile',
          DIRECTORY => "$ENV{HDDATA}/business/business/$business/teams/$team/busappttab",
          SUFIX => '.rec',
          SCHEMA => {
          ORDER => ['entryno', 'login', 'month', 'day', 'year',
            'hour', 'min', 'meridian', 'dhour', 'dmin',
            'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
           'subject', 'street', 'city', 'state', 'zipcode', 'country',
            'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };
	   if (exists($busappttab{$entryno})){
	      delete $busappttab{$entryno};
	      tied(%busappttab)->sync();
           }
       }
   }

   (@hshgroups) = split(" ", $meetingtab{$entryno}{groups});
   $num = $#hshgroups;
   for ($i = 0; $i <= $num; $i = $i + 1) {
      $group = trim $group;
      system "mkdir -p $ENV{HDDATA}/listed/groups/$group/appttab";
      system "chmod 755 $ENV{HDDATA}/listed/groups/$group/appttab";

      # bind group appt table vars
      tie %appttab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/listed/groups/$group/appttab",
      SUFIX => '.rec',
      SCHEMA => {
        ORDER => ['entryno', 'login', 'month', 'day', 'year',
        'hour', 'min', 'meridian', 'dhour', 'dmin',
        'dtype', 'atype', 'desc', 'zone', 'recurtype', 'share', 'free',
        'subject', 'street', 'city', 'state', 'zipcode', 'country',
        'venue', 'person', 'phone', 'banner', 'confirm', 'id', 'type'] };
      if (exists($appttab{$entryno})) {
	  delete $appttab{$entryno};
          tied(%appttab)->sync();
      }
   } 

  
   (@businesses) = split(" ", $meetingtab{$entryno}{businesses});
   $num = $#hshbusinesses;
   for ($i = 0; $i <= $num; $i = $i + 1) {
      $biz = trim $hshbusiness[$i];
      if (!-d "$ENV{HDDATA}/business/business/$biz/meetingtab") {
	 next;
      }
      
      tie %meetingtab, 'AsciiDB::TagFile',
      DIRECTORY => "$ENV{HDDATA}/business/business/$biz/meetingtab",
      SUFIX => '.rec',
      SCHEMA => {
         ORDER => ['entryno', 'invitees', 'numinvitees', 'organizer',
               'numresources', 'resources', 'teams', 'groups', 'mem',
               'businesses'] };

      if (exists($meetingtab{$entryno})) {
	  delete $meetingtab{$entryno};
          tied(%meetingtab)->sync();
      }
   }
   return 1;
}
