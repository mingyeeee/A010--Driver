from fpioa_manager import fm
from machine import UART
import lcd, image

# lcd.init(invert=True)
lcd.init()
img = image.Image()

fm.register(24, fm.fpioa.UART1_TX, force=True)
fm.register(25, fm.fpioa.UART1_RX, force=True)

uart_A = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)

def uart_readBytes():
    return uart_A.read()


def uart_hasData():
    return uart_A.any()


def uart_sendCmd(cmd):
    uart_A.write(cmd)

uart_sendCmd(b"AT+BAUD=5\r") # Set baud to 5
 
uart_A.deinit()

uart_A = UART(UART.UART1, 921600, 8, 0, 0, timeout=1000, read_buf_len=4096) # reinit at 921000



def show(frameData, res):
    resR = res[0]
    resC = res[1]
    for y in range(resR):
        for x in range(resC):
            pixel_cmap_rgb = jetcolors[frameData[y*resR + x]]
            img.set_pixel(110 + x, 70 + y, pixel_cmap_rgb)
    lcd.display(img)
    img.clear()

FRAME_HEAD = b"\x00\xFF"
FRAME_TAIL = b"\xCC"

from struct import unpack
# send_cmd("AT+BINN=2\r")
uart_sendCmd(b"AT+DISP=5\r") # set display 5
uart_sendCmd(b"AT+FPS=10\r") # set fps 10

# while True:
#     if uart_hasData():
#         print(uart_readBytes())

rawData = b''
while True:
    if not uart_hasData():
        continue
    rawData += uart_readBytes() # append the byte
    idx = rawData.find(FRAME_HEAD) # find frame head "\x00\xFF"
    if idx < 0: # if not found, keep waiting for bytes
        continue
    rawData = rawData[idx:]
    # print(rawData)
    # check data length 2Byte
    dataLen = unpack("H", rawData[2: 4])[0] 
    # print("len: "+str(dataLen))
    frameLen = len(FRAME_HEAD) + 2 + dataLen + 2# checksum has 1 byte, and EOT byte
    frameDataLen = dataLen - 16

    if len(rawData) < frameLen:
        continue
    # get data
    frame = rawData[:frameLen]
    # print(frame.hex())
    rawData = rawData[frameLen:]

    frameTail = frame[-1]
    # print("tail: "+str(hex(frameTail)))
    _sum = frame[-2]
    # print("checksum: "+str(hex(_sum)))
    # check sum
    # spi has no checksum but i add one
    if frameTail != 0xdd and _sum != sum(frame[:frameLen - 2]) % 256:
        continue

    frameID = unpack("H", frame[16:18])[0]
    # print("frame ID: "+str(frameID))

    resR = unpack("B", frame[14:15])[0]
    resC = unpack("B", frame[15:16])[0]
    res = (resR, resC)
    # print(res)
    # frameData=[ unpack("H", frame[20+i:22+i])[0] for i in range(0, frameDataLen, 2) ]
    frameData = [unpack("B", frame[20+i:21+i])[0]
                    for i in range(0, frameDataLen, 1)]

    show(frameData, res)

    del frameData
