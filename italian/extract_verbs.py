import re

from bs4 import BeautifulSoup
import pandas as pd
import requests
from tqdm import tqdm


def main():
    url = "https://languageposters.com/pages/italian-verbs"

    r= requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    verb_urls = []
    english = []
    for li in soup.find_all("li"):
        match = re.search("https://languageposters.com/pages/italian-verbs-[^-]*?-conjugation", str(li))
        if match is not None:
            verb_urls.append(match.group(0))
            english.append(li.find("span").text.strip("()"))

    assert len(verb_urls) == 100

    conjugations = []
    for definition, verb_url in zip(english, tqdm(verb_urls)):
        r = requests.get(verb_url)
        soup = BeautifulSoup(r.content, "html.parser")
        tables = soup.find_all(attrs={"class": "verb"})
        assert len(tables) == 1
        table = tables[0]
        conjugation = []
        for td in table.find_all("td"):
            conjugation.append(td.text)
        header = conjugation[::2]
        words = conjugation[1::2]
        data = {k:v for k, v in zip(header, words)}
        data["Definition"] = definition
        conjugations.append(data)

    pd.DataFrame(conjugations).to_csv("verbs.csv", index=False)


if __name__ == "__main__":
    main()
