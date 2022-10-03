from crop import splitbase
from post_process import txt2xml, delEmptyFile, layoutTestTxt

BASE_DATA = [r'C:/Users/Kazusa/Desktop/DOTA_TRAIN_BASE/',
             r'C:/Users/Kazusa/Desktop/DOTA_VAL_BASE/']

MULTICROP_DATA = [r'C:/Users/Kazusa/Desktop/DOTA_TRAIN_MULTICROP/',
                  r'C:/Users/Kazusa/Desktop/DOTA_VAL_MULTICROP/']

SINGLECROP_DATA = [r'C:/Users/Kazusa/Desktop/DOTA_TRAIN_SINGLE/',
                   r'C:/Users/Kazusa/Desktop/DOTA_VAL_SINGLE/']


MULTICROP_PARA = {'train': [(480, 100), (1280, 256)],
                  'test': [(480, 100), (1280, 100)]}

SINGLECROP_PARA = {'train': [(1280, 50)],
                   'test': [(1280, 50)]}


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
    # cropWithParams(SINGLECROP_PARA['train'], base_path=BASE_DATA[0], out_path=SINGLECROP_DATA[0])
    # cropWithParams(SINGLECROP_PARA['test'], base_path=BASE_DATA[1], out_path=SINGLECROP_DATA[1])

    """
    Multi crop
    """
    # cropWithParams(MULTICROP_PARA['train'], base_path=BASE_DATA[0], out_path=MULTICROP_DATA[0])
    # cropWithParams(MULTICROP_PARA['test'], base_path=BASE_DATA[1], out_path=MULTICROP_DATA[1])

    # Creat test.txt under ./Project1/DOTA/ImageSets/Main
    # print('Layout test.txt for evaluate.')
    layoutTestTxt(MULTICROP_DATA[1])
    # txt2xml(BASE_DATA[1])
