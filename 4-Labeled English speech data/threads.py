import threading
import time
import pandas
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import requests
import warnings


class downloadScripts (threading.Thread):
    def __init__(self, threadID, df, output_dir):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.df = df
        self.output_dir = output_dir

    def run(self):
        """
        Spawns a new thread and calls the get audio and transcript
        methods, which they will save the file in the `output_dir`.
        """
        chrome = webdriver.Chrome('./chromedriver')
        self.df.apply(self.get_audio, axis=1, args=(chrome,))
        chrome.quit()

    def get_transcript(self, row, chrome):
        """
        For a given url it will create a list of transcripts and timestamps
        and it will write them as a `csv` file in the `output_dir`.
        """

        full_transcipt = []

        # Find the transcript element in the page and click on it
        chrome.find_element_by_xpath('//span[.="Transcript"]').click()
        sleep(0.2)

        # All the transcripts are stored in the div tag with the follwing
        # class names
        transcript = chrome.find_elements_by_xpath(
            '//div[contains(@class,"Grid Grid--with-gutter")]')

        # Iterate through all the elements and seperate the timestamp
        # from the text
        for t in transcript:
            splitted = t.text.split('\n')
            time = splitted[0]
            text = '\n'.join(splitted[1:])
            full_transcipt.append([time, text])

        # Convert the list into a Pandas' Dataframe and write it
        # in the `output_dir`.
        df = pd.DataFrame(full_transcipt, columns=['time', 'text'])
        df.to_csv(f'{self.output_dir}/{row.title}.csv', index=False)

    def get_audio(self, row, chrome):
        """
        Main method which downloads the audio files and its transcript
        from TedTalk's main website.
        """
        # Local variables
        url = row.link
        title = row.title

        # Open the page in chromium driver
        chrome.get(url)
        sleep(2)

        # First get the transcript and write it to the file
        get_transcript(row, chrome)

        # Find the share button, which contains the download button
        share = chrome.find_elements_by_xpath('//*[.="share" or . ="Share"]')

        # Sometimes the page generates multiple elements to make
        # it harder to scrape data. Therefore, find the element
        # that is clickable, and click on it.
        for e in share:
            try:
                e.click()
                break
            except:
                next

        # To be able to download the audio, first we must click on the
        # Download button and then the options for downloading come up.
        sleep(0.3)
        dl_elements = chrome.find_elements_by_xpath(
            '//*[.="Download" or .="download"]')

        # Similar to the share button, the website sometimes generate
        # elements to throw off scrapers.
        for e in dl_elements:
            try:
                e.click()
                break
            except:
                next
        sleep(0.1)

        # Some ted talks do not have audio file available for downloading
        # here I check if the `Download audio` button is available, if not
        # we delete the transcript, it is mostly here as a placeholder to
        # find a way to only download the audio from TedTalks if only the
        # video is available.
        download_audio = chrome.find_elements_by_xpath(
            '//a[.="Download audio" or .="download audio"]')
        if len(download_audio) == 0:
            # TODO: Figure out how to extract audio from videos
            os.remove(f'{self.output_dir}/{title}.csv')
            return

        # Get the downloadable link from the element and download
        # and write the file
        audio_file = requests.get(download_audio[0].get_attribute('href'))
        fname = f'{self.output_dir}/{title}.mp3'
        with open(fname, 'wb') as f:
            f.write(audio_file.content)
        f.close()

        # Print the title of the TedTalk.
        print(row.title)
