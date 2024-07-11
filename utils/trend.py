import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_macd_signal_line(data, short_window = 5, long_window = 20, signal_window = 12):
    """
    Get SMA, LMA, MACD, signal_line
    
    parameters
    -----------------------------
    short_window: short moving average size
    long_window: long moving average size
    signal_window: moving average size for signal line
    Output:
    Data frame with sensor, SMA, LMA, MACD, signal_line
    SMA: short moving average
    LMA: long moving average
    MACD: SMA - LMA
    signal_line: moving average of MACD
    """
    macd_data = data.copy()
    # Create the set of short and long simple moving average, MACD, signal line over the 
    # respective periods
    macd_data["SMA"] = macd_data['sensor'].rolling(window = short_window, center=False).mean()
    macd_data["LMA"] = macd_data['sensor'].rolling(window = long_window, center=False).mean()
    macd_data["MACD"] = macd_data['SMA'] - macd_data['LMA']
    macd_data['signal_line'] = macd_data['MACD'].rolling(window = signal_window).mean()
    return macd_data



def get_signal_macd_crossover(macd_signal_line, long_window=10):
    """
    Get signal from macd crossover
    
    parameters
    -------------------------
    Input: 
    SMA, LMA, MACD, signal_line
    output: Trading signal from cross over of long and short moving average
    Buy Signal = 1, Sell Signal = -1, Do nothing = 0
    """
    signals = pd.DataFrame(index = macd_signal_line.index)
    signals['sensor'] = macd_signal_line['sensor']
    signals['up_down'] = 0.0
    signals['up_down'][long_window:] = np.where((macd_signal_line.MACD)[long_window:] 
                                            > 0, 1.0, 0.0)  
    signals['up_down'] = signals['up_down'].diff()
    # return buy and sell signal
    return signals


def plot_macd_up_down(macd_signal_line, signals, symbol = 'Sensor Data'):
    """
    Get plot for macd sensor, shortma, longma, buy signal, sell signal
    Input: data frame with all above information
    Output: None
    """
    # putting all above together
    fig = plt.figure(figsize=(12,8))
    plt.title(symbol)
    #fig1
    ax1 = fig.add_subplot(411, ylabel='average crossing')
    macd_signal_line['sensor'].plot(ax=ax1, color = 'r', lw = 2.)
    macd_signal_line[['SMA', 'LMA']].plot(ax = ax1, lw=2.)
    #fig2
    ax2 = fig.add_subplot(412, ylabel = 'UP signal')
    signals['sensor'].plot(ax=ax2, color = 'r', lw = 2.)
    ax2.plot(signals.loc[signals.up_down == 1.0].index, signals.sensor[signals.up_down == 1.0], '^', markersize=10, color = 'g')
    #fig3
    ax3 = fig.add_subplot(413, ylabel = 'Down signal')
    signals['sensor'].plot(ax=ax3, color = 'r', lw = 2.)
    ax3.plot(signals.loc[signals.up_down == -1.0].index, signals.sensor[signals.up_down == -1.0], 'v', markersize=10, color='k')
    #fig4
    ax4 = fig.add_subplot(414, ylabel='Up Down signal')
    signals['sensor'].plot(ax=ax4, color = 'r', lw = 2.)
    # add buy sell
    ax4.plot(signals.loc[signals.up_down == 1.0].index, signals.sensor[signals.up_down == 1.0], '^', markersize=10, color = 'g')
    ax4.plot(signals.loc[signals.up_down == -1.0].index, signals.sensor[signals.up_down == -1.0], 'v', markersize=10, color='k')
    #
    plt.show()