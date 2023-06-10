# Multiprocessing Video Frame Extraction

## Utilizes mutiprocessing and opencv to extract frames from videos


Credits: @chi0tzp https://github.com/chi0tzp/PyVideoFramesExtractor

This code borrows heavily from the original github above. Please do check it out!

This github was created as the original code did not work for me.

## Usage

```commandline
usage: Extract frames from videos [-h] [--single_vid SINGLE_VID | --data_dir DATA_DIR] [--output_dir OUTPUT_DIR]
                                  [--sample_freq SAMPLE_FREQ] [--num_workers NUM_WORKERS] [--outcsv_dir OUTCSV_DIR]

optional arguments:
  -h, --help            show this help message and exit
  --single_vid SINGLE_VID
                        set single video filename
  --data_dir DATA_DIR   path to source videos
  --output_dir OUTPUT_DIR
                        path to output dir (default='./extracted_frames')
  --sample_freq SAMPLE_FREQ
                        number of frames per second. Input '-1' for all possible frames (default=1)
  --num_workers NUM_WORKERS
                        number of workers for multiprocessing (default=0)
  --outcsv_dir OUTCSV_DIR
                        directory to save csv. Saved at {input}/extracted_frames.csv (default=None)
```

### Example for single video
```commandline
    python extract.py --single_vid test/talking_dog.mp4 --output_dir "./frames" --sample_freq 0.3
```

Extracted frames for the above example will be stored under as follows:

~~~
frames
└── talking_dog
    ├── talking_dog_0.jpg
    ├── talking_dog_1.jpg
    ├── ...
    └── talking_dog_42.jpg
~~~

### Example of output csv

|    | filepath                            | vid_name   |   frame_num |
|---:|:------------------------------------|:-----------|------------:|
|  0 | extracted_frames\abcde\abcde_0.png  | abcde      |           0 |
|  1 | extracted_frames\abcde\abcde_1.png  | abcde      |           1 |
|  2 | extracted_frames\abcde\abcde_2.png  | abcde      |           2 |
|  3 | extracted_frames\abcde\abcde_3.png  | abcde      |           3 |
|  4 | extracted_frames\abcde\abcde_4.png  | abcde      |           4 |
|  5 | extracted_frames\abcde\abcde_5.png  | abcde      |           5 |
|  6 | extracted_frames\abcde\abcde_6.png  | abcde      |           6 |
|  7 | extracted_frames\abcde\abcde_7.png  | abcde      |           7 |
|  8 | extracted_frames\abcde\abcde_8.png  | abcde      |           8 |
|  9 | extracted_frames\abcde\abcde_9.png  | abcde      |           9 |
| 10 | extracted_frames\abcde\abcde_10.png | abcde      |          10 |


Once again, 

Credits: @chi0tzp https://github.com/chi0tzp/PyVideoFramesExtractor
