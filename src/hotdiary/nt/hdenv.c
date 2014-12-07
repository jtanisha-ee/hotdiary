#include <stdio.h>

struct hdvar {
    char name[1024];
    char value[1024];
    struct hdvar* next;
};

struct hdvar *hdvarlist;

int initConfig(char* filename) {
   FILE* fd;
   char aline[1024];
   struct hdvar* hdnext;
   struct hdvar* hdprev;
   int i;
   int k, g;

   memset(aline, 0, 1024); 
   if ((fd = fopen(filename, "r")) == 0) {
      perror("fopen");
      exit(1);
   }

   hdvarlist = (struct hdvar*)malloc(sizeof(struct hdvar));
   memset(hdvarlist->name, 0, 1024);
   memset(hdvarlist->value, 0, 1024);
   hdnext = 0;
   hdprev = 0;

   while (1) {
/* if finished with file, exit the loop */
      if (fgets(aline, 1024, fd) == 0) {
          break;
      }
/* Reject blank and commented lines */
      if ( (aline[0] == '#') || (aline[0] == '\n') ) {
          continue;      
      }  else {
              for (i = 0; i < strlen(aline); i++) {
                   if ( (aline[i] != ' ') && (aline[i] != '\t') ) {
                       break;
                   }
              }
              if (aline[i] == '\n') break;
              /* printf("line = %s", aline); */
/* if this is the first element of list, do different stuff */
              if (hdnext != 0) {
                 hdnext = (struct hdvar*)malloc(sizeof(struct hdvar));
                 memset(hdnext->name, 0, 1024);
                 memset(hdnext->value, 0, 1024);
                 hdprev->next = hdnext;
                 hdnext->next = 0;
                 hdprev = hdnext;
              } else {
                    hdnext = hdvarlist;
                    hdprev = hdvarlist;
              }
              /* printf("%s = %s\n", hdvarlist->name, hdvarlist->value); */
              for (k = 0; i < strlen(aline); i++,k++) {
                   if ( (aline[i] != '=') && (aline[i] != ' ') && (aline[i] != '\t') ) {
                       hdnext->name[k] = aline[i];
                   } else {
                       break;
                   }
              }
              hdnext->name[i] = 0;
              /* printf("hdnext->name = %s\n", hdnext->name); */
/* allow for arbitrary number of blanks, tabs and one equal to */
              for (; i < strlen(aline); i++) {
                   if ( (aline[i] != '=') && (aline[i] != ' ') && (aline[i] != '\t') ) {
                       break;
                   }
              }
              for (k = 0; i < strlen(aline); i++,k++) {
                   if (aline[i] != '\n') {
                          hdnext->value[k] = aline[i];
                   } else { 
                         hdnext->value[k] = 0;
                         break;
                   }
              }
              hdnext->value[k] = 0;
              /* printf("hdnext->value = %s\n", hdnext->value); */
      }
   }

}

void debugConfig() {
    struct hdvar* hdnext;
/* Print the linked list */
   hdnext = hdvarlist;
   /* printf("%s = %s\n", hdvarlist->name, hdvarlist->value); */
   do  {
         printf("%s = \"%s\"\n", hdnext->name, hdnext->value);
         hdnext = hdnext->next;
   } while (hdnext != 0);
}

const char* getValue(char* name) {
   struct hdvar* hdnext;
   hdnext = hdvarlist;
   while (hdnext != 0) {
        if (strcmp(hdnext->name, name) == 0) {
            return hdnext->value;
        }
        hdnext = hdnext->next;
   }
   return "";
}

