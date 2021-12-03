# coding=utf-8
from HaveFun import common
from matplotlib import pyplot as plt
import sys
import numpy as np

if __name__ == '__main__':
    search_dir = sys.argv[1]
    file_type = sys.argv[2]
    time_unit = sys.argv[3]

    print("Loading image data ...")
    paths, names, files = common.findFiles(search_dir, file_type)
    print("Loaded image data!")

    timestamps = []
    if time_unit == 's' or time_unit == 'sec':
        for i in range(len(names)):
            timestamps.append(float(names[i].split(".")[0]))
    elif time_unit == 'ms' or time_unit == 'MS':
        for i in range(len(names)):
            timestamps.append(float(names[i].split(".")[0]) / 1000.0)
    elif time_unit == 'us' or time_unit == 'US':
        for i in range(len(names)):
            timestamps.append(float(names[i].split(".")[0]) / 1000000.0)
    elif time_unit == 'ns' or time_unit == 'NS':
        for i in range(len(names)):
            timestamps.append(float(names[i].split(".")[0]) / 1000000000.0)
    elif time_unit == 'ps' or time_unit == 'PS':
        for i in range(len(names)):
            timestamps.append(float(names[i].split(".")[0]) / 1000000000000.0)

    time_intervals = []
    for i in range(1, len(timestamps)):
        time_intervals.append(timestamps[i] - timestamps[i - 1])

    mean_interval = np.mean(time_intervals)
    max_interval = max(time_intervals)
    min_interval = min(time_intervals)
    var_interval = np.var(time_intervals)
    mean_fps = 1.0 / mean_interval

    print("\nStatistics:")
    print("max interval:", max_interval, "(sec)")
    print("min interval:", min_interval, "(sec)")
    print("mean interval:", mean_interval, "(sec)")
    print("variance interval:", var_interval)
    print("mean fps:", mean_fps)
    print("\nPlotting ...")

    plt.bar(range(len(time_intervals)), time_intervals)
    plt.xlabel("Frame number")
    plt.ylabel("Time interval")
    plt.title("Mean interval:" + str(round(mean_interval, 9)) +
              "(sec)\nMean FPS:" + str(round(mean_fps, 1)) +
              " Variance:" + str(round(var_interval, 5)))
    plt.axhline(mean_interval, color='orange')
    plt.show()
