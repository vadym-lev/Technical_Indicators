import asyncio
import time
import json
import argparse
from datetime import datetime
from dateutil.relativedelta import relativedelta

import aiohttp


parser = argparse.ArgumentParser(description='A tutorial of price_parser script')
parser.add_argument(
    "--start_date",
    default=(datetime.now() - relativedelta(years=1)).strftime("%Y-%m-%d"),
    type=datetime.fromisoformat,
    required=False,
    help="The starting date from which to request data YYYY-MM-DD")
parser.add_argument(
    "--end_date",
    default=datetime.now().strftime("%Y-%m-%d"),
    type=datetime.fromisoformat,
    required=False,
    help="The end date by which to request data YYYY-MM-DD")
parser.add_argument(
    "--interval",
    default="1d",
    choices=["1m", "2m", "5m", "15m", "60m", "1d"],
    type=str,
    required=False,
    help="The interval step for data parsing")

args = parser.parse_args()
start_time = time.time()


async def get_commodity_data(session, url: str, symbol: str):
    async with session.get(url) as resp:
        commodity_data = await resp.json()
        commodity_data = commodity_data['chart']['result'][0]
        commodity_data = {
            symbol: {
                "timestamp": commodity_data['timestamp'],
                "adjclose": commodity_data['indicators']['adjclose'][0]['adjclose'],
                "close": commodity_data['indicators']['quote'][0]['close'],
                "high": commodity_data['indicators']['quote'][0]['high'],
                "low": commodity_data['indicators']['quote'][0]['low'],
                "open": commodity_data['indicators']['quote'][0]['open'],
                "volume": commodity_data['indicators']['quote'][0]['volume']
            }
        }

        return commodity_data


async def main(
        start_date: datetime,
        end_date: datetime,
        interval: str
):

    start_date = int(datetime.timestamp(start_date))
    end_date = int(datetime.timestamp(end_date))

    with open("list_symbols.json", "r") as f:
        list_symbol = json.load(f)

    print(start_date, end_date)

    async with aiohttp.ClientSession() as session:

        tasks = []

        for symbol in list_symbol:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}" \
                  f"?symbol={symbol}" \
                  f"&period1={start_date}" \
                  f"&period2={end_date}" \
                  f"&useYfid=true" \
                  f"&interval={interval}" \
                  f"&includePrePost=true" \
                  f"&events=div%7Csplit%7Cearn" \
                  f"&lang=en-US" \
                  f"&region=US" \
                  f"&crumb=G8gtv6j043L" \
                  f"&corsDomain=finance.yahoo.com"

            tasks.append(asyncio.ensure_future(get_commodity_data(session, url, symbol)))

        commodites_data = await asyncio.gather(*tasks)

        with open("symbols_data.json", "w") as f:

            json.dump({key: d[key] for d in commodites_data for key in d}, f)

print(
    f"start_date = {args.start_date},"
    f"end_date = {args.end_date},"
    f"interval = {args.interval},"
)


asyncio.run(main(
    start_date=args.start_date,
    end_date=args.end_date,
    interval=args.interval
))

print("--- %s seconds ---" % (time.time() - start_time))