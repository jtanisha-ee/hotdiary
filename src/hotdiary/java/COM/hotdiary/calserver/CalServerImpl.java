package COM.hotdiary.calserver;

import java.rmi.*;
import java.rmi.server.UnicastRemoteObject;
import java.io.*;
import COM.hotdiary.vcardio.*;
import COM.hotdiary.vcalendario.*;

public class CalServerImpl extends UnicastRemoteObject implements CalServer {

    public Vcardin getVcard(String login, String passwd) throws java.rmi.RemoteException {
           Vcardin vcard = new Vcardin();
           vcard.uid = "manoj@hotdiary.com";
	   return vcard;
    }

    public void setVcard(Vcardin vc) throws java.rmi.RemoteException {
    }

    public Vcalendar getVcalendar(String login, String passwd) throws java.rmi.RemoteException {
    //public String getVcalendar(String login, String passwd) throws java.rmi.RemoteException {
	   return null; 
    }

    public void setVcalendar(Vcalendar vc) throws java.rmi.RemoteException {
    }

    public CalServerImpl() throws java.rmi.RemoteException {
       super();
    }

    public static void main(String args[])
    {
	// Create and install the security manager
	System.setSecurityManager(new RMISecurityManager());

	try {
	    CalServer obj = new CalServerImpl();
	    Naming.rebind("HDCalServer", obj);
	    System.out.println("HDCalServerImpl created and bound in the registry to the name HDCalServer");
	} catch (Exception e) {
	    System.out.println("CalServerImpl.main: an exception occurred:");
	    e.printStackTrace();
	}
    }
}
