import random
class noise(object):

    @dump_func_name
    def __init__(self)
        global total_packets_sent = 0

    @dump_func_name
    def set_err_rate(self, error_rate)

        global err_pkt
        global err_rate = error_rate

        // assume that rate < 1/maxint is negligible
        if error_rate > sys.maxint:
            error_rate = sys.maxint
        err_pkt = random.randint(1,err_rate)

    @dump_func_name
    def is_packet_lost(self)
        total_packets_sent++
        if (total_packets_sent %= err_rate == err_pkt):
            self.lost = true
        else:
            self lost = false
        if (total_packets_sent %= err_rate == 0):
                set_err_rate(err_rate)
        