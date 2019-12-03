# coding: utf-8
#
# Licence : MIT Licence
# owner   : Fumiya Shibamata
#
import os
import configparser
#
# configparser wrapper class
# if there is no file or key, create it
#
# How to Use
# [sample code]
# import ConfigController as cc
# cini = cc.ConfigController('config.ini')
# value = cini.getProperties("Application","setting","defaultValue")
#
# [sample code2]
# import ConfigController as cc
# cini = cc.ConfigController('config.ini')
# cini.setSection("Application")
# value = cini.getProperties("setting","defaultValue")

class ConfigController:
    config_ini = configparser.ConfigParser()
    # -------------------------
    # constructor
    # -------------------------
    def __init__(self,configFilePath):
        # check has property file
        if not os.path.exists(configFilePath):
            # if property file is null make file
            f = open(configFilePath, "w")
            f.close()
        # read property file
        self.configFile = configFilePath
        self.config_ini.read(configFilePath, encoding='utf-8')
    
    # ------------------------
    # set section
    # ------------------------
    # this logic don't must use
    # if you set a section, you will not need to set a section anymore.
    #
    # * argument
    # [0] section name
    #
    def setSection(self,asg):
        self.sectionName = asg
        return 1
    
    # ------------------------
    # get property value
    # ------------------------
    # If there is no value, a default is registered.
    #
    # * argument(Use setSection() in advance)
    # [0] properties name
    # [1] default value
    #
    # * argument2
    # [0] section name
    # [1] properties name
    # [2] default value
    #
    def getProperties(self,*properties):
        if len(properties) == 2 :
            # set 2 arguments
            try :
                sectionName = self.sectionName
            except AttributeError as e:
                print("error")
                return 0
            
            propertiesName = properties[0]
            defaultValue = properties[1]
        elif len(properties) == 3 :
            # set 3 arguments
            sectionName = properties[0]
            propertiesName = properties[1]
            defaultValue = properties[2]
        else :
            print("error")
            return 0
        # get properties.
        try :
            resultValue = self.config_ini[sectionName][propertiesName]
        except KeyError as e:
            self.setProperties(sectionName,propertiesName,defaultValue)
            resultValue = self.config_ini[sectionName][propertiesName]
        return resultValue

    # ------------------------
    # set properties Value
    # ------------------------
    # register properties
    #
    # * argument(Use setSection() in advance)
    # [0] properties name
    # [1] default value
    #
    # * argument2
    # [0] section name
    # [1] properties name
    # [2] default value
    #
    def setProperties(self,*properties):
        if len(properties) == 2 :
            # set 2 arguments
            try :
                sectionName = self.sectionName
            except AttributeError as e:
                print("Plese set section.")
                return 0
            propertiesName = properties[0]
            setValue = properties[1]
        elif len(properties) == 3 :
            # set 3 arguments
            sectionName = properties[0]
            propertiesName = properties[1]
            setValue = properties[2]
        else :
            print("error")
            return 0
        # check section
        self.hasSection(sectionName)
        # wright properties file
        self.config_ini.set(sectionName, propertiesName, setValue)
        with open(self.configFile, 'w') as file:
            self.config_ini.write(file)
        return 1

    # ------------------------
    # set section
    # ------------------------
    # 
    def hasSection(self,sectionName):
        if not(self.config_ini.has_section(sectionName)):
            self.config_ini.add_section(sectionName)
            with open(self.configFile, 'w') as file:
                self.config_ini.write(file)
        return 1
