from typing import List
from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import spectrogram as _spectrogram
from torchvision.models import resnet18, ResNet, shufflenet_v2_x0_5
from pthflops import count_ops
from torchmetrics import ConfusionMatrix as _ConfusionMatrix
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
    if True:
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

class ConfusionMatrix(_ConfusionMatrix):
    def __init__(self, classes: List[str], *args, **kwargs):
        self.classes = classes
        super().__init__(len(classes), *args, **kwargs)

    def accuracy(self):
        matrix = self.compute()

        return (torch.trace(matrix) / torch.sum(matrix)).item()

    def plot(self):
        matrix = self.compute()
        fig, ax = plt.subplots(1, 1)
        ax.imshow(matrix)
        ax.set_xticks(np.arange(self.num_classes))
        ax.set_yticks(np.arange(self.num_classes))
        ax.set_xticklabels(self.classes)
        ax.set_yticklabels(self.classes)
        ax.set_ylabel("Ground truth")
        ax.set_xlabel("Prediction")
        ax.set_title("Confusion matrix")
        for (i, j), z in np.ndenumerate(matrix.numpy()):
            ax.text(j, i, str(z), ha="center", va="center")
        plt.show()

        accuracy = (torch.trace(matrix) / torch.sum(matrix)).item()
        print(f"Total accuracy: {accuracy*100:.2f}%")
        for i, class_name in enumerate(self.classes):
            class_accuracy = matrix[i, i] / torch.sum(matrix[i])
            print(f"Recall '{class_name}': {class_accuracy*100:.2f}%")

