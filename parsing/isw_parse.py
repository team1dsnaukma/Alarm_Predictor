#new
import csv
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

BASE = "https://www.understandingwar.org/" \
       "backgrounder/russian-offensive-campaign-assessment"

start_date = datetime(2022, 2, 23)
end_date = datetime(2023, 1, 25)
period = end_date - start_date

special_urls = {
    datetime(2022, 2, 24): "https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-initial-russian-offensive-campaign-assessment",
    datetime(2022, 2, 25): "https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-25-2022",
    datetime(2022, 2, 26): "https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-26",
    datetime(2022, 2, 27): "https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-27",
    datetime(2022, 5, 5): "https://www.understandingwar.org/backgrounder/russian-campaign-assessment-may-5",
    datetime(2022, 7, 11): "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-update-july-11",
    datetime(2022, 8, 12): "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-august-12-0"
}

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
    for delta in range(period.days + 1):
        date = start_date + timedelta(delta)
        page = BeautifulSoup(
            requests.get(BASE + date.strftime("-%B-%#d-%Y")).content,
            "html.parser"
        )

        if page.find("link")["href"] == "/404":
            page = BeautifulSoup(
                requests.get(BASE + date.strftime("-%B-%#d")).content,
                "html.parser"
            )
            if page.find("link")["href"] == "/404" and date in special_urls:
                page = BeautifulSoup(
                    requests.get(special_urls[date]).content,
                    "html.parser"
                )
        writer.writerow([date.strftime("%d-%m-%Y"), get_news_by_page(page)])
