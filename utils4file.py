import os
from PIL import Image

import dota_utils as utils
from merge import mergebypoly


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

            fout.write('\t' + '<folder>DOTA 1.0</folder>' + '\n')
            fout.write('\t' + '<filename>' + image_name + '.jpg' + '</filename>' + '\n')

            fout.write('\t' + '<source>' + '\n')
            fout.write('\t\t' + '<database>' + 'DOTA 1.0' + '</database>' + '\n')
            fout.write('\t\t' + '<annotation>' + 'DOTA 1.0' + '</annotation>' + '\n')
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


def crateClassifyRes(result_dir, classify_res_dir):
    result_files = os.listdir(result_dir)
    for file in result_files:
        img_id = file.split('\\')[-1][:-4]
        for line in open(os.path.join(result_dir, file)):
            line = line.strip('\n').split(' ')
            # print(line)
            cat, conf = line[0], line[1]
            xmin, ymin, xmax, ymax = line[2], line[3], line[4], line[5]
            with open(os.path.join(classify_res_dir, cat + '.txt'), 'a+') as f:
                f.write(img_id + ' ' + conf + ' ')
                f.write(xmin + ' ' + ymin + ' ' + xmax + ' ' + ymin + ' ')
                f.write(xmax + ' ' + ymax + ' ' + xmin + ' ' + ymax + '\n')


def mergedRes2ImageRes(merged_path, detection_path):
    merged_files = os.listdir(merged_path)
    for file in merged_files:
        cat = file.split('\\')[-1][:-4]
        for line in open(os.path.join(merged_path, file)):
            line = line.strip('\n').split(' ')
            img_id, conf = line[0], line[1]
            xmin, ymin, xmax, ymax = line[2], line[3], line[6], line[7]
            with open(os.path.join(detection_path, img_id + '.txt'), 'a+') as f:
                f.write(cat + ' ' + conf + ' ')
                f.write(xmin + ' ' + ymin + ' ' + xmax + ' ' + ymax + '\n')


if __name__ == "__main__":
    detections = r'C:\Users\Kazusa\Desktop\Project1-main\map_out\detection-results'
    out_path = r'C:\Users\Kazusa\Desktop\out_path1'
    # first classify detection results by category
    crateClassifyRes(detections, out_path)

    # merge sub-images results into full image results
    mergebypoly(out_path, r'C:\Users\Kazusa\Desktop\merged_results')

    # transform merged resuls into the required format
    mergedRes2ImageRes(r'C:\Users\Kazusa\Desktop\merged_results',
                       r'C:\Users\Kazusa\Desktop\Project1-main\map_out\detection-results')
