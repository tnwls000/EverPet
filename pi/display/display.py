import sys
from PIL import Image
import adafruit_ssd1306
import board
import digitalio
import busio

# board 라이브러리에서 사용하는 지정된 이름은 아래의 경로에서 확인이 가능함.
# /.local/lib/python3.x/site-packages/adafruit_blinka/board/raspberrypi/raspi_40pin.py

# board.SCK_1 = pin.D21
# board.MOSI_1 = pin.D20
# board.MISO_1 = pin.D19
# board.MISO = pin.D9
# board.MOSI = pin.D10
# board.SCK = pin.D11

def update_oled_image(oled1, oled2, imageName):
    # OLED 화면 초기화
    oled1.fill(0)
    oled2.fill(0)
    
    # 감정에 해당하는 이미지 로드
    image1 = Image.open(imageName+"_1.PNG").resize((oled1.width, oled1.height), Image.ANTIALIAS).convert('1')
    image2 = Image.open(imageName+"_2.PNG").resize((oled2.width, oled2.height), Image.ANTIALIAS).convert('1')
    
    # 왼쪽 OLED에 이미지 표시
    oled1.image(image1)
    oled1.show()
    # 오른쪽 OLED에 이미지 표시
    oled2.image(image2)
    oled2.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python display_emotion.py <emotion>")
        sys.exit(1)
    
    # 첫 번째 파라미터로 표시하고자 하는 감정을 받음.
    emotion = sys.argv[1]

    WIDTH = 128
    HEIGHT = 64

    # OLED 세팅
    
    #SPI0 초기세팅
    spi1 = board.SPI() 
    oled1_reset = digitalio.DigitalInOut(board.D25)
    oled1_cs = digitalio.DigitalInOut(board.D8)
    oled1_dc = digitalio.DigitalInOut(board.D24)
    oled1 = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi1, oled1_dc, oled1_reset, oled1_cs)

    #SPI1 초기세팅
    spi2 = busio.SPI(board.SCK_1, MOSI=board.MOSI_1, MISO=board.MISO_1)
    oled2_reset = digitalio.DigitalInOut(board.D26)
    oled2_cs = digitalio.DigitalInOut(board.D18)
    oled2_dc = digitalio.DigitalInOut(board.D13)
    oled2 = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi2, oled2_dc, oled2_reset, oled2_cs)
    
    image_path = f"{emotion}"
    # 이미지의 이름을 감정으로 저장했으므로 그에 맞게 지정
    update_oled_image(oled1, oled2, image_path)