char* goodwebstr(char* str) {
     char* goodstr;
     int i;
     goodstr = (char*)malloc(4096);
     memset(goodstr, 0, 4096);
     /* printf("strlen = %d\n", strlen(str)); */
     for (i = 0; i < strlen(str); i++) {
/*           if (str[i] == '|') {
                   strcat(goodstr, "%7c");
              } else {
              if (str[i] == '\'') {
                   strcat(goodstr, "%27");
              } else {
              if (str[i] == ';') {
                   strcat(goodstr, "%3b");
              } else {
              if (str[i] == '#') {
                   strcat(goodstr, "%23");
              } else {
              if (str[i] == ':') {
                   strcat(goodstr, "%3a");
              } else {
              if (str[i] == '/') {
                   strcat(goodstr, "%2f");
              } else {
              if (str[i] == ')') {
                   strcat(goodstr, "%29");
              } else {
              if (str[i] == '(') {
                   strcat(goodstr, "%28");
              } else {
              if (str[i] == '+') {
                   strcat(goodstr, "%2b");
              } else {
              if (str[i] == ',') {
                   strcat(goodstr, "%2c");
              } else {
              if (str[i] == '-') {
                   strcat(goodstr, "%2d");
              } else {
              if (str[i] == '.') {
                   strcat(goodstr, "%2e");
              } else {
              if (str[i] == '>') {
                   strcat(goodstr, "%3e");
              } else {
              if (str[i] == '<') {
                   strcat(goodstr, "%3c");
              } else {
              if (str[i] == '"') {
                   strcat(goodstr, "%22");
              } else {
              if (str[i] == '!') {
                   strcat(goodstr, "%21");
              } else {
              if (str[i] == '~') {
                   strcat(goodstr, "%7e");
               } else {
              if (str[i] == '{') {
                   strcat(goodstr, "%7b");
               } else {
              if (str[i] == '}') {
                   strcat(goodstr, "%7d");
              } else {
              if (str[i] == '[') {
                   strcat(goodstr, "%5b");
              } else {
              if (str[i] == '\\') {
                   strcat(goodstr, "%5c");
              } else {
              if (str[i] == ']') {
                   strcat(goodstr, "%5d");
              } else {
              if (str[i] == '_') {
                   strcat(goodstr, "%5f");
              } else {
              if (str[i] == '^') {
                   strcat(goodstr, "%5e");
              } else {   */
              if (str[i] == ' ') {
                   strcat(goodstr, "%20");
              } else {
              if (str[i] == '\r') {
                 strcat(goodstr, "%0d");
              } else {
              if (str[i] == '\n') {
                 strcat(goodstr, "%0a");
              } else {
              strncat(goodstr, &str[i], 1);
              }}} /* }}}}}}}}}}}}}}}}}}}}}}}} */
     }
     return goodstr;    
}

void status(char* msg) {
     printf("Content-type: text/html\n\n");
     printf("<HTML><HEAD><META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html;CHARSET=iso-8859-1\"><TITLE>1800Calendar - Calendar Reminders Address Book Organizer PIM Memo To-Do Pager Fax Groups Planner Appointments Free</TITLE></HEAD><BODY BGCOLOR=ffffff><TABLE BORDER=0 BORDERCOLOR=0000ff WIDTH=\"100%\" HEIGHT=\"100%\" CELLSPACING=0 CELLPADDING=0> <TR> <TD VALIGN=CENTER ALIGN=CENTER><TABLE BORDER=2 BORDERCOLOR=0000ff WIDTH=\"80%\" HEIGHT=\"20%\" CELLSPACING=0 CELLPADDING=0> <TR BGCOLOR=dddddd> <TD ALIGN=CENTER>Status Message</TD></TR><TR><TD>ALIGN=CENTER><FONT SIZE=3 FACE=Verdana>%s</FONT></TD></TR></TABLE></TD></TR></TABLE></BODY></HTML>", msg);
}

/*
int main(int argc, char** argv) {
    if (argc != 2) {
       fprintf(stderr, "Usage: %s <name>\n", argv[0]);
       exit(1);
    }
    initConfig("isail.vip.best.com.env");
    debugConfig();
    printf("%s = %s\n", argv[1], getValue(argv[1]));
    printf("%s\n", goodwebstr("&|\'=?;#:/)(+,-.><\"!~{}a[\\]_^ "));
} 
*/