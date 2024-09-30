import requests
import yfinance as yf


def get_weather(api_key, lat, lon, units="metric", lang="en"):
    """
    获取指定位置的天气信息.

    参数:
        api_key (str): 你的 OpenWeatherMap API 密钥.
        lat (float): 纬度.
        lon (float): 经度.
        units (str): 温度单位 ("metric" 对应摄氏度, "imperial" 对应华氏度, "standard" 对应开氏度). 默认为 "metric".
        lang (str): 返回数据的语言. 默认为 "en" (英文).

    返回:
        dict: 天气数据.
    """
    url = "https://api.openweathermap.org/data/3.0/onecall"

    # 定义请求参数
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
    }

    try:
        # 发送请求
        response = requests.get(url, params=params)
        # 检查响应状态码
        response.raise_for_status()
        # 返回JSON格式的响应内容
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None




def get_historical_stock_data(ticker, start_date, end_date, interval='1d'):
    """
    获取指定股票在某个时间段内的历史市场数据

    参数:
    ticker (str): 股票代码，例如 'AAPL' 或 'MSFT'
    start_date (str): 开始日期，格式为 'YYYY-MM-DD'
    end_date (str): 结束日期，格式为 'YYYY-MM-DD'
    interval (str): 数据间隔，默认为 '1d'（每日数据）

    返回:
    DataFrame: 包含历史股票数据的DataFrame
    """
    stock = yf.Ticker(ticker)

    # 获取历史数据
    historical_data = stock.history(start=start_date, end=end_date, interval=interval)

    return historical_data

# ticker = 'AAPL'
# start_date = '2024-01-01'
# end_date = '2024-09-01'
#
# historical_data = get_historical_stock_data(ticker, start_date, end_date)
# print(historical_data)

