import csv
import re
    
def preprocess_message(message):

    # Convert to lowercase
    message = message.lower()

    # Remove double quotes
    message = message.replace('"', '')

    # Handle missing values (NaN)
    if not message:
        message = ''

    # Remove extra spaces
    message = re.sub(r'\s+', ' ', message.strip())

    # Remove special characters
    message = re.sub(r'→', '', message)
    message = re.sub(r'[“”]', '', message)
    message = re.sub(r'"', '', message)

    # Remove links
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    message = url_pattern.sub('', message)

    # Replace emojis with spaces
    emoj = re.compile("["
                        u"\U0001F600-\U0001F64F"  # emoticons
                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        u"\U00002500-\U00002BEF"  # chinese char
                        u"\U00002702-\U000027B0"
                        u"\U000024C2-\U0001F251"
                        u"\U0001f926-\U0001f937"
                        u"\U00010000-\U0010ffff"
                        u"\u2640-\u2642"
                        u"\u2600-\u2B55"
                        u"\u200d"
                        u"\u23cf"
                        u"\u23e9"
                        u"\u231a"
                        u"\ufe0f"  # dingbats
                        u"\u3030"
                        "]+", re.UNICODE)
    message = re.sub(emoj, ' ', message)

    return message.strip()
