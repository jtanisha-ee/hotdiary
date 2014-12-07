package COM.hotdiary.main;

import java.sql.*;

public class TestPg {

   public static void main(String args[]) {


      try {
         Class.forName("postgresql.Driver");
         Connection db = DriverManager.getConnection("jdbc:postgresql://hotdiary.com:5432/dataroom", "hotdiary", "icuin1c");
// Was able to successfully login as pgtest also. At this time, the passwd
// was not set. But now pgtest hjas the same passwd as hotdiary login, so
// the code below will be changed.
         //Connection db = DriverManager.getConnection("jdbc:postgresql://hotdiary.com:5432/dataroom", "pgtest", "");
         //Connection db = DriverManager.getConnection("jdbc:postgresql://hotdiary.com:5432/dataroom", "pgtest", "icuin1c");
         Statement s = db.createStatement();
         ResultSet rs = s.executeQuery("select * from pg_user;");
         //ResultSetMetaData rsmd = db.getRSMD();
         //int cols = rsmd.getColumnCount();
         while (rs.next()) {
            for (int i = 1; i <= 5; i++) {
                System.out.println(rs.getObject(i));
            }
         }
      } catch (Exception e) {
          e.printStackTrace();
      }
 
   }

}
