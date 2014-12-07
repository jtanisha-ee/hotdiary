package COM.hotdiary.vcalendario;
import java.io.*;
import java.util.*;
import java.sql.*;
import java.lang.*;


/** file extensions for vcalendar end with .ics */
public class vcalparmsin {

    /** common name associated with the calendar user */
    public  String cn;

    /** default is individual or it could be group/resource/room/unknown */
    public  String cutype;

    /** can specify the group or list membership of the calendar user  */
    public  String member;

    public  String partstart;

    public  String range;

    /** alarm trigger related  */
    public  String related;
    public  String reltype;

    public  String uid;

    /** dtstamp : DTSTAMP:19970901T1300Z 
      * yyyymmddThhmmssZ
      */

    public  String dtstamp;
    public  String dtstart;
    public  String dtend;
    public  String summary;
    public  String calclass;
    public  String categories;
    public  String transp;
    public  String rrule;
    public  String freq;
    public  String organizer;
    public  String attendee[];
    public  String comment[];
    public  String rstatus[];
    public  String due;
    public  String priority;
    public  String status;

    public  String value;
    public  String mailto[];
    public  String repeat[]; 
    public  String trigger;
    public  String action;

    /** interval is PT */
    public  String pt[];

    /* ATTENDEE;DELEGATED-FROM="MAILTO:jsmitha@host.com":MAILTO:jdoe@host.com */
    public  String delegator;

    public  String dirtype;
    public  String language;
    public  String url;
    public  String duration;

}
