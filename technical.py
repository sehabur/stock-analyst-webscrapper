import numpy as np

def calculate_sma(prices, period):
  if len(prices) < period:
    return None
  
  sma = [None] * (period - 1)

  for i in range(period - 1, len(prices)):
      sma.append(sum(prices[i - period + 1:i + 1]) / period)

  return round(sma[-1], 2)

def calculate_ema(prices, period):
  if len(prices) < period:
    return None
  
  ema = [None] * (period - 1) 
  sma = sum(prices[:period]) / period
  ema.append(sma)
  
  multiplier = 2 / (period + 1)

  for price in prices[period:]:
      sma = (price - sma) * multiplier + sma
      ema.append(sma)

  return round(ema[-1], 2)

def calculate_rsi(prices, period=14):
  if len(prices) < period:
    return None

  deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
  gains = [delta if delta > 0 else 0 for delta in deltas]
  losses = [-delta if delta < 0 else 0 for delta in deltas]

  avg_gain = sum(gains[:period]) / period
  avg_loss = sum(losses[:period]) / period

  rs = avg_gain / avg_loss if avg_loss != 0 else 0
  rsi = [None] * (period - 1)
  rsi.append(100 - (100 / (1 + rs)))

  for i in range(period, len(deltas)):
      avg_gain = (avg_gain * (period - 1) + gains[i]) / period
      avg_loss = (avg_loss * (period - 1) + losses[i]) / period
      rs = avg_gain / avg_loss if avg_loss != 0 else 0
      rsi.append(100 - (100 / (1 + rs)))

  return round(rsi[-1], 2)

def calculate_true_range(highs, lows, closes):
    true_ranges = []
    for i in range(1, len(highs)):
        high_low = highs[i] - lows[i]
        high_close = abs(highs[i] - closes[i - 1])
        low_close = abs(lows[i] - closes[i - 1])
        true_ranges.append(max(high_low, high_close, low_close))
    return true_ranges

def calculate_directional_movement(highs, lows):
    plus_dm = []
    minus_dm = []
    for i in range(1, len(highs)):
        up_move = highs[i] - highs[i - 1]
        down_move = lows[i - 1] - lows[i]
        plus_dm.append(up_move if up_move > down_move and up_move > 0 else 0)
        minus_dm.append(down_move if down_move > up_move and down_move > 0 else 0)
    return plus_dm, minus_dm

def calculate_smoothed_values(values, period):
    smoothed_values = []
    sum_values = sum(values[:period])
    smoothed_values.append(sum_values / period)
    for i in range(period, len(values)):
        sum_values = smoothed_values[-1] * (period - 1) + values[i]
        smoothed_values.append(sum_values / period)
    return smoothed_values

def calculate_adx(highs, lows, closes, period=14):
    tr = calculate_true_range(highs, lows, closes)

    plus_dm, minus_dm = calculate_directional_movement(highs, lows)

    smoothed_tr = calculate_smoothed_values(tr, period)
    smoothed_plus_dm = calculate_smoothed_values(plus_dm, period)
    smoothed_minus_dm = calculate_smoothed_values(minus_dm, period)

    plus_di = [(0 if smoothed_tr[i] == 0 else (val / smoothed_tr[i]) * 100) for i, val in enumerate(smoothed_plus_dm)]
    minus_di = [(0 if smoothed_tr[i] == 0 else (val / smoothed_tr[i]) * 100) for i, val in enumerate(smoothed_minus_dm)]

    dx = []
    for i in range(len(plus_di)):
        di_diff = abs(plus_di[i] - minus_di[i])
        di_sum = plus_di[i] + minus_di[i]
        dx.append(0 if di_sum ==0 else (di_diff / di_sum) * 100)

    adx = calculate_smoothed_values(dx, period)
    return round(adx[-1], 2)

def calculate_stochastic_k(data, period=14, smooth_k=3, smooth_d=3):
    if len(data) < period:
        return None

    stoch_k = []    
    for i in range(period - 1, len(data)):
        period_prices = data[i - period + 1:i + 1]
        high = max([d['high'] for d in period_prices])
        low = min([d['low'] for d in period_prices])
        current_close = data[i]['close']

        if high - low == 0:
            k = 0
        else:    
            k = ((current_close - low) / (high - low)) * 100
        stoch_k.append(k)

    slow_k = calculate_sma(stoch_k, smooth_k)
    return slow_k

