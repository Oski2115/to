import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
import requests

class IRate:
    def getName(self):
        pass

    def getCode(self):
        pass
    
    def getRate(self):
        pass

class Rate(IRate):
    def __init__(self, name, code, rate):
        self._name = name
        self._code = code
        self._rate = rate
    
    def getName(self):
        return self._name
    
    def getCode(self):
        return self._code
    
    def getRate(self):
        return self._rate
    
class IRateCollection(ABC):
    @abstractmethod
    def addRate(self, rate):
        pass

    @abstractmethod
    def findRate(self, code):
        pass

class RateCollection(IRateCollection):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RateCollection, cls).__new__(cls)
            cls._instance._rates = []
        return cls._instance 
    
    def addRate(self, rate):
        self._rates.append(rate)

    def findRate(self, code):
        for rate in self._rates:
            if rate.getCode() == code:
                return rate 
        return None

class Data:
    @staticmethod
    def extractDataFromAPI(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch data")

class Parser:
    def parseData(self, data):
        for item in data[0]['rates']:
            name = item['currency']
            code = item['code']
            rate = item['mid']
            newRate = Rate(name, code, rate)
            database = RateCollection()
            database.addRate(newRate)
        database.addRate(Rate('zloty', 'PLN', 1.0))

class Exchange:
    def Exchanger(self, base, target, amount):
        rates_database = RateCollection()

        baseElement = rates_database.findRate(base)
        baseRate = float(baseElement.getRate())
        
        targetElement = rates_database.findRate(target)
        targetRate = float(targetElement.getRate())

        return round(amount * (baseRate / targetRate), 2)
    
class Interface:
    def displayInterface(self):
        database = RateCollection()
        while True:
            baseRate = None
            targetRate = None
            amount = None
            
            while baseRate is None:
                baseRate = database.findRate(input('Podaj kod waluty źródłowej: ').upper())
                if baseRate is None:
                    print('Wprowadzono błędne dane')
            
            while amount is None:
                try:
                    amount  = float(input('Podaj kwotę: '))
                except ValueError:
                    print('Wprowadzono błędną kwotę')

            while targetRate is None:
                targetRate = database.findRate(input('Podaj kod waluty docelowej: ').upper())
                if targetRate is None:
                    print('Wprowadzono błędne dane')

            Exchanger = Exchange()
            exchangedAmount = Exchanger.Exchanger(baseRate.getCode(), targetRate.getCode(), amount)
            print(f'Przewalutowano {amount} {baseRate.getCode()} na {exchangedAmount} {targetRate.getCode()}')

url = 'https://api.nbp.pl/api/exchangerates/tables/a/'
data = Data.extractDataFromAPI(url)
Parser().parseData(data)
Interface().displayInterface()
