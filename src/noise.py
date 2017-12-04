import random
from debug import dump_func_name
import sys
import logging

class noise(object):

#    @dump_func_name
    def __init__(self, ber):
        self.total_packets_sent = 0
        self.total_errors = 0
        self.set_err_rate(ber)


#    @dump_func_name
    def set_err_rate(self, ber):
        self.err_rate = ber
        # assume that rate < 1 / maxint is negligible
        if self.err_rate > sys.maxsize:
            self.err_rate = sys.maxsize
        # set error packet as random packet between 1 & ber
        self.err_pkt = random.randint(1,self.err_rate)
        print("packet", self.err_pkt, " of ",self.err_rate," will be lost")
#        mylog.info('BER: 1/',ber,'packet: ',self.err_pkt)
        
#    @dump_func_name
    def is_packet_lost(self):
        self.total_packets_sent += 1

        # Is_error if total_packets mod ber = error_packet
        if (self.total_packets_sent % self.err_rate == self.err_pkt):
            self.lost = True
            self.total_errors += 1
        else:
            self.lost = False

        # change error packet sequence number on every ber packets
        if (self.total_packets_sent % self.err_rate == self.err_rate - 1):
            self.set_err_rate(self.err_rate)

        return self.lost
    
if __name__ == "__main__":
    # lose 1 in 500
    mylog = logging.getLogger('myapp')
    hdlr = logging.FileHandler('./noise.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    mylog.addHandler(hdlr) 
    mylog.setLevel(logging.WARNING)
    n = noise(10)
    for i in range(30):
        f = n.is_packet_lost()
        str = "# %s err: %s BER:1/%s >%s %s"%(n.total_packets_sent,n.total_errors,n.err_rate,n.err_pkt,f)
        mylog.error(str)
        if f is True:
            print(i, " is lost - ",f)
#        else:
#            print(i, " is a-okay")