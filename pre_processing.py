from crop import SplitBase
from txt2xml import txt2xml, delEmptyFile, layoutTestTxt

BASE_DATA = [r'C:/Users/Kazusa/Desktop/DOTA_TRAIN_BASE/',
             r'C:/Users/Kazusa/Desktop/DOTA_VAL_BASE/']

CROP_DATA = [r'C:/Users/Kazusa/Desktop/DOTA_TRAIN_CROP/',
             r'C:/Users/Kazusa/Desktop/DOTA_VAL_CROP/']


CROP_PARA = {'train': [(640, 50), (1280, 100)],
             'test': [(960, 50)]}


if __name__ == '__main__':
    """
    split = SplitBase(basepath=r'C:/Users/Kazusa/Desktop/DOTA_TRAIN_BASE',
                      outpath=r'C:/Users/Kazusa/Desktop/DOTA_TRAIN_CROP',
                      gap=50,
                      subsize=960)
    split.splitdata(1)
    """
    print('Start cropping train and val data.')
    for crop_para in CROP_PARA['train']:
        crop_size, gap = crop_para
        print('Cropping train set with subsize: %d, gap: %d' % (crop_size, gap))
        split = SplitBase(basepath=BASE_DATA[0], outpath=CROP_DATA[0], gap=gap, subsize=crop_size)
        split.splitdata(1)
    print('Crop finished.')

    print('Start cropping test data.')
    crop_size, gap = CROP_PARA['test']
    split = SplitBase(basepath=BASE_DATA[1], outpath=CROP_DATA[1], gap=gap, subsize=crop_size)
    split.splitdata(1)
    print('Crop finished.')

    print('Start delete empty file and convert annotation into xml format.')
    for crop_data in CROP_DATA:
        delEmptyFile(crop_data)
        txt2xml(crop_data)
    print('Done.')

    """
    Creat test.txt under ./Project1/DOTA/ImageSets/Main
    """
    print('Layout test.txt for evaluate.')
    layoutTestTxt(CROP_DATA[1])




