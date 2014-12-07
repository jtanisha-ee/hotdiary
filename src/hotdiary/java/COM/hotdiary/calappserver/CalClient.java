package COM.hotdiary.calappserver;

import java.awt.*;
import java.applet.*;
import java.rmi.*;
import COM.hotdiary.calappserver.*;

public class CalClient {

    public static void main(String args[]) {
       if (args.length != 5) {
         System.out.println("Usage: java COM.hotdiary.calappserver.CalClient <url> <firewall> <proxyPort> <proxyHost> <proxySet>");
         System.exit(1);
       }
       initRmi(args[0], args[1], args[2], args[3], args[4]);
    }

    public static void initRmi(String url, String firewall, String proxyPort, String proxyHost, String proxySet) {
       try {
           calappserver = (COM.hotdiary.calappserver.CalAppServer)Naming.lookup("rmi://www.hotdiary.com/CalAppServer");
           System.out.println(new String(calappserver.fetchCal(url, firewall, proxyPort, proxyHost, proxySet)));
       } catch (Exception e) { 
           e.printStackTrace();
       }
    }


    public static COM.hotdiary.calappserver.CalAppServer calappserver;
}
