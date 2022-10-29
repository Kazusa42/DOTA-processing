import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = 1000000000

CLASSES = ['plane', 'ship', 'storage-tank', 'baseball-diamond', 'tennis-court',
           'basketball-court', 'ground-track-field', 'harbor', 'bridge', 'large-vehicle',
           'small-vehicle', 'helicopter', 'roundabout', 'soccer-ball-field', 'swimming-pool']


def txt2xml(data_dir):
    """
    Script for converting DOTA annotation to VOC annotation
    DOTA annotation format:
    x1, y1, x2, y2, x4, y4, x3, y3, class_name, difficulty, (vertices are arranged in a clockwise order)
    (x1, y1)-----------(x2, y2)
        |                  |
        |                  |
        |                  |
        |                  |
        |                  |
    (x3, y3)-----------(x4, y4)
    """

    annotations_dir = data_dir + r'labelTxt/'
    img_dir = data_dir + r'images/'
    xml_dir = data_dir + r'XML/'
    for filename in os.listdir(annotations_dir):
        fin = open(annotations_dir + filename, 'r')
        image_name = filename.split('.')[0]
        img = Image.open(img_dir + image_name + ".jpg")
        xml_name = xml_dir + image_name + '.xml'
        with open(xml_name, 'w') as fout:
            fout.write('<annotation>' + '\n')

            fout.write('\t' + '<folder>DOTA</folder>' + '\n')
            fout.write('\t' + '<filename>' + image_name + '.jpg' + '</filename>' + '\n')

            fout.write('\t' + '<source>' + '\n')
            fout.write('\t\t' + '<database>' + 'DOTA' + '</database>' + '\n')
            fout.write('\t\t' + '<annotation>' + 'DOTA' + '</annotation>' + '\n')
            fout.write('\t\t' + '<image>' + 'flickr' + '</image>' + '\n')
            fout.write('\t\t' + '<flickrid>' + 'Unspecified' + '</flickrid>' + '\n')
            fout.write('\t' + '</source>' + '\n')

            fout.write('\t' + '<owner>' + '\n')
            fout.write('\t\t' + '<flickrid>' + 'Kazusa' + '</flickrid>' + '\n')
            fout.write('\t\t' + '<name>' + 'Kazusa' + '</name>' + '\n')
            fout.write('\t' + '</owner>' + '\n')

            fout.write('\t' + '<size>' + '\n')
            fout.write('\t\t' + '<width>' + str(img.size[0]) + '</width>' + '\n')
            fout.write('\t\t' + '<height>' + str(img.size[1]) + '</height>' + '\n')
            fout.write('\t\t' + '<depth>' + '3' + '</depth>' + '\n')
            fout.write('\t' + '</size>' + '\n')

            fout.write('\t' + '<segmented>' + '0' + '</segmented>' + '\n')

            for line in fin.readlines():
                line = line.split(' ')
                label = str(line[8])
                # only transfer classes for DOTA v1.0
                if label in CLASSES:
                    fout.write('\t' + '<object>' + '\n')
                    fout.write('\t\t' + '<name>' + str(line[8]) + '</name>' + '\n')
                    fout.write('\t\t' + '<pose>' + 'Unspecified' + '</pose>' + '\n')
                    fout.write('\t\t' + '<truncated>' + line[6] + '</truncated>' + '\n')
                    fout.write('\t\t' + '<difficult>' + str(int(line[9])) + '</difficult>' + '\n')
                    fout.write('\t\t' + '<bndbox>' + '\n')
                    fout.write('\t\t\t' + '<xmin>' + line[0] + '</xmin>' + '\n')
                    fout.write('\t\t\t' + '<ymin>' + line[1] + '</ymin>' + '\n')
                    fout.write('\t\t\t' + '<xmax>' + line[4] + '</xmax>' + '\n')
                    fout.write('\t\t\t' + '<ymax>' + line[5] + '</ymax>' + '\n')
                    fout.write('\t\t' + '</bndbox>' + '\n')
                    fout.write('\t' + '</object>' + '\n')

            fin.close()
            fout.write('</annotation>')


