from bidict import bidict


class packet_parser(object):
    def __init__(self):
        self.packet_types = bidict(
            ACK=0x1,
            SYN=0x2,
            PUT=0x4,
            GET=0x8,

            PSH=0x10,
            RSD=0x20,
            EM3=0x40,
            DRP=0x80,
        )

        self.allowed_multi_types = bidict(
            SYN_ACK=(self.packet_types["ACK"] ^ self.packet_types["SYN"]),
            ACK_PSH=(self.packet_types["ACK"] ^ self.packet_types["PSH"]),
        )

    def get_packet_type(self, binary):
        t = self.packet_types.get(binary)
        print("{0:b}".format(binary))
        if t is not None:
            return t
        else:
            print("Multi-type packet found")
            t = self.allowed_multi_types.inv.get(binary)
            return t

    def parse_packet(self, pkt):
        print(bin(pkt.packet_type))
        return self.get_packet_type(pkt.packet_type)


class packet(object):
    def __init__(self, packet_type=0x1, sequence_number=0x1,
                 ack_number=0x0, rport=0x0, data=None):
        self.packet_type = packet_type
        self.sequence_number = sequence_number
        self.ack_number = ack_number
        self.rport = rport
        self.data = data

    def packetize(self):
        if self.data is not None:
            self.datasize = len(self.data)

        return "{0:X}:{1:X}:{2:X}:{3:X}:{4:X}:{5}".format(self.packet_type,
                                                          self.sequence_number,
                                                          self.ack_number,
                                                          self.rport,
                                                          self.datasize,
                                                          self.data)