def calculate_ema_for_macd(prices, period):
    ema = []
    multiplier = 2 / (period + 1)
    
    sma = np.mean(prices[:period])
    ema.append(sma)
    
    for price in prices[period:]:
        ema_value = (price - ema[-1]) * multiplier + ema[-1]
        ema.append(ema_value)
    
    return ema

def calculate_macd(prices, short_period=12, long_period=26, signal_period=9):
    short_ema = calculate_ema_for_macd(prices, short_period)
    long_ema = calculate_ema_for_macd(prices, long_period)
    
    macd_line = [short - long for short, long in zip(short_ema[long_period - short_period:], long_ema)]
    
    valid_macd_line = macd_line[signal_period - 1:]
    
    macd_last_value = round(valid_macd_line[-1], 2)
    
    return float(macd_last_value)

def calculate_williams_percent_r(highs, lows, closes, period=14):
    if len(highs) < period or len(lows) < period or len(closes) < period:
        return None

    williams_r = []

    for i in range(period - 1, len(highs)):
        highest_high = max(highs[i - period + 1:i + 1])
        lowest_low = min(lows[i - period + 1:i + 1])
        current_close = closes[i]
        percent_r = 0 if highest_high - lowest_low == 0 else (((highest_high - current_close) / (highest_high - lowest_low)) * -100)
        williams_r.append(percent_r)

    williams_r_last_value = round(williams_r[-1], 2)

    return williams_r_last_value


def calculate_typical_price(highs, lows, closes):
    return [(high + low + close) / 3 for high, low, close in zip(highs, lows, closes)]

def calculate_raw_money_flow(typical_prices, volumes):
    return [price * volume for price, volume in zip(typical_prices, volumes)]

def calculate_money_flow_index(highs, lows, closes, volumes, period=10):
    if len(highs) < period or len(lows) < period or len(closes) < period or len(volumes) < period:
        return None

    typical_prices = calculate_typical_price(highs, lows, closes)
    raw_money_flow = calculate_raw_money_flow(typical_prices, volumes)

    positive_money_flow = []
    negative_money_flow = []

    for i in range(1, len(typical_prices)):
        if typical_prices[i] > typical_prices[i - 1]:
            positive_money_flow.append(raw_money_flow[i])
            negative_money_flow.append(0)
        elif typical_prices[i] < typical_prices[i - 1]:
            positive_money_flow.append(0)
            negative_money_flow.append(raw_money_flow[i])
        else:
            positive_money_flow.append(0)
            negative_money_flow.append(0)

    mfi = []

    for i in range(period - 1, len(positive_money_flow)):
        positive_flow_sum = sum(positive_money_flow[i - period + 1:i + 1])
        negative_flow_sum = sum(negative_money_flow[i - period + 1:i + 1])

        if negative_flow_sum == 0:
            money_flow_ratio = float('inf')
        else:
            money_flow_ratio = positive_flow_sum / negative_flow_sum
        
        money_flow_index = 100 - (100 / (1 + money_flow_ratio))
        mfi.append(money_flow_index)

    mfi_last_value = round(mfi[-1], 2) if mfi else None

    return mfi_last_value

def calculate_pivot_points(high, low, close):
    P = (high + low + close) / 3

    S1 = 2 * P - high
    R1 = 2 * P - low
    S2 = P - (high - low)
    R2 = P + (high - low)
    S3 = low - 2 * (high - P)
    R3 = high + 2 * (P - low)

    return {
        'P': round(P, 2),
        'S1': round(S1, 2),
        'S2': round(S2, 2),
        'S3': round(S3, 2),
        'R1': round(R1, 2),
        'R2': round(R2, 2),
        'R3': round(R3, 2),
    }

