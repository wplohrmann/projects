import numpy as np
from scipy.signal import spectrogram as _spectrogram
import torch

def get_spectrogram(nperseg, x, samplerate):
    mode = "magnitude"
    f, t, spectrogram = _spectrogram(x, samplerate, window="hann", nperseg=nperseg, mode=mode)
    f = f[:64][::-1]
    spectrogram = spectrogram[:64][::-1]
    spectrogram = np.log(spectrogram)
    spectrogram -= np.min(spectrogram)
    spectrogram /= np.max(spectrogram)

    return f, t, spectrogram

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
