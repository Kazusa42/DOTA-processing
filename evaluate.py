import numpy as np


def parse_gt(filename):
    objects = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        splitlines = [x.strip().split(' ') for x in lines]
        for splitline in splitlines:
            object_struct = {'name': splitline[8]}
            if len(splitline) == 9:
                object_struct['difficult'] = 0
            elif len(splitline) == 10:
                object_struct['difficult'] = int(splitline[9])
            # object_struct['difficult'] = 0
            object_struct['bbox'] = [int(float(splitline[0])),
                                     int(float(splitline[1])),
                                     int(float(splitline[4])),
                                     int(float(splitline[5]))]
            w = int(float(splitline[4])) - int(float(splitline[0]))
            h = int(float(splitline[5])) - int(float(splitline[1]))
            object_struct['area'] = w * h
            objects.append(object_struct)
    return objects


def voc_ap(rec, prec, use_07_metric=False):
    """
    ap = voc_ap(rec, prec, [use_07_metric])
    Compute VOC AP given precision and recall.
    If use_07_metric is true, uses the
    VOC 07 11 point method (default:False).
    """
    if use_07_metric:
        ap = 0.
        for t in np.arange(0., 1.1, 0.1):
            if np.sum(rec >= t) == 0:
                p = 0
            else:
                p = np.max(prec[rec >= t])
            ap = ap + p / 11.
    else:
        mrec = np.concatenate(([0.], rec, [1.]))
        mpre = np.concatenate(([0.], prec, [0.]))

        for i in range(mpre.size - 1, 0, -1):
            mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

        i = np.where(mrec[1:] != mrec[:-1])[0]

        ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
    return ap


def voc_eval(detpath, annopath, imagesetfile, classname, ovthresh=0.5, use_07_metric=False):
    """
    rec, prec, ap = voc_eval(detpath, annopath, imagesetfile, classname, [ovthresh], [use_07_metric])
    Top level function that does the PASCAL VOC evaluation.
    detpath: Path to detections
        detpath.format(classname) should produce the detection results file.
    annopath: Path to annotations
        annopath.format(imagename) should be the xml annotations file.
    imagesetfile: Text file containing the list of images, one image per line.
    classname: Category name (duh)
    [ovthresh]: Overlap threshold (default = 0.5)
    [use_07_metric]: Whether to use VOC07's 11 point AP computation
        (default False)
    """

    # first load gt
    # read list of images
    with open(imagesetfile, 'r') as f:
        lines = f.readlines()
    imagenames = [x.strip() for x in lines]
    # print('imagenames: ', imagenames)

    # load annots
    recs = {}
    for i, imagename in enumerate(imagenames):
        # print('parse_files name: ', annopath.format(imagename))
        recs[imagename] = parse_gt(annopath.format(imagename))

    class_recs = {}
    npos = 0
    for imagename in imagenames:
        R = [obj for obj in recs[imagename] if obj['name'] == classname]
        bbox = np.array([x['bbox'] for x in R])
        difficult = np.array([x['difficult'] for x in R]).astype(np.bool)
        det = [False] * len(R)
        npos = npos + sum(~difficult)
        class_recs[imagename] = {'bbox': bbox,
                                 'difficult': difficult,
                                 'det': det}

    # read detection results
    detfile = detpath.format(classname)
    with open(detfile, 'r') as f:
        lines = f.readlines()

    splitlines = [x.strip().split(' ') for x in lines]
    image_ids = [x[0] for x in splitlines]
    confidence = np.array([float(x[1]) for x in splitlines])

    BB = np.array([[float(z) for z in x[2:]] for x in splitlines])

    # sort by confidence
    sorted_ind = np.argsort(-confidence)

    BB = BB[sorted_ind, :]
    image_ids = [image_ids[x] for x in sorted_ind]

    nd = len(image_ids)
    tp, fp = np.zeros(nd), np.zeros(nd)
    for d in range(nd):
        R = class_recs[image_ids[d]]
        bb = BB[d, :].astype(float)
        ovmax = -np.inf
        BBGT = R['bbox'].astype(float)

        if BBGT.size > 0:
            # compute overlaps
            ixmin = np.maximum(BBGT[:, 0], bb[0])
            iymin = np.maximum(BBGT[:, 1], bb[1])
            ixmax = np.minimum(BBGT[:, 2], bb[2])
            iymax = np.minimum(BBGT[:, 3], bb[3])
            iw = np.maximum(ixmax - ixmin + 1., 0.)
            ih = np.maximum(iymax - iymin + 1., 0.)
            inters = iw * ih

            # union
            uni = ((bb[2] - bb[0] + 1.) * (bb[3] - bb[1] + 1.) +
                   (BBGT[:, 2] - BBGT[:, 0] + 1.) *
                   (BBGT[:, 3] - BBGT[:, 1] + 1.) - inters)

            overlaps = inters / uni
            ovmax = np.max(overlaps)
            jmax = np.argmax(overlaps)

        if ovmax > ovthresh:
            if not R['difficult'][jmax]:
                if not R['det'][jmax]:
                    tp[d] = 1.
                    R['det'][jmax] = 1
                else:
                    fp[d] = 1.
        else:
            fp[d] = 1.

    # compute precision recall

    print('check fp:', fp)
    print('check tp', tp)

    print('npos num:', npos)
    fp = np.cumsum(fp)
    tp = np.cumsum(tp)

    rec = tp / float(npos)
    # avoid divide by zero in case the first detection matches a difficult
    # ground truth
    prec = tp / np.maximum(tp + fp, np.finfo(np.float64).eps)
    ap = voc_ap(rec, prec, use_07_metric)

    return rec, prec, ap


def evaluate():
    detpath = r'PATH_TO_BE_CONFIGURED/Task2_{:s}.txt'
    # change the directory to the path of val/labelTxt, if you want to do evaluation on the valset
    annopath = r'PATH_TO_BE_CONFIGURED/{:s}.txt'
    imagesetfile = r'PATH_TO_BE_CONFIGURED/valset.txt'

    classnames = ['plane', 'baseball-diamond', 'bridge', 'ground-track-field', 'small-vehicle', 'large-vehicle', 'ship',
                  'tennis-court',
                  'basketball-court', 'storage-tank', 'soccer-ball-field', 'roundabout', 'harbor', 'swimming-pool',
                  'helicopter']
    classaps = []
    mAP = 0
    for classname in classnames:
        print('classname:', classname)
        rec, prec, ap = voc_eval(detpath, annopath, imagesetfile, classname, ovthresh=0.5, use_07_metric=False)
        mAP = mAP + ap
        # print('rec: ', rec, 'prec: ', prec, 'ap: ', ap)
        print('ap: ', ap)
        classaps.append(ap)

        # uncomment to plot p-r curve for each category
        # plt.figure(figsize=(8,4))
        # plt.xlabel('recall')
        # plt.ylabel('precision')
        # plt.plot(rec, prec)
        # plt.show()
    mAP = mAP / len(classnames)
    print('map:', mAP)
    classaps = 100 * np.array(classaps)
    print('classaps: ', classaps)


if __name__ == '__main__':
    evaluate()
