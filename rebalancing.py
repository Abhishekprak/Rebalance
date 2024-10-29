from fastapi import HTTPException
import pandas as pd
import io

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """Replace NaN or Infinity values in the DataFrame with None."""
    df = df.replace([pd.NA, pd.NaT, float('inf'), float('-inf')], None)
    df = df.fillna(0)  # Or replace with 0 or any other default value
    return df


def process_portfolios_rebalance(df_old: pd.DataFrame, df_new: pd.DataFrame, rows: int):
    try:
        
        df_old.rename({'current_price': 'Last Close'}, axis=1, inplace=True)
        print("Issue is below")
        first_n_new = df_new.head(rows).copy()
        first_n_new.rename({'Trading Symbol': 'Ticker'}, axis=1, inplace=True)

        # Shares to sell
        shares_to_sell = df_old[~df_old['Ticker'].isin(first_n_new['Ticker'])]

        # Shares to keep
        shares_to_keep = df_old[df_old['Ticker'].isin(first_n_new['Ticker'])].copy()
        shares_to_keep.drop(columns=[ "returns_percent", "weightage"], inplace=True)

        # average_price
        total_from_selling = sum(shares_to_sell["Last Close"] * shares_to_sell["shares"])

        new_addition = first_n_new[~first_n_new['Ticker'].isin(df_old['Ticker'])]
        new_addition = new_addition.head(shares_to_sell["Name"].count())
        new_addition.drop(columns=[
            "Return Six Months", "Return Three Months", "Return One Month", 
            "Sharpe Return One Year", "Sharpe Return Nine Months", 
            "Sharpe Return Six Months", "Sharpe Return Three Months", 
            "Sharpe Return One Month", "Average Sharpe of 12-6 Months", 
            "Average Sharpe of 12-6-3 Months", "Volatility One Year", 
            "Volatility Nine Months", "Volatility Six Months", 
            "Volatility Three Months", "Beta", "Return One Year", 
            "Return Nine Months", "Average Sharpe of 12-9-6-3 Months", 
            "One Year High", "Away from 1 Year High", "Away from ATH", 
            "MA 200", "MA 100", "MA 50", "MA 20", "Median Volume (in Rupees)", 
            "Marketcap (in Crores)"
        ], inplace=True)

        num_shares = shares_to_sell["Name"].count()
        new_addition["shares"] = (total_from_selling / num_shares) / new_addition["Last Close"]
        new_addition["shares"] = new_addition["shares"].astype(int)

        # Combine the new model
        
        new_model = pd.concat([shares_to_keep, new_addition])
        new_model_value = (new_model["Last Close"] * new_model["shares"]).sum().round()
        new_model['weightage']=round(((new_model["Last Close"]*new_model["shares"])/new_model_value)*100,2)
        mask = new_model['average_price'].isna()

        # print(mask)
        new_model.loc[mask, 'average_price'] = new_addition['Last Close']
        new_model['returns_percent'] = round(
            ((new_model['Last Close'] - new_model['average_price']) / new_model['average_price'].replace(0, float('nan'))) * 100, 
            2
        )
        new_model = new_model.drop(columns=["id"])
        new_model.rename({"Last Close":'current_price'}, axis=1, inplace=True)
        # if new_model["average_price"].empty():
        #     new_model['average_price'] = new_addition['Last Close']
        new_model = clean_df(new_model)
        shares_to_sell = clean_df(shares_to_sell)
        new_addition = clean_df(new_addition)

        return {
            'shares_to_sell': shares_to_sell.to_dict(orient='records'),
            'shares_to_buy': new_addition.to_dict(orient='records'),
            'new_model_portfolio': new_model.to_dict(orient='records'),
            'new model pf value': new_model_value
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

