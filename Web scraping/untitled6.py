# -*- coding: utf-8 -*-
"""
Created on Fri May 18 11:20:42 2018

@author: 何友鑫
"""
from PIL import Image  
from PIL import ImageEnhance  
import pytesseract
#原始图像  

i2 = Image.open("./valid_pic/ImageCode2.jpg")
imgry = i2.convert('L')   #图像加强，二值化，PIL中有九种不同模式。分别为1，L，P，RGB，RGBA，CMYK，YCbCr，I，F。L为灰度图像
sharpness =ImageEnhance.Contrast(imgry)#对比度增强
i3 = sharpness.enhance(3.0)  #3.0为图像的饱和度
enh_bri = ImageEnhance.Brightness(i3)  
brightness = 3.0  
i4 = enh_bri.enhance(brightness)  
enh_con = ImageEnhance.Contrast(i4)  
contrast = 2.5  
i5 = enh_con.enhance(contrast)  
i4.save("./valid_pic/ImageCode2.jpg")

tessdata_dir_config ='--tessdata-dir "C:\\ProgramFiles (x86)\\Tesseract-OCR\\tessdata"'
code = pytesseract.image_to_string(i3,config=tessdata_dir_config)
print(code)

text=''
text=pytesseract.image_to_string(img)
print(text)
#亮度增强  
enh_bri = ImageEnhance.Brightness(image)  
brightness = 1.5  
image_brightened = enh_bri.enhance(brightness)  
#image_brightened.show()  
#色度增强  
enh_col = ImageEnhance.Color(image)  
color = 1.5  
image_colored = enh_col.enhance(color)  
image_colored.show()  
#对比度增强  
enh_con = ImageEnhance.Contrast(image)  
contrast = 1.5  
image_contrasted = enh_con.enhance(contrast)  
image_contrasted.show()  
#锐度增强  
enh_sha = ImageEnhance.Sharpness(image)  
sharpness = 3.0  
image_sharped = enh_sha.enhance(sharpness)  
image_sharped.show()  
def image_file_to_string(file):

    im=Image.open("./valid_pic/0457.jpg")
    imgry = im.convert('L')#图像加强，二值化
    sharpness =ImageEnhance.Contrast(imgry)#对比度增强
    sharp_img = sharpness.enhance(2.0)
    sharp_img.save("./valid_pic/i0457.jpg")
    #http://www.cnblogs.com/txw1958/archive/2012/02/21/2361330.html
    #imgry.show()#这是分布测试时候用的，整个程序使用需要注释掉
    #imgry.save("E:\\image_code.jpg")
    
    code= pytesseract.image_to_string(im)#code即为识别出的图片数字str类型
    print (code)
    
    
import cv2
    
    
    

def interference_point(img,img_name, x = 0, y = 0):
    """点降噪
    9邻域框,以当前点为中心的田字框,黑点个数
    :param x:
    :param y:
    :return:
    """
    filename =  './out_img/' + img_name.split('.')[0] + '-interferencePoint.jpg'
    # todo 判断图片的长宽度下限
    cur_pixel = img[x,y]# 当前像素点的值
    height,width = img.shape[:2]

    for y in range(0, width - 1):
      for x in range(0, height - 1):
        if y == 0:  # 第一行
            if x == 0:  # 左上顶点,4邻域
                # 中心点旁边3个点
                sum = int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右上顶点
                sum = int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            else:  # 最上非顶点,6邻域
                sum = int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 3 * 245:
                  img[x, y] = 0
        elif y == width - 1:  # 最下面一行
            if x == 0:  # 左下顶点
                # 中心点旁边3个点
                sum = int(cur_pixel) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x, y - 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右下顶点
                sum = int(cur_pixel) \
                      + int(img[x, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y - 1])

                if sum <= 2 * 245:
                  img[x, y] = 0
            else:  # 最下非顶点,6邻域
                sum = int(cur_pixel) \
                      + int(img[x - 1, y]) \
                      + int(img[x + 1, y]) \
                      + int(img[x, y - 1]) \
                      + int(img[x - 1, y - 1]) \
                      + int(img[x + 1, y - 1])
                if sum <= 3 * 245:
                  img[x, y] = 0
        else:  # y不在边界
            if x == 0:  # 左边非顶点
                sum = int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])

                if sum <= 3 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右边非顶点
                sum = int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x - 1, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1])

                if sum <= 3 * 245:
                  img[x, y] = 0
            else:  # 具备9领域条件的
                sum = int(img[x - 1, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1]) \
                      + int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 4 * 245:
                  img[x, y] = 0
    cv2.imwrite(filename,img)
    return img
    
    
img = Image.open('./valid_pic/ImageCode2.jpg')  
img_name='ImageCode2.jpg' 

new_img=interference_point(img,img_name)

img[0,0]
    
    
    
    
from PIL import Image
from pytesseract import *
import PIL.ImageOps
def initTable(threshold=140):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table

im = Image.open('./valid_pic/ImageCode2.jpg')
#图片的处理过程
im = im.convert('L')
binaryImage = im.point(initTable(), '1')
im1 = binaryImage.convert('L')
im2 = PIL.ImageOps.invert(im1)
im3 = im2.convert('1')
im4 = im3.convert('L')
#将图片中字符裁剪保留
box = (30,10,90,28) 
region = im4.crop(box)  
#将图片字符放大
out = i4.resize((120,60)) 
asd = pytesseract.image_to_string(out)
print (asd)
print (out.show())










import itertools



def blackWrite(img):
    blackXY = []

    # 遍历像素点
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            print (img.getpixel((x,y)))
            if img.getpixel((x,y))<128:
                img.putpixel((x,y),0) # 置为黑点
                blackXY.append((x,y))
            else:
                img.putpixel((x,y),255) # 置为白点
    return blackXY


# 去除干扰点
def clrImg(img,pointArr):
    # 获取周围黑点的个数
    def getN(p):
        count = 0
        x = [p[0]-1,p[0],p[0]+1]
        y = [p[1]-1,p[1],p[1]+1]
        for i in itertools.product(x,y):  # 笛卡尔积
            try:
                if img.getpixel(i) == 0:
                    count +=1
            except:
                print ('out of')
                continue
        print (count)
        return count

    for p in pointArr:
        if getN(p)<5:  #  周围黑点个数 <5 的黑点认为是干扰点,置为白点
            img.putpixel(p,255)

pointArr =  blackWrite(img)
clrImg(img,pointArr)
img.save("C:/img_1.jpg")




