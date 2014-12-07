From Manoj.Joshi@BankAmerica.com  Mon Apr 19 10:56:58 1999
Return-Path: <Manoj.Joshi@BankAmerica.com>
Received: from mail2.bankamerica.com (gatekeeper.bankamerica.com [165.32.204.3])
	by hotdiary.com (8.8.7/8.8.7) with ESMTP id KAA25562
	for <hotdiary@hotdiary.com>; Mon, 19 Apr 1999 10:56:58 -0700
From: Manoj.Joshi@BankAmerica.com
Received: from mail1.bankamerica.com ([165.32.209.33])
	by mail2.bankamerica.com (8.9.2/8.9.2) with ESMTP id KAA05380
	for <hotdiary@hotdiary.com>; Mon, 19 Apr 1999 10:54:05 -0700 (PDT)
Received: from smtpsw02 (smtpsw02.bankamerica.com [165.37.204.30])
	by mail1.bankamerica.com (8.9.2/8.9.2) with ESMTP id KAA21579
	for <hotdiary@hotdiary.com>; Mon, 19 Apr 1999 10:54:04 -0700 (PDT)
Date: Mon, 19 Apr 1999 10:48:04 -0700
Subject: SendPageUsingProxy.java
To: hotdiary@hotdiary.com
Message-id: <88256758.006233E4.00@notes.bankamerica.com>
MIME-version: 1.0
Content-type: text/plain; charset=us-ascii
Content-disposition: inline
Content-transfer-encoding: 7BIT
Status: RO


Please save this newly developed program under this file name, in the
java/COM/hotdiary/.... folder where the SendPage.java program is
stored. Use the file name that is given in the subject.

Manoj


import java.net.*;
import java.util.*;
import java.io.*;

public class SendPageUsingProxy {

   public static void main(String args[]) {

      if (args.length != 3) {
         System.out.println("Usage: java SendPage <to-pager-no> <message>
<from>");
         System.exit(1);
      }

      System.getProperties().put("proxySet", "true");
      System.getProperties().put("proxyHost", "proxy.bankamerica.com");
      System.getProperties().put("proxyPort", "8080");

      StringTokenizer st = new StringTokenizer(args[1]);
      String msg = null;
      if (st.hasMoreTokens()) {
         msg = st.nextToken();
      } else {
           System.out.println("Empty Message String");
           System.exit(1);
      }
      while (st.hasMoreTokens()) {
         msg += "%20" + st.nextToken();
      }
      String urls = "http://www.skytel.com/cgi-bin/page.pl?to=" + args[0] +
 "&message=" + "\"" + msg + "\"" + "&from=" + args[2];
      //System.out.println(urls);
      try {
         URL sup = new URL(urls);
         URLConnection cn = sup.openConnection();
/*
         cn.setDoOutput(true);
         cn.setUseCaches(false);
         cn.setAllowUserInteraction(false);
*/
         BufferedReader in = new BufferedReader(new
InputStreamReader(cn.getInputStream()));
         StringBuffer sb = new StringBuffer();
         String inputLine;
         while ((inputLine = in.readLine()) != null){
           sb.append(inputLine);
           sb.append("\n");
         }
         in.close();
         //System.out.println(sb);
      } catch (Exception e) {
         e.printStackTrace();
      }
   }
}


