from __future__ import annotations
import struct
from dataclasses import dataclass

MAGIC = b"VS"           # 2 bytes
VERSION = 1             # 1 byte
# Header format: ! 2s B B I H H H  (big-endian / network byte order)
# Fields: magic(2s), version(B), flags(B), frame_id(I), packet_idx(H), total_packets(H), payload_size(H)
HEADER_STRUCT = struct.Struct("!2sBBIHHH")
HEADER_SIZE = HEADER_STRUCT.size  # 14 bytes

FLAG_MARKER = 0x01  # last packet of the frame

MAX_DATAGRAM = 1400  # conservative to avoid IP fragmentation on most networks
MAX_PAYLOAD = MAX_DATAGRAM - HEADER_SIZE

@dataclass
class Header:
    magic: bytes = MAGIC
    version: int = VERSION
    flags: int = 0
    frame_id: int = 0
    packet_idx: int = 0
    total_packets: int = 0
    payload_size: int = 0

    def pack(self) -> bytes:
        return HEADER_STRUCT.pack(
            self.magic, self.version, self.flags,
            self.frame_id, self.packet_idx, self.total_packets, self.payload_size
        )

    @staticmethod
    def unpack(data: bytes) -> "Header":
        magic, version, flags, frame_id, packet_idx, total_packets, payload_size = HEADER_STRUCT.unpack(data)
        return Header(magic, version, flags, frame_id, packet_idx, total_packets, payload_size)
