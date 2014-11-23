#!/usr/bin/env python

class frame:
    msg_id = 0
    remote_request = 0
    DLC = 0
    data = []
    CRC_seq = 0
    ACK = 0

    EOF = 0x7F

    def __init__(self):
        self.msg_id = 0
        self.remote_request = 0
        self.dlc = 0
        self.data = []
        self.crc_seq = 0
        self.ack = 0

    def __init__(self, msg_id, RTR, dlc, data, CRC, ACK):
        self.msg_id = msg_id
        self.remote_request = RTR
        self.dlc = dlc
        self.data = data
        self.crc_seq = CRC
        self.ack = ACK

