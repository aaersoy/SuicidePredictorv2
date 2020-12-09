import codecs
import csv
import json
import os
from pathlib import Path
import pandas as pd

class FileOperation:
    __instance = None
    __settings_path = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)+"\\Settings.json"

    def __init__(self):
        if FileOperation.__instance is None:
            FileOperation.__instance = self
        else:
            raise Exception("FileOperation object exist.")

    @staticmethod
    def get_instance():
        if not FileOperation.__instance:
            __instance = FileOperation()
        return FileOperation.__instance



    """MEMORY REPOSITORY OBJECT IS PASSED AS passed_obj"""

    def memory_initializer(self, passed_obj):

        self.read_settings(passed_obj)
        self.read_top_countries(passed_obj)
        self.read_cities_countries(passed_obj)
        self.read_suicide_rate(passed_obj)
        self.read_co2_emission(passed_obj)
        self.read_city_weather(passed_obj)
        self.write_all_data(passed_obj)


    def check_value(self,passed_obj):
        items={}

        #1985-2016
        for i in range(1980,2020):
            items[i]=0
        for item in passed_obj.__suicide_rate.keys():

            print(int(passed_obj.__suicide_rate[item]['year']))
            items[int(passed_obj.__suicide_rate[item]['year'])]=items[int(passed_obj.__suicide_rate[item]['year'])]+1
        print(items)


    """CAPITAL CITY OF COUNTRIES ARE READED"""

    def read_cities_countries(self, passed_obj):
        ret_dict = dict()
        len_file = 0
        settings=passed_obj.get_settings()
        with open(settings["CITY AND COUNTRIES"]) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if len_file > 0:
                    if row[1]!="N/A":
                        ret_dict[row[0]] = row[1]
                len_file = len_file + 1
        passed_obj.countries_and_cities = ret_dict


    """READ SETTING FILE"""

    def read_settings(self, passed_obj):

        if len(passed_obj.get_settings()) ==0:
            with open(self.__settings_path, 'r', encoding='utf8') as wf:
                passed_obj.settings = json.loads(wf.read())

    """READ SUICIDE RATE FILE"""
    def read_suicide_rate(self,passed_obj):
        settings = passed_obj.get_settings()
        with open(settings['SUICIDE RATE'], 'r', encoding='utf8') as wf:
            passed_obj.suicide_rate = json.loads(wf.read())


    """READ CO2 EMISSION FILE"""

    def read_co2_emission(self,passed_obj):
        csv_list = list()
        ret_dict=dict()
        settings = passed_obj.get_settings()
        with open(settings["CO2 EMISSION"]) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for item in csv_reader:
                csv_list.append(item)

            csv_list.pop(0)

        for item in csv_list:
            if (item[0]+item[2]) in passed_obj.suicide_rate.keys():
                ret_dict[item[0]+item[2]]=dict()
                ret_dict[item[0]+item[2]]["co2 emission"]=float(item[3])
        passed_obj.co2_emission=ret_dict
        with codecs.open("co2_emission.json", 'w', encoding='utf8') as wf:
            json.dump(passed_obj.co2_emission, wf, ensure_ascii=False)


    """READ COUNTRIES FILE"""

    def read_top_countries(self,passed_obj):
        settings=passed_obj.get_settings()
        csv_list = list()
        with open(settings["COUNTRIES"]) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for item in csv_reader:
                csv_list.append(item[0])

            csv_list.pop(0)
        passed_obj.top_countries=csv_list;

    """TRANSFORM SUICIDE RATE FILE TO JSON"""

    def suicide_rates_to_json(self,passed_obj):
        ret_dict = dict()
        csv_list=list()
        len_file = 0
        min_year=2025
        max_year=1900
        with open(passed_obj.__settings["SUICIDE DETAILED"]) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for item in csv_reader:
                csv_list.append(item)


            csv_list.pop(0)
            for row in csv_list:

                will_check_variable=row[7]
                ret_dict[will_check_variable]=dict()
                ret_dict[will_check_variable]['country']=row[0]



                ret_dict[will_check_variable]['year']=row[1]
                ret_dict[will_check_variable]['suicide no'] = 0
                ret_dict[will_check_variable]['population'] = 0
                ret_dict[will_check_variable]['gdp_per_capita']=int(row[10])

                for row_temp in csv_list:
                    if row_temp[7]==will_check_variable:

                        ret_dict[will_check_variable]['suicide no']=ret_dict[will_check_variable]['suicide no']\
                                                                    +int(row_temp[4])
                        ret_dict[will_check_variable]['population']=ret_dict[will_check_variable]['population']\
                                                                    +int(row_temp[5])

                        len_file=len_file+1

                ret_dict[will_check_variable]['suicides/100k pop']= float(format(100000 * (ret_dict[will_check_variable]['suicide no'])/(int(ret_dict[will_check_variable]['population'])+1),".2f"))
                print(ret_dict[will_check_variable]['suicides/100k pop'])

        passed_obj.__all_data = ret_dict
        with codecs.open("suicide_rate.json", 'w', encoding='utf8') as wf:
            json.dump(passed_obj.suicide_rate, wf, ensure_ascii=False)
        print(passed_obj.suicide_rate)


    """READ CITY WEATHER DATA"""

    def read_city_weather(self,passed_obj):
        weathers=dict()
        settings=passed_obj.get_settings()
        for file in (passed_obj.filter_top_cities_country()).values():
            with open(settings["CITIES WEATHER PATH"]+file+".csv",encoding="utf8") as csv_file:

                for e in passed_obj.countries_and_cities.keys():
                    if file == passed_obj.countries_and_cities[e]:
                        country_name=e
                        break

                csv_reader=csv.reader(csv_file,delimiter=',')
                list=next(csv_reader)
                for item in csv_reader:

                    weathers[country_name +item[1][0:4]]=dict()
                    weathers[country_name+ item[1][0:4]][list[0]]=file
                    weathers[country_name+ item[1][0:4]][list[1]]=item[1][0:4]

                    i = 2
                    while i<len(list):
                        weathers[country_name+ item[1][0:4]][list[i]]=item[i]
                        i=i+1

        passed_obj.city_weather=weathers



    """WRITE TO ALL DATA OF TOP 50"""

    def write_all_data(self,passed_obj):
        settings=passed_obj.get_settings()

        with codecs.open(settings['ALL DATA PATH']+"all_data.json", 'w', encoding='utf8') as wf:
            json.dump(passed_obj.combine_top_all_data(), wf, ensure_ascii=False)


    def read_all_data_dataframe(self,passed_obj):
        settings=passed_obj.get_settings()
        dataframe = pd.read_csv(settings['ALL DATA CSV PATH'])


        return dataframe



