from bidict import bidict
from debug import dump_func_name
from binascii import unhexlify

packet_types = bidict(
    ACK=0x1,
    SYN=0x2,
    PUT=0x4,
    GET=0x8,

    PSH=0x10,
    RSD=0x20,
    TMT=0x40,
    DRP=0x80,
)

allowed_multi_types = bidict(
    SYN_ACK=(packet_types["ACK"] ^ packet_types["SYN"]),
    ACK_PSH=(packet_types["ACK"] ^ packet_types["PSH"]),
    PUT_PSH=(packet_types["PUT"] ^ packet_types["PSH"]),
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
        return packet(packet_type=int(pkt_string[0:2], 16),
                      sequence_number=int(pkt_string[2:6], 16),
                      ack_number=int(pkt_string[6:10], 16),
                      rport=int(pkt_string[10:14], 16),
                      window_size=int(pkt_string[14:16], 16),
                      datasize=int(pkt_string[16:24], 16),
                      data=(pkt_string[24:]))


class packet(object):
    def __init__(self, packet_type=0x1, sequence_number=0x1, ack_number=0x0, window_size=5, rport=0x0, datasize=0, data=None):
        self.packet_type = packet_type
        self.sequence_number = sequence_number
        self.ack_number = ack_number
        self.rport = rport
        self.window_size = window_size
        self.datasize = datasize
        self.data = data

    def __str__(self):
        return b"%2X%4X%4X%4X%2X%8X%b" % (self.packet_type,
                                          self.sequence_number,
                                          self.ack_number,
                                          self.rport,
                                          self.window_size,
                                          self.datasize,
                                          self.data)


# quick packetize so that no object has to be made
def packetize(packet_type, sequence_number, ack_number, window_size, rport, data):
    if data is not None:
        datasize = len(data)
    else:
        datasize = 0

    return b"%2X%4X%4X%4X%2X%8X%b" % (packet_type,
                                      sequence_number,
                                      ack_number,
                                      rport,
                                      window_size,
                                      datasize,
                                      data)


class reassembler(object):
    def __init__(self, file_name):
        self.filename = file_name
        self.file = open(file_name, "wb")

    def __del__(self):
        if self.file is not None:
            self.file.close()

    @dump_func_name
    def put_chunk(self, pkt):
        print(pkt.data)
        self.file.write(pkt.data)
        self.file.flush()
