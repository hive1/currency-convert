import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arbitrage import find_arbitrage_opportunities


def test_find_arbitrage_opportunity():
    market_rates = {
        ('USD', 'EUR'): 0.91,
        ('EUR', 'GBP'): 0.86,
        ('GBP', 'USD'): 1.30,
    }

    opportunities = find_arbitrage_opportunities(1000, market_rates, base_currency='USD')

    assert len(opportunities) >= 1
    assert opportunities[0]['cycle'] == ('USD', 'EUR', 'GBP')
    assert opportunities[0]['profit'] > 0
