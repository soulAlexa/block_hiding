from PIL import Image, ImageDraw
import numpy as np
import cv2


def cod_img(img, bits):
    pix = img.load()
    width = img.size[0]
    height = img.size[1]
    draw = ImageDraw.Draw(img)
    mes_counter = 0
    blue = 0
    for i in range(0, width):
        b = 0
        for j in range(0, height):
            red, green, blue = pix[(i, j)]
            b ^= (blue & 1)
        if mes_counter != len(bits):
            if bits[mes_counter] != b:
                blue ^= 1
                mes_counter += 1
                draw.point((i, j), (red, green, blue))
            else:
                mes_counter += 1
                draw.point((i, j), (red, green, blue))

    img.save("cod_kodim03.bmp")


def decod_img(enc_img, num):
    ret = ''
    pix = enc_img.load()
    width = enc_img.size[0]
    height = enc_img.size[1]
    mes_counter = 0
    dec_bits = []
    tmp = 0
    c = 0
    for i in range(0, width):
        b = 0
        for j in range(0, height):
            red, green, blue = pix[(i, j)]
            b ^= (blue & 1)
        if mes_counter != num:
            dec_bits.append(b)
    for i in range(num):
        c += 1
        tmp += dec_bits[i]
        tmp = tmp << 1
        if c == 8:
            tmp = tmp >> 1
            ret += chr(tmp)
            tmp = 0
            c = 0
    return ret


def txt_to_arrbit(messege):
    bits = []
    for line in messege:
        for sim in line:
            sim = ord(sim)
            for i in range(8):
                bits.append((sim & 0x1))
                sim = sim >> 1
            bits[len(bits) - 8:] = reversed(bits[len(bits) - 8:])
    return bits, len(bits)


def get_color(img, c):
    out = []
    for i, e in enumerate(img):
        out.append(np.zeros(e.shape[0]))
        for ii, ee in enumerate(e):
            out[i][ii] = ee[c]

    return np.array(out)

def PSNR(original, compressed):
    original = get_color(original, 0)
    compressed = get_color(compressed, 0)
    mse = np.mean((original - compressed) ** 2)
    if mse == 0:
        return 100
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr


if __name__ == '__main__':
    messege = 'Hello I am AlexasfgsdfgsdfHello I am AlexasfgsdfgsdfHello I am Alex'
    bits, num_of_bits = txt_to_arrbit(messege)
    img = Image.open('kodim03.bmp')
    cod_img(img, bits)
    f_1 = open('test_3.txt', 'w')
    f_1.write(str(num_of_bits))
    f_1.close()
    f_2 = open('test_3.txt', 'r')
    num_of_bits = int(f_2.read())
    enc_img = Image.open('cod_kodim03.bmp')
    print(decod_img(enc_img, num_of_bits))

    img1 = cv2.imread('kodim03.bmp')
    enc_img1 = cv2.imread('cod_kodim03.bmp', 1)
    print(f'Размер сообщения = {len(messege)} PSNR(blue) = {PSNR(img1, enc_img1)}')