def delEmptyFile(data_dir):
    cnt = 0
    txt_dir = data_dir + r'labelTxt/'
    img_dir = data_dir + r'images/'
    txt_list = os.listdir(txt_dir)
    for file in txt_list:
        if os.path.getsize(txt_dir + file) == 0:
            cnt += 1
            file_id = file.split('.')[0]
            img_name = file_id + '.jpg'
            os.remove(txt_dir + file)
            os.remove(img_dir + img_name)
    print('Delete %d empty file in dir: %s' % (cnt, data_dir))


def layoutTestTxt(test_dir):
    """
    test_dir: DOTA_VAL_CROP
    """
    img_dir = test_dir + r'images/'
    img_list = os.listdir(img_dir)
    with open('test.txt', 'w') as f:
        for img_id in img_list:
            f.write(img_id.split('.')[0] + '\n')
    f.close()


def crateClassifyRes(in_dir, out_dir, classes=None):
    """
    Classify row detection results (results from sub-images) into Catalogs (plane.txt, ship.txt, ...)
    params:
    in_dir: path for row detection results
    out_dir: path to store classified results
    """
    if classes is None:
        classes = CLASSES
    file_dict = {}
    for cls in classes:
        cls_file = open(os.path.join(out_dir, cls + '.txt'), 'w')
        file_dict[str(cls)] = cls_file

    result_files = os.listdir(in_dir)
    for file in result_files:
        img_id = file.split('\\')[-1][:-4]
        for line in open(os.path.join(in_dir, file)):
            line = line.strip('\n').split(' ')
            cat, conf = line[0], line[1]
            xmin, ymin, xmax, ymax = line[2], line[3], line[4], line[5]
            file_dict[cat].write(img_id + ' ' + conf + ' ')
            file_dict[cat].write(xmin + ' ' + ymin + ' ' + xmax + ' ' + ymin + ' ')
            file_dict[cat].write(xmax + ' ' + ymax + ' ' + xmin + ' ' + ymax + '\n')

    for val in file_dict.values():
        val.close()


def mergedRes2ImageRes(in_dir, out_dir):
    """
    Use classified results to create results for each full image
    params:
    in_dir: path for classified results, the out_dir in function "crateClassifyRes"
    out_dir: path to store the final results for each full image in test set
    """
    file_dict = {}
    for cls in list(open(r'./test_full_img_name.txt', 'r')):
        cls_file = open(os.path.join(out_dir, cls.strip('\n') + '.txt'), 'w')
        file_dict[str(cls.strip('\n'))] = cls_file

    merged_files = os.listdir(in_dir)
    for file in merged_files:
        print(file)
        cat = file.split('\\')[-1][:-4]
        for line in open(os.path.join(in_dir, file)):
            line = line.strip('\n').split(' ')
            img_id, conf = line[0][:5], line[1]
            xmin, ymin, xmax, ymax = line[2], line[3], line[6], line[7]
            file_dict[img_id].write(cat + ' ' + conf + ' ')
            file_dict[img_id].write(xmin + ' ' + ymin + ' ' + xmax + ' ' + ymax + '\n')

    for val in file_dict.values():
        val.close()

    # creat empty txt for pictures of objects not detected, in case error accurs while running get_map.py
    gt_imgs = list(open(r'./test_full_img_name.txt', 'r'))
    detection_imgs = os.listdir(out_dir)
    for gt in gt_imgs:
        name = gt.strip('\n') + '.txt'
        if name not in detection_imgs:
            open(os.path.join(final_path, gt.strip('\n') + '.txt'), 'w')


if __name__ == "__main__":
    detections = r'C:\Users\Kazusa\Desktop\yolox-pytorch-main\map_out\detection-results'
    out_path = r'C:\Users\Kazusa\Desktop\out_path1'
    merge_path = r'C:\Users\Kazusa\Desktop\merged_results'
    final_path = r'C:\Users\Kazusa\Desktop\final_result'

    # first classify detection results by category
    # crateClassifyRes(detections, out_path)

    # merge sub-images results into full image results
    # mergebypoly(out_path, merge_path)

    # transform merged resuls into the required format
    mergedRes2ImageRes(merge_path, final_path)
