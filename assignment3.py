import argparse
import csv
import urllib.request
import io
import re
import datetime

# other imports go here





def downloadData(url):
    with urllib.request.urlopen(url) as response:
        response = response.read().decode("utf-8")
    return response


def processData(file):
    data = csv.reader(io.StringIO(file))

    # Set regex patterns to find
    filePattern = re.compile(r"\.(jpg|jpeg|gif|png)$", re.IGNORECASE)
    browserPattern = re.compile(
        r"(Firefox|MSIE|Trident|Chrome|Safari)", re.IGNORECASE
    )

    # Define variables needed: image hits, total hits, browser count obj
    imageHits = 0
    totalHits = 0
    browserCount = {"Firefox": 0, "Internet Explorer": 0, "Chrome": 0, "Safari": 0}

    # Define and initialize obj for tracking number of hits for each hour
    hitsByHour = {}
    for hour in range(24):
        hitsByHour[hour] = 0
    # Loop through all csv data
    for hit in data:

        # Find how many hits are images
        totalHits+=1
        if filePattern.search(hit[0]):
            imageHits+=1

        # Find which browser is used the most
        userAgentString = hit[2]
        browser = browserPattern.search(userAgentString).group()
        if browser == "Firefox":
            browser = "Firefox"
        elif browser == "MSIE" or browser == "Trident":
            browser = "Internet Explorer"
        elif browser == "Chrome":
            browser = "Chrome"
        elif browser == "Safari":
            browser = "Safari"
        browserCount[browser] += 1

        # Find how many hits each hour has
        hitDate = datetime.datetime.strptime(hit[1], "%Y-%m-%d %H:%M:%S")
        hitsByHour[hitDate.hour] +=1

    # Last calculations: percentage of hits that are images, getting the actual most popular browser, sort hits by hour
    imagePercentage = imageHits / totalHits * 100
    mostPopular = max(browserCount, key=browserCount.get)
    sortedHitsByHour = sorted(hitsByHour.items(), key=lambda i: i[1], reverse=True)

    # Print everything
    print(f"Image requests account for {imagePercentage}% of all requests")
    print(
        f"The most popular browser is {mostPopular} with {max(browserCount.values())} hits"
    )

    # Only print if the given hour has hits: personaly preference to keep console looking cleaner
    for hour in sortedHitsByHour:
        if hour[1]:
            print(f'Hour {hour[0]+1} has {hour[1]} hits')
    print('All the rest have 0 hits')

# THOUGHTS: I originally had separate functions for different processes eg to count the image
# hits and find out the most popular browser. I think that this more modular set up is better
# in that it is more reusable, but it ends up looping through all the data for every single function.
# Putting all the functionality in one process data function is more efficient for the assignment,
#  but is not as future proof or easily reusable.

# def countImageHits(data):
#     pattern = re.compile(r"\.(jpg|gif|png)$", re.IGNORECASE)
#     imageHits = 0
#     for hit in data:
#         if pattern.search(hit[0]):
#             imageHits += 1
#     imagePercentage = imageHits / len(data) * 100
#     print(f"Image requests account for {imagePercentage}% of all requests")


# def findPopularBrowser(data):
#     pattern = re.compile(
#         r"(Firefox|MSIE|Trident|Chrome|(?<!Chrome)Safari)", re.IGNORECASE
#     )
#     browserCount = {"Firefox": 0, "Internet Explorer": 0, "Chrome": 0, "Safari": 0}
#     for hit in data:
#         userAgentString = hit[2]
#         browser = pattern.search(userAgentString).group()
#         if browser == "Firefox":
#             browser = "Firefox"
#             browserCount[browser] += 1
#         elif browser == "MSIE" or browser == "Trident":
#             browser = "Internet Explorer"
#         elif browser == "Chrome":
#             browser = "Chrome"
#         elif browser == "Safari":
#             broswer = "Safari"
#         browserCount[browser] += 1

#     mostPopular = max(browserCount, key=browserCount.get)

#     print(
#         f"The most popular browser is {mostPopular} with {max(browserCount.values())} hits"
#     )


def main(url):
    print(f"Running main with URL = {url}...")
    file = downloadData(url)
    processData(file)


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
