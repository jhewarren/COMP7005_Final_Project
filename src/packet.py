from bidict import bidict


packet_types = bidict(
    ACK=0x1,
    SYN=0x2,
    PUT=0x4,
    GET=0x8,

    PSH=0x10,
    RSD=0x20,
    EM3=0x40,
    DRP=0x80,
)

allowed_multi_types = bidict(
    SYN_ACK=(packet_types["ACK"] ^ packet_types["SYN"]),
    ACK_PSH=(packet_types["ACK"] ^ packet_types["PSH"]),
)


class packet_parser(object):

    def get_packet_type(self, binary):
        t = packet_types.get(binary)
        print("{0:b}".format(binary))
        if t is not None:
            return t
        else:
            print("Multi-type packet found".find)
            t = allowed_multi_types.inv.get(binary)
            return t

    def parse_packet_string(self, pkt_string):
        split = pkt_string.split(":")
        datasize = int(split[5], 10)
        return packet(packet_type=hex(int(split[0], 16)),
                      sequence_number=hex(int(split[1], 16)),
                      ack_number=hex(int(split[2], 16)),
                      window_size=hex(int(split[3], 16)),
                      rport=hex(int(split[4], 16)),
                      data=["".join(split[6:])[i] for i in range(datasize)])


class packet(object):
    def __init__(self, packet_type=0x1, sequence_number=0x1, ack_number=0x0, window_size=5, rport=0x0, data=None):
        self.packet_type = packet_type
        self.sequence_number = sequence_number
        self.ack_number = ack_number
        self.rport = rport
        self.window_size = window_size
        self.data = data

    def __str__(self):
        datasize = len(self.data)
        return "{0}:{1}:{2}:{3}:{4}:{5}:{6}".format(self.packet_type,
                                                    self.sequence_number,
                                                    self.ack_number,
                                                    self.rport,
                                                    self.window_size,
                                                    datasize,
                                                    self.data)


# quick packetize so that no object has to be made
def packetize(packet_type, sequence_number, ack_number, window_size, rport, datasize, data):
    if data is not None:
        datasize = len(data)
    else:
        datasize = 0

    return "{0:2X}:{1:4X}:{2:4X}:{3:4X}:{4:2X}:{5:8X}:{6}".format(packet_type,
                                                                  sequence_number,
                                                                  ack_number,
                                                                  rport,
                                                                  window_size,
                                                                  datasize,
                                                                  data)
