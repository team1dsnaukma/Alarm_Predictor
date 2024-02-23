import csv
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

BASE = "https://www.understandingwar.org/" \
       "backgrounder/russian-offensive-campaign-assessment"

start_date = datetime(2022, 2, 24)
end_date = datetime(2023, 1, 25)
period = end_date - start_date


def get_news_by_page(data):
    parsed_page = []
    # ignore first three <p> tags about report info
    for elem in data.find_all("p")[3:]:
        if not elem.find_all("a"):
            parsed_page.append(elem.text)
    # cleaning bad data
    for row in parsed_page[::-1]:
        if row.startswith(("[", "\xa0")):
            parsed_page.remove(row)
        else:
            break
    if parsed_page and parsed_page[-1] == "Immediate items to watch":
        parsed_page.pop()
    return "\n".join(parsed_page)


with open("../raw_data_from_parsing/isw/isw.csv", 'w', encoding="utf-8") as f:
    writer = csv.writer(f)
    for delta in range(period.days):
        date = start_date + timedelta(delta)
        page = BeautifulSoup(
            requests.get(BASE + date.strftime("-%B-%d-%Y")).content,
            "html.parser"
        )
        if page.find("link")["href"] == "/404":
            page = BeautifulSoup(
                requests.get(BASE + date.strftime("-%B-%d")).content,
                "html.parser"
            )
        writer.writerow([date.strftime("%d-%m-%Y"), get_news_by_page(page)])
