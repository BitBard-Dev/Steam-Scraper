# ISMG6020 PYTHON: PROJECT PHASE 1 DATA COLLECTION AND MONGODB
Table of Contents:
- Introduction
- Obstacles
- Step 1: Query the ISteam API to Determine Total Number of Valid Steam Apps
- Step 2: Remove Duplicate Steam App IDs from the list of Valid Steam Apps
- Step 3: Query Steam API to Pull All AppDetails for Each Steam App ID
- Step 4: Pull Game AppDetails from the steam_apps_grouped JSON File
    - Step 4a: Remove Documents with Duplicate App ID
- Step 5: Split JSON File Into Smaller Chunks (<16MB Each)
- Step 6: Batch Import All Chunked JSON Files Into Locally Hosted MongoDB Server
- Conclusion
- References
## Introduction
- This project seeks to scrape the entirety of Valve Corporation's Steam Marketplace to perform market analysis and trend analysis on possible growing markets
#### Process
- We first use Steam's GetAppList, filtering out any appid without a valid "title"
- We then take all those appid's and remove any duplicates
- We then query Steam's AppDetails API for each unique "steam_appid" value
- Because the produced JSON file is very large (~1.6GB), we must then split the file into chunks that will be accepted by MongoDB
- We then batch import the chunked JSON files
## Errors/Issues
- Failure to filter out duplicates in Step 2 led to a longer Step 4 and issues with filtering out duplicates in Step 4a
    - Failure to sort .csv file by ascending/descending appid led to semi-random query logic and lack of oversight
- Step 3 was started on 11FEB2025, but due to an unknown error, the program overwrote the .json file and started over at 0%. This lost ~20% of progress.
    - Step 3 restarted late on 13FEB2025. With regular backups, there are no further fears of not pulling the data. However, this step is **still** not complete prior to Stage 1 submission deadline.
    - Therefore, a backup v30.steam_games_grouped is used to demonstrate competency in Stage 1 tasks
- Step 4a led to a drop from ~118,000 games to 166 unique games. A clear issue as proven by the loss of data for known games.
## Step 1: Query the ISteam API to Determine Total Number of Valid Steam Apps
#### Details
- When connecting to the GetAppList API interface, there are numerous entries with an empty "title" string. These were filtered out in the below code.
- The list was saved to a .csv file due to the belief that the Steam API could more easily interact with the .csv instead of a .json file
## Step 2: Remove Duplicate Steam App IDs from the list of Valid Steam Apps
There are 233925 valid steam apps, quite a large dataset. Looking at the .csv file, reveals that there are many duplicate titles.
# **🚨PULL NEW SCREENSHOT🚨**
![image.png](attachment:c9ac1f4e-e3d6-49d1-ac54-adb5e4373a69.png)
#### This step removed over 60,000 duplicates!

#### At the Steam API rate limit, this saves over 25 hours in query time!
## Step 3: Query Steam API to Pull All AppDetails for Each Steam App ID
- Cell not run as it was run in a separate .ipynb file (due to long runtime)
#### Current State of Data
- At this point we only have "appid" and "title" for valid, non-duplicate Steam IDs.
- To filter out apps that aren't games (dlc, demo, etc.), we must query the appdetails API
- This query also pulls the other desired metrics for each Steam app
#### Estimated time to pull all data:
- Steam AppDetails API rate limit: 200 queries/5 minutes --> 2,400/hour
- Estimated time: 172,803/2,400 = ~72.0hours --> 3.0 days!!!
- 🚨🚨🚨Therefore program was automated using asyncio🚨🚨🚨
#### JSON Methodology
- 🚨🚨🚨JSON file is a dictionary of arrays for each "type" of steam app🚨🚨🚨
    - 🚨🚨🚨"game" apps are a separate array from "dlc" apps which are separate from "invalid" apps🚨🚨🚨
- 🚨🚨🚨This allows us to easily pull the "game" apps by simply reading the "game" array and writing it to a separate JSON file which will be uploaded to MongoDB🚨🚨🚨

#### 📊 Total games in JSON file: 96087
#### Total apps processed: 172803
#### Percentage complete: 100.00%
## Step 4: Ensure All Steam Apps Were Processed by Comparing steam_valid_apps_unique.csv and processed_apps.csv
#### All apps were successfully processed! We can now clean the data and incorporate more data from a 3rd party API SteamSpy
## Step 5: Clean steam_games_filtered.json Data to Remove Unnecessary Key-Value Pairs
#### This cleaning reduced the steam_games_filtered.json file from 1,356,846KB to 365,374KB.
#### This saves 991,472KB of memory! That's almost 1GB of data!
#### Our output also reveals that <u>there are only 96,087 games in the steam catalogue!</u> Though numerous, this is a far cry from the originally assessed 172,803 unique steam app IDs
## Step: 6: Clean the supported_languages Values for Follow-On Analysis
## Step 7: Query SteamSpy to Retrieve Tags Data & Add it To steam_games_cleaned_languages.json
#### At SteamSpy's rate limits of 1query/second, our full query should take ~26.7hours
#### Create .csv file of current games for tracking purposes
#### Query SteamSpy API, Save Data, and Ensure All Games are Queried


## References
Mongo Import Documentation Page:
- https://www.mongodb.com/docs/database-tools/mongoimport/

MongoDB Database Tools Installation Page:
- https://www.mongodb.com/docs/database-tools/installation/installation-windows/

Stack Overflow Post "Steam API all games" - Response by EliteRaceElephant 27JUN2020
- https://stackoverflow.com/questions/46330864/steam-api-all-games







