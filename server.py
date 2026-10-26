from mcp.server.fastmcp import FastMCP
import pandas as pd

mcp = FastMCP("SalesServer")


@mcp.tool()
def read_sales_data():

    df = pd.read_excel("sales.xlsx", engine="openpyxl")

    total_records = len(df)
    records=df.to_dict(orient="records")

    return {"Total Records Available": total_records,
       "Records": records}



@mcp.tool()
def generate_summary(start_date: str, end_date: str):

    df = pd.read_excel("sales.xlsx", engine="openpyxl")

    df["Date"] = pd.to_datetime(df["Date"])

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered = df[
        (df["Date"] >= start_date)
        & (df["Date"] <= end_date)
    ]

    total_sales = filtered["SalesAmount"].sum()

    report = f"""
Sales Summary Report

Start Date : {start_date.date()}
End Date   : {end_date.date()}

Total Records : {len(filtered)}

Total Sales : {total_sales}
"""

    with open("report.txt", "w") as file:
        file.write(report)

    return report


if __name__ == "__main__":
    
    print("===================================")
    print("Sales MCP Server Started")
    print("Waiting for client requests...")
    print("===================================")

    mcp.run()