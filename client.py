import asyncio

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            print("\n1. Read Total Records")
            print("2. Generate Sales Summary")

            choice = input("\nEnter Choice: ")

            if choice == "1":

                result = await session.call_tool(
                    "read_sales_data",
                    {}
                )

            elif choice == "2":

                start_date = input(
                    "Enter Start Date (YYYY-MM-DD): "
                )

                end_date = input(
                    "Enter End Date (YYYY-MM-DD): "
                )

                result = await session.call_tool(
                    "generate_summary",
                    {
                        "start_date": start_date,
                        "end_date": end_date
                    }
                )

            else:
                print("Invalid Choice")
                return

            print("\n===== RESPONSE =====\n")

            if hasattr(result, "content"):
                for item in result.content:
                    if hasattr(item, "text"):
                        print(item.text)
            else:
                print(result)


if __name__ == "__main__":
    asyncio.run(main())