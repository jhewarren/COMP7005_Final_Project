from bidict import bidict

PACKET_TYPES = bidict(
    ACK=0x1,
    SYN=0x2,
    PUT=0x4,
    GET=0x8,

    PSH=0x10,
    RSD=0x20,
    TMT=0x40,
    DRP=0x80,
)

ALLOWED_MULTI_TYPES = bidict(
    SYN_ACK=(PACKET_TYPES["ACK"] ^ PACKET_TYPES["SYN"]),
    ACK_PSH=(PACKET_TYPES["ACK"] ^ PACKET_TYPES["PSH"]),
    PUT_PSH=(PACKET_TYPES["PUT"] ^ PACKET_TYPES["PSH"]),
)


class packet_parser(object):

    def get_packet_type(self, binary):
        t = PACKET_TYPES.get(binary)
        if t is not None:
            return t

        t = PACKET_TYPES.inv.get(binary)
        if t is not None:
            return t

        t = ALLOWED_MULTI_TYPES.get(binary)
        if t is not None:
            return t

        t = ALLOWED_MULTI_TYPES.inv.get(binary)
        if t is not None:
            return t

        return None

    def parse_packet_string(self, pkt_string):
        return packet(packet_type=int(pkt_string[0:2], 16),
                      sequence_number=int(pkt_string[2:6], 16),
                      ack_number=int(pkt_string[6:10], 16),
                      rport=int(pkt_string[10:14], 16),
                      window_size=int(pkt_string[14:16], 16),
                      datasize=int(pkt_string[16:24], 16),
                      data=(pkt_string[24:]))


class packet(object):
    def __init__(self, packet_type=0x1, sequence_number=0x0, ack_number=0x0, window_size=5, rport=0x0, datasize=0, data=None):
        self.packet_type = packet_type
        self.sequence_number = sequence_number
        self.ack_number = ack_number
        self.rport = rport
        self.window_size = window_size
        self.datasize = datasize
        self.data = data

    def check_packet(self, packet_type=None, sequence_number=None, ack_number=None):
        pt_true = True
        sn_true = True
        an_true = True
        if packet_type is not None:
            pt_true = self.packet_type == packet_type
        if sequence_number is not None:
            sn_true = self.sequence_number == sequence_number
        if ack_number is not None:
            an_true = self.ack_number == ack_number

        return pt_true & sn_true & an_true

    def packetize(self):
        return packetize(packet_type=self.packet_type,
                         sequence_number=self.sequence_number,
                         ack_number=self.ack_number,
                         window_size=self.window_size,
                         rport=self.rport,
                         data=self.data)


# quick packetize so that no object has to be made
def packetize(packet_type, sequence_number, ack_number, window_size, rport, data):
    if data is not None:
        datasize = len(data)
    else:
        datasize = 0
        data = b''

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

    def put_chunk(self, pkt):
        self.file.write(pkt.data)
        self.file.flush()
