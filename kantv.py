import requests
import json
import sys, os

myURL = "http://www.kantv6.com/index.php/video/play?tvid={}&part_id={}&line=1&seo={}"
fake_header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

def reconstruct_link(url):
	url = url.replace("https://", "")
	url = url.replace("http://", "")
	parts = url.split("/")
	seo   = parts[-2]
	parts = parts[-1].split("-")
	tvid    = parts[0]
	part_id = parts[1]
	link = myURL.format(tvid, part_id, seo)
	return link

def get_m3u8_url(url):
	link = reconstruct_link(url)
	data = requests.get(link, headers=fake_header).text
	sys.stderr.write(data)
	data = json.loads(data)
	m3u8_url = data['data']['url']
	title    = data['data']['part_title']
	m3u8_url = "https:" + m3u8_url
	title = title.replace("/", "_")
	title = title.replace(" ", "_")
	title = title.replace("?", "_")
	return m3u8_url, title

def kantv_download(url):
    url, name = get_m3u8_url(url)
    name = name + ".mp4"
    cmd = 'ffmpeg -i \"' + url + '\"' + ' -vcodec copy -strict -2 \"' + name + '\"'
    os.system(cmd)
    print(cmd)

if __name__ == "__main__":
    url = sys.argv[1]
    kantv_download(url)
