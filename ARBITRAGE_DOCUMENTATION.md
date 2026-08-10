# Arbitrage.py Documentation
## How It Works in Simulated FX Exchange Context

---

## Table of Contents
1. [Overview](#overview)
2. [Core Concepts](#core-concepts)
3. [Module Functions](#module-functions)
4. [Algorithm Deep Dive](#algorithm-deep-dive)
5. [Data Structures](#data-structures)
6. [Example Walkthrough](#example-walkthrough)
7. [Precision & Decimal Handling](#precision--decimal-handling)
8. [Performance Considerations](#performance-considerations)

---

## Overview

**arbitrage.py** is a foreign exchange (FX) arbitrage detection module designed to identify profitable trading cycles in a simulated currency market. It searches for triangular (and n-way) arbitrage opportunities by analyzing conversion rates between multiple currency pairs.

### What is Arbitrage?

**Arbitrage** is a risk-free trading strategy that exploits price discrepancies across different markets or currency pairs. In the FX context, a trader can convert:

```
USD → EUR → GBP → USD (with profit)
```

If the cumulative conversion rates result in more currency than the initial amount, that represents a profitable arbitrage cycle.

### Simulation Context

This module operates on a **simulated FX market** where:
- Exchange rates are fixed and predefined
- There are no transaction costs or latency
- Multiple currencies and conversion paths exist
- The goal is to find any cycle starting from a base currency that yields profit

---

## Core Concepts

### 1. **Currency Pairs & Exchange Rates**

Exchange rates are represented as directional pairs:

```python
{
    ('USD', 'EUR'): 0.91,  # 1 USD = 0.91 EUR
    ('EUR', 'GBP'): 0.86,  # 1 EUR = 0.86 GBP
    ('GBP', 'USD'): 1.30   # 1 GBP = 1.30 USD
}
```

Each rate is **unidirectional**. If you have `('USD', 'EUR')`, the reverse path `('EUR', 'USD')` must be defined separately.

### 2. **Cycles & Paths**

A **cycle** is a sequence of currencies where:
- The starting currency is the base currency
- The path traverses through intermediate currencies
- The final currency converts back to the starting currency

Example cycle: `(USD, EUR, GBP, USD)`

### 3. **Profit Calculation**

For a given cycle and initial amount:

```
Final Amount = Initial Amount × Rate₁ × Rate₂ × ... × Rateₙ

Profit = Final Amount - Initial Amount

Profit % = (Profit / Initial Amount) × 100
```

If `Final Amount > Initial Amount`, the cycle is profitable.

---

## Module Functions

### `find_arbitrage_opportunities(amount, rate_pairs, base_currency='USD')`

**Purpose:** Discovers all profitable arbitrage cycles in the FX market.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `amount` | numeric | Initial investment amount in the base currency |
| `rate_pairs` | dict | Mapping of `(source, target)` currency pairs to exchange rates |
| `base_currency` | str | Currency to start and end each cycle (default: `'USD'`) |

#### Returns

| Type | Description |
|------|-------------|
| `list[dict]` | List of profitable opportunities, sorted by highest profit first |

#### Return Structure

Each dictionary in the list contains:

```python
{
    'cycle': tuple,           # e.g., ('USD', 'EUR', 'GBP', 'USD')
    'start_amount': Decimal,  # Initial amount
    'end_amount': Decimal,    # Final amount after conversions
    'profit': Decimal,        # Absolute profit (end - start)
    'profit_pct': Decimal,    # Profit percentage
}
```

#### Exceptions

| Exception | Condition |
|-----------|-----------|
| `ValueError` | If `amount <= 0` |

---

### `print_opportunities(amount, rate_pairs, base_currency='USD')`

**Purpose:** Convenience function to display arbitrage opportunities in human-readable format.

#### Behavior

- Calls `find_arbitrage_opportunities()` internally
- Prints formatted results to console
- Displays cycle path, end amount, profit, and profit percentage
- Shows "No profitable FX arbitrage cycles were found." if no opportunities exist

#### Example Output

```
Profitable FX arbitrage cycles:
1. Cycle: USD -> EUR -> GBP -> USD | End amount: 1011.80 | Profit: 11.80 | Profit %: 1.1800%
2. Cycle: USD -> EUR -> USD | End amount: 1001.00 | Profit: 1.00 | Profit %: 0.1000%
```

---

## Algorithm Deep Dive

### Step-by-Step Execution

#### 1. **Initialization**
```python
currencies = set([base_currency])
for pair in rate_pairs:
    source, target = pair
    currencies.add(source)
    currencies.add(target)
```

Collects all unique currencies from the rate pairs and the base currency.

#### 2. **Generate All Possible Cycles**
```python
for cycle_len in range(2, len(currency_list) + 1):
    for cycle in permutations(currency_list, cycle_len):
        if cycle[0] != base_currency:
            continue
```

- Iterates through cycle lengths from 2 to total number of currencies
- Generates all permutations of currencies for each length
- **Filters to only cycles starting with the base currency** (optimization)

**Why permutations?** This ensures every possible path combination is explored.

#### 3. **Traverse Each Cycle**
```python
for i in range(len(path)):
    start = path[i]
    end = path[(i + 1) % len(path)]
    
    if (start, end) not in rate_pairs:
        valid = False
        break
    
    product *= Decimal(str(rate_pairs[(start, end)]))
```

- Iterates through each currency transition in the cycle
- Uses modulo operator `%` to wrap back to the start (creating a closed loop)
- **Checks if the currency pair exists** in the rate_pairs mapping
- Multiplies rates sequentially to compute final amount
- Marks cycle as invalid if any conversion is impossible

#### 4. **Evaluate Profitability**
```python
if product > Decimal(str(amount)):
    profit = product - Decimal(str(amount))
    percentage = (profit / Decimal(str(amount))) * Decimal('100')
    opportunities.append({...})
```

- Compares final amount against initial amount
- Calculates absolute and percentage profit
- Only appends profitable cycles

#### 5. **Sort Results**
```python
opportunities.sort(key=lambda item: item['profit'], reverse=True)
```

Returns opportunities ordered by highest profit first.

---

## Data Structures

### Rate Pairs Dictionary

**Structure:**
```python
{
    (currency_1, currency_2): rate_value,
    (currency_3, currency_4): rate_value,
    ...
}
```

**Example:**
```python
sample_rates = {
    ('USD', 'EUR'): 0.91,    # 1 USD converts to 0.91 EUR
    ('EUR', 'GBP'): 0.86,    # 1 EUR converts to 0.86 GBP
    ('GBP', 'USD'): 1.30,    # 1 GBP converts to 1.30 USD
    ('USD', 'JPY'): 150.0,   # 1 USD converts to 150 JPY
    ('JPY', 'EUR'): 0.006,   # 1 JPY converts to 0.006 EUR
    ('EUR', 'USD'): 1.10,    # 1 EUR converts to 1.10 USD
}
```

### Opportunities List

**Structure:**
```python
[
    {
        'cycle': ('USD', 'EUR', 'GBP', 'USD'),
        'start_amount': Decimal('1000'),
        'end_amount': Decimal('1011.80'),
        'profit': Decimal('11.80'),
        'profit_pct': Decimal('1.1800'),
    },
    {
        'cycle': ('USD', 'EUR', 'USD'),
        'start_amount': Decimal('1000'),
        'end_amount': Decimal('1001.00'),
        'profit': Decimal('1.00'),
        'profit_pct': Decimal('0.1000'),
    },
]
```

---

## Example Walkthrough

### Setup

```python
amount = 1000  # Start with 1000 USD
sample_rates = {
    ('USD', 'EUR'): 0.91,
    ('EUR', 'GBP'): 0.86,
    ('GBP', 'USD'): 1.30,
    ('USD', 'JPY'): 150.0,
    ('JPY', 'EUR'): 0.006,
    ('EUR', 'USD'): 1.10,
}
```

### Finding Cycle: USD → EUR → GBP → USD

**Step 1: Initial Setup**
- Start: 1000 USD
- Product: 1000

**Step 2: USD → EUR**
- Conversion rate: 0.91
- Amount: 1000 × 0.91 = 910 EUR
- Product: Decimal('910')

**Step 3: EUR → GBP**
- Conversion rate: 0.86
- Amount: 910 × 0.86 = 782.6 GBP
- Product: Decimal('782.6')

**Step 4: GBP → USD**
- Conversion rate: 1.30
- Amount: 782.6 × 1.30 = 1,017.38 USD
- Product: Decimal('1017.38')

**Step 5: Evaluate Profitability**
- Final Amount: 1,017.38
- Initial Amount: 1,000
- Profit: 1,017.38 - 1,000 = **17.38 USD**
- Profit %: (17.38 / 1,000) × 100 = **1.738%**

**Result:**
```python
{
    'cycle': ('USD', 'EUR', 'GBP', 'USD'),
    'start_amount': Decimal('1000'),
    'end_amount': Decimal('1017.38'),
    'profit': Decimal('17.38'),
    'profit_pct': Decimal('1.738'),
}
```

### Execution Example

```python
result = find_arbitrage_opportunities(1000, sample_rates, base_currency='USD')
print(result[:3])
```

Would output something like:
```python
[
    {
        'cycle': ('USD', 'EUR', 'GBP', 'USD'),
        'start_amount': Decimal('1000'),
        'end_amount': Decimal('1017.38'),
        'profit': Decimal('17.38'),
        'profit_pct': Decimal('1.738000...'),
    },
    {
        'cycle': ('USD', 'EUR', 'USD'),
        'start_amount': Decimal('1000'),
        'end_amount': Decimal('1001.00'),
        'profit': Decimal('1.00'),
        'profit_pct': Decimal('0.100000...'),
    },
    # ... additional results
]
```

---

## Precision & Decimal Handling

### Why Use Decimal?

```python
from decimal import Decimal, getcontext
getcontext().prec = 28
```

**Reasons:**

1. **Floating-Point Errors:** Standard float operations can introduce rounding errors
   ```python
   0.1 + 0.2 == 0.3  # False! (due to floating-point representation)
   ```

2. **Financial Accuracy:** Currency calculations require exact arithmetic
   - Decimal maintains precision to 28 decimal places
   - Prevents loss of fractional cents across multiple conversions

3. **Consistency:** All intermediate calculations use Decimal
   - Input rates are converted: `Decimal(str(rate_pairs[(start, end)]))`
   - Ensures no precision loss during multiplication chains

### Example

```python
# With floats (problematic)
result_float = 1000 * 0.91 * 0.86 * 1.30  # May have rounding errors

# With Decimal (precise)
result_decimal = (Decimal('1000') * 
                  Decimal('0.91') * 
                  Decimal('0.86') * 
                  Decimal('1.30'))  # Exact arithmetic
```

---

## Performance Considerations

### Time Complexity

**Worst Case:** O(n! × n)

- **Permutations:** n! possible cycles (factorial complexity)
- **Per Cycle:** O(n) to traverse the path and multiply rates

**Practical Implication:**
- With 5 currencies: ~120 cycles to check
- With 6 currencies: ~720 cycles to check
- With 10 currencies: ~3.6 million cycles to check

### Space Complexity

**O(n + m)**

- **n:** Number of unique currencies
- **m:** Number of rate pairs

### Optimization Strategies

1. **Filter by Base Currency:**
   ```python
   if cycle[0] != base_currency:
       continue
   ```
   Reduces permutations by ~n times (only cycles starting with base currency)

2. **Early Exit on Invalid Path:**
   ```python
   if (start, end) not in rate_pairs:
       valid = False
       break
   ```
   Avoids unnecessary computations for incomplete cycles

3. **Limit Cycle Length:** Consider capping `cycle_len` in production (e.g., max 4-5 currencies) to reduce computational overhead

### Scalability Notes

- **Small Markets (< 10 currencies):** Fast execution, no optimization needed
- **Medium Markets (10-20 currencies):** Consider caching or limiting cycle lengths
- **Large Markets (> 20 currencies):** May require algorithmic optimization or heuristic-based search

---

## Integration in Simulated FX Exchange

### Workflow

1. **Market Data Collection:** Populate `rate_pairs` from simulated exchange
2. **Opportunity Detection:** Call `find_arbitrage_opportunities()` regularly
3. **Strategy Execution:** Execute profitable cycles found by the algorithm
4. **Profit Realization:** Convert back to base currency and record gains

### Example Integration

```python
# Simulated exchange with historical rates
def run_arbitrage_simulation(exchange_rates_snapshot):
    """Run arbitrage detection on current market snapshot."""
    opportunities = find_arbitrage_opportunities(
        amount=10000,
        rate_pairs=exchange_rates_snapshot,
        base_currency='USD'
    )
    
    if opportunities:
        print(f"Found {len(opportunities)} profitable cycle(s)")
        best_cycle = opportunities[0]  # Highest profit
        execute_trade(best_cycle)
    else:
        print("Market is efficient - no arbitrage opportunities")
```

### Constraints in Simulation

- **Atomic Execution:** All conversions happen simultaneously (no slippage)
- **Perfect Liquidity:** Unlimited funds available at given rates
- **No Costs:** No transaction fees or bid-ask spreads
- **Market Snapshot:** Rates fixed during cycle execution

---

## Summary

**arbitrage.py** provides a comprehensive toolkit for detecting profitable foreign exchange cycles in a simulated market. It uses:

- **Permutation-based search** to explore all possible conversion paths
- **Decimal arithmetic** for financial precision
- **Path validation** to ensure all conversions are available
- **Profit ranking** to prioritize best opportunities

This module is ideal for:
- ✅ Educational purposes (understanding arbitrage)
- ✅ Simulation and backtesting
- ✅ Proof-of-concept implementations
- ✅ Market analysis and research

It may require optimization for real-time production use with large currency universes.
