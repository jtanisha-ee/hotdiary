#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "hdcgic.h"
#include "hdenv.h"

char* getField(char*);
char* getFieldValue(char*);
char* getFirstField(char*);
char* getFieldWithNewline(char*);
/* char* goodwebstr(char*);  */
const char* getEnv(char*, char*);
const char* cgiGetEnv(char*);
extern char* cgiProg;

int cgiMain() {
        char parms[4096];
        char allparms[4096];
        char prog[64];
        char prog1[64];
        char* f;
        int i;
        char configFile[256];

        memset(prog, 0, 64);
        memset(parms, 0, 4096);
        memset(allparms, 0, 4096);
        memset(prog1, 0, 64);
        memset(configFile, 0, 256);

	/* cgiHeaderContentType("text/html"); */
        system("cat content.html");
        
	/* fprintf(cgiOut, "<HTML><HEAD>\n");
	fprintf(cgiOut, "<TITLE>cgic test</TITLE></HEAD>\n");
	fprintf(cgiOut, "<BODY>Hello World</BODY>"); */
        
        
        strcat(parms, "/cgi-bin/");
      
        /* for (i = 0; i < strlen(cgiProg); i++) {
            memset(prog, 0, 64);
            if ( (i + strlen("/exec")) < strlen(cgiProg) ) {
               strncpy(prog, &cgiProg[i], 5);
               if (strcmp(prog, "/exec") == 0) {
                  strcpy(prog, &cgiProg[i+1]);
                  prog[strlen(prog) - 1] = 0; 
                  break;  
               }
            }        
        }
        
        if (strcmp(prog, "execdologin.cgi") == 0) {
           strcpy(prog, "proxy/execproxylogin.cgi");
        } else {
           sprintf(prog1, "%s%s", "calendar/", prog);
           strcpy(prog, prog1);
           fprintf(cgiOut, "<h1>prog = %s</h1>\n", prog); 
        } */

        if (strstr((const char*)cgiProg, (const char*)"execdologin.cgi") != 0) {
           strcpy(prog, "proxy/execproxylogin.cgi");
        } else {
        if (strstr((const char*)cgiProg, (const char*)"execdoprofile.cgi") != 0) {
           strcpy(prog, "proxy/execproxyprofile.cgi");
        } else {
        if (strstr((const char*)cgiProg, (const char*)"execdoprofupdate.cgi") != 0) {
           strcpy(prog, "proxy/execproxyprofupdate.cgi");
        } else {
        if (strstr((const char*)cgiProg, (const char*)"execdocalclient.cgi") != 0) {
           strcpy(prog, "execcalclient.cgi");
        } else {
        if (strstr((const char*)cgiProg, (const char*)"execcalclient.cgi") != 0) {
           strcpy(prog, "execcalclient.cgi");
        } else {
        if (strstr((const char*)cgiProg, (const char*)"execaccessprivatecal.cgi") != 0) {
           strcpy(prog, "execaccessprivatecal.cgi");
        } else {
        if (strstr((const char*)cgiProg, (const char*)"execcreateprivatecal.cgi") != 0) {
           strcpy(prog, "execcreateprivatecal.cgi");
        } else {
        if (strstr((const char*)cgiProg, (const char*)"execeditprivatecal.cgi") != 0) {
           strcpy(prog, "execeditprivatecal.cgi");
        } else {
        if (strstr((const char*)cgiProg, (const char*)"execeditsubscribegroupcal.cgi") != 0) {
           strcpy(prog, "execeditsubscribegroupcal.cgi");
        } else {
        if (strstr((const char*)cgiProg, (const char*)"execgroupcal.cgi") != 0) {
           strcpy(prog, "execgroupcal.cgi");
        } else {
        if (strstr((const char*)cgiProg, (const char*)"execmanagegroupcal.cgi") != 0) {
           strcpy(prog, "execmanagegroupcal.cgi");
        } else {
        if (strstr((const char*)cgiProg, (const char*)"execregister.cgi") != 0) {
           strcpy(prog, "execregister.cgi");
        } else {
        if (strstr((const char*)cgiProg, (const char*)"execsearchgroupcal.cgi") != 0) {
           strcpy(prog, "execsearchgroupcal.cgi");
        } else {
        if (strstr((const char*)cgiProg, (const char*)"execsubscribeprivatecal.cgi") != 0) {
           strcpy(prog, "execsubscribeprivatecal.cgi");
        }  else {
        if (strstr((const char*)cgiProg, (const char*)"execupdategroupcal.cgi") != 0) {
           strcpy(prog, "execupdategroupcal.cgi");
        } } } } } } } } } } } } } } } 

        strcat(parms, prog);
        strcat(parms, "?");
        strcat(parms, getFirstField("biscuit"));
        strcat(parms, getField("password"));
        /* strcat(parms, getField("rpassword")); */
        strcat(parms, getField("login"));
        strcat(parms, getField("jp"));
        strcat(parms, getField("g"));
        strcat(parms, getField("ebanner"));
        strcat(parms, getField("evenue"));
        strcat(parms, getField("eurl"));
        f = strdup(getField("f"));
        strcat(parms, f);
/*        if (strcmp(f, "h") == 0) {
           printf("<HTML><BODY><h1>Logged Out</h1></BODY></HTML>");
           return;
        }  */
        strcat(parms, getField("pgroups"));
        strcat(parms, getField("vw"));
        strcat(parms, getField("dy"));
        strcat(parms, getField("mo"));
        strcat(parms, getField("yr"));
        strcat(parms, getField("h"));
        strcat(parms, getField("m"));
        strcat(parms, getField("a"));
        strcat(parms, getField("en"));
        strcat(parms, getField("jvw"));
        strcat(parms, getField("month"));
        strcat(parms, getField("day"));
        strcat(parms, getField("year"));
        strcat(parms, getField("zone"));
        strcat(parms, getField("hour"));
        strcat(parms, getField("meridian"));
        strcat(parms, getField("min"));
        strcat(parms, getField("recurtype"));
        strcat(parms, getField("atype"));
        strcat(parms, getField("dtype"));
        strcat(parms, getField("subject"));
        strcat(parms, getField("ctype"));
        strcat(parms, getField("corg"));
        strcat(parms, getField("calname"));
        strcat(parms, getField("caltitle"));
        strcat(parms, getField("calpassword"));
        strcat(parms, getField("calrpassword"));
        strcat(parms, getFieldWithNewline("cdesc"));
        strcat(parms, getField("listed"));
        strcat(parms, getField("readonly"));
        strcat(parms, getField("cpublish"));
        strcat(parms, getField("edit"));
        strcat(parms, getField("unsubscribe"));
        strcat(parms, getField("radio1"));
        strcat(parms, getField("status"));
        strcat(parms, getField("delete"));
        strcat(parms, getField("action"));
        strcat(parms, getField("email"));
        strcat(parms, getField("acceptit"));
        strcat(parms, getField("fname"));
        strcat(parms, getField("lname"));
        strcat(parms, getField("street"));
        strcat(parms, getField("city"));
        strcat(parms, getField("state"));
        strcat(parms, getField("zipcode"));
        strcat(parms, getField("country"));
        strcat(parms, getField("phone"));
        strcat(parms, getField("pager"));
        strcat(parms, getField("fax"));
        strcat(parms, getField("cellp"));
        strcat(parms, getField("busp"));
        strcat(parms, getField("pagertype"));
        strcat(parms, getField("checkid"));	
        strcat(parms, getField("informme"));
        strcat(parms, getField("dhour"));
        strcat(parms, getField("dmin"));
        strcat(parms, getField("free"));
        strcat(parms, getField("share"));
        strcat(parms, getFieldWithNewline("desc"));
        strcat(parms, getField("rurl"));
        strcat(parms, getField("priority"));
        strcat(parms, getField("cserver"));
        strcat(parms, getField("hearaboutus"));
        strcat(parms, getField("upgrade"));
        strcat(parms, getField("calkey"));
        strcpy(configFile, cgiGetEnv("SERVER_NAME"));
        strcat(configFile, ".env");
        initConfig(configFile);
        /* strcat(allparms, "export CLASSPATH=/temp/download/jar/hd.jar;"); */
        strcat(allparms, "export CLASSPATH=");
        strcat(allparms, getValue("CLASSPATH"));
        strcat(allparms, ";");
        /* strcat(allparms, "export CLASSPATH=./hd.jar;"); */
        /* strcat(allparms, "export FIREWALL=no;");
        strcat(allparms, "export proxyPort=8080;");
        strcat(allparms, "export CGISUBDIR=calendar;");
        strcat(allparms, "export HTTPSUBDIR=cal;");
        strcat(allparms, "export HDLIC=3243-4323-3434-3243;");
        strcat(allparms, "export proxyHost=proxy.bankamerica.com;");
        strcat(allparms, "export proxySet=true;"); */
        strcat(allparms, "java COM.hotdiary.franchise.FetchCal ");
       
        strcat(parms, "&rh=");
        strcat(parms, getValue("CGISUBDIR"));
        strcat(parms, "&hs=");
        strcat(parms, getValue("HTTPSUBDIR"));
        strcat(parms, "&HDLIC=");
        strcat(parms, getValue("HDLIC"));
        strcat(parms, getEnv("vdomain", "SERVER_NAME"));
        /* strcat(parms, "&rh=calendar");
        strcat(parms, "&hs=hd"); */
        strcat(parms, "&os=nt");
        /* strcat(parms, "&HDLIC=GY99-34JH-37YT-34KJ"); */
        strcat(allparms, " '");
        strcat(allparms, parms);
        strcat(allparms, "' ");
        /* strcat(allparms, cgiGetEnv("FIREWALL")); */
        strcat(allparms, "'");
        strcat(allparms, getValue("FIREWALL"));
        strcat(allparms, "' ");
        /* strcat(allparms, "'yes' "); */
        /* strcat(allparms, cgiGetEnv("proxyPort")); */
        strcat(allparms, "'");
        strcat(allparms, getValue("proxyPort"));
        strcat(allparms, "' ");
        /* strcat(allparms, "'8080' "); */
        strcat(allparms, "'");
        /* strcat(allparms, cgiGetEnv("proxyHost")); */
        strcat(allparms, getValue("proxyHost"));
        /* strcat(allparms, "proxy.bankamerica.com"); */
        strcat(allparms, "' ");
        strcat(allparms, "'");
        /* strcat(allparms, cgiGetEnv("proxySet")); */
        /* strcat(allparms, "true"); */
        strcat(allparms, getValue("proxySet"));
        strcat(allparms, "\' 2>&1");
        /* fprintf(cgiOut, "%s\n", allparms); */
        if (strcmp(getFieldValue("f"), "h") == 0) {
           memset(allparms, 0, 4096);
           sprintf(allparms, "export CLASSPATH=%s; %s '/cgi-bin/proxy/execproxylogout.cgi?biscuit=%s&HDLIC=%s&vdomain=%s&hs=%s&jp=%s' '%s' '%s' '%s' '%s' 2>&1", getValue("CLASSPATH"), "java COM.hotdiary.franchise.FetchCal", getField("biscuit"), getValue("HDLIC"), cgiGetEnv("SERVER_NAME"), getValue("HTTPSUBDIR"), "", getValue("FIREWALL"), getValue("proxyPort"), getValue("proxyHost"), getValue("proxySet"));
        }
        system(allparms);
        return 0;
}

