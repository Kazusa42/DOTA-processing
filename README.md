# DOTA-processing  
Codes and tools for pre-processing DOTA dataset and processing precdiction results.

To use the code, especially `merge.py`, please install `swig`. For Windows system, go to the homepage of swig and download the zip pakage and unzip it.

Then add the unzipped folder into system variable. And use the code blow to create the `c++` associations used in `polyiou.py`.
```
./swig -c++ -python file_path_for_polyiou.i
cd to this project's dir
python setup.py build_ext --inplace
```

---

# Update on 2023/05/07  
Integrate some functions.

# Pre-processing  
Pre-processing including crop images and labels, delete empty txt lable file and corresponding images, transform txt label file into xml format.  

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

---

# Post-processing  
Post-processing including transform detection results into required formats and merage results.

All process are in the `main` function of `utils4file.py`. Usages are shown blow.

This script has been rewrotten, in order to speed up file read/write process.


### Transform detection results format  
The original detection result by yolo is like this:  
```
image_id.txt: class_name, confidence, xmin, ymin, xmax, ymax
```  
The required format is like this:  
```
class_name.txt: img_id, configdence, 8 poly coords.
```  
This function is relaised in `crateClassifyRes`.
```
crateClassifyRes(detections_results, classify_results)
```

### Merge
The code is copy from official code. This function will merge all sub-image based results into full image results.  
Still, the output files will be classified based on category
```
mergebypoly(unmerged_label_path, output_path)
```

### Transform merged results to the format for evaluating
The function will transform the mergerd results into the results classified by image id. To let us use `get_map.py` in `Project1` to evaluate the model based on real DOTA v1.0's validation set.
```
mergedRes2ImageRes(merged_results, final_results)
```


 
