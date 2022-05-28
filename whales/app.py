from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
from scipy.io import wavfile
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

from utils import get_spectrogram as _get_spectrogram

@st.cache
def get_arrays():
    arrays = {}
    for file_name in os.listdir("data"):
        if not file_name.endswith(".wav"):
            continue
        samplerate, data = wavfile.read(os.path.join("data", file_name))
        arrays[os.path.splitext(file_name)[0]] = data

    # Assume the same sample rate for all audio files
    return arrays, samplerate

arrays, samplerate = get_arrays()

label = st.selectbox("Choose file", arrays.keys())

st.audio("data/"+label + ".wav")

columns = st.columns(3)
nperseg = columns[0].number_input("nperseg", value=3000)
opacity = columns[1].number_input("Opacity", min_value=16, value=128, max_value=255)

@st.cache
def get_spectrogram(nperseg, x, samplerate):
    f, t, spectrogram = _get_spectrogram(nperseg, x, samplerate)
    plt.imsave("haha.png", spectrogram)

    return f, t, Image.open("haha.png")

f, t, spectrogram = get_spectrogram(nperseg, arrays[label], samplerate)

stroke_width = 5
width = 1000
height = 400
data = st_canvas(
    background_image=spectrogram,
    stroke_width=stroke_width,
    stroke_color="#000000" + hex(opacity)[2:],
    key="annotations",
    width=width,
    height=height,
)
st.session_state.data = data.json_data
if not st.button("Save"):
    st.stop()

points = []
for i, object in enumerate(data.json_data["objects"]):
    for point in object["path"]:
        points.append({"Event": i, "t / s": point[-2] * t[-1] / width, "f / Hz": (height - point[-1]) * f[0] / height})
df = pd.DataFrame(points)
st.write(df)
df.to_csv(f"data/{label}.csv", index=False)