def detect_double_top(prices, window=5, tolerance=0.02):
    """
    Detect double top pattern in a series of closing prices.

    Parameters:
    prices (list of float): List of closing prices.
    window (int): Number of periods to consider for local peaks and troughs.
    tolerance (float): Acceptable percentage difference between the two peaks to be considered a double top.

    Returns:
    list of tuple: List of indices where a double top pattern is detected. Each tuple contains the indices of the first peak, the trough, and the second peak.
    """
    def is_local_maxima(i):
        return all(prices[i] >= prices[j] for j in range(max(0, i - window), min(len(prices), i + window + 1)) if i != j)

    def is_local_minima(i):
        return all(prices[i] <= prices[j] for j in range(max(0, i - window), min(len(prices), i + window + 1)) if i != j)

    peaks = [i for i in range(len(prices)) if is_local_maxima(i)]
    troughs = [i for i in range(len(prices)) if is_local_minima(i)]

    double_tops = []

    for i in range(len(peaks) - 1):
        peak1 = peaks[i]
        peak2 = peaks[i + 1]

        if abs(prices[peak1] - prices[peak2]) / prices[peak1] > tolerance:
            continue

        potential_troughs = [t for t in troughs if peak1 < t < peak2]

        if not potential_troughs:
            continue

        trough = potential_troughs[0]  # Pick the first trough between the peaks

        if prices[trough] < prices[peak1] and prices[trough] < prices[peak2]:
            double_tops.append((peak1, trough, peak2))

    return double_tops

def detect_double_bottom(prices, window=5, tolerance=0.02):
    """
    Detect double bottom pattern in a series of closing prices.

    Parameters:
    prices (list of float): List of closing prices.
    window (int): Number of periods to consider for local peaks and troughs.
    tolerance (float): Acceptable percentage difference between the two troughs to be considered a double bottom.

    Returns:
    list of tuple: List of indices where a double bottom pattern is detected. Each tuple contains the indices of the first trough, the peak, and the second trough.
    """
    def is_local_minima(i):
        return all(prices[i] <= prices[j] for j in range(max(0, i - window), min(len(prices), i + window + 1)) if i != j)

    def is_local_maxima(i):
        return all(prices[i] >= prices[j] for j in range(max(0, i - window), min(len(prices), i + window + 1)) if i != j)

    troughs = [i for i in range(len(prices)) if is_local_minima(i)]
    peaks = [i for i in range(len(prices)) if is_local_maxima(i)]

    double_bottoms = []

    for i in range(len(troughs) - 1):
        trough1 = troughs[i]
        trough2 = troughs[i + 1]

        if abs(prices[trough1] - prices[trough2]) / prices[trough1] > tolerance:
            continue

        potential_peaks = [p for p in peaks if trough1 < p < trough2]

        if not potential_peaks:
            continue

        peak = potential_peaks[0]  # Pick the first peak between the troughs

        if prices[peak] > prices[trough1] and prices[peak] > prices[trough2]:
            double_bottoms.append((trough1, peak, trough2))

    return double_bottoms

def detect_head_and_shoulders(prices, window=5, tolerance=0.02):
    """
    Detect head and shoulders pattern in a series of closing prices.

    Parameters:
    prices (list of float): List of closing prices.
    window (int): Number of periods to consider for local peaks and troughs.
    tolerance (float): Acceptable percentage difference for shoulders to be considered approximately equal.

    Returns:
    list of tuple: List of indices where a head and shoulders pattern is detected. Each tuple contains the indices of the left shoulder, head, right shoulder, and neckline.
    """
    def is_local_maxima(i):
        return all(prices[i] >= prices[j] for j in range(max(0, i - window), min(len(prices), i + window + 1)) if i != j)

    def is_local_minima(i):
        return all(prices[i] <= prices[j] for j in range(max(0, i - window), min(len(prices), i + window + 1)) if i != j)

    peaks = [i for i in range(len(prices)) if is_local_maxima(i)]
    troughs = [i for i in range(len(prices)) if is_local_minima(i)]

    head_and_shoulders = []

    for i in range(1, len(peaks) - 1):
        left_shoulder = peaks[i - 1]
        head = peaks[i]
        right_shoulder = peaks[i + 1]

        if prices[head] <= prices[left_shoulder] or prices[head] <= prices[right_shoulder]:
            continue

        if abs(prices[left_shoulder] - prices[right_shoulder]) / prices[left_shoulder] > tolerance:
            continue

        potential_troughs = [t for t in troughs if left_shoulder < t < head or head < t < right_shoulder]

        if len(potential_troughs) < 2:
            continue

        neckline1 = potential_troughs[0]
        neckline2 = potential_troughs[1]

        head_and_shoulders.append((left_shoulder, head, right_shoulder, neckline1, neckline2))

    return head_and_shoulders

