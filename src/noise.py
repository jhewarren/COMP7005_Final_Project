import random
from debug import dump_func_name
import sys

class noise(object):

    @dump_func_name
    def __init__(self, error_rate):
        self.total_packets_sent = 0
        self.set_err_rate(error_rate)

    @dump_func_name
    def set_err_rate(self, error_rate):
        self.err_rate = error_rate
        # assume that rate < 1 / maxint is negligible
        if self.err_rate > sys.maxsize:
            self.err_rate = sys.maxsize
        
        # set error packet as random packet between 1 & error_rate
        self.err_pkt = random.randint(1, self.err_rate)

    #@dump_func_name
    def is_packet_lost(self)
        # Is_error if total_packets mod error_rate = error_packet
        if (self.total_packets_sent % self.err_rate == self.err_pkt):
            is_lost = True
            # if self.err_pkt == (self.total_packets_sent) 
        else: 
            is_lost = False

        self.total_packets_sent += 1
        # change error packet sequence number on every error_rate packets
        if (total_packets_sent == error_rate):
            self.set_err_rate(error_rate)
        return is_lost


if __name__ == "__main__":
    # lose 1 in 500
    n = noise(10)
    for i in range(10):
        f = n.is_packet_lost()
        if f is True:
            print(f, "packet", i, "is lost")
