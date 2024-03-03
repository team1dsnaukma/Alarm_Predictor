import csv
import re
from datetime import datetime, timedelta
import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE = "https://www.understandingwar.org/" \
       "backgrounder/russian-offensive-campaign-assessment"

special_urls = {
    datetime(2022, 2, 24): "https://www.understandingwar.org/backgrounder/"
                           "russia-ukraine-warning-update-initial-russian-offensive-campaign-assessment",
    datetime(2022, 2, 25): "https://www.understandingwar.org/backgrounder/"
                           "russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-25-2022",
    datetime(2022, 2, 26): "https://www.understandingwar.org/backgrounder/"
                           "russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-26",
    datetime(2022, 2, 27): "https://www.understandingwar.org/backgrounder/"
                           "russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-27",
    datetime(2022, 5, 5): "https://www.understandingwar.org/backgrounder/"
                          "russian-campaign-assessment-may-5",
    datetime(2022, 7, 11): "https://www.understandingwar.org/backgrounder/"
                           "russian-offensive-campaign-update-july-11",
    datetime(2022, 8, 12): "https://www.understandingwar.org/backgrounder/"
                           "russian-offensive-campaign-assessment-august-12-0"
}


def get_news_by_page(data):
    parsed_page = []
    p_tags = data.find_all("p")
    bad_data = ["Mason", "George", "Kateryna", "Fredrick", "Frederick", "Key Takeaways"]
    start_point = 0
    # remove report info
    for elem in p_tags[:5]:
        if elem.strong and re.search("|".join(bad_data), elem.strong.text):
            start_point = p_tags.index(elem) + 1
    # parse necessary data
    for elem in p_tags[start_point:]:
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
        data.append((date.strftime("%d-%m-%Y"), page.title.text, request.url, page, get_news_by_page(page)))
    return data


