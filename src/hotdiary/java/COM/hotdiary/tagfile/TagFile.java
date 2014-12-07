package COM.hotdiary.tagfile;

import java.io.*;

public class TagFile {

   public TagFile(String file) {
      FileInputStream fis = null;

      byte[] inb = null;
      int bytesRead = 0;
      try {
        File f1 = new File(file);
        sz = f1.length();
        fis = new FileInputStream(f1);
        inb = new byte[(int)sz];
        for (int i = 0; i < sz; i++) {
           inb[i] = 0;
        }

        bytesRead = fis.read(inb);
      } catch (IOException e) {
        System.out.println(e.getMessage());
      }
      //inb[bytesRead] = '\0';
      contents = new String(inb); 
   }

   public void dump() {
      System.out.println(contents);
   }

   public String get(String field) {
      int len = contents.indexOf(field);
      len = contents.indexOf(":", len);
      int term = contents.indexOf("\n", len);
      return contents.substring(len+1, term);
   }

   public void set(String field, String value) {
     
   }

   public static void main(String args[]) {
      TagFile t = new TagFile(args[0]);
      System.out.println("Fname = " + t.get("fname"));
      System.out.println("Lname = " + t.get("lname"));
      //t.dump();
   }

   String contents;
   long sz;
}
