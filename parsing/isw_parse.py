import datetime
import requests
from bs4 import BeautifulSoup

# Get html data from ISW via requests
base_url = "https://www.understandingwar.org/" \
           "backgrounder/russian-offensive-campaign-assessment"
# Set time period from 2022-02-24 to 2023-01-25
period = datetime.datetime(2023, 1, 25) - datetime.datetime(2022, 2, 24)
print(period)
# page = requests.get(base_url + "-february-19-2024")
# html_data = BeautifulSoup(page.content, "html.parser")
# # <p> tag elements
# pte = html_data.find_all("p")
# # Get valuable info
# parsed_data = []
# for elem in pte:
#     if not elem.find_all(True):
#         parsed_data.append(elem)
# # Data clearing
# for datum in parsed_data[::-1]:
#     if datum.text == "Nothing significant to report.":
#         parsed_data.remove(datum)
#
# for datum in parsed_data:
#     print(datum)
#
