package COM.hotdiary.vcalendario;
import java.io.*;
import java.util.*;
import java.sql.*;
import java.lang.*;


/** file extensions for vcalendar end with .ics */
public class vcalparmsfmt {

    /** common name associated with the calendar user */
    public  String cn = "CN";

    /** default is individual or it could be group/resource/room/unknown */
    public  String cutype = "CUTYPE";

    /** can specify the group or list membership of the calendar user  */
    public  String member = "MEMBER";

    public  String partstart = "PARTSTART";

    public  String range = "THISANDPRIOR";

    /** alarm trigger related  */
    public  String related = "RELATED";
    public  String reltype = "REL";

    public  String uid = "UID";

    /** dtstamp : DTSTAMP:19970901T1300Z 
      * yyyymmddThhmmssZ
      */

    public String dtstamp = "DTSTAMP";
    public String dtstart = "DTSTART";
    public String dtend = "DTEND";
    public String summary = "SUMMARY";
    public String calclass = "CLASS";
    public String categories = "CATEGORIES";
    public String transp = "TRANSPARENT";
    public String rrule = "RRULE";
    public String freq = "FREQ=";
    public String veventend = "END:VEVENT";
    public String veventbeg = "BEGIN:VEVENT";
    public String organizer = "ORGANIZER";
    public String attendee = "ATTENDEE";
    public String comment= "COMMENT:";
    public String rstatus= "RSTATUS";

    public String vtodobegin = "BEGIN:VTODO";
    public String vtodoend = "END:VTODO";
    public String due = "DUE:";
    public String priority = "PRIORITY:";
    public String status = "STATUS:";

    public String vjournalbegin = "BEGIN:VJOURNAL";
    public String vjournalend = "END:VJOURNAL";

    public String value = "VALUE=";
    public String mailto = "MAILTO:";

    public String valarmbegin = "BEGIN:VALARM";
    public String valarmend = "END:VALARM";
    public String repeat = "REPEAT";
    public String duartion = "DURATION";
    public String trigger = "TRIGGER";
    public String action = "ACTION";
    /** interval is PT */
    public String pt = "PT";

    /**  ATTENDEE;DELEGATED-FROM="MAILTO:jsmitha@host.com":
	MAILTO:jdoe@host.com
     */
    public String delegator = "DELEGATED-FROM";

    public String dirtype = "DIR";
    public String language = "LANGUAGE";
    public String url = "url";
}
