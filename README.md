# GenericWebCrawlerPrototype

This repository contains the code for the prototype of webcrawler for P3MI e-Democracy Data Integration project.

To try the demo, run the following script:
```bash
$ MONGODB_URI=<MongoDB URI> python crawl.py
```
Replace `MongoDB URI` with actual connection parameter, e.g. `mongodb://localhost:27017/`


### Selenium set up
#### Drivers
Selenium requires a driver to interface with the chosen browser. Firefox, for example, requires geckodriver, which needs to be installed before the below examples can be run. Make sure it’s in your PATH, e. g., place it in /usr/bin or /usr/local/bin.

Failure to observe this step will give you an error selenium.common.exceptions.WebDriverException: Message: ‘geckodriver’ executable needs to be in PATH.

Other supported browsers will have their own drivers available. Links to some of the more popular browser drivers follow.

| Web Browser   | Link                                                                  |
|:-------------:|:---------------------------------------------------------------------:| 
| Chrome:       |	https://sites.google.com/a/chromium.org/chromedriver/downloads      |
| Edge:         | https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ |
| Firefox:      | https://github.com/mozilla/geckodriver/releases                       |
| Safari:       |	https://webkit.org/blog/6900/webdriver-support-in-safari-10/        |
 
#### Detailed instructions for Windows users
1. Install Python 3.6 using the MSI available in python.org download page.
2. Start a command prompt using the cmd.exe program and run the pip command as given below to install selenium.
    ```
    C:\Python35\Scripts\pip.exe install selenium
    ```
    
Now you can run your test scripts using Python. For example, if you have created a Selenium based script and saved it inside C:\my_selenium_script.py, you can run it like this:
```
C:\Python35\python.exe C:\my_selenium_script.py
```

#### Downloading Selenium server
> Note
>
> **The Selenium server is only required if you want to use the remote WebDriver.** See the Using Selenium with remote WebDriver section for more details. If you are a beginner learning Selenium, you can skip this section and proceed with next chapter.

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
