import os
from supabase import create_client, Client
from dotenv import load_dotenv
from enum import Enum
load_dotenv()

class StratagyName(str, Enum):
    nifty_n200_rebalance = "n200"
    lv="lv"
    nifty_n50_rebalance="n50"
    nifty_n500_rebalance="n500"

new_column_names = {
    "Name": "Name",
    "Ticker": "Ticker",
    "Current Price (Rs.)": "current_price",
    "Avg Buy Price (Rs.)": "average_price",
    "Returns (%)": "returns_percent",
    "Weightage": "weightage",
    "Shares": "shares"
}

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
