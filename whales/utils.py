from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import spectrogram as _spectrogram
from torchvision.models import resnet18, ResNet, shufflenet_v2_x0_5
from pthflops import count_ops
import torch

classes = ["Whale (other)", "Dolphin", "Up call", "Breathing"]

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


# TODO: Other models:
# ShuffleNet, SqueezeNet, RegNet, MobileNet, MNASNet, EfficientNet
def get_resnet18(num_classes: int, model_path: str = None) -> ResNet:
    if False:
        model = resnet18(num_classes=num_classes)
        model.conv1 = torch.nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
    else:
        model = shufflenet_v2_x0_5(num_classes=num_classes)
        input_channels = 1
        output_channels = model._stage_out_channels[0]
        model.conv1 = torch.nn.Sequential(
            torch.nn.Conv2d(input_channels, output_channels, 3, 2, 1, bias=False),
            torch.nn.BatchNorm2d(output_channels),
            torch.nn.ReLU(inplace=True),
        )

    if model_path is not None:
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

    return model

def summarise_model(model: torch.nn.Module, input_shape):
    num_params = sum(x.size for x in model.parameters())
    random_input = torch.rand(input_shape).type(torch.float32)
    # https://github.com/1adrianb/pytorch-estimate-flops
    flops, _ = count_ops(model, random_input, print_readable=False)
    return {
        "Number of parameters": num_params,
        "FLOPs": flops,
    }
