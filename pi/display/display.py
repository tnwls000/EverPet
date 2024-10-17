import sys
from PIL import Image
import adafruit_ssd1306
import board
import digitalio
import busio

# board ���̺귯������ ����ϴ� ������ �̸��� �Ʒ��� ��ο��� Ȯ���� ������.
# /.local/lib/python3.x/site-packages/adafruit_blinka/board/raspberrypi/raspi_40pin.py

# board.SCK_1 = pin.D21
# board.MOSI_1 = pin.D20
# board.MISO_1 = pin.D19
# board.MISO = pin.D9
# board.MOSI = pin.D10
# board.SCK = pin.D11

def update_oled_image(oled1, oled2, imageName):
    # OLED ȭ�� �ʱ�ȭ
    oled1.fill(0)
    oled2.fill(0)
    
    # ������ �ش��ϴ� �̹��� �ε�
    image1 = Image.open(imageName+"_1.PNG").resize((oled1.width, oled1.height), Image.ANTIALIAS).convert('1')
    image2 = Image.open(imageName+"_2.PNG").resize((oled2.width, oled2.height), Image.ANTIALIAS).convert('1')
    
    # ���� OLED�� �̹��� ǥ��
    oled1.image(image1)
    oled1.show()
    # ������ OLED�� �̹��� ǥ��
    oled2.image(image2)
    oled2.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python display_emotion.py <emotion>")
        sys.exit(1)
    
    # ù ��° �Ķ���ͷ� ǥ���ϰ��� �ϴ� ������ ����.
    emotion = sys.argv[1]

    WIDTH = 128
    HEIGHT = 64

    # OLED ����
    
    #SPI0 �ʱ⼼��
    spi1 = board.SPI() 
    oled1_reset = digitalio.DigitalInOut(board.D25)
    oled1_cs = digitalio.DigitalInOut(board.D8)
    oled1_dc = digitalio.DigitalInOut(board.D24)
    oled1 = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi1, oled1_dc, oled1_reset, oled1_cs)

    #SPI1 �ʱ⼼��
    spi2 = busio.SPI(board.SCK_1, MOSI=board.MOSI_1, MISO=board.MISO_1)
    oled2_reset = digitalio.DigitalInOut(board.D26)
    oled2_cs = digitalio.DigitalInOut(board.D18)
    oled2_dc = digitalio.DigitalInOut(board.D13)
    oled2 = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi2, oled2_dc, oled2_reset, oled2_cs)
    
    image_path = f"{emotion}"
    # �̹����� �̸��� �������� ���������Ƿ� �׿� �°� ����
    update_oled_image(oled1, oled2, image_path)
