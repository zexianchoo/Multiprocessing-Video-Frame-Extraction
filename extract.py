import os
from os import walk
import os.path as osp
import argparse
import cv2
import math
from tqdm import tqdm
import pandas as pd
from functools import partial
from  multiprocessing import Pool

supported_video_ext = ('.avi', '.mp4')
supported_frame_ext = ('.jpg', '.png')


class FrameExtractor:
    def __init__(self, video_file, output_dir, frame_ext='.png', sampling=-1):

        # Check if given video file exists -- abort otherwise
        if osp.exists(video_file):
            self.video_file = video_file
        else:
            raise FileExistsError('Video file {} does not exist.'.format(video_file))

        self.sampling = sampling

        # Create output directory for storing extracted frames
        self.output_dir = output_dir
        if not osp.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Get extracted frame file format
        self.frame_ext = frame_ext

        # Capture given video stream
        self.video = cv2.VideoCapture(self.video_file)

        # Get video fps
        self.video_fps = self.video.get(cv2.CAP_PROP_FPS)

        # Get video length in frames
        self.video_length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        if self.sampling != -1:
            self.video_length = self.video_length // self.sampling

        self.file_name = self.video_file.split('\\')[-1].split(".")[0]

    def extract(self):
        # Get first frame
        success, frame = self.video.read()
        frame_cnt = 0
        frame_num = 0
        while success:
            # get current frame filename
            curr_frame_filename = osp.join(self.output_dir, "{}_{}{}".format(self.file_name, frame_num, self.frame_ext))
            cv2.imwrite(curr_frame_filename, frame)

            # Get next frame
            success, frame = self.video.read()

            if self.sampling != -1:
                frame_cnt += math.ceil(self.sampling * self.video_fps)
                self.video.set(1, frame_cnt)
            else:
                frame_cnt += 1
            frame_num += 1

        return frame_num


def extract_video_frames_mp(data_dir, output_dir, sample_freq, v_file):
    if os.stat(osp.join(data_dir, v_file[0])).st_size > 0:
        # Set up video extractor for given video file
        extractor = FrameExtractor(video_file=osp.join(data_dir, v_file[0]),
                                   output_dir=osp.join(output_dir, v_file[1]),
                                   sampling=sample_freq)

        # Extract and crop frames
        num_frames = extractor.extract()

        # return a tuple of file num, and num_frames
        return extractor.file_name, num_frames

def check_sampling_param(s):
    s_ = float(s)
    if (s_ <= 0) and (s_ != -1):
        raise argparse.ArgumentTypeError("Please give a positive number of seconds or -1 for extracting all frames.")
    return s_


def main():
    # set args
    global args

    parser = argparse.ArgumentParser("Extract frames from videos")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--single_vid', type=str, help='set single video filename')
    group.add_argument("--data_dir", type=str, help="path to source videos")
    parser.add_argument("--output_dir", type=str, default='./extracted_frames', help="path to output dir (default='./extracted_frames')")
    parser.add_argument("--sample_freq", type=check_sampling_param, default=1, help="number of frames per second. Input '-1' for all possible frames (default=1)")
    parser.add_argument("--num_workers", type=int, default=0, help="number of workers for multiprocessing (default=0)")
    parser.add_argument("--outcsv_dir", type=str, default=None, help="directory to save csv. Saved at {input}/extracted_frames.csv (default=None)")
    args = parser.parse_args()

    # make output folders
    os.makedirs(os.path.join(args.output_dir), exist_ok=True)

    if args.sample_freq == -1:
        print("#. Extract all available frames.")
    else:
        print("#. Extract one frame every {} seconds.".format(args.sample_freq))


    # Extract frames from a (single) given video file
    if args.single_vid:

        # Setup video extractor for given video file
        video_basename = osp.basename(args.single_vid).split('.')[0]
        # Check video file extension
        video_ext = osp.splitext(args.single_vid)[-1]
        if video_ext not in supported_video_ext:
            raise ValueError("Not supported video file format: {}".format(video_ext))
        # Set extracted frames output directory
        output_dir = osp.join(args.output_dir, '{}'.format(video_basename))
        # Set up video extractor for given video file
        extractor = FrameExtractor(video_file=args.single_vid, output_dir=output_dir, sampling=args.sample_freq)
        # Extract frames
        res = extractor.extract()

        if args.outcsv_dir:

            # concat df from this imap to saved_csv
            video_name = extractor.file_name
            max_num = res
            filelist = [osp.join(osp.relpath(args.output_dir), ("{}\{}_{}.png".format(video_name, video_name, i))) for i in
                        range(0, max_num)]
            saved_csv = pd.DataFrame(list(zip(filelist,
                                    [video_name] * max_num,
                                    [i for i in range(0, max_num)])),
                                    columns=['filepath', 'vid_name', 'frame_num'])
    if args.data_dir:
        print("#. Extract frames from videos under dir : {}".format(osp.relpath(args.data_dir)))
        print("#. Store output csv at                  : {}".format(osp.relpath(args.outcsv_dir) + "processed_files.csv"))
        print("#. Scan for video files...")

        # Scan given dir for video files
        video_list = []
        for r, d, f in walk(args.data_dir):
            for file in f:
                file_basename = osp.basename(file).split('.')[0]
                video_list.append([osp.join(osp.relpath(r, args.data_dir), file),
                                   osp.join(osp.relpath(r, args.data_dir), "{}".format(file_basename))])

        # static csv which we will return
        saved_csv = pd.DataFrame()

        # Try multiprocessing:
        partial_augment = partial(extract_video_frames_mp, args.data_dir, args.output_dir, args.sample_freq)
        with Pool(processes=args.num_workers) as p:
            with tqdm(total=len(video_list)) as pbar:
                for i, res in enumerate(p.imap(partial_augment, video_list)):

                    if args.outcsv_dir:

                        # concat df from this imap to saved_csv
                        video_name, max_num = res
                        filelist = [osp.join(args.output_dir, ("{}\{}_{}.png".format(video_name, video_name, i))) for i in range(0, max_num)]
                        df = pd.DataFrame(list(zip(filelist,
                                                   [video_name]*max_num,
                                                   [i for i in range(0,max_num)])),
                                          columns =['filepath', 'vid_name', 'frame_num'])
                        saved_csv = pd.concat([saved_csv, df], axis=0, ignore_index=True)
                    pbar.update()
    print("#. Store extracted frames under: {}".format(osp.relpath(args.output_dir)))

    # save csv to record filenames
    if args.outcsv_dir:
        saved_csv.to_csv(osp.join(args.outcsv_dir, r'processed_files.csv'), index=False)
        print("#. CSV file available at                : {}".format(osp.join(args.outcsv_dir, r'processed_files.csv')))


if __name__ == '__main__':
    main()