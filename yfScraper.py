import requests

class yfScraper:
    def __init__(self, ticker):
        self.ticker = ticker
        self.update()

    def scrape(self):
        session = requests.Session()

        # include header to disguise as browser
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'})

        response = session.get('https://query1.finance.yahoo.com/v8/finance/chart/%s'%(self.ticker))

        self.data = response.json()['chart']['result'][0]['meta']

    def get_last(self):
        return (self.data['regularMarketPrice'])

    def get_prev_close(self):
        return (self.data['previousClose'])

    def update(self):
        self.scrape()
        self.last = self.get_last()
        self.previous_close = self.get_prev_close()
        self.change = self.last / self.previous_close - 1
