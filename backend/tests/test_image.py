import os
import base64
from io import BytesIO
from PIL import Image
from faker import Faker


fak = Faker()

 # 输入为base64格式字符串，输出为PIL格式图片
def base64_to_image(base64_str):  # 用 b.show()可以展示
    image = base64.b64decode(base64_str, altchars=None, validate=False)
    image = BytesIO(image)
    image = Image.open(image)
    return image

if __name__ == '__main__':
    with open('test.png', 'rb') as f:
        base64_data = base64.b64encode(f.read())
    #print(base64_data)
    #str = base64_data.decode()
    img = base64_to_image(base64_data)
    img.show()