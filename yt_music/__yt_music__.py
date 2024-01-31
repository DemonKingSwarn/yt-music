import sys
import re
import subprocess

import httpx
import fzf

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
}

client = httpx.Client(headers=headers, timeout=None)

base_url = "https://vid.puffyan.us"
pattern = r'<a.*?href="/watch\?v=(.*?)".*?><p.*?>(.*?)<\/p></a>'

MPV_EXECUTABLE = "mpv"

try:
    if len(sys.argv) == 1:
        query = input("Search: ")
        if query == "":
            print("ValueError: no query parameter provided")
            exit(1)
    else:
        query = " ".join(sys.argv[1:])
except KeyboardInterrupt:
    exit(0)

query = query.replace(' ', '+')
opts = []


def extract_video_id(video_title):
    match = re.search(r' - ([\w-]+)$', video_title)
    
    #match = re.search(pattern, video_title)
    
    if match:
        video_id = match.group(1)
        return video_id
    else:
        return None

def play_loop(video_id, video_title):
   
    args = [
        MPV_EXECUTABLE,
        f"https://music.youtube.com/watch?v={video_id}",
        f"--force-media-title={video_title}",
        "--no-video",
        "--loop",
    ]

    mpv_process = subprocess.Popen(args, stdout=subprocess.DEVNULL)
    mpv_process.wait()



def play(video_id, video_title):
   
    args = [
        MPV_EXECUTABLE,
        f"https://music.youtube.com/watch?v={video_id}",
        f"--force-media-title={video_title}",
        "--no-video",
    ]

    mpv_process = subprocess.Popen(args, stdout=subprocess.DEVNULL)
    mpv_process.wait()


def main():
    fetch = client.get(f"{base_url}/search?q={query}")
    matches = re.findall(pattern, fetch.text)
    for match in matches:
        video_id,  title = match
        opt = f"{title} - {video_id}"
        opts.append(opt)
    ch = fzf.fzf_prompt(opts)
    print(ch)
    idx = extract_video_id(ch)
    play_ch = fzf.fzf_prompt(["play", "loop"])
    try:
        if play_ch == "play":
            play(idx, ch)
        else:
            play_loop(idx, ch)
    except KeyboardInterrupt:
        exit(0)

main()
