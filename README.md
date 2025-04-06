# ecom-clothing-pipeline

An ELT pipeline that scrapes data from an e-commerce clothing website.

## Objectives

This is a study case project designed to learn how to build ELT pipelines using data engineering frameworks and tools.  
The goal is to create a web scraper that extracts clothing data such as price, category, size, and more, loads it into a database, and transforms the data to be ready for use in a dashboard.

## What I’ve Learned from This Project

So far, I’ve learned the following:

- How to design and implement a web scraping process and architecture  
- How to set up Docker environments to run the project

## Installation
To set up the scraper environment follow the next instructions
1. Pip intall the dependecies
```shell
# Activate virtual environment
source venv/bin/activate # For Unix OS
venv/Scripts/activate # For Windows OS

pip install -r scraper_requirements.txt
```

2. Install the playwright browsers
```shell
playwright install

# For installing specific browsers
playwright install chromium firefox
```

## License

This project is licensed under the [MIT License](LICENSE).

You are free to use this code in any way, including for commercial purposes, as long as the license terms are respected.

⚠️ **Disclaimer**: This project was created for educational purposes. The author assumes no responsibility for any misuse, legal consequences, or damage resulting from its use. Always check the Terms of Service of any website you interact with.
