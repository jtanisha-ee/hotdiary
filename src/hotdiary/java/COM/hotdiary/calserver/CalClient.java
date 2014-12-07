
import java.awt.*;
import java.applet.*;
import java.rmi.*;
import COM.hotdiary.calserver.*;
import COM.hotdiary.vcalendario.*;
import COM.hotdiary.vcardio.*;

public class CalClient {

    public static void main(String args[]) {
	initRmi();
    }

    public static void initRmi() {
       try {
           //calserver = (COM.hotdiary.calserver.CalServer)Naming.lookup("//" + new MyApplet().getCodeBase().getHost() + "/HDCalServerImpl");
           calserver = (COM.hotdiary.calserver.CalServer)Naming.lookup("rmi://www.hotdiary.com/HDCalServer");
           Vcardin vcard = calserver.getVcard("Manoj", "Joshi");
           System.out.println("vcard = " + vcard);
           System.out.println("vcard.uid = " + vcard.uid);
       } catch (Exception e) {
           e.printStackTrace();
       }
    }


    public static COM.hotdiary.calserver.CalServer calserver;
}

class MyApplet extends Applet {

}
