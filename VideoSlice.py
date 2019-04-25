#!/usr/bin/python
# coding = utf-8
"""
Project: Video Slice
Author:  Zhang Li
Time:    2019-04-24
Email:   lizhang@buaa.edu.cn
"""

import sys
import time
import os
import cv2


class ShowProcess():
    """
    显示处理进度的类
    调用该类相关函数即可实现处理进度的显示
    """
    i = 0  # 当前的处理进度
    max_steps = 0  # 总共需要处理的次数
    max_arrow = 50  # 进度条的长度
    infoDone = 'done'

    # 初始化函数，需要知道总共的处理次数
    def __init__(self, max_steps, infoDone = 'Done'):
        self.max_steps = max_steps
        self.i = 0
        self.infoDone = infoDone

    # 显示函数，根据当前的处理进度i显示进度
    # 效果为[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]100.00%
    def show_process(self, i=None):
        if i is not None:
            self.i = i
        else:
            self.i += 1
        num_arrow = int(self.i * self.max_arrow / self.max_steps)  # 计算显示多少个'>'
        num_line = self.max_arrow - num_arrow  # 计算显示多少个'-'
        percent = self.i * 100.0 / self.max_steps  # 计算完成进度，格式为xx.xx%
        process_bar = '[' + '>' * num_arrow + '-' * num_line + ']'\
                      + '%.2f' % percent + '%' + '\r'  # 带输出的字符串，'\r'表示不换行回到最左边
        sys.stdout.write(process_bar)  # 这两句打印字符到终端
        sys.stdout.flush()
        if self.i >= self.max_steps:
            self.close()

    def close(self):
        print('')
        print(self.infoDone)
        self.i = 0


def ShowVideoInfo(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        # cap = cv2.VideoCapture(video_path.encode('utf-8'))  # 读取包含汉字的视频路径
        fps = cap.get(cv2.CAP_PROP_FPS)
        if(video_format == "avi"):
            count = 0
            while True:
                ret, frame = cap.read()
                if ret:
                    count = count + 1
                else:
                    break
        else:
            count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        # cap = cv2.VideoCapture(video_path)
        # ret, firstframe = cap.read()
        # if ret:
        #     print("FPS: %.2f" % fps)
        #     print("COUNT: %.2f" % count)
        #     print("WIDTH: %d" % size[0])
        #     print("HEIGHT: %d" % size[1])
        #     print("FORMAT: %s" % video_format)
        # else:
        #     print("Video can not read!")
    except:
        "Error in ShowVideoInfo"
    return count


def VideoSlice(video_path, save_path, save_type="png", img_comp=0, start_idx=1, interval=0):
    """
    :param video_path:
    :param save_path:
    :param save_type:
    :param img_comp: default0:
                    None Higher number increase compressive level
                    png[0-9], jpg[0-100]
    :return:
    """

    if not os.path.exists(save_path):
        os.mkdir(save_path)
        print("Folder created.")
    else:
        print("Folder already exists.")

    cap = cv2.VideoCapture(video_path)
    # cap = cv2.VideoCapture(video_path.encode('utf-8'))  # 读取包含汉字的视频路径
    params = None
    suffix = None

    if save_type.upper() == "JPEG" or save_type.upper() == "JPG":
        img_type = int(cv2.IMWRITE_JPEG_OPTIMIZE)
        suffix = ".jpg"
        params = [img_type, img_comp]
    elif save_type.upper() == "PNG":
        img_type = int(cv2.CV_IMWRITE_PNG_COMPRESSION)
        suffix = ".png"
        params = [img_type, img_comp]
    else:
        print("Do not support %s format!" % save_type)

    idx = start_idx  # 从 000001.xxx 开始命名
    cnt_idx = 1
    max_steps = int(ShowVideoInfo(video_path))
    process_bar = ShowProcess(max_steps)

    while True:
        ret, frame = cap.read()
        if ret:
            process_bar.show_process(cnt_idx)
            time.sleep(0.01)
            if(cnt_idx % interval == 0):
                img_name = save_path + "/" + video_name + ("_%06d" % idx) + suffix
                cv2.imwrite(img_name, frame, params)
                idx += 1
            cnt_idx += 1
        else:
            break


if __name__ == "__main__":
    video_path = "/home/ubuntu/Videos/hand_detection/20190416_234802.avi"
    video_full_name = video_path.split("/")[-1]
    video_name = video_full_name.split(".")[0]
    video_format = video_full_name.split(".")[-1]
    save_path = video_path.split(".")[0]

    # ShowVideoInfo(video_path)
    VideoSlice(video_path, save_path, save_type="jpg", interval=10)
