from crop import splitbase
from post_process import txt2xml, delEmptyFile, layoutTestTxt

BASE_DATA = [r'C:/Users/lyin0/Desktop/DOTA/TRAIN/',
             r'C:/Users/lyin0/Desktop/DOTA/VAL/']

MULTICROP_DATA = [r'C:/Users/lyin0/Desktop/TRAIN_MULTI/',
                  r'C:/Users/lyin0/Desktop/VAL_MULTI/']

SINGLECROP_DATA = [r'C:/Users/lyin0/Desktop/DOTA/TRAIN_SINGLE/',
                   r'C:/Users/lyin0/Desktop/DOTA/VAL_SINGLE/']


MULTICROP_PARA = [(480, 100), (1280, 256)]

SINGLECROP_PARA = [(1280, 50)]


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
    Single crop
    """
    for i in range(len(BASE_DATA)):
        cropWithParams(SINGLECROP_PARA, base_path=BASE_DATA[i], out_path=SINGLECROP_DATA[i])

    """
    Multi crop
    """
    """for i in range(len(BASE_DATA)):
        cropWithParams(MULTICROP_PARA, base_path=BASE_DATA[i], out_path=MULTICROP_DATA[i])"""

    # Creat test.txt under ./Project1/DOTA/ImageSets/Main
    # print('Layout test.txt for evaluate.')
    # layoutTestTxt(MULTICROP_DATA[1])
    # txt2xml(BASE_DATA[1])
