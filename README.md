# Stock Price Alerts

##### Table of Contents

- [Description](#description)
- [How To Use](#how-to-use)
- [References](#references)

---

## Description

This app will access the AlphaVantage API and check to see if there has been a change of greater than 5% in a given stock between yesterday's close and the day before. If the price of the stock changes more than 5% the app will access the NewsAPI to get the three most current articles related to the company in question and send a message to the user containing the amount of percentage change for the stock as well the titles, a brief synopsis of, and urls for the three articles via text message.


##### Technologies

- Python
- Twilio
- API requests
- Visual Studio

---

## How To Use

Download or clone this repository to your desktop. Run main.py in an appropriate Python environment.

---

## References

##### APIs
- AlphaVantage Stock API
https://www.alphavantage.co/

- News API
https://newsapi.org/

##### Continuing Work on

- https://github.com/SDBranka/_100DOP_Exercises

\
[Back To The Top](#stock-price-alerts)