from crop import SplitBase
from txt2xml import txt2xml, delEmptyFile

BASE_DATA = [r'C:/Users/Kazusa/Desktop/DOTA_TRAIN_BASE/',
             r'C:/Users/Kazusa/Desktop/DOTA_VAL_BASE/']

CROP_DATA = [r'C:/Users/Kazusa/Desktop/DOTA_TRAIN_CROP/',
             r'C:/Users/Kazusa/Desktop/DOTA_VAL_CROP/']


MULTI_CROP = r'true'
CROP_SIZE = {'true': [640, 1280],
             'false': [960]}[MULTI_CROP]

CROP_PARA = {'true': [(640, 50), (1280, 100)],
             'false': [(960, 50)]}[MULTI_CROP]


if __name__ == '__main__':
    """
    split = SplitBase(basepath=r'C:/Users/Kazusa/Desktop/DOTA_TRAIN_BASE',
                      outpath=r'C:/Users/Kazusa/Desktop/DOTA_TRAIN_CROP',
                      gap=50,
                      subsize=960)
    split.splitdata(1)
    """
    print('Start cropping.')
    for crop_para in CROP_PARA:
        crop_size, gap = crop_para
        for i in range(len(BASE_DATA)):
            print('Cropping with subsize: %d, gap: %d' % (crop_size, gap))
            split = SplitBase(basepath=BASE_DATA[i], outpath=CROP_DATA[i], gap=gap, subsize=crop_size)
            split.splitdata(1)
    print('Crop finished.')
    print('Start delete empty file and convert annotation into xml format.')
    for crop_data in CROP_DATA:
        delEmptyFile(crop_data)
        txt2xml(crop_data)
    print('Done.')


