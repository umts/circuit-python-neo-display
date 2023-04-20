import board
import busio
from adafruit_neopxl8 import NeoPxl8
from adafruit_pixel_framebuf import PixelFramebuffer
from adafruit_led_animation.helper import PixelMap

uart = busio.UART(None, board.RX, baudrate=1000000, parity="odd", stop=1, timeout=0.1)
NUM_DISPLAYS = 6
STRAND_LENGTH = 128
NUM_PIXELS = NUM_DISPLAYS * STRAND_LENGTH

PIXELS = NeoPxl8(
    board.NEOPIXEL0,
    NUM_PIXELS,
    num_strands=NUM_DISPLAYS,
    auto_write=False,
    brightness=0.02,
)

def map_pixels(display_num):
  return PixelMap(
    PIXELS,
    range(display_num * STRAND_LENGTH, (display_num + 1) * STRAND_LENGTH),
    individual_pixels=True,
  )

def frame_buf(display):
  return PixelFramebuffer(display, 8, 16, alternating=False, rotation=0)

def data_frame_to_int(byte):
  return int.from_bytes(recv_buf[byte:byte+2], 'big')

displays = [map_pixels(i) for i in range(NUM_DISPLAYS)]
frame_bufs = [frame_buf(displays[i]) for i in range(NUM_DISPLAYS)]

digit_pixel_map = {
  0: { 0: [0,1,2,3,4,5,6], 1: [0,4,6], 2: [0,3,6], 3: [0,1,2,3,4,5,6] },
  # 1: { 0: [], 1: [1,6], 2: [0,1,2,3,4,5,6], 3: [6] },
  1: {0: [], 1: [], 2: [], 3: [0,1,2,3,4,5,6]},
  2: { 0: [0,3,4,5,6], 1: [0,3,6], 2: [0,3,6], 3: [0,1,2,3,6] },
  3: { 0: [0,3,6], 1: [0,3,6], 2: [0,3,6], 3: [0,1,2,3,4,5,6] },
  4: { 0: [0,1,2,3], 1: [3], 2: [3], 3: [0,1,2,3,4,5,6] },
  5: { 0: [0,1,2,3,6], 1: [0,3,6], 2: [0,3,6], 3: [0,3,4,5,6] },
  6: { 0: [0,1,2,3,4,5,6], 1: [0,3,6], 2: [0,3,6], 3: [0,3,4,5,6] },
  7: { 0: [0], 1: [0], 2: [0], 3: [0,1,2,3,4,5,6] },
  8: { 0: [0,1,2,3,4,5,6], 1: [0,3,6], 2: [0,3,6], 3: [0,1,2,3,4,5,6] },
  9: { 0: [0,1,2,3,6], 1: [0,3,6], 2: [0,3,6], 3: [0,1,2,3,4,5,6] }
}

frame_buf_color_map = {
  0: 0x7E0A6D,
  1: 0x00467E,
  2: 0x00467E,
  3: 0x00467E,
  4: 0xFF0000
}

def custom_num(buf_num, digit, offset):
  for x in range(4):
    for y in digit_pixel_map[digit][x]:
      frame_bufs[buf_num].pixel((x + 1 + offset), y, frame_buf_color_map[buf_num])

def display_custom_num(buf_num, num):
  if num > 999:
    frame_bufs[buf_num].fill(0)
  elif num > 99:
    custom_num(buf_num, num % 10, 10)
    custom_num(buf_num, num // 10**1 % 10, 5)
    custom_num(buf_num, num // 10**2 % 10, 0)
  elif num > 9:
    custom_num(buf_num, num % 10, 7)
    custom_num(buf_num, num // 10**1 % 10, 2)
  else:
    custom_num(buf_num, num, 4)

while True:
  uart.reset_input_buffer()
  recv_buf = uart.read(NUM_DISPLAYS * 2)

  if recv_buf is not None:
    data_frames = [data_frame_to_int(byte) for byte in range(0, NUM_DISPLAYS * 2, 2)]

    for i, data_frame in enumerate(data_frames):
      print(str(i), '->', str(data_frame))
      frame_bufs[i].fill(0)
      if data_frame < 10:
        frame_bufs[i].text(str(data_frame), 5, 0, 0x00467E)
      elif data_frame < 100:
        frame_bufs[i].text(str(data_frame), 2, 0, 0x00467E)
      elif data_frame > 999:
        frame_bufs[i].fill(0)
      else:
        frame_bufs[i].text(str(data_frame), 0, 0, 0x00467E)
      frame_bufs[i].display()

PIXELS.deinit()
