# coding: utf-8
#
# Licence : MIT Licence
# owner   : Fumiya Shibamata
# web     : https://github.com/sbfm/getChromeWebDriver
#
import os
import re
import zipfile
import ConfigController
import urllib.request
from lxml import html

class getChromeWebDriver :
    """Auto update web driver
    
    you must pip lxml.
    
    * sampleCode
    import getChromeWebDriver
    getDriver = getChromeWebDriver.getChromeWebDriver()
    getDriver.setTempDirectory("temp/") :
    getDriver.upCheckChromeDriver("DrivwrPath")
    """
    
    def __init__(self,configFileName = "config.ini"):
        """constructor
        
        You can set the name of the config file
        If you do not set, an "config.ini" will be set
        
        * argument1
        no set argument 
        
        * argument2
        [0] configFileName
        """
        
        self.configName = configFileName
            
        ccini = ConfigController.ConfigController(self.configName)
        ccini.setSection("getChromeWebDriver")
        # localChromeDriverVersion ( You don't need to set )
        self.localChromeDVersion = ccini.getProperties("localChromeDVersion","1")
        # Chrome ApplicationFolder Path
        self.chromePath         = ccini.getProperties("chromePath","C:\Program Files (x86)\Google\Chrome\Application")
        # temp Directory
        self.tempDirectory      = ccini.getProperties("tempDirectory","")
        # Use Proxy Flag
        self.useProxy           = ccini.getProperties("useProxy","false")
        # httpProxy
        self.httpProxy          = ccini.getProperties("httpProxy","")
        # httpsProxy
        self.httpsProxy         = ccini.getProperties("httpsProxy","")

    # ---------------------
    # setter
    # ---------------------
    # Use when setting from Program
    #
    # * argument1
    # [0] value
    #
    def setChromePath(self, setValue) :
        self.chromePath = setValue
        return 1
    def setChromePath(self, setValue) :
        self.chromePath = setValue
        return 1
    def setTempDirectory(self, setValue) :
        self.tempDirectory = setValue
        return 1
    def setUseProxy(self, setValue) :
        self.useProxy = setValue
        return 1
    def setHttpProxy(self, setValue) :
        self.httpProxy = setValue
        return 1
    def setHttpsProxy(self, setValue) :
        self.httpsProxy = setValue
        return 1

    def checkLocalChromeVersion(self) :
        """check Chrome Version (for Windows) 
        
        check local Chrome Browser Version
        """
        # get CromeApplicationFolderTree
        files = os.listdir(self.chromePath)
        # Collect directories only
        filesDir = [f for f in files if os.path.isdir(os.path.join(self.chromePath, f))]
        
        # get lastest Version
        version = 0
        for folder in filesDir :
            # get Major Version
            filePattern = re.compile(r'([0-9]+(?=\.))')
            result = filePattern.match(folder)
            if result:
                version = max(version,int(result.group()))
        
        # can't get Chrome Version return 0
        return version
    
    def checkLocalChromeDriverVersion(self) :
        """check Chrome Version
        """
        return self.localChromeDVersion
    
    def checkLatestChromeDriverVersion(self, localChromeVersion) :
        """get chromeDriver Address for match local chrome version
        """
        # if 
        if self.useProxy == "true" :
            os.environ["http_proxy"] = self.httpProxy
            os.environ["https_proxy"] = self.httpsProxy
        
        url = 'https://chromedriver.chromium.org/downloads'
        try:
            with urllib.request.urlopen(url) as f:
                htmltext = f.read().decode('utf-8')
        except URLError as e:
            print("error")
        
        #debug
        #print(htmltext.replace('\xa0', ''))
        
        title = html.fromstring(htmltext).xpath("//table[@class='sites-layout-name-one-column sites-layout-hbox']/tbody//ul")
        # Full Path from 2019/11/20 
        # //table[@class='sites-layout-name-one-column sites-layout-hbox']/tbody/tr/td/div/div/ul/li
        #
        # getLinkTitle
        #aaa = title[0].xpath("span")
        # getLing
        chromeDriverVersionList = title[0].xpath("li")
        
        mi = "0"
        for version in chromeDriverVersionList :
            ccc = version.xpath("a")
            # DriverVersionAll...............................
            if(len(ccc)==0):
                continue
            chromeDriverStatus = ccc[0].text
            m = re.search('(?<=ChromeDriver )[0-9]*', chromeDriverStatus)
            if(str(m.group()) == str(localChromeVersion)) :
                versionOfMajor = re.search('(?<=ChromeDriver ).*', chromeDriverStatus)
                mi = str(versionOfMajor.group())
        if mi == "0":
            # no match ////////////////////////////////////
            print("No Match Chrome Driver Version")
            return 0
        return mi
        
    def upCheckChromeDriver(self, chromeDriverDirectory) :
        """check chromeDriver Version
        """
        localversion = self.checkLocalChromeVersion()
        if localversion == int(self.localChromeDVersion) : 
            # ///////////////////////////////
            print("end")
            return 1
        
        fna = self.checkLatestChromeDriverVersion(localversion)
        if fna == 0 :
            print("miss")
            return 0
        furl = "https://chromedriver.storage.googleapis.com/" + fna + "/chromedriver_win32.zip"
        urllib.request.urlretrieve(furl, self.tempDirectory + "howa1.zip")
        with zipfile.ZipFile(self.tempDirectory + 'howa1.zip') as zipF:
            zipF.extractall(chromeDriverDirectory)

        majorVersion = re.search('^[0-9]*', fna)
        ccini = ConfigController.ConfigController(self.configName)
        ccini.setProperties("getChromeWebDriver", "localChromeDVersion", majorVersion.group())
        print("end")

#debugCode
#aaa = getChromeWebDriver()
#aaa.upCheckChromeDriver("")

