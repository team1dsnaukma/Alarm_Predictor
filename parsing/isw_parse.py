import csv
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

BASE = "https://www.understandingwar.org/" \
       "backgrounder/russian-offensive-campaign-assessment"

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


def writer(to_write, directory):
    with open(directory, 'w', encoding="utf-8") as f:
        writer_obj = csv.writer(f)
        writer_obj.writerow(["col" + f"{i}" for i in range(len(to_write[0]))])
        for row in to_write:
            writer_obj.writerow(row)


def parser(start, end):
    data = []
    period = end - start
    for delta in range(period.days + 1):
        date = start + timedelta(delta)
        request = requests.get(BASE + date.strftime("-%B-%#d"))
        if not request.status_code == 200:
            request = requests.get(BASE + date.strftime("-%B-%#d-%Y"))
            if request.status_code == 200:
                pass
            elif date in special_urls:
                request = requests.get(special_urls[date])
            else:
                data.append((date.strftime("%d-%m-%Y"), "", ""))
                continue
        page = BeautifulSoup(request.content, "html.parser")
        data.append((date.strftime("%d-%m-%Y"), page.title.text, get_news_by_page(page)))
    return data


if __name__ == "__main__":
    DIR = "../raw_data_from_parsing/isw/isw.csv"
    start_date = datetime(2022, 2, 24)
    end_date = datetime(2023, 1, 25)
    parsed = parser(start_date, end_date)
    writer(parsed, DIR)
