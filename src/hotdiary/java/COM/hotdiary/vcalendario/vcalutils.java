
package COM.hotdiary.vcalendario;
import java.io.*;
import java.util.*;
import java.sql.*;
import java.lang.*;


public class vcalutils {

   vcalendario vcalendario;
   String s = vcalendario.s;
   int size = vcalendario.size;
   String msg = vcalendario.msg;
   int numrec = vcalendario.numrec;

   int getIndex(String strind, String pattern) {
      return(strind.indexOf(pattern));
   }


   int checkValidityOfFile() {

      int begincnt = getPatternCnt("BEGIN", s, (int)size);
      int endcnt = getPatternCnt("END", s, (int)size);

      if (begincnt != endcnt) {
         msg = "This file has mismatched BEGIN" + begincnt + "and END" + endcnt;
         msg = vcalendario.getCGIString(msg);
         return 0;
      }

      if (begincnt <= 0) {
         msg = "This file is missing BEGINs";
         msg = vcalendario.getCGIString(msg);
         return 0;
      }

      if (endcnt <= 0) {
         msg = "This file is missing ENDs";
         msg = vcalendario.getCGIString(msg);
         return 0;
      }

      numrec = begincnt;
      return 1;

  }

  /** Need to add additonal checks
      1. check if the string has more than one value seperator for
         a text=value. if it has is this in ":" double quotes. if not
         then it is an error. we should give a valid error. and also
         recover from it or just exit.

   **/


   int getPatternCnt(String pattern, String inbuf, int bufend) {
      int cnt = 0;
      int j = 0;
      for (int i = 0; i < (int)bufend; i = j+1) {
         j = inbuf.indexOf(pattern);
         System.out.println("j =" + j);
         System.out.println("i ="  + i);
         if (j != -1) {
            cnt++;
         } else
            break;
      }
      System.out.println("patterncnt" + cnt);
      return cnt;
   }


}
