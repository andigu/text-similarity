import urllib.request
import re
from bs4 import BeautifulSoup

def clean_encoding(text):
    return text.replace("’", "'").replace("&#39;", "'").replace('“', '"').replace("¾", "").replace(" ", "").replace('”', '"')

section_urls = ["https://ezhome.zendesk.com/hc/en-us/sections/203450598-General",
                "https://ezhome.zendesk.com/hc/en-us/sections/203450588-Getting-Started",
                "https://ezhome.zendesk.com/hc/en-us/sections/203875778-Maintenance",
                "https://ezhome.zendesk.com/hc/en-us/sections/203875798-Scheduling",
                "https://ezhome.zendesk.com/hc/en-us/sections/203875818-Best-Horticultural-Practices",
                "https://ezhome.zendesk.com/hc/en-us/sections/203835297-Billing"]

question_urls = []
for url in section_urls:
    with urllib.request.urlopen(url) as response:
        html = response.read().decode("utf-8")
        url_indices = [m.start() for m in re.finditer('/hc/en-us/articles', html)]
        for index in url_indices:
            url = ""
            current = index
            while html[current] != '"':
                url += html[current]
                current += 1
            question_urls.append("https://ezhome.zendesk.com/" + url)

faq = {}
for url in question_urls:
    with urllib.request.urlopen(url) as response:
        html = response.read().decode()
        question_index = html.rfind("<h1>")
        question = ""
        current = question_index + 18
        while html[current] != "?":
            question += html[current]
            current += 1
        question += html[current]
        question = clean_encoding(question)

        answer_index = html.find('<div class="article-body markdown">')
        end_index = html[answer_index:].find("</div>") + answer_index
        answer = clean_encoding(html[answer_index: end_index]).replace("</li><li>", " ")
        answer = BeautifulSoup(answer, "lxml").get_text().replace("\n", "")
        faq[question] = answer

count = 1
to_write = ""
for question in faq:
    file = open("corpus/faq/" + str(count) + ".txt", "w")
    to_write += question + "\n"
    file.write(question + "\n")
    file.write(faq[question])
    file.close()
    count += 1

file = open("questions.txt", "w")
file.write(to_write)
file.close()
