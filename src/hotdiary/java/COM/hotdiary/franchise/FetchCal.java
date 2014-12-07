package COM.hotdiary.franchise;

import java.net.*;

/**
# (C) Copyright 1998 HotDiary Inc.
#
# Software is confidential copyrighted information of HotDiary and
# title to all copies is retained by HotDiary and/or its licensors.
# Licensee shall not modify, decompile, disassemble, decrypt, extract,
# or otherwise. Software may not be leased, assigned, or sublicensed,
# in whole or in part.
*/


public class FetchCal {

   public FetchCal(String url) {
      SUR sur = new SUR(url);
      System.out.println(sur.getContent());
   }

   public static void main(String args[]) {
 
      if (args.length != 6) {
         System.out.println("Usage: java COM.hotdiary.franchise.FetchCal <url> <firewall> <proxyPort> <proxyHost> <proxySet> <ip-address>");
         System.exit(1);
      }
  
      if (args[1].equals("yes")) {
         System.getProperties().put("proxyPort", args[2]);
         System.getProperties().put("proxyHost", args[3]);
         System.getProperties().put("proxySet", args[4]);
      }
      String ip = args[5];
      ip = ip.intern();

      //InetAddress ia = null;
      //String ip = null;
      //int ip = 0;
      //try {
          //ia = InetAddress.getLocalHost();
          //ip = ia.getHostAddress(); 
      //    ip = (InetAddress.getByName("hotdiary.com")).hashCode();
      //} catch (Exception e) {
      //   e.printStackTrace();
      //}
      String url = "http://www.hotdiary.com" + args[0] + "&ip=" + ip;
      FetchCal up = new FetchCal(url);
   }
}
