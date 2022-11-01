import os

from crop import splitbase
from post_process import txt2xml, delEmptyFile, layoutTestTxt

BASE_DATA = [r'C:/Users/Kazusa/Desktop/DOTA/TRAIN/',
             r'C:/Users/Kazusa/Desktop/DOTA/VAL/']

MULTICROP_DATA = [r'C:/Users/Kazusa/Desktop/DOTA/TRAIN_MULTI/',
                  r'C:/Users/Kazusa/Desktop/DOTA/VAL_MULTI/']

SINGLECROP_DATA = [r'C:/Users/Kazusa/Desktop/DOTA/TRAIN_SINGLE/',
                   r'C:/Users/Kazusa/Desktop/DOTA/VAL_SINGLE/']


MULTICROP_PARA = [(480, 100), (1280, 256)]

SINGLECROP_PARA = [(1280, 50)]


def createFakeTestLabel(test_dir):
    img_dir = test_dir + r'images/'
    # print(img_dir)
    fakeLable_dir = r'C:\Users\Kazusa\Desktop\DOTA\TEST\labelTxt'
    img_list = os.listdir(img_dir)
    for img in img_list:
        print(img.split('.')[0])
        open(os.path.join(fakeLable_dir, img.split('.')[0] + r'.txt'), 'w')


def cropWithParams(crop_paras, base_path, out_path):
    for crop_para in crop_paras:
        crop_size, gap = crop_para
        print('Cropping %s with subsize: %d, gap: %d' % (base_path, crop_size, gap))
        split = splitbase(basepath=base_path, outpath=out_path, gap=gap, subsize=crop_size)
        split.splitdata(1)
        delEmptyFile(out_path)
        txt2xml(out_path)
    print('Crop %s finished.' % base_path)


if __name__ == '__main__':
    """
    # Single crop
    for i in range(len(BASE_DATA)):
        cropWithParams(SINGLECROP_PARA, base_path=BASE_DATA[i], out_path=SINGLECROP_DATA[i])

    """
    # Multi crop
    
    """for i in range(len(BASE_DATA)):
        cropWithParams(MULTICROP_PARA, base_path=BASE_DATA[i], out_path=MULTICROP_DATA[i])"""

    # Creat test.txt under ./Project1/DOTA/ImageSets/Main
    print('Layout test.txt for evaluate.')
    layoutTestTxt(MULTICROP_DATA[1])
    # createFakeTestLabel(BASE_DATA[2])
    # cropWithParams(SINGLECROP_PARA, base_path=BASE_DATA[2], out_path=SINGLECROP_DATA[2])
    # txt2xml(BASE_DATA[1])
