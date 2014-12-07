The JDK 1.1.4 implementation is different between
NT 3.51 and Win95.

Win95

- It is case sensitive. NETSCAPE.HST and netscape.hst
are assumed to be two different files in JDK.
- If you use F:\, it does not work. You cannot have
a backslash (or even forward slash) after the 
drive letter. You have to use F: only.

NT 3.51

- It is not case senstive. File.list() returns
only lowercase names.
- F:\ works fine.

So we need to take care of all these ideosyncracies
between platforms. The goal is to make everything
work automatically in the code, irrespective of
what the user types on any platform.