def detect_inverse_head_and_shoulders(prices, window=5, tolerance=0.02):
    """
    Detect inverse head and shoulders pattern in a series of closing prices.

    Parameters:
    prices (list of float): List of closing prices.
    window (int): Number of periods to consider for local peaks and troughs.
    tolerance (float): Acceptable percentage difference for shoulders to be considered approximately equal.

    Returns:
    list of tuple: List of indices where an inverse head and shoulders pattern is detected. Each tuple contains the indices of the left shoulder, head, right shoulder, and neckline.
    """
    def is_local_minima(i):
        return all(prices[i] <= prices[j] for j in range(max(0, i - window), min(len(prices), i + window + 1)) if i != j)

    def is_local_maxima(i):
        return all(prices[i] >= prices[j] for j in range(max(0, i - window), min(len(prices), i + window + 1)) if i != j)

    troughs = [i for i in range(len(prices)) if is_local_minima(i)]
    peaks = [i for i in range(len(prices)) if is_local_maxima(i)]

    inverse_head_and_shoulders = []

    for i in range(1, len(troughs) - 1):
        left_shoulder = troughs[i - 1]
        head = troughs[i]
        right_shoulder = troughs[i + 1]

        if prices[head] >= prices[left_shoulder] or prices[head] >= prices[right_shoulder]:
            continue

        if abs(prices[left_shoulder] - prices[right_shoulder]) / prices[left_shoulder] > tolerance:
            continue

        potential_peaks = [p for p in peaks if left_shoulder < p < head or head < p < right_shoulder]

        if len(potential_peaks) < 2:
            continue

        neckline1 = potential_peaks[0]
        neckline2 = potential_peaks[1]

        inverse_head_and_shoulders.append((left_shoulder, head, right_shoulder, neckline1, neckline2))

    return inverse_head_and_shoulders

def detect_channel_up(prices, window=20, tolerance=0.02):
    """
    Detect channel up pattern in a series of closing prices.

    Parameters:
    prices (list of float): List of closing prices.
    window (int): Number of periods to use for linear regression.
    tolerance (float): Acceptable deviation from the trendline.

    Returns:
    list of tuple: List of indices where a channel up pattern is detected. Each tuple contains the start and end indices of the pattern.
    """
    def linear_regression(x, y):
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]
        return m, c

    channel_up_patterns = []

    for i in range(len(prices) - window):
        x = np.arange(i, i + window)
        y = prices[i:i + window]
        
        m, c = linear_regression(x, y)
        if m <= 0:
            continue

        upper_trendline = m * x + c
        lower_trendline = (m - tolerance) * x + (c - tolerance)

        if all(prices[i + j] >= lower_trendline[j] and prices[i + j] <= upper_trendline[j] for j in range(window)):
            channel_up_patterns.append((i, i + window - 1))

    return channel_up_patterns

def detect_channel_down(prices, window=20, tolerance=0.02):
    """
    Detect channel down pattern in a series of closing prices.

    Parameters:
    prices (list of float): List of closing prices.
    window (int): Number of periods to use for linear regression.
    tolerance (float): Acceptable deviation from the trendline.

    Returns:
    list of tuple: List of indices where a channel down pattern is detected. Each tuple contains the start and end indices of the pattern.
    """
    def linear_regression(x, y):
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]
        return m, c

    channel_down_patterns = []

    for i in range(len(prices) - window):
        x = np.arange(i, i + window)
        y = prices[i:i + window]
        
        m, c = linear_regression(x, y)
        if m >= 0:
            continue

        upper_trendline = (m + tolerance) * x + (c + tolerance)
        lower_trendline = m * x + c

        if all(prices[i + j] <= upper_trendline[j] and prices[i + j] >= lower_trendline[j] for j in range(window)):
            channel_down_patterns.append((i, i + window - 1))

    return channel_down_patterns

