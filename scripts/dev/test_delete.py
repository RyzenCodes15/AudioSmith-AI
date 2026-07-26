import urllib.request
import urllib.parse
import json
import os
import subprocess

BASE_URL = "http://localhost:8000/api/v1"

# Register
req = urllib.request.Request(f"{BASE_URL}/auth/register", data=json.dumps({"email": "delete_test4@example.com", "password": "password123", "full_name": "Test Delete"}).encode(), headers={"Content-Type": "application/json"})
try:
    urllib.request.urlopen(req)
except Exception:
    pass

# Login
data = urllib.parse.urlencode({"username": "delete_test4@example.com", "password": "password123"}).encode()
req = urllib.request.Request(f"{BASE_URL}/auth/token", data=data)
resp = urllib.request.urlopen(req)
token = json.loads(resp.read())["access_token"]
print("Got token")

# Create wav
os.system("echo 'RIFF....WAVEfmt ........data....' > dummy.wav")

# Upload via curl
out = subprocess.check_output(f'curl -s -X POST -H "Authorization: Bearer {token}" -F "file=@dummy.wav;type=audio/wav" {BASE_URL}/uploads/upload', shell=True)
print(out)
audio_id = json.loads(out)["id"]
print(f"Uploaded: {audio_id}")

# Delete via curl
resp = subprocess.check_output(f'curl -s -o /dev/null -w "%{{http_code}}" -X DELETE -H "Authorization: Bearer {token}" {BASE_URL}/uploads/{audio_id}', shell=True)
print(f"Delete response code: {resp.decode()}")

