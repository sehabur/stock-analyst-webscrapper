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