def clean_data(path):
    data = pd.read_csv(path)
    data.rename(columns={
        'col0': 'date', 'col1': 'title', 'col2': 'url', 'col3': 'html', 'col4': 'main_text'
    },
        inplace=True
    )

    # convert all the data in the column "main_text" to str
    data['main_text'] = data['main_text'].astype(str)

    # remove the dates
    date_pattern = r'\b(?:January|February|March|April|May|June|July|August|September|October' \
                   r'|November|December)\s+\d{1,2},\s+(?:\d{1,2}:\d{2}\s*(?:am|pm)?\s*ET?' \
                   r'|\d+(?:\s*pm|am)?\s*ET?)\b'
    data['main_text'] = data['main_text'].apply(lambda x: re.sub(date_pattern, '', x).lstrip())
    specific_pattern = r'\bDecember 8, 6:40 PM ET\b'
    data['main_text'] = data['main_text'].apply(lambda x: re.sub(specific_pattern, '', x).lstrip())

    # remove symbols [1], [2], ... [n]
    unnecessary_numeration = r'\[\d+\]'
    data['main_text'] = data['main_text'].apply(lambda x: re.sub(unnecessary_numeration, '', x))

    # remove symbols "\r\n" and "\xa0"
    data['main_text'] = data['main_text'].replace({'\r\n': ' ', '\xa0': ' ', '\xad': ''}, regex=True)

    # remove unnecessary text in rows
    unwanted_text = "We do not report in detail on Russian war crimes because those activities" \
                    " are well-covered in Western media and do not directly affect the military" \
                    " operations we are assessing and forecasting. We will continue to evaluate" \
                    " and report on the effects of these criminal activities on the Ukrainian" \
                    " military and population and specifically on combat in Ukrainian urban areas." \
                    " We utterly condemn these Russian violations of the laws of armed conflict," \
                    " Geneva Conventions, and humanity even though we do not describe them in" \
                    " these reports."
    data['main_text'] = data['main_text'].replace(unwanted_text, '', regex=True)

    # remove unnecessary text in rows
    imm_text = "Immediate items to watch"
    data['main_text'] = data['main_text'].replace(imm_text, '', regex=True)

    # remove unnecessary text in rows
    unw_text = r'Idata is publishing an abbreviated campaign update today,' \
               r' (January|October|November|December) \d{1,2}\.'
    data['main_text'] = data['main_text'].apply(lambda x: re.sub(unw_text, '', x))

    # remove unnecessary text in rows
    unwn_text = r'Note: Idata does not receive any classified material from any source, uses' \
                r' only publicly available information, and draws extensively on Russian,' \
                r' Ukrainian, and Western reporting and social media as well as commercially' \
                r' available satellite imagery and other geospatial data as the basis for these' \
                r' reports. References to all sources used are provided in the endnotes of each' \
                r' update.'
    data['main_text'] = data['main_text'].replace(unwn_text, '', regex=True)
    u1_text = "Note: Idata and CTP will not publish a campaign assessment (or maps) tomorrow," \
              " December 25, in observance of the Christmas holiday. Coverage will resume" \
              " Monday, December 26."
    u2_text = "Note: Idata and CTP will not publish a campaign assessment (or maps) tomorrow, " \
              "January 1, in observance of the New Year\'s Holiday. Coverage will resume on " \
              "Monday, January 2."
    data['main_text'] = data['main_text'].str.replace(u1_text, '', regex=False)
    data['main_text'] = data['main_text'].str.replace(u2_text, '', regex=False)

    # remove unnecessary text in rows
    unss_text = r'This new section in the daily update is not in itself a forecast' \
                r' or assessment. It lays out the daily observed indicators we are ' \
                r'using to refine our assessments and forecasts, which we expect to' \
                r' update regularly. Our assessment that the MDCOA remains unlikely' \
                r' has not changed.'
    data['main_text'] = data['main_text'].replace(unss_text, '', regex=True)
    unss_text = r'We will update this header if and when the assessment changes.'
    data['main_text'] = data['main_text'].replace(unss_text, '', regex=True)
    unss_text = r'Observed indicators for the MDCOA in the past 24 hours:'
    data['main_text'] = data['main_text'].replace(unss_text, '', regex=True)
    unss_text = r'Observed ambiguous indicators for MDCOA in the past 24 hours:'
    data['main_text'] = data['main_text'].replace(unss_text, '', regex=True)
    unss_text = r'Observed counter-indicators for the MDCOA in the past 24 hours:'
    data['main_text'] = data['main_text'].replace(unss_text, '', regex=True)
    unss_text = r'We will update this header if the assessment changes.'
    data['main_text'] = data['main_text'].str.replace(unss_text, '', regex=False)

    # remove quotation marks
    data['main_text'] = data['main_text'].apply(lambda x: re.sub(r'[“”]', '', x))
    data['main_text'] = data['main_text'].apply(lambda x: re.sub(r'"', '', x))
    un_text = 'Idata does not receive any classified material from any source,' \
              ' uses only publicly available information, and draws extensively on Russian,' \
              ' Ukrainian, and Western reporting and social media as well as commercially' \
              ' available satellite imagery and other geospatial data as the basis for' \
              ' these reports.'
    data['main_text'] = data['main_text'].str.replace(un_text, '', regex=False)
    un_text = 'Idata specifically does not receive information from Prigozhin’s' \
              ' deceased mother-in-law, as he (ironically) suggested.'
    data['main_text'] = data['main_text'].str.replace(un_text, '', regex=False)
    un_text = 'Note: Idata will report on activities in Kherson Oblast as part of' \
              ' the Southern Axis in this and subsequent updates.'
    data['main_text'] = data['main_text'].str.replace(un_text, '', regex=False)

    # remove extra spaces
    data['main_text'] = data['main_text'].apply(lambda x: re.sub(r'\s+', ' ', x.strip()).lower())
    data.to_csv(path, index=False)


if __name__ == "__main__":
    DIR = "../../raw_data_from_parsing/isw/isw.csv"
    start_date = datetime(2022, 2, 24)
    end_date = datetime(2023, 1, 25)
    parsed = parser(start_date, end_date)
    writer(parsed, DIR)
    clean_data(DIR)

