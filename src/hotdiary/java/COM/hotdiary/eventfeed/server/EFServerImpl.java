package COM.hotdiary.eventfeed.server;

import java.rmi.*;
import java.rmi.server.UnicastRemoteObject;
import java.io.*;
import java.lang.*;
import java.util.*;
import COM.hotdiary.eventfeed.hdif.*;
import COM.hotdiary.fileutil.*;

public class EFServerImpl extends UnicastRemoteObject implements EFServer {

    public void feedEvent(String title, String desc) throws java.rmi.RemoteException {
       System.out.println("Title = " + title + ",Desc = " + desc);
    }

    public EFServerImpl() throws java.rmi.RemoteException {
       super();
    }

    public static void main(String args[])
    {
	// Create and install the security manager
	System.setSecurityManager(new RMISecurityManager());

	try {
	    EFServer obj = new EFServerImpl();
	    Naming.rebind("EFServer", obj);
	    System.out.println("EFServerImpl created and bound in the registry to the name EFServer");
	} catch (Exception e) {
	    System.out.println("EFServerImpl.main: an exception occurred:");
	    e.printStackTrace();
	}
    }

    public String authUser(HDLogin sess) throws java.rmi.RemoteException {

       //FileIO.status("authuser");
       String pprog = "/home/httpd/cgi-bin/execauthuser.cgi";

       FileIO.status("Registering login = " + sess.login + ",  password = " + sess.passwd);

       if ((sess.login != null) && (sess.passwd != null)) {
	  try {

                String login = getCGIString(sess.login);
                String passwd = getCGIString(sess.passwd);

                Process p = Runtime.getRuntime().exec(pprog + " " +
                   "login=" + login + " " +  
                   "password=" + passwd + " ");
                InputStream is = p.getInputStream();
                byte b[] = new byte[256];
                int len;
                try {
                   while ((len = is.read(b)) != -1) {
	              String biscuit = new String(b, 0, len);
                      FileIO.status("Created biscuit = " + biscuit); 
	              return (biscuit);
                   }
                } catch (NullPointerException e) {
                } 
	        return(sess.biscuit);
             } catch (Exception e) {
                e.printStackTrace();
             }
          }
       return("");
    }

    String getCGIString(String s) {

       if (s == null)  return null;
          
        
       StringTokenizer st = new StringTokenizer(s);
       String msg = null;

       if (st.hasMoreTokens()) {
          msg = st.nextToken();
       }

       while (st.hasMoreTokens()) {
          msg += "+" + st.nextToken();
       }

       return msg;
    }

    public String setEvent(HDEvent ev) throws java.rmi.RemoteException {

       String pprog = "/home/httpd/cgi-bin/execaddevent.cgi";
       FileIO.status("Invoked setEvent");
       //FileIO.status("ev.day=" +ev.day);
       //FileIO.status("ev.month=" +ev.month);
       //FileIO.status("ev.year=" +ev.year);
       //FileIO.status("ev.zone=" +ev.zone);
       try {
          Process p = Runtime.getRuntime().exec(pprog + " " +
          "biscuit=" + getCGIString(ev.biscuit) + " " +
          "month=" + getCGIString(ev.month) + " " +
          "day=" + getCGIString(ev.day) + " " +
          "year=" + getCGIString(ev.year) + " " +
          "zone=" + getCGIString(ev.zone) + " " +
          "hour=" + getCGIString(ev.hour) + " " +
          "meridian=" + getCGIString(ev.meridian) + " " +
          "min=" + getCGIString(ev.min) + " " +
          "desc=" + getCGIString(ev.desc) + " " +
          "subject=" + getCGIString(ev.subject) + " " +
          "phone=" + getCGIString(ev.phone) + " " +
          "city=" + getCGIString(ev.city) + " " +
          "url=" + getCGIString(ev.url) + " " +
          "imgfn=" + getCGIString(ev.imgfn) + " " +
          "venue=" + getCGIString(ev.venue) + " "); 
          /* 
          InputStream is = p.getInputStream();
          byte b[] = new byte[256];
          int len; 
          try {
             while ((len = is.read(b)) != -1) {
                String status = new String(b, 0, len);
                System.out.print(status);
                FileIO.status("status =" + status);
                return(status);
             }  
	     FileIO.status("len =" + len);
          } catch (NullPointerException e) {
          }  */ 
       } catch (Exception e) {
          e.printStackTrace();
       }  
       return(null);
    } 

}
