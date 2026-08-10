from decimal import Decimal, getcontext
from itertools import permutations

getcontext().prec = 28


def find_arbitrage_opportunities(amount, rate_pairs, base_currency='USD'):
    """
    Search a directed FX market for profitable triangular cycles.

    Parameters
    ----------
    amount : numeric
        Initial amount in base_currency.
    rate_pairs : dict
        Mapping of currency pairs to FX rates. Expected to be of the form
        {('USD', 'EUR'): 0.91, ('EUR', 'GBP'): 0.86, ...} where each pair
        rate is the conversion factor from the first currency to the second.
        Example: 1 USD -> 0.91 EUR.
    base_currency : str
        Currency used to compute the return percentage from each cycle.

    Returns
    -------
    list[dict]
        A list of candidate arbitrage opportunities ordered by highest profit.
    """
    if amount <= 0:
        raise ValueError('amount must be positive')

    currencies = set([base_currency])
    for pair in rate_pairs:
        source, target = pair
        currencies.add(source)
        currencies.add(target)

    currency_list = sorted(currencies)

    opportunities = []

    for cycle_len in range(2, len(currency_list) + 1):
        for cycle in permutations(currency_list, cycle_len):
            if cycle[0] != base_currency:
                continue

            path = list(cycle)
            product = Decimal(str(amount))
            valid = True

            for i in range(len(path)):
                start = path[i]
                end = path[(i + 1) % len(path)]

                if (start, end) not in rate_pairs:
                    valid = False
                    break

                product *= Decimal(str(rate_pairs[(start, end)]))

            if not valid:
                continue

            if product > Decimal(str(amount)):
                profit = product - Decimal(str(amount))
                percentage = (profit / Decimal(str(amount))) * Decimal('100')

                opportunities.append({
                    'cycle': tuple(path),
                    'start_amount': Decimal(str(amount)),
                    'end_amount': product,
                    'profit': profit,
                    'profit_pct': percentage,
                })

    opportunities.sort(key=lambda item: item['profit'], reverse=True)
    return opportunities


def print_opportunities(amount, rate_pairs, base_currency='USD'):
    """Convenience function that prints a readable result list."""
    opportunities = find_arbitrage_opportunities(amount, rate_pairs, base_currency)

    if not opportunities:
        print('No profitable FX arbitrage cycles were found.')
        return

    print('Profitable FX arbitrage cycles:')
    for index, item in enumerate(opportunities, start=1):
        cycle_text = ' -> '.join(item['cycle'])
        profit = item['profit']
        percentage = item['profit_pct']
        print(
            f'{index}. Cycle: {cycle_text} | '
            f'End amount: {item["end_amount"]:.2f} | '
            f'Profit: {profit:.2f} | Profit %: {percentage:.4f}%'
        )


if __name__ == '__main__':
    sample_rates = {
        ('USD', 'EUR'): 0.91,
        ('EUR', 'GBP'): 0.86,
        ('GBP', 'USD'): 1.30,
        ('USD', 'JPY'): 150.0,
        ('JPY', 'EUR'): 0.006,
        ('EUR', 'USD'): 1.10,
    }

    result = find_arbitrage_opportunities(1000, sample_rates, base_currency='USD')
    print(result[:3])
