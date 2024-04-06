import httpx
import asyncio
from bs4 import BeautifulSoup as bs
import unicodedata
import json
import genanki
import re
from random import randrange

CONFIG_PATH = "./config.json"
EXCLUDED_PATH = "./__excluded.txt"
URL = "https://www.tagalog.com/dictionary/roots.php"
NEW_WORD = {}

with open(CONFIG_PATH, 'r') as c:
    config = json.load(c)

#* I don't know. But is there any way of instead of creating a clone of this with open...bla...bla...bla f, I can just combine them, allowing it to append and reading the file?
with open(EXCLUDED_PATH, 'r') as f:
    lines = f.readlines()
with open(EXCLUDED_PATH, 'a') as f:
    #? Remove diacritics. Example, ""iyón" => "iyon""
    def REMOVE_DIACRITICS(input_str):
        nfkd_form = unicodedata.normalize('NFD', input_str)
        only_ascii = nfkd_form.encode('ASCII', 'ignore')
        return only_ascii.decode()

    #? Compare a given text to any text in the given array of excluded word.
    def COMPARE(text):
        lower_array = [item.casefold() for item in lines]
        lower_text = text.casefold() + "\n" # kinda silly, because I could've deleted those "\n" on the readlines. But yeah idc.
        return lower_text in lower_array

    #? Do a GET HTTP Request to the url, parsing it via lxml, and then returning the content.
    async def GET(url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            soup = bs(response.content, 'lxml')
            return soup

    async def EACH_GET_CONTENT(url):
        soup = await GET(url)
        div = soup.select_one("#skipstart > div > div > div")
        for element in div.find_all():
            element.decompose()
        return div.text.strip()

    #? For each links in the url, go to the url, fetch the vocabulary, and the meaning/explanation of it.
    async def main(url):
        current_word = 0
        max_word = config["Notes_per_deck"]
        soup = await GET(url)
        #* Such anchor tag are looks like this: <a href="/dictionary/root-word-na" class="standout-link" style="  margin-bottom:8px;">na</a>, where href and the class being the main indicator.
        div = soup.select_one("#skipstart > div > div")
        links = div.find_all("a", class_="standout-link")
        for link in links:
            if current_word <= max_word:
                #! BE CAREFUL! Don't do `url + link['href']`! It gives you "https://www.tagalog.com/dictionary/roots.php/dictionary/root-word-na", which is doesn't exist! Instead! Cut some part of the `url` and then append the `link['href']`, and it should return "https://www.tagalog.com/dictionary/root-word-na"
                content_url = url[:23] + link['href'] 
                content_soup = await GET(content_url)
                content_div = content_soup.select('#skipstart > div[class="standard-white-box standard-single-content-box centering-div"] > div[class="centering-div"] > div > a[class="word-link"]')

                # Check if the anchor tag is found
                if content_div:
                    # Select the parent <div> tag
                    for e in range(0, len(content_div)):
                        div_tag = content_div[e].find_parent('div')
                        Vocabulary = div_tag.select_one('a[href]').get_text(strip=True)
                        if not COMPARE(REMOVE_DIACRITICS(Vocabulary)) and current_word <= max_word:
                            # TODO: In next feature, add a configuration for the user to pick whether they want the printed text to be with diacritics or not.
                        
                            # Remove all <a> tags within this <div>
                            for a_tag in div_tag.find_all('a'):
                                a_tag.decompose()
                            
                            # Extract the text content of the <div>
                            div_text = div_tag.get_text(strip=True)
                            Meaning = div_text[2:]
                            NEW_WORD[current_word] = [Vocabulary, Meaning]
                            f.write(REMOVE_DIACRITICS(Vocabulary) + '\n')
                            
                            if Meaning and Vocabulary:
                                current_word += 1
                        else:
                            break
                print(NEW_WORD)
            else:
                break
        Generate(NEW_WORD)

    def Generate(word_dict):

        Words = word_dict

        CONFIG_PATH = "./config.json"
        EXCLUDED_PATH = "./__excluded.txt"

        with open(CONFIG_PATH, 'r') as c:
            config = json.load(c)
        with open(EXCLUDED_PATH, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("#"):
                    day_step = re.search(r'\d+', line).group()
        Model = genanki.Model(
        randrange(1 << 30, 1 << 31), # Unique ID. Shalln't be the same with other one.
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
            {
            'name': 'Card 2',
            'qfmt': '{{Answer}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Question}}',
            },
        ])

        my_deck = genanki.Deck(
        randrange(1 << 30, 1 << 31),  # Unique ID.
        re.sub(r'\(n\)', day_step, config["Deck_template"]))

        for key in Words:
            my_note = genanki.Note(
            model=Model,
            fields=Words[key])
            my_deck.add_note(my_note)


        line_number_to_change = 0  # Python uses 0-based indexing btw...

        # (don't edit the daystep lord.)
        new_text = f"#day_step:{int(day_step)+1}\n"
        genanki.Package(my_deck).write_to_file('Output.apkg')
        lines[line_number_to_change] = new_text

        with open(EXCLUDED_PATH, 'w') as f:
            f.writelines(lines)

    looper = asyncio.get_event_loop()
    content = looper.run_until_complete(main(URL))