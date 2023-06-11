# Multiprocessing Video Frame Extraction (Python)

## Utilizes Mutiprocessing and OpenCV to Extract Frames From Videos

### Credits to: @chi0tzp https://github.com/chi0tzp/PyVideoFramesExtractor
This code copies heavily from the original github above. Please do check it out!

This github was created as the code above did not work for me.


This applications allows for customizable multiprocessing of video frame extraction, with an optional CSV output at the end containing filepaths to all extracted frames for easier further data processing.

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

### Example for single video (use --single_vid)
```commandline
    python extract.py --single_vid test/abcde.mp4 --output_dir "./frames" --sample_freq 0.3 --outcsv_dir "./"
```

Extracted frames for the above example will be stored under as follows:

~~~
frames
└── abcde
    ├── abcde_0.p
    ├── abcde_1.png
    ├── ...
    └── abcde_2.png
~~~

Output CSV for the above example will be as follows

|    | filepath                            | vid_name   |   frame_num |
|---:|:------------------------------------|:-----------|------------:|
|  0 | extracted_frames\abcde\abcde_0.png  | abcde      |           0 |
|  1 | extracted_frames\abcde\abcde_1.png  | abcde      |           1 |
|  2 | extracted_frames\abcde\abcde_2.png  | abcde      |           2 |
|  3 | extracted_frames\abcde\abcde_3.png  | abcde      |           3 |
...

### Samples Usage for a directory with multiprocessing (use --data-dir)
```commandline
    python extract.py --data_dir "./videos" --sample_freq 2 --num_workers 4 --outcsv_dir "./" 
```

Once again, 

Credits to: @chi0tzp https://github.com/chi0tzp/PyVideoFramesExtractor
