import asyncio
import httpx
import os

API_URL = "http://localhost:8000/api/v1"

async def test():
    email = "test_upload@example.com"
    password = "Password123!"
    
    async with httpx.AsyncClient() as client:
        # Register
        r = await client.post(f"{API_URL}/auth/register", json={
            "email": email,
            "password": password,
            "full_name": "Test User"
        })
        
        # Login
        r = await client.post(f"{API_URL}/auth/login", json={
            "email": email,
            "password": password
        })
        if r.status_code != 200:
            print(f"Login failed: {r.status_code} {r.text}")
            return
            
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Upload valid files
        for ext in ["wav", "mp3", "flac"]:
            filename = f"test.{ext}"
            path = f"/tmp/{filename}"
            with open(path, "rb") as f:
                files = {"file": (filename, f, f"audio/{ext}")}
                r = await client.post(f"{API_URL}/uploads/upload", headers=headers, files=files)
                print(f"Upload {ext}: {r.status_code} {r.text}")
                
        # Invalid file upload
        files = {"file": ("invalid.txt", b"this is not audio", "text/plain")}
        r = await client.post(f"{API_URL}/uploads/upload", headers=headers, files=files)
        print(f"Upload invalid: {r.status_code} {r.text}")
        
        # Fetch history
        r = await client.get(f"{API_URL}/uploads", headers=headers)
        print(f"History: {r.status_code}")
        for item in r.json():
            print(item["filename"], item["status"])

asyncio.run(test())