def detect_ascending_triangle(prices, window=20, tolerance=0.02):
    """
    Detect ascending triangle pattern in a series of closing prices.

    Parameters:
    prices (list of float): List of closing prices.
    window (int): Number of periods to use for pattern detection.
    tolerance (float): Acceptable deviation for horizontal resistance.

    Returns:
    list of tuple: List of indices where an ascending triangle pattern is detected.
    """
    def linear_regression(x, y):
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]
        return m, c

    ascending_triangle_patterns = []

    for i in range(len(prices) - window):
        x = np.arange(i, i + window)
        y = prices[i:i + window]

        # Find local minima (support line)
        support_indices = [i for i in range(1, len(y) - 1) if y[i] < y[i - 1] and y[i] < y[i + 1]]
        if len(support_indices) < 2:
            continue

        # Fit support line
        support_x = np.array(support_indices)
        support_y = np.array([y[j] for j in support_indices])
        m_support, c_support = linear_regression(support_x, support_y)

        if m_support <= 0:
            continue

        # Find local maxima (resistance line)
        resistance_indices = [i for i in range(1, len(y) - 1) if y[i] > y[i - 1] and y[i] > y[i + 1]]
        if len(resistance_indices) < 2:
            continue

        resistance_y = [y[j] for j in resistance_indices]
        max_resistance = max(resistance_y)
        min_resistance = min(resistance_y)

        if abs(max_resistance - min_resistance) / max_resistance > tolerance:
            continue

        ascending_triangle_patterns.append((i, i + window - 1))

    return ascending_triangle_patterns

def detect_descending_triangle(prices, window=20, tolerance=0.02):
    """
    Detect descending triangle pattern in a series of closing prices.

    Parameters:
    prices (list of float): List of closing prices.
    window (int): Number of periods to use for pattern detection.
    tolerance (float): Acceptable deviation for horizontal support.

    Returns:
    list of tuple: List of indices where a descending triangle pattern is detected.
    """
    def linear_regression(x, y):
        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]
        return m, c

    descending_triangle_patterns = []

    for i in range(len(prices) - window):
        x = np.arange(i, i + window)
        y = prices[i:i + window]

        # Find local maxima (resistance line)
        resistance_indices = [i for i in range(1, len(y) - 1) if y[i] > y[i - 1] and y[i] > y[i + 1]]
        if len(resistance_indices) < 2:
            continue

        resistance_x = np.array(resistance_indices)
        resistance_y = np.array([y[j] for j in resistance_indices])
        m_resistance, c_resistance = linear_regression(resistance_x, resistance_y)

        if m_resistance >= 0:
            continue

        # Find local minima (support line)
        support_indices = [i for i in range(1, len(y) - 1) if y[i] < y[i - 1] and y[i] < y[i + 1]]
        if len(support_indices) < 2:
            continue

        support_y = [y[j] for j in support_indices]
        max_support = max(support_y)
        min_support = min(support_y)

        if abs(max_support - min_support) / min_support > tolerance:
            continue

        descending_triangle_patterns.append((i, i + window - 1))

    return descending_triangle_patterns

# Function to detect Hammer
def is_hammer(open, high, low, close):
    body_length = abs(close - open)
    upper_shadow = high - max(open, close)
    lower_shadow = min(open, close) - low
    return lower_shadow > 2 * body_length and upper_shadow < body_length

# Function to detect Inverted Hammer
def is_inverted_hammer(open, high, low, close):
    body_length = abs(close - open)
    upper_shadow = high - max(open, close)
    lower_shadow = min(open, close) - low
    return upper_shadow > 2 * body_length and lower_shadow < body_length

# Function to detect Bullish Harami
def is_bullish_harami(open1, close1, open2, close2):
    return close1 < open1 and close2 > open2 and close2 > open1 and open2 < close1

# Function to detect Bearish Harami
def is_bearish_harami(open1, close1, open2, close2):
    return close1 > open1 and close2 < open2 and close2 < open1 and open2 > close1

# Function to detect Bullish Engulfing
def is_bullish_engulfing(open1, close1, open2, close2):
    return close1 < open1 and close2 > open2 and open2 < close1 and close2 > open1

# Function to detect Bearish Engulfing
def is_bearish_engulfing(open1, close1, open2, close2):
    return close1 > open1 and close2 < open2 and open2 > close1 and close2 < open1

# Function to detect Bullish Pin Bar
def is_bullish_pin_bar(open, high, low, close):
    body_length = abs(close - open)
    upper_shadow = high - max(open, close)
    lower_shadow = min(open, close) - low
    return lower_shadow > 2 * body_length and upper_shadow < body_length and close > open

