package COM.hotdiary.db;

import java.sql.*;
import java.io.*;

public class PgUtil {

   /**
    * Initializes driver, and connection.
    */
   public PgUtil(String sql) {
      insql = sql;
      if (!(loadDriver())) {
         return; 
      }
      if (!(makeConnection())) {
         connected = false;
      }
   }

   /**
    * Loads the postgres jdbc driver.
    */
   private boolean loadDriver() {
      try {
          Class.forName("postgresql.Driver");
      } catch (Exception e) {
          e.printStackTrace();
          return false;
      }
      return true;
   }

   /**
    * Establishes a connection with the database.
    */
   private boolean makeConnection() {
      try {
          conn = DriverManager.getConnection("jdbc:postgresql://hotdiary.com:5432/dataroom", "hotdiary", "icuin1c");
      } catch (Exception e) {
          e.printStackTrace();
          return false;
      }
      return true;
   }

   /**
    * Return the status of the connection.
    **/
   public boolean getStatus() {
      return connected;
   }

   public boolean executeSet() {
      try {
          if (stmt == null) {
             stmt = conn.createStatement(); 
          } 
          stmt.executeUpdate(insql);
      } catch (Exception e) {
          e.printStackTrace();
          return false;
      }
      return true;
   }

   public ResultSet executeGet() {
      rs = null;
      try {
          if (stmt == null) {
             stmt = conn.createStatement(); 
          } 
          rs = stmt.executeQuery(insql);
      } catch (Exception e) {
          e.printStackTrace();
          return null;
      }
      return rs;
   }

   public void printData(FileWriter fw) {
      try {
         rsmd = rs.getMetaData(); 
         int cols = rsmd.getColumnCount();
         while (rs.next()) {
            for (int i = 1; i <= cols; i++) {
                if (fw != null) {
                   fw.write(rs.getObject(i).toString());
                   if (i < cols)
                      fw.write("::");
                } else {
                   System.out.print(rs.getObject(i).toString());
                   if (i < cols)
                      System.out.print("::");

                }
            }
            if (fw != null) {
               fw.write("\n");
            } else {
               System.out.println("");
            }
         }
         if (fw != null) {
            fw.flush();
         }
      } catch (Exception e) {
         e.printStackTrace();
      }
   }

   private boolean connected = true;
   private String insql;
   private Statement stmt = null;
   private Connection conn;
   private ResultSet rs = null;
   private ResultSetMetaData rsmd = null;
}

