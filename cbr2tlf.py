#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
import time

class Logfile(object):
    def __init__(self, fname):
        self.fname = fname
        self.fpopened = False
        self.lines = []

    def open(self, mode = "r"):
        if self.fpopened == False:
            try:
                self.fp = open(self.fname, mode)
                self.fpopened = True
            except:
                print "Can't open file: %s" % (self.fname)
                return False
        return True

    def read(self):
        if self.fpopened != True:
            print "File isn't opened: %s" % (self.fname)
            return False
        self.lines = [l.strip() for l in self.fp.readlines()]
        return True

    def close(self):
        if self.fpopened == True:
            self.fp.close()
        return True

    def write(self):
        if self.fpopened != True:
            print "File isn't opened: %s" % (self.fname)
            return False
        for l in self.lines:
            self.fp.write(l + "\n")
        return True

class Cabrillo(Logfile):
    def __init__(self, fname):
        Logfile.__init__(self, fname)

    def write(self):
        pass

    def parse(self):
        lines = []
        for l in self.lines:
            words = l.split()
            if words[0] == "QSO:":
                lines.append(words[1:])
        return lines

class Tlflog(Logfile):
    def __init__(self, fname):
        Logfile.__init__(self, fname)

    def read(self):
        pass

class CBR2Tlf(object):
    def __init__(self, src):
        self.fieldmaps = {
            3: 6,
            4: 7,
            5: 5,
            6: 8,
            7: 9,
        }
        self.src = src
        dst = ".".join(self.src.split(".")[:-1]) + ".log"
        self.cabrillo = Cabrillo(src)
        self.tlflog = Tlflog(dst)

    def convert(self):
        self.cabrillo.open()
        self.cabrillo.read()
        self.tlflog.open("w")
        for l in self.cabrillo.parse():
            line = []
            line.append(self.freq2band(l[0], l[1]))
            line.append(time.strftime("%d-%b-%y", time.strptime(l[2], "%Y-%m-%d")))
            t = [l[3][0:2], l[3][2:4]]
            line.append("%s:%s" % (t[0], t[1]))
            line.append(l[6])
            line.append(l[7].ljust(15))
            line.append(l[5])
            line.append(l[8])
            line.append(l[9])
            line.append("1")
            line.append("%s.0" % l[0])
            self.tlflog.lines.append("%5s  %s %s %s  %15s%s  %s %4s                    %s  %7s" % (tuple(line)))
        self.tlflog.write()
        self.tlflog.close()
        self.cabrillo.close()

    def freq2band(self, freq, mode):
        if int(freq) < 2000:
            band = "160"
        elif int(freq) < 4000:
            band = " 80"
        elif int(freq) < 8000:
            band = " 40"
        elif int(freq) < 15000:
            band = " 20"
        elif int(freq) < 22000:
            band = " 15"
        else:
            band = " 10"

        if mode == "CW":
            band += "CW"
        if mode == "PH":
            band += "SSB"

        return band

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Argument missing"
        print "Use: %s CABRILLO.LOG" % (sys.argv[0])
        sys.exit(-1)
    src = sys.argv[1]
    cbr2tlf = CBR2Tlf(src)
    cbr2tlf.convert()


