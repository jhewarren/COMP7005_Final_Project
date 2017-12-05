import random
from debug import dump_func_name
import sys
import logging
import time


class noise(object):

    #    @dump_func_name
    def __init__(self, ber, delay):

        self.total_packets_sent = 0
        self.total_errors = 0

        self.logger = logging.getLogger('myapp')
        hdlr = logging.FileHandler('./noise.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)

        self.set_err_rate(ber)
        self.set_ave_delay(delay)

    @dump_func_name
    def set_ave_delay(self, delay):
        if 2 * delay > sys.maxsize:
            self.ave_delay = sys.maxsize / 2
        else:
            self.ave_delay = delay

#    @dump_func_name
    def get_delay(self):
        self.delay = random.randint(0, 2 * self.ave_delay)
#        logger.info('%sms delay',self.delay)
        return self.delay

#    @dump_func_name
    def set_err_rate(self, ber):
        self.err_rate = ber
        # assume that rate < 1 / maxint is negligible
        if self.err_rate > sys.maxsize:
            self.err_rate = sys.maxsize
        # set error packet as random packet between 1 & ber
        self.err_pkt = random.randint(1, self.err_rate)
        print("packet", self.err_pkt, " of ", self.err_rate, " will be lost")
#        logger.info('BER: 1/',ber,'packet: ',self.err_pkt)
        str = "BER:1/%s #%s" % (self.err_rate, self.err_pkt)
        self.logger.warning(str)

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

        self.get_delay()

        str = "# %s err: %s BER:1/%s >%s %s - delay %sms" % (self.total_packets_sent,
                                                             self.total_errors, self.err_rate, self.err_pkt, self.lost, self.delay)
        self.logger.info(str)
        time.sleep(self.delay / 1000)

        return self.lost

    @dump_func_name
    def apply_emu(self):
        self.get_delay()
        self.is_packet_lost()


if __name__ == "__main__":
    # lose 1 in 500
    n = noise(18, 100)
    for i in range(50):
        f = n.is_packet_lost()
        if f is True:
            print(i, " is lost - ", f)
#        else:
#            print(i, " is a-okay")
