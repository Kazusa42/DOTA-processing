from crop import splitbase
from utils4file import txt2xml, delEmptyFile, layoutTestTxt

BASE_DATA = [r'C:/Users/Kazusa/Desktop/DOTA_TRAIN_BASE/',
             r'C:/Users/Kazusa/Desktop/DOTA_VAL_BASE/']

MULTICROP_DATA = [r'C:/Users/Kazusa/Desktop/DOTA_TRAIN_MULTICROP/',
                  r'C:/Users/Kazusa/Desktop/DOTA_VAL_MULTICROP/']

SINGLECROP_DATA = [r'C:/Users/Kazusa/Desktop/DOTA_TRAIN_SINGLE/',
                   r'C:/Users/Kazusa/Desktop/DOTA_VAL_SINGLE/']


MULTICROP_PARA = {'train': [(640, 50), (1280, 100)],
                  'test': [(640, 50), (1280, 100)]}

SINGLECROP_PARA = {'train': [(1024, 50)],
                   'test': [(1024, 50)]}


if __name__ == '__main__':
    """
    print('Start multi-cropping train and val data.')
    for crop_para in MULTICROP_PARA['train']:
        crop_size, gap = crop_para
        print('Cropping with subsize: %d, gap: %d' % (crop_size, gap))
        split = splitbase(basepath=BASE_DATA[0], outpath=MULTICROP_DATA[0], gap=gap, subsize=crop_size)
        split.splitdata(1)
    print('Multi-crop finished.')
    
    print('Start multi-cropping test data.')
    for crop_para in MULTICROP_PARA['test']:
        crop_size, gap = crop_para
        print('Cropping with subsize: %d, gap: %d' % (crop_size, gap))
        split = splitbase(basepath=BASE_DATA[1], outpath=MULTICROP_DATA[1], gap=gap, subsize=crop_size)
        split.splitdata(1)
    print('Multi-crop finished.')

    print('Start delete empty file and convert annotation into xml format.')
    for crop_data in MULTICROP_DATA:
        delEmptyFile(crop_data)
        txt2xml(crop_data)
    print('Done.')
    
    print('Start single-cropping train and val data.')
    for crop_para in SINGLECROP_PARA['train']:
        crop_size, gap = crop_para
        print('Cropping with subsize: %d, gap: %d' % (crop_size, gap))
        split = splitbase(basepath=BASE_DATA[0], outpath=SINGLECROP_DATA[0], gap=gap, subsize=crop_size)
        split.splitdata(1)
    print('Single-crop for train and val data finished.')

    print('Start single-cropping test data.')
    for crop_para in SINGLECROP_PARA['test']:
        crop_size, gap = crop_para
        print('Cropping with subsize: %d, gap: %d' % (crop_size, gap))
        split = splitbase(basepath=BASE_DATA[1], outpath=SINGLECROP_DATA[1], gap=gap, subsize=crop_size)
        split.splitdata(1)
    print('Single-crop for test data finished.')

    print('Start delete empty file and convert annotation into xml format.')
    for crop_data in SINGLECROP_DATA:
        delEmptyFile(crop_data)
        txt2xml(crop_data)
    print('Done.')
    """
    # Creat test.txt under ./Project1/DOTA/ImageSets/Main

    # print('Layout test.txt for evaluate.')
    # layoutTestTxt(BASE_DATA[1])
    # txt2xml(BASE_DATA[1])






