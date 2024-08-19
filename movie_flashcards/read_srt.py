from collections import defaultdict
import re
from typing import Dict, List
import nltk
import numpy as np
import pandas as pd
import streamlit as st
from pysrt import SubRipFile
from argostranslate import translate, package

@st.cache_data
def get_dictionary_freqs():
    # From https://github.com/olastor/german-word-frequencies/tree/main/decow?tab=readme-ov-file
    return pd.read_csv("opensubtitles_cistem_freq.csv").set_index('word')

stemmer = nltk.stem.Cistem()

def calculate_occurences(words: List[str]) -> Dict[str, int]:
    occurences = defaultdict(int)
    for i, word in enumerate(words):
        stemmed = stemmer.stem(word)
        occurences[stemmed] += 1
    real_occurences = {}
    for i, word in enumerate(words):
        stemmed = stemmer.stem(word)
        real_occurences[word] = occurences[stemmed]
    return real_occurences

@st.cache_resource
def get_translator():
    from_code = "de"
    to_code = "en"
    package.update_package_index()
    available_packages = package.get_available_packages()
    available_package = list(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )[0]
    download_path = available_package.download()
    package.install_from_path(download_path)
    installed_languages = translate.get_installed_languages()
    from_lang = list(filter(
            lambda x: x.code == from_code,
            installed_languages))[0]
    to_lang = list(filter(
            lambda x: x.code == to_code,
            installed_languages))[0]

    return from_lang.get_translation(to_lang)

@st.cache_data
def translate_word(word):
    translator = get_translator()
    return translator.translate(word)




@st.cache_data(show_spinner=False, hash_funcs={SubRipFile: lambda x: "wow"})
def calculate_top_n(srt):
    lines = [sub.text for sub in srt]
    without_tags = [re.sub(r"(\<\/?\w+\>)|\n", "", line) for line in lines]
    words = [word.strip() for line in without_tags for word in re.split("[ ,.\?\!]", line) if word.strip()]
    st.write("Number of words:", len(words))

    dictionary_freqs = get_dictionary_freqs()
    top_100_dict_words = set(dictionary_freqs.sort_values('freq', ascending=False).head(100).index)
    occurences = calculate_occurences(words)
    words = []
    relative_freqs = []
    st.write(f"Calculating most frequent words")
    pbar = st.progress(0)
    for i, (word, num) in enumerate(occurences.items()):
        stemmed = stemmer.stem(word)
        pbar.progress(i / len(occurences))
        words.append(word)
        if num < 10:
            relative_freqs.append(0)
        elif stemmed in top_100_dict_words:
            relative_freqs.append(0)
        elif stemmed not in dictionary_freqs.index:
            relative_freqs.append(0)
        else:
            relative_freqs.append(np.log(num) / dictionary_freqs.at[stemmed, 'freq'])

    indices = np.argsort(np.array(relative_freqs))[::-1]
    top_n = [words[i] for i in indices]
    return top_n

f = st.file_uploader("SRT file")
if not f:
    st.stop()

srt = SubRipFile.from_string(f.read().decode("utf-8"))

translator = get_translator()
top_50 = calculate_top_n(srt)
covered = set()
if st.button("Reset"):
    st.session_state.clear()
st.subheader("Top 50 words")
columns = st.columns(5)
for i, word in enumerate(top_50[:500]):
    stemmed = stemmer.stem(word)
    if stemmed in covered:
        continue
    covered.add(stemmed)

    with columns[i % 5]:
        key = f"{stemmed}_flip"
        is_flip = key in st.session_state
        if key in st.session_state:
            translated = translate_word(word)
            st.button(translated, on_click=lambda k: st.session_state.__delitem__(k), args=[key], key=f"{stemmed}_button")
        else:
            st.button(word, on_click=lambda k: st.session_state.__setitem__(k, True), args=[key], key=f"{stemmed}_button")


