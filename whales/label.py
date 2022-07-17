import pickle
import os
from matplotlib import pyplot as plt
from scipy.io import wavfile
import numpy as np

import matplotlib.patches as patches
from tqdm import tqdm
from detect_events import read_and_get_spectrogram
from utils import get_spectrogram, plot_spectrogram
import sounddevice as sd
from matplotlib.widgets import Button
import csv

def play(path):
    samplerate, data = wavfile.read(path)
    sd.play(data, samplerate)
    sd.wait()



def label(file, bbox, out, classes):
    samplerate, data = wavfile.read(file)
    data_t = np.arange(len(data)) / samplerate
    m, t, spectrogram = get_spectrogram(1024, data, samplerate)
    mosaic = [["A"] * len(classes)]*3 + [[class_name for class_name in classes]]
    fig, axes = plt.subplot_mosaic(mosaic)
    axes["A"].pcolormesh(t, m, spectrogram)
    rect = patches.Rectangle((bbox[1], bbox[0]), bbox[3] - bbox[1], bbox[2] - bbox[0], linewidth=1, edgecolor='r', facecolor='none')
    axes["A"].add_patch(rect)
    axes["A"].set_title(file)

    def on_clicked(class_name):
        print(class_name)
        if not os.path.exists(out):
            with open(out, "w") as f:
                f.write("file,min_t,min_m,max_t,max_m,class_name\n")
        with open(out, "a") as f:
            writer = csv.writer(f)
            writer.writerow([file, *bbox, class_name])
        plt.close(fig)

    buttons = {}
    for class_name in classes:
        buttons[class_name] = Button(axes[class_name], class_name)
        buttons[class_name].on_clicked(lambda _, arg=class_name: on_clicked(arg))
    min_index = np.argmin(np.abs(bbox[1] - 1 - data_t))
    max_index = np.argmin(np.abs(bbox[3] + 1 - data_t))
    to_play = np.concatenate([data[min_index:max_index],  np.zeros(samplerate * 2, dtype=np.int16)])
    print(len(to_play) / samplerate)
    sd.play(to_play, samplerate, loop=True)
    plt.show()
    sd.stop()


if __name__ == "__main__":
    out = "labels.csv"
    classes = ["Whale (other)", "Dolphin", "Up call", "Breathing"]
    with open("sound_events.pkl", "rb") as f:
        all_bboxes = pickle.load(f)
    for i in tqdm(range(len(all_bboxes))):
        *bbox, intensity, filename = all_bboxes[i]
        bbox = list(map(float, bbox))
        label(filename, bbox, out, classes)
