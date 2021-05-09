# Layout
# On the left, a table of bird species
# If one is clicked, table switches to all recordings with info
# If one is clicked the right-hand side is opened.

# RHS: Information about the recording, play button + spectrogram
from random import randint
from datetime import date
from bokeh.models import ColumnDataSource, TableColumn, DateFormatter, DataTable
from bokeh.layouts import column, row
from bokeh.models.widgets import TextInput
from bokeh.plotting import curdoc, figure
from bokeh.palettes import Inferno
import pandas as pd
import os
from bokeh.models.widgets.markups import Div
import soundfile as sf
from scipy import signal
import numpy as np



def get_species_table(metadata, labels):
    species_info = {x["primary_label"]:x["common_name"] for i, x in metadata.drop_duplicates("primary_label").iterrows()}

    source = ColumnDataSource({"primary_label": list(species_info.keys()), "common_name": list(species_info.values())})

    columns = [
            TableColumn(field="primary_label", title="Label"),
            TableColumn(field="common_name", title="Common name"),
            ]

    div = Div(text=f"<h3>All species in short-audio train set<h3>")
    table = DataTable(source=source, columns=columns)

    return column(div, table)

def get_recordings_table(metadata, label):
    recordings = os.listdir(os.path.join(short_audio_path, label))
    data = metadata[metadata["primary_label"]==label]
    source = ColumnDataSource(data)
    columns = [
            TableColumn(field="filename", title="Filename"),
            TableColumn(field="rating", title="Rating"),
            TableColumn(field="time", title="Time"),
            TableColumn(field="secondary_labels", title="Other birds")
            ]
    div = Div(text=f"<h3>Recordings for {label}<h3>")
    table = DataTable(source=source, columns=columns)


    return column(div, table)

def get_recording_info(path_to_recording):
    data, samplerate = sf.read(path_to_recording)
    nperseg = int(samplerate * 20e-3) # 20ms
    f, t, spectrogram = signal.spectrogram(data, samplerate, nperseg=nperseg)
    spectrogram  = np.log(spectrogram+1e-9)
    print(spectrogram)
    p = figure()
    div = Div(text=f"<h3>{path_to_recording}<h3>")
    p.image(image=[spectrogram], x=0, y=0, dw=t[1]-t[0], dh=f[1]-f[0], palette=Inferno[256])

    return column(div, p)

    print("hello")



metadata_path = "input/train_metadata.csv"
metadata = pd.read_csv(metadata_path)

short_audio_path = "input/train_short_audio"
labels = os.listdir(short_audio_path)
species_table = get_species_table(metadata, labels)
recordings_table = get_recordings_table(metadata, labels[0])

path_to_recording = "input/train_short_audio/acafly/XC569943.ogg"
recording_info = get_recording_info(path_to_recording)

curdoc().add_root(column(row(species_table, recordings_table), recording_info))

# Table of species
# Get name of each species from folder
# Also include in the table: folder name, 

