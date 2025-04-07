from langgraph_sdk import get_client
from pprint import pprint

async def run_cron():
    client = get_client(url="http://localhost:8123")
    # Using the graph deployed with the name "agent"
    assistant_id = "agent"
    # create thread
    cron_job_stateless = await client.crons.create(
        assistant_id,
        schedule="* * * * *",
        input={"messages": [{"role": "user", "content": "What time is it?"}]},
    )
    pprint(cron_job_stateless)

async def main():
   client = get_client(url="http://localhost:8123")
   my_assistant = await client.assistants.search()
   pprint(my_assistant)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())