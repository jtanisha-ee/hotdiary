import java.util.Vector;
import intrasail.fileutil.*;

public class jfind {

   public static void main(String[] argv) {
      if (argv.length != 2) {
         System.out.println("Usage: java jfind <filter> <startdir>");
         System.exit(1);
      }
      Vector v = fileutil.find(argv[0], argv[1]);
      System.out.println(v.toString());
   }

}