# Function to detect Bearish Pin Bar
def is_bearish_pin_bar(open, high, low, close):
    body_length = abs(close - open)
    upper_shadow = high - max(open, close)
    lower_shadow = min(open, close) - low
    return upper_shadow > 2 * body_length and lower_shadow < body_length and close < open

# Function to detect Morning Star
def is_morning_star(open1, close1, open2, close2, open3, close3):
    return close1 < open1 and close2 < open2 and close3 > open3 and open2 < close1 and close3 > (open1 + close1) / 2

# Function to detect Evening Star
def is_evening_star(open1, close1, open2, close2, open3, close3):
    return close1 > open1 and close2 < open2 and close3 < open3 and open2 > close1 and close3 < (open1 + close1) / 2

# Function to detect Shooting Star
def is_shooting_star(open, high, low, close):
    body_length = abs(close - open)
    upper_shadow = high - max(open, close)
    lower_shadow = min(open, close) - low
    return upper_shadow > 2 * body_length and lower_shadow < body_length and close < open

# Function to detect Three White Soldiers
def is_three_white_soldiers(open1, close1, open2, close2, open3, close3):
    return close1 > open1 and close2 > open2 and close3 > open3 and open2 > close1 and open3 > close2

# Function to detect Three Black Crows
def is_three_black_crows(open1, close1, open2, close2, open3, close3):
    return close1 < open1 and close2 < open2 and close3 < open3 and open2 < close1 and open3 < close2

# Function to detect Three Inside Down
def is_three_inside_down(open1, close1, open2, close2, open3, close3):
    return close1 < open1 and close2 > open2 and close3 < open3 and close3 < open2

# Function to detect Three Outside Up
def is_three_outside_up(open1, close1, open2, close2, open3, close3):
    return close1 > open1 and close2 < open2 and close3 > open3 and close3 > open2

# Function to detect Tweezer Top
def is_tweezer_top(open1, close1, high1, open2, close2, high2):
    return high1 == high2 and close1 < open1 and close2 > open2

# Function to detect Tweezer Bottom
def is_tweezer_bottom(open1, close1, low1, open2, close2, low2):
    return low1 == low2 and close1 > open1 and close2 < open2

# Function to detect Bullish Marubozu
def is_bullish_marubozu(open, high, low, close):
    return open == low and close == high

# Function to detect Bearish Marubozu
def is_bearish_marubozu(open, high, low, close):
    return open == high and close == low

# Function to detect Dragonfly Doji
def is_dragonfly_doji(open, high, low, close):
    return open == close and open > low and high == open

# Function to detect Gravestone Doji
def is_gravestone_doji(open, high, low, close):
    return open == close and open < high and low == open

# Function to detect Dark Cloud Cover
def is_dark_cloud_cover(open1, close1, open2, close2, high2):
    return close1 > open1 and open2 > close1 and close2 < (open1 + close1) / 2 and close2 > open1

# Function to detect Hanging Man
def is_hanging_man(open, high, low, close):
    body_length = abs(close - open)
    lower_shadow = min(open, close) - low
    upper_shadow = high - max(open, close)
    return lower_shadow > 2 * body_length and upper_shadow < body_length and close < open

# Function to detect Mat Hold
def is_mat_hold(df, i):
    if i < 4:
        return False
    c1 = df['Close'][i-4] > df['Open'][i-4]
    c2 = df['Close'][i-3] < df['Open'][i-3]
    c3 = df['Close'][i-2] < df['Open'][i-2]
    c4 = df['Close'][i-1] < df['Open'][i-1]
    c5 = df['Close'][i] > df['Open'][i]
    return c1 and c2 and c3 and c4 and c5

# Function to detect Spinning Top
def is_spinning_top(open, high, low, close):
    body_length = abs(close - open)
    total_length = high - low
    return body_length <= 0.2 * total_length

# Function to detect Falling Three Methods
def is_falling_three_methods(df, i):
    if i < 4:
        return False
    c1 = df['Close'][i-4] < df['Open'][i-4]
    c2 = df['Close'][i-3] > df['Open'][i-3]
    c3 = df['Close'][i-2] > df['Open'][i-2]
    c4 = df['Close'][i-1] > df['Open'][i-1]
    c5 = df['Close'][i] < df['Open'][i]
    return c1 and c2 and c3 and c4 and c5 and df['Close'][i] < df['Close'][i-4]

