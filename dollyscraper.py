#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import sys

if (len(sys.argv) - 3) % 3 != 0:
    print("invalid number of arguments")
    exit()

options = Options()
options.headless = False
browser = webdriver.Firefox(options=options)

browser.get(sys.argv[3])

loginbtn = WebDriverWait(browser, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "btn-primary")))
loginbtn.click()

username = WebDriverWait(browser, 30).until(
    EC.presence_of_element_located((By.ID, "username")))
password = browser.find_element_by_id("password")

username.send_keys(sys.argv[1])
password.send_keys(sys.argv[2])
btn = browser.find_element_by_name("_eventId_proceed")
btn.click()

microsoft = WebDriverWait(browser, 30).until(
    EC.presence_of_element_located((By.ID, "idSIButton9")))
microsoft.click()

def Bibg(outputfile):
    months = {
        "gen" : "01",
        "feb" : "02",
        "mar" : "03",
        "apr" : "04",
        "mag" : "05",
        "giu" : "06",
        "lug" : "07",
        "ago" : "08",
        "set" : "09",
        "ott" : "10",
        "nov" : "11",
        "dic" : "12",
    }

    buttons = WebDriverWait(browser, 30).until(
        EC.presence_of_all_elements_located((By.XPATH, "//td[@class='cell c3 lastcol']/div/span/a[@class='action-icon btn-action text-truncate']")))

    titles = WebDriverWait(browser, 30).until(
        EC.presence_of_all_elements_located((By.XPATH, "//td[@class='cell c0']")))

    dates = browser.find_elements_by_xpath("//td[@class='cell c1']")

    i = 0
    for button in buttons:
        url = button.get_attribute("data-href")[313:]
        print(url)
        desk = "https://davy04.edunova.it/presentation/" + url + "/deskshare/deskshare.mp4"
        webcams = "https://davy04.edunova.it/presentation/" + url + "/video/webcams.mp4"

        desk = "\"" + desk + "\""
        webcams = "\"" + webcams + "\""
        day = dates[i].text[5:7]

        if day[1:2] == " ":
            base = 0
            day = "0" + day
            day = day[:2]
        else:
            base = 1

        mon = months[dates[i].text[base+7:base+10]]
        year = dates[i].text[base+11:base+15]
        hour = dates[i].text[base+17:base+19]
        human = "" + year + "_" + mon + "_" + day + "_" + hour + "_" + titles[i].text

        outputfile.write("wget -c -O \"" + human + ".desk.mp4\" -o \"" + human + ".desk.mp4.log\" " + desk + " &\n")
        outputfile.write("wget -c -O \"" + human + ".webcams.mp4\" -o \"" + human + ".webcams.mp4.log\" " + webcams + " &\n")
        print(human)
        i += 1

def Collaborate(outputfile):
    lessons = WebDriverWait(browser, 40).until(
        EC.presence_of_all_elements_located((By.XPATH, "//ul/li/div/div/div/div/a")))

    lasturlname = "lasturl.txt"
    try: # avoid loading the collaborate page if already downloaded
        lasturlfile = open(lasturlname, "r")
        lasturl = lasturlfile.read()[:-1] # remove newline
        print("last url: ", lasturl)
        lasturlfile.close()
    except:
        lasturl = ""

    urls = []
    humans = []
    go = False
    if len(lasturl) <= 1:
        go = True

    for lesson in lessons:
        try:
            if lesson.text[:1] == "[":
                url = lesson.get_attribute("onclick")[13:]
                url = url[:len(url) - 17]
                if go == True:
                    urls.append(url)
                    humans.append(lesson.text)
                else:
                    print(url, " already downloaded")
                    if url == lasturl:
                        go = True
        except:
            print("invalid link")

    i = 0
    for url in urls:
        print(url)
        try:
            browser.get(url)
            if browser.current_url.find("drive.google") != -1:
                print("skipped gdrive")
                raise ValueError('Gdrive videos cannot be downloaded')

            video = WebDriverWait(browser, 80).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))).get_attribute("src")
        except:
            print("doesn't collaborate")
            continue

        human = humans[i].replace("(", "[")
        if human[:11] == "[Esercizi] ":
            human = human[11:]
        human = human.replace(")", "]")
        human = human.replace("\'", "m")
        human = human.replace("\"", "s")

        human = human[7:11] + "-" + human[4:6] + "-" + human[1:3] + human[12:]
        print(human)
        outputfile.write("wget -c -O \"" + human + ".mp4\" -o \"" + human + ".mp4.log\" \"" + video + "\" &\n")
        i += 1

    if len(urls) > 0:
        lasturlfile = open(lasturlname, "w")
        lasturlfile.write(urls[len(urls) - 1])
        lasturlfile.close()

argcount = 3
while argcount < len(sys.argv):
    browser.get(sys.argv[argcount])
    print("\n", sys.argv[argcount + 1])
    outputfile = open(sys.argv[argcount + 1], "w")
    outputfile.write("#!/bin/sh\n")

    if sys.argv[argcount + 2] == "bigb":
        Bibg(outputfile)
    elif sys.argv[argcount + 2] == "collab":
        Collaborate(outputfile)
    else:
        print("available platforms: bigb collab")

    argcount += 3
    outputfile.close()

browser.close()
