from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import string
from PIL import Image, ImageFilter

def generate_captcha(size=(120, 40), chars=string.ascii_letters + string.digits, captcha_length=5):
    # 随机生成验证码文本
    captcha_text = ''.join(random.choice(chars) for _ in range(captcha_length))

    # 创建一个新图片
    image = Image.new('RGB', size, (255, 255, 255))
    draw = ImageDraw.Draw(image)


    font = ImageFont.truetype("arial.ttf", 24)

    # 绘制文本
    draw.text((10, 10), captcha_text, font=font, fill=(0, 0, 0))
    #draw.text((10, 10), captcha_text, fill=(0, 0, 0))

    # 添加一些噪点
    for _ in range(25):
        draw.point((random.randint(0, size[0]), random.randint(0, size[1])), fill=(0, 0, 0))

    image = image.filter(ImageFilter.GaussianBlur(radius=1.5))

    return image, captcha_text


