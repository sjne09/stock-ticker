#!/usr/bin/env python3

import json
import time

from frame import Frame
from rgbmatrix import graphics
from yfScraper import yfScraper

# stolen from https://github.com/Howchoo/crypto-ticker/
# modified to utilize custom data source (yahoo finance)
class Ticker(Frame):
    def __init__(self, *args, **kwargs):
        self.tickers = self.get_tickers()
        self.data = {k:0 for k in self.tickers}

        for ticker in self.tickers:
            self.data[ticker] = yfScraper(ticker)

        super().__init__(*args, **kwargs)

    def get_tickers(self):
        with open('settings.json') as f:
            ticker_data = json.load(f)
            f.close()

        return ticker_data['tickers']

    def get_ticker_canvas(self, ticker):
        last = self.data[ticker].last
        change = self.data[ticker].change

        flast = f'{last: 10.2f}'
        fchange = f'{change: .2%}'

        canvas = self.matrix.CreateFrameCanvas()
        canvas.Clear()

        font_ticker = graphics.Font()
        font_ticker.LoadFont('fonts/7x13.bdf')

        font_price = graphics.Font()
        font_price.LoadFont('fonts/6x12.bdf')

        font_change = graphics.Font()
        font_change.LoadFont('fonts/6x10.bdf')

        change_width = sum(
            [font_change.CharacterWidth(ord(c)) for c in fchange]
        )

        change_x = 63 - change_width

        main_color = graphics.Color(240, 230, 220)
        change_color = (
            graphics.Color(194, 24, 7)
            if fchange.startswith('-')
            else graphics.Color(46, 139, 87)
        )

        if (change < 0):
            fchange = f'{abs(change): .2%}'

        graphics.DrawText(canvas, font_ticker, 2, 15, main_color, ticker)
        graphics.DrawText(canvas, font_price, 3, 26, main_color, flast)
        graphics.DrawText(canvas, font_change, change_x, 13, change_color, fchange)

        return canvas

    def run(self):
        while True:
            for ticker in self.tickers:
                self.data[ticker].update()
                canvas = self.get_ticker_canvas(ticker)

                self.matrix.SwapOnVSync(canvas)
                time.sleep(3)

if __name__ == "__main__":
    Ticker().process()
