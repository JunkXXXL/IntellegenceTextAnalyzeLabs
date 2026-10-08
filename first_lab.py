import json
import pymorphy3 as p
import re


analyser = p.MorphAnalyzer()

def preprocess_text(text: str):
    text = text.lower()
    link_end = 0
    find_link = True
    while find_link:
        region = re.search("(?P<url>https?://[^\s]+)", text[link_end:])
        if region is None:
            find_link = False
        else:
            text_before = text[:region.start()]
            text_after = text[region.end():]
            text = text_before + "URL" + text_after
            link_end = region.end()
    parsed_text = ""
    for word in text.split():
        parsed_text += analyser.parse(word)[0].normal_form + " "
    return parsed_text


def extract_messages(chat_json):
    messages = []
    for index, item in enumerate(chat_json["messages"]):
        id = chat_json["name"] + f"_{index}"
        raw = item.get("text", "")
        if type(raw) is list:
            new_raw = ""
            for el in raw:
                if type(el) is str:
                    new_raw += " " + el
            raw = new_raw
        if len(raw) < 3:
            continue
        new_item = {"id": id, "raw": raw, "author": item.get('author', ''),
                    "date": item.get('date', ""), 'reactions': item.get('reactions', "[]"),
                    'preprocess_text': preprocess_text(raw)}
        messages.append(new_item)
    print(chat_json["name"], len(messages))
    return messages


if __name__ == "__main__":

    messages = []

    with open("tgjson/vlad.json", 'r', encoding="utf-8") as js:
        data = json.load(js)

    messages.extend(extract_messages(data))

    with open("tgjson/lunapark.json", 'r', encoding="utf-8") as js:
        data = json.load(js)

    messages.extend(extract_messages(data))

    with open("tgjson/m4nu11.json", 'r', encoding="utf-8") as js:
        data = json.load(js)

    messages.extend(extract_messages(data))

    with open("tgjson/podols.json", 'r', encoding="utf-8") as js:
        data = json.load(js)

    messages.extend(extract_messages(data))

    with open("tgjson/grips.json", 'r', encoding="utf-8") as js:
        data = json.load(js)

    messages.extend(extract_messages(data))

    with open("tgjson/transformers.json", 'r', encoding="utf-8") as js:
        data = json.load(js)

    messages.extend(extract_messages(data))

    with open('messages.json', 'w', encoding='utf-8-sig') as f:
        json.dump(messages, f)

    with open('messages.json', 'r', encoding='utf-8-sig') as f:
          data = json.load(f)
    print(data[1103:1110])
