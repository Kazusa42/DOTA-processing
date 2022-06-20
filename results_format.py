"""
re-format the detection results into the format like:
task1_classname.txt
----img_name confidence poly
----img_name confidence poly
...
"""
import os


OUT_PATH = r'C:\Users\lyin0\OneDrive\桌面\format_res/'


def formatRes(res_path):
    resfile_list = os.listdir(res_path)
    for file in resfile_list:
        file_id = file.split('.')[0]
        with open(res_path + file) as f:
            print('open successed')
            lines = f.readlines()
            for line in lines:
                """
                info = [class, confi, x_min, y_min, x_max, y_max]
                """
                line = line.strip('\n')
                info = line.split(' ')
                txt_name = info[0] + '.txt'
                txt = open(OUT_PATH + txt_name, 'a')
                print('writing')
                txt.write(file_id + ' ')
                txt.write(info[1] + ' ')
                txt.write(info[2] + ' ' + info[3] + ' ' + info[4] + ' ' + info[3] + ' ')
                txt.write(info[4] + ' ' + info[5] + ' ' + info[2] + ' ' + info[5] + '\n')
                txt.close()


if __name__ == '__main__':
    formatRes(r'C:\Users\lyin0\OneDrive\桌面\res/')
