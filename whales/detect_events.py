import os
import pickle
from matplotlib.transforms import Bbox
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from tqdm import tqdm
from utils import get_spectrogram, plot_spectrogram
from scipy.ndimage import gaussian_filter
from skimage.filters import apply_hysteresis_threshold
from scipy.ndimage import label
from skimage.color import label2rgb
from skimage.measure import regionprops


def merge_intervals(intervals, max_gap):
    """
    Given intervals (N, 3) with columns (start, end, label)
    and a scalar max_gap
    return a list of lists, each inner list containing
    labels to be merged
    """
    intervals = intervals[np.argsort(intervals[:, 0])]
    stack = []
    # insert first interval into stack
    stack.append([intervals[0, -1]])
    current = intervals[0, :2]
    for interval in intervals[1:]:
        # Check for overlapping interval,
        # if interval overlap
        if current[0] <= interval[0] <= (current[1] + max_gap):
            current[1] = max(interval[1], current[1])
            stack[-1].append(interval[-1])
        else:
            current = interval[:2]
            stack.append([interval[-1]])
    return stack

def detect_sound_events(m, t, spectrogram):
    dt = t[1] - t[0]
    assert np.all(np.isclose(np.diff(t), dt))
    avg_power = spectrogram.mean(axis=1, keepdims=True)
    bright = apply_hysteresis_threshold(spectrogram, avg_power * 1.5, avg_power * 3)
    labels, _ = label(bright)
    regions = regionprops(labels)
    click_labels = np.zeros_like(labels)
    intervals = []
    for region in regions:
        duration = (region.bbox[3] - region.bbox[1]) * dt
        if duration < 0.2:
            labels[region.slice][region.image] = 0
            click_labels[region.slice][region.image] = region.label
        else:
            intervals.append([region.bbox[1] * dt, region.bbox[3] * dt, region.label])
    intervals = np.array(intervals)
    if len(intervals) > 0:
        label_groups = merge_intervals(intervals, max_gap=0.05)
        for label_group in label_groups:
            labels[np.isin(labels, label_group)] = label_group[0]

    return labels, regionprops(labels, spectrogram)

def read_and_get_spectrogram(fp):
    samplerate, data = wavfile.read(fp)
    if len(data) == 0:
        return None, None, None

    return get_spectrogram(1024, data, samplerate)


def inspect(fp):
    m, t, spectrogram = read_and_get_spectrogram(fp)
    plot_spectrogram(m, t, spectrogram)
    plt.show()

    labels, regions = detect_sound_events(m, t, spectrogram)
    gray = np.stack([spectrogram / spectrogram.max() for _ in range(3)], axis=-1)
    colour = label2rgb(labels, gray, alpha=0.2)
    _, axes=  plt.subplots(2, 1, sharex=True, sharey=True)
    axes[0].imshow(spectrogram[::-1])
    axes[1].imshow(colour[::-1])
    plt.show()


def get_bbox(region, m, t):
    bbox = region.bbox
    return (m[bbox[0]], t[bbox[1]], m[bbox[2]-1], t[bbox[3]-1], region.mean_intensity)

if __name__ == "__main__":
    debug = False
    if debug:
        path = "data/station5_converted/EOS_220405_133808.wav"
        inspect(path)
    all_events = []
    for dir_name in tqdm(os.listdir("data")):
        if not dir_name.endswith("converted"):
            continue
        dir = os.path.join("data", dir_name)
        for filename in tqdm(os.listdir(dir)):
            file = os.path.join(dir, filename)
            m, t, spectrogram = read_and_get_spectrogram(file)
            if m is None:
                continue
            # inspect(file)
            labels, regions = detect_sound_events(m, t, spectrogram)
            all_events.extend([get_bbox(region, m, t) + (file,) for region in regions])
    with open("sound_events.pkl", "wb") as f:
        pickle.dump(all_events, f)
