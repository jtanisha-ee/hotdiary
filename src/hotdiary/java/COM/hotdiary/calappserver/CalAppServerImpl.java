package COM.hotdiary.calappserver;

import java.rmi.*;
import java.rmi.server.UnicastRemoteObject;
import java.io.*;
import java.net.*;
import COM.hotdiary.franchise.*;

public class CalAppServerImpl extends UnicastRemoteObject implements CalAppServer {

    public byte[] fetchCal(String url, String firewall, String proxyPort, String proxyHost, String proxySet) throws java.rmi.RemoteException {
       if (firewall.equals("yes")) {
         System.getProperties().put("proxyPort", proxyPort);
         System.getProperties().put("proxyHost", proxyHost);
         System.getProperties().put("proxySet", proxySet);
       }
       InetAddress ia = null;
       String ip = null;
       try {
          ia = InetAddress.getLocalHost();
          ip = ia.getHostAddress();
       } catch (Exception e) {
          e.printStackTrace();
       }
       url = "http://www.hotdiary.com" + url + "&ip=" + ip;

       SUR sur = new SUR(url);
       return sur.getContent().getBytes();
    }

    public CalAppServerImpl() throws java.rmi.RemoteException {
       super();
    }

    public static void main(String args[])
    {
	// Create and install the security manager
	System.setSecurityManager(new RMISecurityManager());

	try {
	    CalAppServer obj = new CalAppServerImpl();
	    Naming.rebind("CalAppServer", obj);
	    System.out.println("CalAppServer created and bound in the registry to the name CalAppServer");
	} catch (Exception e) {
	    System.out.println("CalAppServerImpl.main: an exception occurred:");
	    e.printStackTrace();
	}
    }
}
