import json
import time
import requests
import urllib3
import xmltodict


def podcast_details_retreival(url_data):
    write_data = []
    for url in url_data:
        temp_list = []
        try:
            http = urllib3.PoolManager()
            response = http.request('GET', url)
            data = xmltodict.parse(response.data)
        except:
            resp = requests.get(url)
            if resp.status_code == 404:
                continue
            json_string = json.dumps(xmltodict.parse(resp.content), indent=4)
            data = json.loads(json_string)
        podcast_name = data['rss']['channel']['title']
        podcast_detail = data['rss']['channel']['item']
        for item in podcast_detail:
            if isinstance(item, dict):
                date = item['pubDate']
            elif isinstance(podcast_detail, dict):
                date = podcast_detail['pubDate']
            else:
                print("Error in url: ", url)
                continue
            temp_list.append(date)
        write_data.append({"title": podcast_name, "url": url, "dates": temp_list})
    return write_data


if __name__ == '__main__':
    start_time = time.time()
    urls = open("urls.json", "r")
    url_data = json.loads(urls.read())
    dates = podcast_details_retreival(url_data)
    with open("dates_sync.json", "w") as outfile:
        json.dump(dates, outfile)
    print(f"Execution time: {time.time() - start_time}s")
    print("Complete.")
