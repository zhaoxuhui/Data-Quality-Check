# coding=utf-8
from matplotlib import pyplot as plt
import sys
import numpy as np
import time


def readTimestampsEuRoC(file_path, time_unit):
    timestamps = []
    fin = open(file_path, "r")
    line = fin.readline().strip()
    line = fin.readline().strip()
    while line:
        timestamp = line.split(",")[0]
        if time_unit == 's' or time_unit == 'sec':
            timestamps.append(float(timestamp))
        elif time_unit == 'ms' or time_unit == 'MS':
            timestamps.append(float(timestamp) / 1000.0)
        elif time_unit == 'us' or time_unit == 'US':
            timestamps.append(float(timestamp) / 1000000.0)
        elif time_unit == 'ns' or time_unit == 'NS':
            timestamps.append(float(timestamp) / 1000000000.0)
        elif time_unit == 'ps' or time_unit == 'PS':
            timestamps.append(float(timestamp) / 1000000000000.0)
        line = fin.readline().strip()
    return timestamps


if __name__ == '__main__':
    # 用于检查IMU数据流帧率是否稳定

    time_file = sys.argv[1]  # 待检查IMU数据文件路径
    time_unit = sys.argv[2]  # IMU观测时间戳单位

    print("Loading IMU data ...")
    timestamps = readTimestampsEuRoC(time_file, time_unit)
    print("Loaded IMU data!")

    cur_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    fout = open("./imu_report_" + cur_time + ".txt", 'w')

    time_intervals = []
    for i in range(1, len(timestamps)):
        time_intervals.append(timestamps[i] - timestamps[i - 1])

    mean_interval = np.mean(time_intervals)
    max_interval = max(time_intervals)
    min_interval = min(time_intervals)
    var_interval = np.var(time_intervals)
    mean_fps = 1.0 / mean_interval
    max_difference = max_interval - min_interval

    index_max = time_intervals.index(max_interval)
    index_min = time_intervals.index(min_interval)
    timestamp_max = timestamps[index_max]
    timestamp_min = timestamps[index_min]

    str_line1 = "max interval:" + str(max_interval) + "(sec), index:" + str(index_max) + "/" + str(
        len(timestamps)) + ", timestamp:" + str(timestamp_max) + "\n"
    str_line2 = "min interval:" + str(min_interval) + "(sec), index:" + str(index_min) + "/" + str(
        len(timestamps)) + ", timestamp:" + str(timestamp_min) + "\n"
    str_line3 = "mean interval:" + str(mean_interval) + "\n"
    str_line4 = "variance interval:" + str(var_interval) + "\n"
    str_line5 = "max interval difference:" + str(max_difference) + "\n"
    str_line6 = "mean fps:" + str(mean_fps) + "\n"

    fout.write(str_line1)
    fout.write(str_line2)
    fout.write(str_line3)
    fout.write(str_line4)
    fout.write(str_line5)
    fout.write(str_line6)

    print("\nStatistics:")
    print(str_line1)
    print(str_line2)
    print(str_line3)
    print(str_line4)
    print(str_line5)
    print(str_line6)
    print("\nPlotting ...")

    plt.bar(range(len(time_intervals)), time_intervals)
    plt.xlabel("Frame number")
    plt.ylabel("Time interval")
    plt.title("Mean interval:" + str(round(mean_interval, 9)) +
              "(sec)\nMean FPS:" + str(round(mean_fps, 1)) +
              " Variance:" + str(round(var_interval, 5)))
    plt.axhline(mean_interval, color='orange', label='Mean')
    plt.legend()
    plt.savefig("./imu_report_" + cur_time + ".png", dpi=600)
    plt.show()
