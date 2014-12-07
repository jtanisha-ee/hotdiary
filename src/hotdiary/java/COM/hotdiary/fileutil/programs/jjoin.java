import java.util.Vector;
import intrasail.fileutil.*;

public class jjoin {

   public static void main(String[] argv) {
      if (argv.length != 3) {
         System.out.println("Usage: java jjoin <prefix> <numfiles> <outfile>");
         System.exit(1);
      }
      fileutil.join(argv[0], (new Integer(argv[1])).intValue(), argv[2]);
   }

}