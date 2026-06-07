from fastapi import FastAPI, Query
from fastapi.responses import Response
import httpx
import asyncio

app = FastAPI()

# Запасные прокси
FALLBACKS = [
    "https://silent-tuna-64.attrib.deno.net/proxy?url=",
    "https://claude-gateway.andrey710000.workers.dev/proxy?url=",
]

@app.get("/health")
async def health():
    return {"status": "ok", "name": "renpr", "type": "python-smart-proxy"}

@app.get("/proxy/{path:path}")
async def proxy(path: str):
    url = f"https://{path}"
    
    # 1. Прямой запрос
    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            r = await client.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"})
            if r.status_code != 403:
                return Response(content=r.content, status_code=r.status_code, headers={"X-Proxy": "direct"})
    except:
        pass
    
    # 2. Через запасные прокси
    for fb in FALLBACKS:
        try:
            async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
                r = await client.get(fb + url, headers={"User-Agent": "Mozilla/5.0"})
                if r.status_code == 200:
                    return Response(content=r.content, status_code=r.status_code, headers={"X-Proxy": fb.split("?url=")[0]})
        except:
            continue
    
    return Response(content="All proxies failed", status_code=502)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
