package COM.hotdiary.calmgmtserver;

import java.io.*;
import java.net.*;
import COM.hotdiary.franchise.*;

public class RequestHandler extends Thread {

   public RequestHandler(Socket conn) {
      connection = conn;
   }

   public void run() {
     int len;
     byte[] urlb = null;
     String url = null;
     byte[] firewallb = null;
     String firewall = null;
     byte[] proxyPortb = null;
     String proxyPort = null;
     byte[] proxyHostb = null;
     String proxyHost = null;
     byte[] proxySetb = null;
     String proxySet = null;
     byte[] outb = null;
     String outs = null;
     DataInputStream dis = null;
     DataOutputStream dos = null;

     try {
        dis = new DataInputStream(connection.getInputStream()); 
        len = dis.readInt();
        urlb = new byte[len];
        int bread = 0;
        int offset = 0;
        while (true) {
           dis.read(urlb, offset, len-offset);
           if (bread == -1) break;
           offset += bread;
        }
        url = new String(urlb);
        System.out.println("url = " + url);
   
        len = dis.readInt();
        System.out.println("len = " + len);
        firewallb = new byte[len];
        bread = 0;
        offset = 0;
        while (true) {
           dis.read(firewallb, offset, len-offset);
           if (bread == -1) break;
           offset += bread;
        }
        firewall = new String(firewallb);
        System.out.println("firewall = " + firewall);

        if (firewall.compareTo("yes") == 0) {
   
           len = dis.readInt();
           proxyPortb = new byte[len];
           bread = 0;
           offset = 0;
           while (true) {
              dis.read(proxyPortb, offset, len-offset);
              if (bread == -1) break;
              offset += bread;
           }
           proxyPort = new String(proxyPortb);
           System.out.println("proxyPort = " + proxyPort);
      
           len = dis.readInt();
           proxyHostb = new byte[len];
           bread = 0;
           offset = 0;
           while (true) {
              dis.read(proxyHostb, offset, len-offset);
              if (bread == -1) break;
              offset += bread;
           }
           proxyHost = new String(proxyHostb);
           System.out.println("proxyHost = " + proxyHost);
      
           len = dis.readInt();
           proxySetb = new byte[len];
           bread = 0;
           offset = 0;
           while (true) {
              dis.read(proxySetb, offset, len-offset);
              if (bread == -1) break;
              offset += bread;
           }
           proxySet = new String(proxySetb);
           System.out.println("proxySet = " + proxySet);
          
           System.getProperties().put("proxyPort", proxyPort);
           System.getProperties().put("proxyHost", proxyHost);
           System.getProperties().put("proxySet", proxySet);
        }
   
        sur = new SUR(url);
        outs = sur.getContent();
        outb = outs.getBytes();
        dos = new DataOutputStream(connection.getOutputStream()); 
        System.out.println("outb.length = " + outb.length);
        dos.writeInt(outb.length);
        System.out.println(outs);
        dos.writeBytes(outs);
     } catch (Exception e) {
        //e.printStackTrace(); 
     } finally {
/*
        try {
           connection.close();
        } catch (Exception e) {
           e.printStackTrace();
        }
        destroy();
*/
     } 
   }

   Socket connection;
   SUR sur;
}

