from lib.repo.FileOperation import FileOperation


class MemoryRepository:


    __instance=None
    countries_and_cities={}
    settings={}
    suicide_rate={}
    co2_emission={}
    top_countries=[]
    city_weather={}



    def __init__(self):
        if MemoryRepository.__instance is None:

            MemoryRepository.__instance = self
            FileOperation().get_instance().memory_initializer(self)
            self.combine_top_all_data()
        else:
            raise Exception("MemoryRepository object exist.")

    @staticmethod
    def get_instance():
        if  MemoryRepository.__instance == None:
            __instance=MemoryRepository()

        return MemoryRepository.__instance


    def get_settings(self):
        return self.settings


    """FILTER TO SUICIDE RATE DUE TOP 50 COUNTRY"""
    def filter_top_suicide_rate(self):

        suicide_rate={}
        for item in self.suicide_rate.keys():
            if self.suicide_rate[item]['country'] in self.top_countries:
                suicide_rate[item]=self.suicide_rate[item]

        return suicide_rate

    """FILTER TO COUNTRY&CITY DICT DUE TOP 50 COUNTRY"""
    def filter_top_cities_country(self):

        cities={}
        for item in self.countries_and_cities.keys():
            if item in self.top_countries:
                cities[item]=self.countries_and_cities[item]


        return cities


    def combine_top_all_data(self):
        all_data={}
        suicide_rate=self.filter_top_suicide_rate()
        city_weather=self.city_weather
        for item in suicide_rate.keys():
            all_data[item]=suicide_rate[item]

            if item in city_weather.keys():
                for e in city_weather[item].keys():
                        all_data[item][e]=city_weather[item][e]

            if item in self.co2_emission.keys():
                for k in self.co2_emission[item].keys():
                    all_data[item][k]=self.co2_emission[item][k]

        return all_data



    def get_all_data_dataframe(self):
        return FileOperation.get_instance().read_all_data_dataframe(self)

