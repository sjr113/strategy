# -*- coding:utf8 -*-
# coding=utf-8
__author__ = 'shen'


# import cPickle
import os
import numpy
import data.packer
from classifier import svm
import timeit


def test_data_set():

    s_time = timeit.default_timer()
    os.chdir("E:\\gamewatcher\schemes\sjr\\naive_demo_only_read_dat")
    print os.getcwd()

    data_set = data.packer.load("2_frame_hog_crop_04.dat")  # data_set是一个字典  # list

    # 分别代表负样本和对应的帧编号
    negative_sample, negative_index = data_set[0]
    # 分别代表正样本和正样本对应的帧编号
    positive_sample, positive_index = data_set[1]

    # 对所有的正负样本分别按照其编号进行排序，恢复成原始的视频帧顺序
    # 首先合并所有的帧编号, 此时index的大小应该是（m+n, ）
    index = numpy.hstack((negative_index[:], positive_index[:]))  # (27987L,)
    label = numpy.hstack((numpy.zeros_like(negative_index[:]), numpy.ones_like(positive_index[:])))  # (27987L,)

    # 合并所有的正负样本
    sample = numpy.vstack((negative_sample[:, :], positive_sample[:, :]))  # (27987L, 4536L)

    arg_sort_index = numpy.argsort(index)
    index = index[arg_sort_index]  # 排序好的所有的帧编号  <type 'numpy.ndarray'>  (27987L,)
    label = label[arg_sort_index]  # 对所有的label排序  <type 'numpy.ndarray'>   (27987L,)
    sample = sample[arg_sort_index]  # 排序好的所有的样本  <type 'numpy.ndarray'> (27987L, 4536L)

    e_time = timeit.default_timer()
    print "Load data-adjust data*********The time is " + str(e_time-s_time)
    return index, label, sample


def model_test():
    index, label, data_sample = test_data_set()

    # 加载model
    # 使用model对test数据集进行测试
    # load model
    model = svm.SVM(None)
    model.load("svm_rbf_c_4.0_gamma_0.01.dat")

    p_labels, h_values = model.predict(data_sample, return_prob=True)  # (27987L,) <type 'numpy.ndarray'>
    list_frame = []
    old_index = -31
    i = 0

    while i < numpy.shape(p_labels)[0]:
        start_time = timeit.default_timer()
        if p_labels[i] == 1 and index[i]-old_index>30:
            old_index = index[i]
            list_frame.append(old_index % 2000000)
            # print "The ball in!" + "predixt frames: " + str(old_index)
            end_time = timeit.default_timer()
            print "The ball goal! **********" + "The" + str(i) + "th frame : the time is " + str(end_time-start_time)
        # else:
        #     end_time = timeit.default_timer()
        #     print "None goaling ***********The" + str(i) + "th frame : the time is " + str(end_time-start_time)
        i += 1

    # print "The ball in:"
    # print list_frame

    segment = data.packer.load("04_segment_only_frame.gz")
    # print "The correct segment: "
    # print segment
    return list_frame, segment


def output_result(list_frame, segment):
    # i = 0
    # if len(list_frame)<len(segment):
    #     while i < len(list_frame):
    #         print str(segment[i]) + str(list_frame[i])
    #         i += 1
    #     print "rest:"
    #     print segment[i-1:-1]
    # elif len(list_frame)>= len(segment):
    #     while i < len(segment):
    #         print str(segment[i]) + str(list_frame[i])
    #         i += 1
    #     print "rest:"
    #     print list_frame[i-1:-1]

    j = 0
    m = len(list_frame)
    n = len(segment)
    inner_thresh = 5
    s = 0
    start_time = timeit.default_timer()
    s_temp = 0
    s_delete = 0
    while j < m:
        while s < n:
            if segment[s][2] == 2:
                s += 1
                s_delete += 1
                print "Delete Frames " + str(segment[s][0])
                continue
            if (list_frame[j] < segment[s][0] + inner_thresh) and (list_frame[j] > segment[s][0] - inner_thresh):
                print "The ball goal!   " + "predict_positive  " + str(list_frame[j]) + "segment  " + str(segment[s])
                s_temp += 1
                s_ori = s + 1
                while s_ori > s_temp:
                    print "Cannot recognise Positve...Flase negative:  " + str(segment[s_ori])
                    s_ori -= 1
                break
            s += 1
            s_temp += 1
        if s == n:
            s = j - 1
            print "False Positive:  " + "predict_positive  " + str(list_frame[j])
        else:
            s = j
        s_temp = s
        j += 1
    end_time = timeit.default_timer()
    print "Adjust the ball goaling format: **************the time is " + str(end_time-start_time)


def output_result_2(list_frame, segment):
    # i = 0
    # if len(list_frame)<len(segment):
    #     while i < len(list_frame):
    #         print str(segment[i]) + str(list_frame[i])
    #         i += 1
    #     print "rest:"
    #     print segment[i-1:-1]
    # elif len(list_frame)>= len(segment):
    #     while i < len(segment):
    #         print str(segment[i]) + str(list_frame[i])
    #         i += 1
    #     print "rest:"
    #     print list_frame[i-1:-1]

    j = 0
    m = len(list_frame)
    n = len(segment)
    inner_thresh = 5

    start_time = timeit.default_timer()

    while j < m:
        s = 0
        while s < n:
            if segment[s][2] == 2:
                s += 1
                # print "Delete frame" + str(segment[s][0])
                continue
            if (list_frame[j] < segment[s][0] + inner_thresh) and (list_frame[j] > segment[s][0] - inner_thresh):
                print "The ball goal!   " + "predict_positive  " + str(list_frame[j]) + "segment  " + str(segment[s]) + str(s)

                break
            s += 1
        if s == n:
            print "False Positive:  " + "predict_positive  " + str(list_frame[j])
        j += 1
    end_time = timeit.default_timer()
    print "Adjust the ball goaling format: **************the time is " + str(end_time-start_time)


list_frame, segment = model_test()
output_result_2(list_frame, segment)

# segment = data.packer.load("04segment.gz")
# print segment
# i = 0
# while i < len(segment)-1:
#     if (segment[i+1][0] - segment[i][0]) < 50:
#         print segment[i][0]
#         print segment[i+1][0] - segment[i][0]
#     i += 1



