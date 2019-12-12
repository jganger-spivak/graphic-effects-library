import lzma

class ByteReader:
    def __init__(self, file):
        self.data = lzma.decompress(file.read(-1))
        self.pointer = 0
    def read(self, numbytes):
        returnbytes = bytearray(numbytes)
        try:
            for index in range(0, numbytes):
                returnbytes[index] = self.data[self.pointer+index]
        except IndexError: #EOF! Return empty bytes
            return bytes(0)
        self.pointer += numbytes
        return returnbytes
    def peek(self, numbytes):
        returnbytes = bytearray(numbytes)
        try:
            for index in range(0, numbytes):
                returnbytes[index] = self.data[self.pointer+index]
        except IndexError: #EOF! Return empty bytes
            return bytes(0)
        return returnbytes
