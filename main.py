import json
from fastapi import FastAPI, HTTPException, UploadFile, File,Query
import pandas as pd
import io
from configuration import StratagyName, supabase,new_column_names
from rebalancing import clean_df, process_portfolios_rebalance
import datetime
# from logging_config import logger
app = FastAPI(title="Nifty-shloka-rebalancing",version="0.0.1")


@app.post("/portfolio/{strategy_name}")
async def get_portfolio_for_strategy(
    strategy_name: StratagyName,
    new_file: UploadFile = File(..., description="CSV file for new lookback data")
):
    try:
        # Read the uploaded files into pandas DataFrames
        old_df = supabase.table(strategy_name.name).select("*").execute()
        old_df=old_df.model_dump_json()
        old_df=pd.DataFrame(json.loads(old_df)['data'])
        old_df.drop('id', axis=1)
        # pd.read_csv(io.BytesIO(await old_file.read()))
        new_df = pd.read_csv(io.BytesIO(await new_file.read()))
        # logger.info(old_df)
        new_df=new_df.rename(columns=new_column_names)
        old_df = clean_df(old_df)
        new_df = clean_df(new_df)
        # print(old_df)
        # print()
        # print(new_df)
        if strategy_name.value == "n200":
            rows = 40  # Custom row count for strategy1
        elif strategy_name.value == "lv":
            rows = 60  # Custom row count for strategy2
        elif strategy_name.value == "n50":
            rows = 10  # Custom row count for strategy3
        elif strategy_name.value == "n500":
            rows = 50
        rebalance_processed_data=process_portfolios_rebalance(old_df, new_df, rows)
        """
        add the data back to {strategy_name.name} table
        create a history tradelog for each and push
        """
        return rebalance_processed_data['new_model_portfolio']

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {e}")

"""
cron endpoint to check if the current day falls under any of the logic? if so add the corrosponding
"""

@app.get("/check/rebalance", name="Cron endpoint for getting next update date")
async def check_rebalance():
    current_date = datetime.date.today()
    day_of_week = current_date.strftime("%A")  # Get the day name like "Monday"
    return {"current_date": str(current_date), "day_of_week": day_of_week}