import argparse
import csv
import urllib.request
import io
import re

# other imports go here


def getData(url):
    response = urllib.request.urlopen(url)
    lines = [l.decode("utf-8") for l in response.readlines()]
    cr = csv.reader(lines)

    for row in cr:
        print(row)


def downloadData(url):
    with urllib.request.urlopen(url) as response:
        response = response.read().decode("utf-8")
    return response


def processData(file):
    data = csv.reader(io.StringIO(file))
    return list(data)


def countImageHits(data):
    pattern = re.compile(r"\.(jpg|gif|png)$", re.IGNORECASE)
    imageHits = 0
    for hit in data:
        if pattern.search(hit[0]):
            imageHits += 1
    imagePercentage = imageHits / len(data) * 100
    print(f"Image requests account for {imagePercentage}% of all requests")


def findPopularBrowser(data):
    pattern = re.compile(
        r"(Firefox|MSIE|Trident|Chrome|(?<!Chrome)Safari)", re.IGNORECASE
    )
    browserCount = {"Firefox": 0, "Internet Explorer": 0, "Chrome": 0, "Safari": 0}
    for hit in data:
        userAgentString = hit[2]
        browser = pattern.search(userAgentString).group()
        if browser == "Firefox":
            browser = "Firefox"
            browserCount[browser] += 1
        elif browser == "MSIE" or browser == "Trident":
            browser = "Internet Explorer"
        elif browser == "Chrome":
            browser = "Chrome"
        elif browser == "Safari":
            broswer = "Safari"
        browserCount[browser] += 1

    mostPopular = max(browserCount, key=browserCount.get)

    print(
        f"The most popular browser is {mostPopular} with {max(browserCount.values())} hits"
    )


def main(url):
    print(f"Running main with URL = {url}...")
    file = downloadData(url)
    data = processData(file)
    countImageHits(data)
    findPopularBrowser(data)


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
