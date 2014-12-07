package COM.hotdiary.main;

import java.util.Vector;
import COM.hotdiary.vcardio.*;

public class jvcard {

   public static void main(String[] argv) {
      vcardio vcard = new vcardio();
      if (argv.length != 2) {
         // we just read the vcard records and write as .rec files in addrtab. 
         // the print statements are for debug only
         System.out.println("Usage: <infile> <perlfile>");
         System.exit(1);
      }
      vcard.vcard_read(argv[0], argv[1]);
   }

}
