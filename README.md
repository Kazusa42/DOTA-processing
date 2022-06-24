# DOTA-processing  
Codes and tools for pre-processing DOTA dataset and processing precdiction results.

To use the code, especially `merge.py`, please install `swig`. For Windows system, go to the homepage of swig and download the zip pakage and unzip it.

Then add the unzipped folder into system variable. And use the code blow to create the `c++` associations used in `polyiou.py`.
```
./swig -c++ -python
python setup.py build_ext --inplace
```

However, `merge.py` has been removed.
---

# Pre-processing  
Pre-processing including crop images and labels, delete empty txt lable file and corresponding images, transform txt label file into xml format, split data into train, val.

All these process are in `pre_processing.py`. Usages are shown blow.

### Crop  
```
split = SplitBase(basepath=r'C:/Users/Kazusa/Desktop/DOTA_TRAIN_BASE',
                      outpath=r'C:/Users/Kazusa/Desktop/DOTA_TRAIN_CROP',
                      gap=50,
                      subsize=960)
    split.splitdata(1)
```

### Delete empty txt file  
```
delEmptyFile(dataset_dir)
```

### Txt to xml  
```
txt2xml(dataset_dir)
```  
