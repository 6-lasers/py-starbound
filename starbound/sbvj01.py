import struct
from . import sbon

class SBVJ01(object):
    def __init__(self, stream=None, player_json=None):
        if stream:
            self.stream = stream
            self.read_header()
        if player_json:
            self.name = player_json['name']
            self.version = player_json['version']
            self.data = player_json['data']

    def read_header(self):
        self.stream.seek(0)
        assert self.stream.read(6) == b'SBVJ01', 'Invalid file format'
        
        self.name = sbon.read_string(self.stream)

        # Not sure what this part is.
        assert self.stream.read(1) == b'\x01'

        self.version, = struct.unpack('>i', self.stream.read(4))
        self.data = sbon.read_dynamic(self.stream)
    
    def deserialize(self):
        return self.data
    
    def serialize(self, stream):
        stream.write(b'SBVJ01')
        sbon.write_document(stream, self.name, self.version, self.data)
