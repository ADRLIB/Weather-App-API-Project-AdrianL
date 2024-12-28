# coding: utf-8
"""
Citations and acknowledgments:
* API from openweathermap.org, Supplier of Achilles UVDB community
"""

import requests
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox 
from PIL import Image, ImageTk 
import ttkbootstrap

# creating api key and getting user input
api_key = '...' #your own api key from openweathermap.org

def temp_3_major_cities():
    """ Function that collects temperatures information for 3 major cities: Mexico city, Delhi, Tokyo
    Paramaters: None 
    Returns: 
        temp_of_cities: list -temperature of 3 cities
        cities_list: tuple -3cities
        
    """
    temp_of_cities = []
    cities_list = ('Mexico City', 'Delhi', 'Tokyo')
    
    for city in cities_list:
        current_cities_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}")
        cities_data = current_cities_data.json()
        temp_of_cities.append(cities_data['main']['temp'])
    return temp_of_cities, cities_list

def current_weather_information(city):
    """ Function that collects the current weather information for the city the user has input

    Parameters: city (str) a city you input
    Return: 
        None: returns a message if incorrect city is input
        icon_id: ---
        current_weather_description: string - descriptition of weather of city
        current_temp: float - temperature for city
        current_humidity: integer - humidity for city 
        icon_url: --
        Country: string - country of city 
            
    """
    #accessing the current date for the city you input
    current_weather_info = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}")

    #
    if current_weather_info.status_code != 200:
        messagebox.showerror("Error", f"Error fetching data for {city}")
        return None
    
    current_data = current_weather_info.json()
    icon_id = current_data['weather'][0]['icon']
    current_weather = current_data['weather'][0]['main']
    current_weather_description = current_data['weather'][0]['description']
    current_temp = round(current_data['main']['temp'])
    current_humidity = current_data['main']['humidity']
    country = current_data['sys']['country']


    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_id, current_weather, current_weather_description, current_temp, current_humidity, icon_url, country)
    
    
def weather_forecast_5Days_graph(city):
    """ Function that creates a graph of future weather 
        forecast using future_data. Up to 5 days in advance
        
    Paramaters: None
    Return: None 
    """
    future_weather_info = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=imperial&appid={api_key}")
    
    if future_weather_info.status_code != 200:
        messagebox.showerror("Error", f"Error fetching data for {city}")
        return None

    future_data = future_weather_info.json()
    future_temp = []
    list_of_dates = []
    for items in range(len(future_data['list'])):
        dates = future_data['list'][items]['dt_txt']
        temperature = future_data['list'][items]['main']['temp']
        list_of_dates.append(dates)
        future_temp.append(temperature)
    list_of_only_dates = []
    # This line of code is eliminating the timestamp to make the graph more clear
    for index in list_of_dates:
        date_only = index.split()[0]
        list_of_only_dates.append(date_only)
        
    plt.plot(list_of_only_dates[::8], future_temp[::8])
    plt.xlabel('Dates')
    plt.ylabel('Temperature')
    plt.title('Forecast of Weather: 5 days in advanced')
    plt.show()

    
    
def search():
    """ Function gets user input and calls both of the functions above
    weather_forecast_5Days_graph and current_weather_information 
    also formats them into text so that the graphics can properly display information
    ****weather_forecast_5Days_graph was not able to be in the display graphics***
    """
    city = city_input.get()
    result = current_weather_information(city)
    cities = temp_3_major_cities()
    if result is None:
        messagebox.showerror("Error", f"Invalid city: {city}")
        return

    icon_id, current_weather, current_weather_description, current_temp, current_humidity, icon_url, country = result
    cities_list,temp_of_cities = cities
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon
    
    location_label.configure(text=f'{city},{country}')
    temp_label.configure(text=f"Temperature: {current_temp:.2f} F")
    descr_label.configure(text=f"Description: {current_weather_description}")
    humid_label.configure(text=f"Humidty: {current_humidity}")
    big_city_label.configure(text=f"Weather In Other Major Cities: {temp_of_cities[0]} is {cities_list[0]}, {temp_of_cities[1]} is {cities_list[1]}, {temp_of_cities[2]} is {cities_list[2]}")
    weather_forecast_5Days_graph(city)



# Setting Windows and Title                        
root = ttkbootstrap.Window(themename='darkly')
root.title('Weather Application')
root.geometry('600x450')
#Entry Tool
city_input = ttkbootstrap.Entry(root,font='Times,18')
city_input.pack(pady=10)
# Confirm Entry
search_button = ttkbootstrap.Button(root,text='Search', command = search, bootstyle='warning')
search_button.pack(pady=10)
#Location Label
location_label = tk.Label(root, font='Times,25')
location_label.pack(pady=20)
#Icon Image
icon_label = tk.Label(root)
icon_label.pack()
#Temp Label
temp_label = tk.Label(root,font='Times,20')
temp_label.pack()
# Description
descr_label = tk.Label(root,font='Times,20')
descr_label.pack()
# Humidty
humid_label = tk.Label(root,font='Times,20')
humid_label.pack()
#label for major cities
big_city_label = tk.Label(root,font="Times,20")
big_city_label.pack(pady=10)
#show
root.mainloop()

# gaining access to future weather information as well as getting user_input
user_input = city_input.get()
current_weather_info = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}")
future_weather_info = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={user_input}&units=imperial&appid={api_key}")


