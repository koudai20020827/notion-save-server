from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_SECRET = os.getenv("NOTION_SECRET")
DATABASE_ID = os.getenv("DATABASE_ID")

@app.post("/addToNotion")
async def add_to_notion(req: Request):
    data = await req.json()
    prompt = data.get("prompt")
    answer = data.get("answer")

    notion_data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "prompt": {
                "title": [{"text": {"content": prompt}}]
            },
            "answer": {
                "rich_text": [{"text": {"content": answer}}]
            },
            "status": {
                "select": {"name": "未確認"}
            }
        }
    }

    headers = {
        "Authorization": f"Bearer {NOTION_SECRET}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    response = requests.post(NOTION_API_URL, json=notion_data, headers=headers)
    return {"status": response.status_code}
