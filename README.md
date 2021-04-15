# Dollyscraper

Downloads lessons recorded with BigBlueButton or Collaborate from
dolly.fim.unimore using web scraping.

## Dependencies

python and selenium:

```bash
pip3 install selenium
```

Wget, Firefox and [geckodriver](https://github.com/mozilla/geckodriver/releases)

## Usage

```bash
python dollyscraper.py <user> <password> <url1> </path/to/outputfile1> (bigb|collab) <url2> </path/to/outputfile2> (bigb|collab) ...
sh </path/to/outputfile1>
sh </path/to/outputfile2> ...
```

Your dolly credentials must be given as first 2 parameters. <url> is the page of
the class with the links to the recordings, bigb and Collaborate are the
available platforms where videos can be downloaded from.

<outputfile> is a POSIX shell script generated by ``dollyscraper.py`` which uses
wget to actually download the videos (wget is called with the --continue option,
which prevents re-downloading). This allows to download videos without a
browser, edit the script afterwards and facilitates testing.

``dollyscraper.py`` generates ``lasturl.txt``, which contains the url of the
last available lesson. It will prevent useless requests to Collaborate the next
time new lessons will be downloaded. With bigb this is not necessary.

To see the download progess of the output script run this on the same directory:

```bash
tail -n 2 *.mp4.log
```
