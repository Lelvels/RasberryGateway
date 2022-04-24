from socket import timeout
import serial

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

ser = serial.Serial('COM5', 9600, timeout = 1)
start_trans = False;

while True:
    if(ser.in_waiting):
        byte1 = int_from_bytes(ser.read(1))
        byte2 = int_from_bytes(ser.read(1))
        byte3 = int_from_bytes(ser.read(1))
        byte4 = int_from_bytes(ser.read(1))
        byte5 = int_from_bytes(ser.read(1))
        if(byte5 == 0):
            print("Byte1: ", byte1, " ", "Byte2: ", byte2, " ", "Byte3: ", byte3, " ", "Byte4: ", byte4, " ")
            ch1 = 256*byte1 + byte2
            ch2 = 256*byte3 + byte4
            print("CH1: ", ch1, " ", "CH2: ", ch2)
        # recv_byte = ser.read(1)
        # value = int_from_bytes(recv_byte)
        # print(value)
        
    

ser.close()