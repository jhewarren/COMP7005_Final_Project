import random
from debug import dump_func_name
import sys

class noise(object):

    @dump_func_name
    def __init__(self, ber):
        self.total_packets_sent = 0
        self.set_err_rate(ber)

    @dump_func_name
    def set_err_rate(self, ber):
        self.err_rate = ber
        # assume that rate < 1 / maxint is negligible
        if self.err_rate > sys.maxsize:
            self.err_rate = sys.maxsize
        # set error packet as random packet between 1 & ber
        self.err_pkt = random.randint(1, self.err_rate)    
        print("packet", self.err_pkt, " of ",self.err_rate," will be lost")
        
    @dump_func_name
    def is_packet_lost(self):

        # Is_error if total_packets mod ber = error_packet
        if (self.total_packets_sent % self.err_rate == self.err_pkt):
            self.lost = True
        else:
            self.lost = False

        # change error packet sequence number on every ber packets
        if (self.total_packets_sent % self.err_rate == self.err_rate - 1):
            self.set_err_rate(self.err_rate)

        self.total_packets_sent+=1

        return self.lost
    
if __name__ == "__main__":
    # lose 1 in 500
    n = noise(10)
    for i in range(30):
        f = n.is_packet_lost()
        if f is True:
            print(f, "packet", i, "is lost")
        else:
            print(i, " is a-okay")