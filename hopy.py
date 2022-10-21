# The HOPI meter with USB is a CH340 USB-to-serial device, that talks Modbus-RTU
# 
# Piggybacking on the research in  https://github.com/lornix/hopi_hp-9800/blob/master/hopi.c
# - 9600 baud
# - device ID 1
# - data is 20 16-bit words
# - values are mostly 
#   Seems to be 9 floats 
#       32-bit floats values, each spread over 2 registers, DCBA style  https://www.libmodbus.org/docs/v3.1.2/modbus_get_float_dcba.html
#       ...so 18 of the words
#            Active Power   W
#            Current RMS    A
#            Voltage RMS    V
#            Frequency      Hz
#            Power Factor  
#            Annual Power   kWh
#            Active Power   kWh
#            Reactive Power kWh
#            Load Time      mins
#  And two words:
#            Work Hours per Day
#            Device Address
# 
# Uses much of the code from  https://gist.github.com/raplin/76da6392f34934738ff865891a7b672f#file-hopi_hp-9800_python_simple-py
#   so that we can avoid a modbus library as a depdendency


import struct

import serial
import serial.tools.list_ports


def detect_ch340():
    ''' returns a list of pyserial port objects. If we can read out the VID and PID, it will be filtered for only CH340s '''
    ports = list(serial.tools.list_ports.comports())
    filtered_ports = []
    for port in ports:
        if hasattr(ports[0], 'vid'): # seems fair to assume this isn't always there
            if port.vid == 0x1A86  and  port.pid == 0x7523: # TODO: see if there are any more PIDs that should be checked for
                #print("filtered in CH340 serial device: %s, description %s"%(port.name, port.description))
                filtered_ports.append( port )
        else: # can't filter
            filtered_ports.append( port )
    return filtered_ports

def crc(data: bytes):
    poly = 0xa001
    crc  = 0xffff
    for b in data:
        #print( b )
        cur_byte = 0xff & b
        for _ in range(0, 8):
            if (crc & 0x0001) ^ (cur_byte & 0x0001):
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
            cur_byte >>= 1
    ret = struct.pack("<H", crc&0xffff)
    #print(data, ret)
    return ret

def bytes_as_hex(data:bytes):
    return " ".join(["%02x"% d for d in data])


class Hopi:
    REGS = [
            ("Active Power","W"),
            ("RMS Current","A"),
            ("Voltage RMS","V"),
            ("Frequency","Hz"),
            ("Power Factor",""),
            ("Annual Power","kWh"),
            ("Active Power","kWh"),
            ("Reactive Power","kWh"),
            #("Load Time","mins"),
    ]

    def __init__(self, portname=None, verbose=False):
        ' If you do not give this a known port name, it will try to find a CH340 device '
        self.verbose = verbose
        if portname == None:
            ports = detect_ch340()
            #print("Possible ports: %s"%(', '.join(port.name  for port in ports)))
            if len(ports)==0:
                raise RuntimeError( 'No CH340 device found - is the HOPI plugged in?' )

        portname = ports[-1].name # assume it's the last
        #print("Assuming and trying %s"%portname)
        self.port = serial.Serial(portname, baudrate=9600, timeout=1)


    def readRegs(self, first, count, addr=1):
        ' read an amount of Modbus registers from a device ' 
        cmd = 0x03
        fout = []
        m = struct.pack(">BBHH",addr,cmd,first,count)
        m += crc(m)
        if self.verbose:
            print( "\t>", bytes_as_hex(m) )
        self.port.write(m)
        replyLen = 3+(count*2)+2
        r = self.port.read(replyLen)
        if self.verbose:
            print( "\t<", bytes_as_hex(r))
        if len(r) != replyLen:
            print( "Bad reply len",len(r) )
            return
        ccrc = crc( r[:-2] )
        #if ccrc!=r[-2:]: # TODO: fix crc function
        #    print( "bad crc")
        #    return
        addr, f, bcount = struct.unpack(">BBB",r[:3])
        if addr==addr and f==cmd:
            #unpack floats from hopi
            d=r[3:-2]
            fpos=0
            while fpos<len(d):
                fpval=d[fpos:fpos+4]
                v=struct.unpack("<f",fpval)[0]
                fout.append(v)
                fpos+=4
                #print( fpos/2,v)
            return fout
        else:
            print( "Bad reply" )

    def read_all(self):
        ' updates the list of floats that is self.regs '
        self.regs = self.readRegs( 0, len(self.REGS)*2 )



if __name__ == '__main__':
    ' test of this module when you run it directly, not for regular use '
    import time, datetime

    try:
        import serial
    except ImportError as ie:
        print("Error importing pyserial.  You may want to do:  pip3 install pyserial")

    hopi = Hopi()
    while True:
        print('\n===== %s ====='%datetime.datetime.now())
        hopi.read_all()
        for i, reg in enumerate(hopi.regs):
            what, unit = hopi.REGS[i]
            print( '%20s: %10.2f %-5s '%(what,hopi.regs[i], unit) )

        time.sleep( 1 )
