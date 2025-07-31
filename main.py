from flask import Flask, Response, request
import requests

app = Flask(__name__)

# Config
BASE_URL = "https://mtlivestream.com/asian/ytlive/"
HEADERS = {
    "Origin": "https://www.asiantvonline.com",
    "Referer": "https://www.asiantvonline.com/",
    "User-Agent": "Mozilla/5.0"
}

@app.route("/index.m3u8")
def proxy_playlist():
    try:
        r = requests.get(BASE_URL + "index.m3u8", headers=HEADERS, timeout=10)
        r.raise_for_status()
        content = r.text

        # Rewrite .ts URLs to local route
        lines = []
        for line in content.splitlines():
            if line.endswith(".ts"):
                line = "/" + line.strip()
            lines.append(line)
        
        modified_content = "\n".join(lines)
        return Response(modified_content, content_type="application/vnd.apple.mpegurl")
    except Exception as e:
        return Response(f"# Error fetching playlist: {e}", status=500)

@app.route("/<segment>.ts")
def proxy_segment(segment):
    try:
        segment_url = BASE_URL + f"{segment}.ts"
        r = requests.get(segment_url, headers=HEADERS, stream=True, timeout=10)
        r.raise_for_status()
        return Response(r.iter_content(chunk_size=1024), content_type="video/MP2T")
    except Exception as e:
        return Response(f"# Error fetching segment: {e}", status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
