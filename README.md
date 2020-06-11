# GenericWebCrawlerPrototype

This repository contains the code for the prototype of webcrawler for P3MI e-Democracy Data Integration project.


## Getting Started

### Prerequisites

What things you need to install the software and how to install them

```
python3
pip
virtualenv  --  you may skip this if you prefer to use your global pip executable
```

### Installing

A step by step series of examples that tell you how to get a development env running

1. Create virtualenv and using it

    ```
    virtualenv venv
    . venv/bin/activate
    ```
    
    For Windows users, 
    
    ```
    virtualenv venv
    venv\Scripts\activate
    ```

2. Installing all needed package

    ```
    pip install -r requirements.txt
    ```


### Selenium set up

#### Chromium Driver
Selenium requires a driver to interface with the chosen browser. Chrome, for example, requires **chromium**, which needs to be installed before the below examples can be run. Make sure it’s in your PATH, e. g., 
1. for Ubuntu / Linux,place it in `/usr/bin` or `/usr/local/bin`.
2. for Windows, add this chromium to environment variable path.


Failure to observe this step will give you an error selenium.common.exceptions.WebDriverException: Message: ‘chromium’ executable needs to be in PATH.

As this project is developed using Chromium driver, Chromium download link is as follow.

| Web Browser   | Link                                                                  |
|:-------------:|:---------------------------------------------------------------------:| 
| Chrome:       |	https://sites.google.com/a/chromium.org/chromedriver/downloads      |


#### Downloading Selenium server
> ~**NOTE**~
>
> **The Selenium server is only required if you want to use the remote WebDriver.** See the Using Selenium with remote WebDriver section for more details. If you are a beginner learning Selenium, you can skip this section.

Selenium server is a Java program. Java Runtime Environment (JRE) 1.6 or newer version is recommended to run Selenium server.

You can download Selenium server 2.x from the download page of selenium website. The file name should be something like this: `selenium-server-standalone-2.x.x.jar`. You can always download the latest 2.x version of Selenium server.

If Java Runtime Environment (JRE) is not installed in your system, you can download the JRE from the Oracle website. If you are using a GNU/Linux system and have root access in your system, you can also use your operating system instructions to install JRE.

If java command is available in the PATH (environment variable), you can start the Selenium server using this command:
```
java -jar selenium-server-standalone-2.x.x.jar
```
Replace 2.x.x with the actual version of Selenium server you downloaded from the site.

If JRE is installed as a non-root user and/or if it is not available in the PATH (environment variable), you can type the relative or absolute path to the java command. Similarly, you can provide a relative or absolute path to Selenium server jar file. Then, the command will look something like this:
```
/path/to/java -jar /path/to/selenium-server-standalone-2.x.x.jar
```


### Running the Project

To try the demo, run the following script:
```bash
$ MONGODB_URI=<MongoDB URI> python crawl.py
```

Replace `MONGODB_URI` with actual connection parameter, e.g. `mongodb://localhost:27017/`.

If `MONGODB_URI` isn't provided, default goes to `mongodb://localhost:27017/` 


## Develop the Project
If you want to add another Parser Class, proceed to folder `./genericWebCrawler/genericWebCrawler/parsers`. Be sure to add item instance / model in folder `./genericWebCrawler/genericWebCrawler/items.py` and register in `./genericWebCrawler/genericWebCrawler/settings.py` for the relevant pipeline in folder `./genericWebCrawler/genericWebCrawler/pipelines.py`.

Seek for **Scrapy** Documentation to have a better understanding.

For the Parser with no specific class, it will be treated as Generic Class Parser.
