from bidict import bidict


class packet_parser(object):
    def __init__(self):
        self.packet_types = bidict(
            ACK=0b00000001,
            SYN=0b00000010,
            PUT=0b00000100,
            GET=0b00001000,

            PSH=0b00010000,
            RSD=0b00100000,
            EM3=0b01000000,
            DRP=0b10000000,
        )

        self.allowed_multi_types = bidict(
            SYN_ACK=(self.packet_types["ACK"] ^ self.packet_types["SYN"]),
            ACK_PSH=(self.packet_types["ACK"] ^ self.packet_types["PSH"]),
        )

    def get_packet_type(self, binary):
        t = self.packet_types.get(binary)
        if t is not None:
            return t
        else:
            print("Multi-type packet found")
            t = self.allowed_multi_types.inv.get(binary)
            return t

    def parse_packet(self, pack):
        return self.get_packet_type(pack.packet_type)


class packet(object):
    def __init__(self, packet_type=0b00000000, sequence_number=0b0000000000000000,
                 ack_number=0b0000000000000000, rport=0b0000000000000000):
        self.packet_type = packet_type
        self.sequence_number = sequence_number
        self.ack_number = ack_number
        self.rport = rport
