from time import sleep
import youtube_dl
import selenium.webdriver as driver
import sys
import warnings
import pandas as pd


def get_transcript(yt_url, output_loc):
    """
    Given a youtube video id, it will get it's transcript.
    """

    # Setting up the driver
    chrome = driver.Chrome('./chromedriver')
    chrome.get(f'https://youtube.com/watch?v={yt_url}')
    sleep(1.5)

    # Opening up the transcript menu
    more_action_button = chrome.find_elements_by_xpath(
        "//button[@aria-label='More actions'\
            and @class='style-scope yt-icon-button']")
    for e in more_action_button:
        try:
            e.click()
            break
        except:
            next
    sleep(0.2)
    open_transcript = chrome.find_elements_by_xpath(
        '//yt-formatted-string[. = "Open transcript"]')
    for e in open_transcript:
        try:
            e.click()
            break
        except:
            next

    # Generate a warning if the transcript is automatically generated
    try:
        sleep(2)
        langs = chrome.find_elements_by_xpath(
            '//div[@id="label-text" and @class="style-scope yt-dropdown-menu" \
                and .= "English (auto-generated)"]')
        if len(langs) == 1:
            warnings.warn('The captions are not user generated')
    except:
        pass

    # Get the transcript and put it in a dataframe
    transcripts = chrome.find_elements_by_xpath(
        '//div[@class = "cue-group style-scope ytd-transcript-body-renderer"]')
    transcript = []
    for t in transcripts:
        transcript.append(t.text.split('\n'))
    df = pd.DataFrame(transcript, columns=['time', 'text'])

    # Write it to the file
    df.to_csv(os.path.join(output_loc, 'transcript.csv'), index=False)
    chrome.quit()


def main(yt_url, output_loc):
    """
    Given a youtube video id, it will download its audio and saves it
    int `output_loc`.
    """

    # Options for the youtube-dl
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_loc}/audio.mp3'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f'https://youtube.com/watch?v={yt_url}'])
    get_transcript(yt_url, output_loc)


if __name__ == "__main__":
    yt_url = sys.argv[1]
    output_loc = sys.argv[2]
    main(yt_url, output_loc)
