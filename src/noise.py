import random
from debug import dump_func_name
import sys

class noise(object):

    @dump_func_name
    def __init__(self, error_rate):
        self.total_packets_sent = 0
        self.set_err_rate(error_rate)
        self.is_packet_lost()

    @dump_func_name
    def set_err_rate(self, error_rate):
        self.err_rate = error_rate
        # assume that rate < 1 / maxint is negligible
        if self.err_rate > sys.maxsize:
            self.err_rate = sys.maxsize
        self.err_pkt = random.randint(1, self.err_rate)    
        print("packet", self.err_pkt, " of ",self.err_rate," will be lost")
        
    @dump_func_name
    def is_packet_lost(self):
        self.total_packets_sent+=1
        if (self.total_packets_sent % self.err_rate == self.err_pkt):
            self.lost = 1
        else:
            self.lost = 0
        if (self.total_packets_sent % self.err_rate == 0):
            self.set_err_rate(self.err_rate)
        return self.lost
    
if __name__ == "__main__":
    # lose 1 in 500
    n = noise(10)
    for i in range(10):
        f = n.is_packet_lost()
        if f is True:
            print(f, "packet", i, "is lost")