#!/usr/bin/env python
# coding: utf-8

# %%
import argparse
import os
import sys
import subprocess
from time import sleep
from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options


class IFVOD():

    def __init__(self,):
        options = Options()
        # options.headless = True
        self.browser = webdriver.Firefox(options=options)
        self.base_folder = os.getcwd()

    def find_playlist(self, playlist_url):
        video_links = []

        episodes_xpath = "//a[contains(@href, '/play?id=')]"

        self.browser.get(playlist_url)

        # click this will show all episodes
        earlier = self.browser.find_element_by_link_text("更早")
        if earlier:
            earlier.click()

        # find all episode links
        count = 0
        while True:
            elems = self.browser.find_elements_by_xpath(episodes_xpath)
            if elems:
                break
            else:
                if count < 10:
                    sleep(1)
                    count += 1
                else:
                    print("Can't find episode information")
                    return video_links

        for ele in elems:
            url = ele.get_attribute("href")
            video_links.append(url)
            print(f"find episode {ele.text} with url: {url}")
        return video_links

    # find title
    def get_playlist_folder(self):
        title = self.browser.find_element_by_tag_name("h1").text

        save_folder = os.path.join(self.base_folder, title)
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        print(f"saving to {save_folder}")
        return save_folder

    def download_playlist(self, playlist_url):
        video_links = self.find_playlist(playlist_url)
        self.do_download_playlist(video_links)

    # download videos
    def do_download_playlist(self, video_links):
        save_folder = self.get_playlist_folder()
        for video_url in video_links:
            self.download_video(save_folder, video_url)

    def download_video(self, folder, video_url):
        print(f"downloading {video_url}")
        del self.browser.requests
        self.browser.get(video_url)

        title = self.browser.find_element_by_class_name("vg-overlay-title").text
        file_name = os.path.join(folder, f"{title}.mp4")
        if os.path.exists(file_name):
            print(f"{file_name} exists, skipped")
            return

        # find playlist m3u8 file
        count = 0
        while count < 10:
            m3u8_urls = [r.url for r in self.browser.requests if "m3u8" in r.url]
            if m3u8_urls:
                m3u8_url = m3u8_urls[0]
                break
            else:
                sleep(1)
                count += 1
        if count >= 10:
            print("Can't find m3u8 information")
            return

        # download using ffmpeg
        print(f"find url for video: {m3u8_url}, saving to {file_name}")
        p = subprocess.Popen(["ffmpeg", "-i", m3u8_url, "-c", "copy", file_name, "-loglevel", "warning"],
                             stdout=subprocess.PIPE,
                             universal_newlines=True)
        while True:
            line = p.stdout.readline()
            if line == '' and p.poll() is not None:
                break
            sys.stdout.write(line)
            sys.stdout.flush()


if __name__ == "__main__":
    # %%
    # sys.argv = ["", "https://www.ifvod.tv/detail?id=G7oanMwSKn6"]

    # %%
    parser = argparse.ArgumentParser(description='download ifvod.tv videos')
    parser.add_argument('url', type=str, help='url')
    args = parser.parse_args()
    url = args.url

    client = IFVOD()
    if "ifvod.tv/detail?" in url:
        client.download_playlist(url)
    elif "ifvod.tv/play?" in url:
        client.download_video(os.getcwd(), url)
    else:
        print(f"don't know how to handle {url}")