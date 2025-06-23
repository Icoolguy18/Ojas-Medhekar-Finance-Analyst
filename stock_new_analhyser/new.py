from datetime import datetime, timedelta
import yfinance as yf
import pytz
import os
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:8888'


from dependencies.proxy import SimpleHTTPProxy

PROXY_HOST = '127.0.0.1'
PROXY_PORT = 8888

my_proxy = SimpleHTTPProxy(host=PROXY_HOST, port=PROXY_PORT)

def get_stock_value_at_timestamp(company_ticker: str, timestamp: datetime) -> float | None:

    try:

        timestamp_utc = timestamp.replace(tzinfo=pytz.utc)


        if datetime.now(pytz.utc) - timestamp_utc > timedelta(days=7):
            print(f"Warning: For precise intraday data, the timestamp should be within the last 7 days for {company_ticker}.")
            print("Falling back to daily data for older timestamps. This might not be exact for the given time.")
            data = yf.download(company_ticker, start=timestamp_utc.date(), end=timestamp_utc.date() + timedelta(days=1), interval="1d")
        else:
            # Fetch a wider window for 1-minute data to ensure we capture the specific timestamp
            data = yf.download(company_ticker, start=timestamp_utc - timedelta(minutes=30), end=timestamp_utc + timedelta(minutes=30), interval="1m")

        if data.empty:
            print(f"No data found for {company_ticker} around {timestamp}.")
            return None

      
        if data.index.tz is None:
            try:
                market_tz = pytz.timezone('Indian/Kolkata') # Common US market timezone
                data.index = data.index.tz_localize(market_tz, errors='coerce').tz_convert(pytz.utc)
            except pytz.UnknownTimeZoneError:
                print("Warning: Could not localize market timezone. Assuming naive timestamps are UTC for comparison.")
                data.index = data.index.tz_localize(pytz.utc)
        else:
            data.index = data.index.tz_convert(pytz.utc)


        closest_index = (data.index - timestamp_utc).abs().argsort()[0]
        closest_price = data.iloc[closest_index]['Close']

        print(f"Found closest price for {company_ticker} at {data.index[closest_index].isoformat()}: ${closest_price:.2f}")
        return closest_price

    except Exception as e:
        print(f"Error fetching stock value for {company_ticker} at {timestamp}: {e}")
        return None
timestamp_str = '2024-11-21T18:45:00Z'
query_timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
get_stock_value_at_timestamp("TATA", query_timestamp)