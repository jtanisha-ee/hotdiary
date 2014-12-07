package COM.hotdiary.calmgmtserver;

import java.net.*;
import java.io.*;

/**
# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
*/


public class CalAppClient {

   public CalAppClient() {
   }

   public static void main(String args[]) {
 
      if (args.length != 5) {
         System.out.println("Usage: java COM.hotdiary.calmgmtserver.CalAppClient <url> <firewall> <proxyPort> <proxyHost> <proxySet>");
         System.exit(1);
      }
  
      InetAddress ia = null;
      String ip = null;
      try {
          ia = InetAddress.getLocalHost();
          ip = ia.getHostAddress(); 
      } catch (Exception e) {
          e.printStackTrace();
      }
      String url = "http://www.hotdiary.com" + args[0] + "&ip=" + ip;
      Socket clientSocket = null;
      DataOutputStream dos = null;
      DataInputStream dis = null;
      byte[] urlb = null;
      byte[] firewallb = null;
      String firewall = null;
      byte[] proxyPortb = null;
      String proxyPort = null;
      byte[] proxyHostb = null;
      String proxyHost = null;
      byte[] proxySetb = null;
      String proxySet = null;
      try {
          clientSocket = new Socket(ia, 8500);
          dos = new DataOutputStream(clientSocket.getOutputStream());
          urlb = url.getBytes();
          dos.writeInt(urlb.length);;
          dos.writeBytes(url);
          firewall = args[1];
          //System.out.println("firewall = " + firewall);
          if (firewall.compareTo("") == 0) {
             firewall = "no";
          }
          firewallb = firewall.getBytes();
          dos.writeInt(firewallb.length);
          dos.writeBytes(firewall);
          if (firewall.compareTo("yes") == 0) {
             proxyPort = args[2];
             //System.out.println("proxyPort = " + proxyPort);
             proxyPortb = proxyPort.getBytes();
             dos.writeInt(proxyPortb.length);
             dos.writeBytes(proxyPort);
             proxyHost = args[3];
             //System.out.println("proxyHost = " + proxyHost);
             proxyHostb = proxyHost.getBytes();
             dos.writeInt(proxyHostb.length);
             dos.writeBytes(proxyHost);
             proxySet = args[4];
             //System.out.println("proxySet = " + proxySet);
             proxySetb = proxySet.getBytes();
             dos.writeInt(proxySetb.length);
             dos.writeBytes(proxySet);
          }
          dis = new DataInputStream(clientSocket.getInputStream());
          int len = dis.readInt();
          byte[] outb = new byte[len];
          int bread = 0;
          int offset = 0;
          while (true) {
             bread = dis.read(outb, offset, len-offset);
             if (bread == -1) break;
             offset += bread;
          }
          //System.out.println("received len = " + offset);
          System.out.println(new String(outb));
      } catch (Exception e) {
          e.printStackTrace();
      }
   }
}
