import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import os


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHAV_API_ENDP = "https://www.alphavantage.co/query"
ALPHAV_API_KEY = os.environ.get("ALPHAV_API_KEY")
NEWS_API_ENDP = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
account_sid = "Your account SID"
auth_token = os.environ.get("AUTH_TOKEN")
twilio_ph_num = "+12057362422"
# twilio can only send texts to numbers verified by the account
receiver_ph_num = "+13066346733"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the 
# day before yesterday then print("Get News").
alphav_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": ALPHAV_API_KEY
}
alphav_response = requests.get(ALPHAV_API_ENDP, params=alphav_params)
# print(alphav_response.status_code)
alphav_response.raise_for_status()
# print(alphav_response.json())
alphav_data = alphav_response.json()["Time Series (Daily)"]
# print(f"alphav_data:\n{alphav_data}")
stock_price_list = [value for (key, value) in alphav_data.items()]
# print(f"stock_price_list:\n{stock_price_list}")
# get the difference yesterday's and the day before's closing price
yest_price = float(stock_price_list[0]["4. close"])
compare_price = float(stock_price_list[1]["4. close"])
difference_between_prices = yest_price - compare_price
# print(f"difference_between_prices: {difference_between_prices}")
price_change_percent = (difference_between_prices / yest_price) * 100
# print(f"price_change_percent: {price_change_percent}")

# for message: determine symbol and format %
if price_change_percent > 0:
    arrow = "🔺"
else:
    arrow = "🔻"
percentage = abs(round(price_change_percent, 2))

# if the price has changed more than +/-5% get the first three 
# relevant news articles and text them to the user

price_change_percent = 14
if abs(price_change_percent) >= 5:
    # print("Get News")
    ## STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the 
    # first 3 news pieces for the COMPANY_NAME. 
    news_params = {
        "q": COMPANY_NAME,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY
    }

    news_response = requests.get(NEWS_API_ENDP, params=news_params)
    # print(news_response.status_code)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"][:3]
    # print(f"news_data: {news_data}")

    #Create the text message to send
    text_message = f"{STOCK}: {arrow}{percentage}%"
    for article in news_data:
        text_message += f"\nHeadline: {article['title']}. \nBrief: {article['description']} \n{article['url']}\n"
    # print(f"text_message: {text_message}")


    ## STEP 3: Use https://www.twilio.com
    # Send a seperate message with the percentage change and each
    # article's title and description to your phone number. 
    #Optional: Format the SMS message like this: 
    """
    TSLA: 🔺2%
    Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
    Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
    or
    "TSLA: 🔻5%
    Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
    Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
    """
    # create proxy client in order to run app from cloud service PythonAnywhere
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    # create twilio client
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body=text_message,
        from_=twilio_ph_num,
        to=receiver_ph_num
    )
    print(message.status)


















