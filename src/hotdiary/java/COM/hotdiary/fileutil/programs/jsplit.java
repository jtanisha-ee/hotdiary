import java.util.Vector;
import intrasail.fileutil.*;

public class jsplit {

   public static void main(String[] argv) {
      if (argv.length != 3) {
         System.out.println("Usage: java jsplit <infile> <chunksize> <outprefix>");
         System.exit(1);
      }
      fileutil.split(argv[0], (new Integer(argv[1])).intValue(), argv[2]);
   }

}