# Function to detect Piercing Line
def is_piercing_line(open1, close1, open2, close2):
    return close1 < open1 and open2 < close1 and close2 > (open1 + close1) / 2 and close2 < open1

# Function to detect the patterns
def detect_candlestick_patterns(df):
    patterns = []

    for i in range(2, len(df)):
        if is_hammer(df['Open'][i], df['High'][i], df['Low'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'hammer'))
        elif is_inverted_hammer(df['Open'][i], df['High'][i], df['Low'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'inverted_hammer'))
        elif is_bullish_harami(df['Open'][i-1], df['Close'][i-1], df['Open'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'bullish_harami'))
        elif is_bearish_harami(df['Open'][i-1], df['Close'][i-1], df['Open'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'bearish_harami'))
        elif is_bullish_engulfing(df['Open'][i-1], df['Close'][i-1], df['Open'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'bullish_engulfing'))
        elif is_bearish_engulfing(df['Open'][i-1], df['Close'][i-1], df['Open'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'bearish_engulfing'))
        elif is_bullish_pin_bar(df['Open'][i], df['High'][i], df['Low'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'bullish_pin_bar'))
        elif is_bearish_pin_bar(df['Open'][i], df['High'][i], df['Low'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'bearish_pin_bar'))
        elif i >= 2 and is_morning_star(df['Open'][i-2], df['Close'][i-2], df['Open'][i-1], df['Close'][i-1], df['Open'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'morning_star'))
        elif i >= 2 and is_evening_star(df['Open'][i-2], df['Close'][i-2], df['Open'][i-1], df['Close'][i-1], df['Open'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'evening_star'))
        elif is_shooting_star(df['Open'][i], df['High'][i], df['Low'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'shooting_star'))
        elif i >= 2 and is_three_white_soldiers(df['Open'][i-2], df['Close'][i-2], df['Open'][i-1], df['Close'][i-1], df['Open'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'three_white_soldiers'))
        elif i >= 2 and is_three_black_crows(df['Open'][i-2], df['Close'][i-2], df['Open'][i-1], df['Close'][i-1], df['Open'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'three_black_crows'))
        elif i >= 2 and is_three_inside_down(df['Open'][i-2], df['Close'][i-2], df['Open'][i-1], df['Close'][i-1], df['Open'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'three_inside_down'))
        elif i >= 2 and is_three_outside_up(df['Open'][i-2], df['Close'][i-2], df['Open'][i-1], df['Close'][i-1], df['Open'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'three_outside_up'))
        elif is_tweezer_top(df['Open'][i-1], df['Close'][i-1], df['High'][i-1], df['Open'][i], df['Close'][i], df['High'][i]):
            patterns.append((df['Date'][i], 'tweezer_top'))
        elif is_tweezer_bottom(df['Open'][i-1], df['Close'][i-1], df['Low'][i-1], df['Open'][i], df['Close'][i], df['Low'][i]):
            patterns.append((df['Date'][i], 'tweezer_bottom'))
        elif is_bullish_marubozu(df['Open'][i], df['High'][i], df['Low'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'bullish_marubozu'))
        elif is_bearish_marubozu(df['Open'][i], df['High'][i], df['Low'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'bearish_marubozu'))
        elif is_dragonfly_doji(df['Open'][i], df['High'][i], df['Low'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'dragonfly_doji'))
        elif is_gravestone_doji(df['Open'][i], df['High'][i], df['Low'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'gravestone_doji'))
        elif is_dark_cloud_cover(df['Open'][i-1], df['Close'][i-1], df['Open'][i], df['Close'][i], df['High'][i]):
            patterns.append((df['Date'][i], 'dark_cloud_cover'))
        elif is_hanging_man(df['Open'][i], df['High'][i], df['Low'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'hanging_man'))
        elif is_mat_hold(df, i):
            patterns.append((df['Date'][i], 'mat_hold'))
        elif is_spinning_top(df['Open'][i], df['High'][i], df['Low'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'spinning_top'))
        elif is_falling_three_methods(df, i):
            patterns.append((df['Date'][i], 'falling_three_methods'))
        elif is_piercing_line(df['Open'][i-1], df['Close'][i-1], df['Open'][i], df['Close'][i]):
            patterns.append((df['Date'][i], 'piercing_line'))    
            
    return patterns




