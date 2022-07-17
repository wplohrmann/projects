from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import spectrogram as _spectrogram
import torch

def to_mel(f):
    return 2595 * np.log10(1 + f / 700)

def from_mel(m):
    return (10**(m / 2595) - 1) * 700

def plot_spectrogram(f, t, spectrogram, log=True):
    if spectrogram.min() > 0 and log:
        spectrogram = np.log(spectrogram)
    plt.pcolormesh(t, f, spectrogram)
    # plt.gca().set_yscale("log")

def get_kernel(f):
    bins = from_mel(np.linspace(0, to_mel(f[-1]), len(f) + 1))
    f_ = (bins[1:] + bins[:-1]) / 2
    widths = np.diff(bins) * 10
    diff = f_[:, None] - f[None, :]
    kernel = np.maximum(0, widths[:, None] - np.abs(diff))
    kernel /= np.sum(kernel, axis=1, keepdims=True)
    return to_mel(f_), kernel

def get_spectrogram(nperseg, x, samplerate):
    mode = "magnitude"
    f, t, spectrogram = _spectrogram(x, samplerate, window="hann", nperseg=nperseg, mode=mode)
    m, kernel = get_kernel(f)
    spectrogram = kernel @ spectrogram
    assert spectrogram.shape == (len(m), len(t))

    return m, t, spectrogram

def get_model(init_features, base_model, out_channels, model_path=None):
    model = torch.hub.load(
        *base_model, in_channels=1, out_channels=out_channels, init_features=init_features, pretrained=False
    )

    if model_path:
        model.load_state_dict(torch.load(model_path))

    return model

classes = {
    "Up call": "#000000",
    "Bubble": "#0000FF",
    "Click": "#FF0000",
    "Exhale": "#00FF00",
    "Humpback song": "#FFFF00",
}
