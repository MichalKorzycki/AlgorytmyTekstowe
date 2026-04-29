import asyncio
import uvicorn
from fastapi import FastAPI
from starlette.responses import StreamingResponse
from datetime import datetime

app = FastAPI()


@app.get("/hello")
async def hello():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    payload = f"{dt_string}"
    return {"Hello World": payload}


@app.get("/stream")
async def stream():
    async def honey_stream():
        yield '<HTML><BODY>'
        while True:
            try:
                await asyncio.sleep(1)
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                payload = f"{dt_string}<BR>"
                yield payload
            except Exception as e:
                print(e)
                break

    return StreamingResponse(
        honey_stream(),
        media_type="text/html"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)