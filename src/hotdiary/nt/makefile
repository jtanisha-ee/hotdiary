#You may wish to add -DNO_UNISTD and -DNO_SYSTEM to CFLAGS if
#your system lacks the /usr/include/unistd.h header file
#or the system() function, respectively. Non-unix systems
#will also definitely have different linker syntax.

CFLAGS=
CC=gcc
AR=ar
LIBS=-L./ -lhdcgic -L./ -lhdenv

all: libhdcgic.a libhdenv.a execdologin.cgi

libhdcgic.a: hdcgic.o hdcgic.h
	rm -f libhdcgic.a
	$(AR) rc libhdcgic.a hdcgic.o

libhdenv.a: hdenv.o hdenv.h
	rm -f libhdenv.a
	$(AR) rc libhdenv.a hdenv.o

execdologin.cgi: execdologin.o libhdcgic.a libhdenv.a
	gcc execdologin.o -o execdologin.cgi ${LIBS}
	
clean:
	rm -f execdologin.o hdcgic.o execdologin.cgi hdenv.o

