try:
    import Image
except ImportError:
    from PIL import Image

import pytesseract
from time import sleep


im = Image.open('code_1.png')
im.show()
sleep(1)
code_result = pytesseract.image_to_string(im)
print(code_result)
