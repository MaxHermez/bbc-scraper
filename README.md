# bbc-scraper
A containerized news articles collector. It scrapes the BBC website and stores the articles in a MongoDB database.

# Setup

This repo can either be ran locally or in a containerized environment.

## Running Locally

### Virutal Environment

Make sure you use **python3.11 or higher** to begin creating the virtual environment.

After cloning the repo, open a terminal and run the following commands:
```terminal
python3 -m venv venv
```
___

### Environment Variables
Define our environment variables for MongoDB, the files we need to adjust should exist in the `venv/bin` or the `venv/scripts` directory.

- if you are using bash, you should edit the `activate` file, add the following lines at the end of the file
```bash
export MONGO_URI=<your_mongo_uri>
export MONGO_DB=<your-db-name>
export MONGO_COL=<your-collection-name>
```
- if you are using windows command line, you should edit the `activate.bat` file, add the following lines at the end of the file
```terminal
set MONGO_URI=<your_mongo_uri>
set MONGO_DB=<your-db-name>
set MONGO_COL=<your-collection-name>
```
- if you are using powershell on windows, you should edit the `Activate.ps1` file, add the following lines at the end of the file
```powershell
$env:MONGO_URI=<your_mongo_uri>
$env:MONGO_DB=<your-db-name>
$env:MONGO_COL=<your-collection-name>
```
___
### Activating the venv
Activate the virtual environment: 

On Linux:
```terminal
source ./venv/bin/activate
```

On Windows:
```terminal
.\venv\Scripts\activate
```
___
### Installing Dependencies
Install the dependencies:
```terminal
pip install -r requirements.txt
```
If you face any errors try just installing the following packages
```terminal
pip install pymongo=3.11 scrapy dnspython
```
___
### Running the Scraper
To run the scraper, run the following command:
```terminal
scrapy crawl bbc_news
```
If you want to dump scrapy logs to file:
```terminal
scrapy crawl bbc_news -s LOG_FILE=bbc.log
```
___

## Running using Docker

### Environment Variables
Prepare your MongoDB connection URI before building the image, we will use it in the next step by passing it as an argument to the "build" command.

### Building the Image
To build the image, run the following command:
```terminal
docker build -t bbc-scraper . --build-arg MONGO_URI=<your_mongo_uri> --build-arg MONGO_DB=<your-db-name> --build-arg MONGO_COL=<your-collection-name>
```

### Running the Container
To run the container, run the following command:
```terminal
docker run -d -p 8000:8000 bbc-scraper
```
You can add the `--rm` flag to remove the container after it stops running.
```terminal
docker run -d --rm -p 8000:8000 bbc-scraper
```
```