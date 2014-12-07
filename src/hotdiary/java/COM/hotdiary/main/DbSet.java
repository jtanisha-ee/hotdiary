package COM.hotdiary.main;

import COM.hotdiary.db.*;

/**
 * The DbSet is an application that modifies the state of the database.
 * It is typically used for doing create, insert, update, delete, drop etc.
 * The nature of all these queries is that they do not return much data or
 * a result set. It only returns with an error code, if there was an error.
 * The program takes as input an SQL statement as the only argument.
 */

public class DbSet {

   /**
    * Create an instance of pgutil, and pass it the sql statement.
    */
   public DbSet(String sql) {
      pgutil = new PgUtil(sql); 
   }

   /**
    * Execute the current statement.
    */
   public void execute() {
      pgutil.executeSet();
   }

   /**
    * This is the main. Validate the input args, create an instance of DbSet
    * and execute the statement.
    */
   public static void main(String args[]) {
      if (args.length != 1) {
         System.out.println("Usage: java DbSet <sql-statement>"); 
         System.exit(1);
      }
      dbset = new DbSet(args[0]);
      dbset.execute();
   }

   static DbSet dbset;
   private PgUtil pgutil;
}
