[![Actions Status](https://github.com/danokp/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/danokp/python-project-83/actions)
[![Github Actions Status](https://github.com/danokp/python-project-83/workflows/Python%20CI/badge.svg)](https://github.com/danokp/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/4f5146dc466b9b4fcddf/maintainability)](https://codeclimate.com/github/danokp/python-project-83/maintainability)

# Page Analyzer

Want to check your website for SEO suitability? Use [Page Analyzer](https://python-project-83-production-bcc2.up.railway.app/)!
## Installation
To download and install this project use the following commands:
```bash
git clone git@github.com:danokp/seo-page-analyzer.git
cd seo-page-analyzer
```
## Usage

Run application on your computer using one following options:
- Docker 
- Virtual environment using Poetry

1. __Docker__

1.1. Run the application:
```bash
docker compose up
```
1.2. Open the application in web browser at [http://localhost:8000](http://localhost:8000).

2. __Virtual environment using Poetry__

2.1. Run the application:
```bash
make install # Install all needed dependencies.
make local_start
```
2.2. Open the application in web browser at [http://localhost:5000](http://localhost:5000).
3. Enter the URL you want to analyze and click **CHECK** button. The URL will be aded into websites' database.
4. On the opened paged you can see results of all completed checks and run another one with use of **START CHECKING** button.

