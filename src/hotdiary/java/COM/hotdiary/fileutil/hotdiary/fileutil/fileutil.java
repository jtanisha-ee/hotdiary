package hotdiary.fileutil;
import java.io.*;
import java.util.*;



public class fileutil {


    /**
     * Find all files matching a given filter, and given root.
     * Return them as vectored list of File(s). On Win95
     * F:\ has to be converted to F:
     */
    public static Vector find(String filter, String r) {

        File rfile = null;
        Vector v = new Vector();

        try {
            String sep = File.separator;
            if (sep.equals("\\")) {
               if (r.endsWith(sep)) {
                  r = r.substring(0, r.length()-1);
               }
            }
            rfile = new File(r);
            v = findf(filter, rfile, v);

        } catch (IOException e) {
            System.out.println(e.getMessage());
        }

        return v;
    }

    /**
     * All comparisons are case insensitive.
     */
    private static Vector findf(String filter,
            File rfile, Vector v) throws java.io.IOException {

        String[] list = null;
        File afile = null;

        if (rfile.isFile()) return v;
        list = rfile.list();
        if ((list != null) && (list.length != 0)) {
           for (int i = 0; i < list.length; i++) {
               afile = new File(rfile, list[i]);
               if ((list[i].toLowerCase()).equals(filter.toLowerCase()))
                  v.addElement(afile.getAbsolutePath());
               if (afile.isDirectory()) {
                  v = findf(filter, afile, v);
               }
           }
        }
        return v;
    }

    public static void join(String prefix, int numfiles, String outfile) {

       FileOutputStream fos = null;
       FileInputStream fis = null;
       byte[] inb = new byte[4096];
       byte[] inempty = new byte[4096];
       int bytesRead;

       try {
           fos = new FileOutputStream(new File(outfile));
           for (int i = 1; i <= numfiles; i++) {
               fis = new FileInputStream(new File(prefix + i));
               for (;;) {
                   System.arraycopy(inempty, 0, inb, 0, 4096);
                   bytesRead = fis.read(inb);
                   if (bytesRead == -1) break;
                   fos.write(inb, 0, bytesRead);
               }
           }
       } catch (IOException e) {
           System.out.println(e.getMessage());
       }
    }

    public static void split(String infile, int chunksize, String outprefix) {
       FileOutputStream fos = null;
       FileInputStream fis = null;
       byte[] inb = new byte[chunksize];
       byte[] inempty = new byte[chunksize];
       int bytesRead;

       try {
           fis = new FileInputStream(new File(infile));
           for (int i = 1; ;i++) {
               System.arraycopy(inempty, 0, inb, 0, chunksize);
               bytesRead = fis.read(inb);
               if (bytesRead == -1) break;
               fos = new FileOutputStream(new File(outprefix + i));
               fos.write(inb, 0, bytesRead);
           }

       } catch (IOException e) {
           System.out.println(e.getMessage());
       }
    }
}
