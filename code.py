import board
from adafruit_neopxl8 import NeoPxl8
from adafruit_pixel_framebuf import PixelFramebuffer

first_led_pin = board.NEOPIXEL0

pixels = NeoPxl8(
  first_led_pin,
  128,
  num_strands=1,
  auto_write=True,
  brightness=0.05,
)

pixel_framebuf = PixelFramebuffer(pixels, 8, 16, alternating=False, rotation=3)
# pixel_framebuf.stride = 16

pixel_framebuf.text("43", 2, 0, 0x00467E)
# pixel_framebuf.fill(0x00467E)
pixel_framebuf.display()
