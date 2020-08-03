# Short introduction

Current implementation only works with the [TED talks](https://www.ted.com/) website.

With this implmentation and working with talks over 18 minutes (filter provided by the website) I could download 698 items (349 audio, transcript pairs). It took around 25 minutes to download the files and its approximately around 130 hours of transcripted audio.

# Usage

Before running, make sure you have requirements listed in the `requirements.txt` file. To do so, run the following command:

```
pip install -r requirements.txt
```

- Make sure `chromedriver` is in the directory you are running the program from.

1. To get started, have a csv file, which will have the following format:

|       title       |      link      |
| :---------------: | :------------: |
| Title of the talk | Ted Talk's url |

Sample data:

[tedtalk links 0-6mins.csv](/links/tedtalk%20links%200-6mins.csv)

2. Create an output folder
3. Run the following command:

```
python main.py [inputfile.csv] [output_dir] [number_of_threads]
```

Sample command:

```
python main.py /links/tedtalk links 18mins+.csv output 4
```

# 1,000+ hrs data

The `links` folder contains more urls for scrapping but I doubt there 1,000+ hrs content in there. To gather more, I wrote a small script for getting closed captions from Youtube. It will check if they're handwritten or automatically generated and uses a third-party to download audio.

The only problem with this approach is to find resources with reliable cc's, which most educational videos come with accurate closed captions (i.e. Khan Academy, Udacity and etc.). Another source of accurate transcripts is the famous speeches (i.e. campaign speeches, graduation speeches and etc.).

Timewise, it should take around 250 minutes (~4 hrs) since the process is quite similar, but can be sped up by increasing the threads or distributing the work over multiple devices.

To run it make sure you have `ffmpeg` installed and also have `youtube-dl` package installed for python.

Similarly you can run the code like this:

```
python youtube.py [youtube_video_id] [output_name]
```

`youtube video id` is the portion of the url that comes after `?v=`. So for example for the `https://www.youtube.com/watch?v=rhFK5_Nx9xY`, the video id is `rhFK5_Nx9xY`.

Sample command:

```
python youtube.py rhFK5_Nx9xY sample
```