char* getField(char* name) {
   char parmpartprefix[32];
   char parmpartsuffix[256];
   char parmpart[256];
   memset(parmpartprefix, 0, 32);
   memset(parmpart, 0, 256);
   memset(parmpartsuffix, 0, 256);
   sprintf(parmpartprefix, "%c%s=", '&', name);
   cgiFormStringNoNewlines(name, parmpartsuffix, 256);
   /* fprintf(cgiOut, "parmpartsuffix = %s\n", parmpartsuffix); */
   strcat(parmpart, parmpartprefix);
   strcat(parmpart, parmpartsuffix);
   return goodwebstr(parmpart);      
}

char* getFieldValue(char* name) {
   char parmpartsuffix[256];
   memset(parmpartsuffix, 0, 256);
   cgiFormStringNoNewlines(name, parmpartsuffix, 256);
   return goodwebstr(parmpartsuffix);      
}

char* getFirstField(char* name) {
   char parmpartprefix[32];
   char parmpartsuffix[256];
   char parmpart[256];
   memset(parmpartprefix, 0, 32);
   memset(parmpart, 0, 256);
   memset(parmpartsuffix, 0, 256);
   sprintf(parmpartprefix, "%s=", name);
   cgiFormStringNoNewlines(name, parmpartsuffix, 256);
   strcat(parmpart, parmpartprefix);
   strcat(parmpart, parmpartsuffix);
   return goodwebstr(parmpart);      
}

