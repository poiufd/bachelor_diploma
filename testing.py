import ctypes, numpy, struct
import Leap

def save_frame(frame,fd):
	serialized_tuple = frame.serialize
	data = serialized_tuple[0]
	size = serialized_tuple[1]
	fd.write(struct.pack("i", size))
	data_address = data.cast().__long__()
	buffer = (ctypes.c_ubyte * size).from_address(data_address)
	fd.write(buffer)

def load_frames(fname):
	fd = open(fname, "rb")
	next_block_size = fd.read(4)
	while next_block_size:
		size = struct.unpack('i', next_block_size)[0]
		data = fd.read(size)
		leap_byte_array = Leap.byte_array(size)
		address = leap_byte_array.cast().__long__()
		ctypes.memmove(address, data, size)

       	#frame = Leap.Frame()
        #frame.deserialize((leap_byte_array, size))
        #next_block_size = fd.read(4)
