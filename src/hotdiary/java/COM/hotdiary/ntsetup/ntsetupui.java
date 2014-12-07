package COM.hotdiary.ntsetup;
import java.io.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.Button;
import java.applet.Applet;
import java.lang.String;

/**
 * ntsetupui setups the ui needed.
 */

public class ntsetupui {

   public TextField nttext;
   public void ntsetui(String labelname, String textfieldname) {
        Frame htdocfr = new Frame("Hotdiary NT JazzIt! Setup"); 
        boolean vis = true;
        htdocfr.setVisible(vis); 
        Window htwin = new  Window(htdocfr);
        System.out.println("ntsetupui labelname: " + labelname);
        System.out.println("ntsetupui textfield: " + textfieldname);
        Label label = new Label(labelname, 1);
        nttext= new TextField(textfieldname, 20);
        Button left1 = new Button("Continue"); 
        Button reset2 = new Button("Reset"); 
        /* ActionListener l;
        addActionListener(this); */
        htwin.pack();
   }

   public void actionPerformed(ActionEvent l) {
       String htdocpath = nttext.getText().toLowerCase();
       if (htdocpath != "") {
	  System.out.println("addActionListener: htdocpath");
       }
       
   }
}