/* char* goodwebstr(char* webstr) {
   return webstr;
} */

const char* getEnv(char* lhs, char* rhs) {
   char parmpart[256];
   char* e;
   memset(parmpart, 0, 256);
   sprintf(parmpart, "%c", '&');
   strcat(parmpart, lhs);
   strcat(parmpart, "=");
   e = getenv(rhs);
   if (!(e)) {
      e = "";
   }
   strcat(parmpart, e);
   /* fprintf(cgiOut, "%s = %s\n", rhs, e); */
   return parmpart;
}

const char* cgiGetEnv(char* name) {
   char* e;
   e = getenv(name);
   if (!(e)) {
      e = "";
   }
   /* fprintf(cgiOut, "%s = %s\n", name, e); */
   return e;
}

char* getFieldWithNewline(char* name) {
   char parmpartprefix[32];
   char parmpartsuffix[256];
   char parmpart[256];
   memset(parmpartprefix, 0, 32);
   memset(parmpart, 0, 256);
   memset(parmpartsuffix, 0, 256);
   sprintf(parmpartprefix, "%c%s=", '&', name);
   cgiFormString(name, parmpartsuffix, 256);
   strcat(parmpart, parmpartprefix);
   strcat(parmpart, parmpartsuffix);
   return goodwebstr(parmpart);      
}