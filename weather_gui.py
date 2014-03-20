import pywapi
import pygame

import weather_status
import os

from settings import ZIP_CODE

pygame.init()

MY_ZIP = ZIP_CODE

DISPLAY_SIZE = (896, 576)

GX = int(DISPLAY_SIZE[0] / 14) # Grid unit
GY = int(DISPLAY_SIZE[1] / 9) # Grid unit

TEXT_COLOR = (215, 215, 215)
BG_COLOR = (15, 15, 45)
RECT_COLOR = (45, 45, 90, 150)
FORECAST_BG_COLOR = (30, 30, 90)

PIC_PATH = "pics/weather"

time_font = pygame.font.SysFont("Arial", int(DISPLAY_SIZE[0] / 10))
subtime_font = pygame.font.SysFont("Arial", int(DISPLAY_SIZE[0] / 18))
forecast_head_font = pygame.font.SysFont("Arial", int(GX / 4))
forecast_temp_font = pygame.font.SysFont("Arial", int(GX / 3))

class WeatherScreen(pygame.Surface):
    code = None
    
    condition = None
    astronomy = None
    atmosphere = None
    forecasts = None
    wind = None

    display = None

    def __init__(self, dimension):
        pygame.Surface.__init__(self, dimension)
        #self.screen = pygame.display.set_mode((960, 720), pygame.FULLSCREEN)
        pygame.time.set_timer(pygame.USEREVENT+2, 10000)
        self.load_data()

    def load_data(self):
        data = pywapi.get_weather_from_yahoo(MY_ZIP)
        condition = data.get("condition")
        if condition:
            self.condition = condition
        self.astronomy = data.get("astronomy")
        self.atmosphere = data.get("atmosphere")
        self.forecasts = data.get("forecasts")
        self.wind = data.get("wind")
        print("Updated")
        return True

    def display(self, py_event):
        if py_event.type == pygame.USEREVENT+2:
            self.load_data()
        self.fill(BG_COLOR)

        self.draw_temp()
        self.draw_description()
        self.draw_forecast(0)
        self.draw_forecast(1)
        self.draw_forecast(2)
        self.draw_forecast(3)

    def draw_temp(self):
        temp = str(round(int(self.condition.get("temp")) * 1.8 + 32,1))
        loc = (GX, GY * 3)
        lbl_temp = time_font.render("{0}".format(temp), 1, TEXT_COLOR)
        w = lbl_temp.get_width()
        lbl_f = forecast_temp_font.render("*F", 1, TEXT_COLOR)
        self.blit(lbl_temp, loc)
        self.blit(lbl_f, (loc[0] + w, int(loc[1]*1.05)))
        
    def draw_forecast(self, index=0):
        forecast = self.forecasts[index]
        x = GX + 3 * GX * index
        y = GY * 6
        fc_surf = ForecastPanel((int(GX * 2.7), int(GY * 2.5)), forecast)
        self.blit(fc_surf, (x,y))

    def draw_description(self):
        code = int(self.condition.get("code"))
        loc = (GX * 4, GY * 3)
        desc = ""
        status = weather_status.statuses.get(code)
        if status:
            desc = status["title"]
        # desc = self.condition.get("text")
        lbl_desc = subtime_font.render(desc, 1, TEXT_COLOR)
        self.blit(lbl_desc, loc)


class ForecastPanel(pygame.Surface):
    code = None
    date = None
    day = None
    high = None
    low = None
    text = None
    h = None
    w = None

    def __init__(self, dimension, record):
        pygame.Surface.__init__(self, dimension)
        self.code = record.get("code")
        self.date = record.get("date")
        self.day = record.get("day")
        self.high = record.get("high")
        self.low = record.get("low")
        self.text = record.get("text")
        self.h = dimension[1]
        self.w = dimension[0]
        self.fill(BG_COLOR)
        #self.set_alpha(255)
        
        self.draw_rect()
        self.draw_date()
        self.draw_forecast_text()
        self.draw_high_temp()
        self.draw_image()
        self.draw_low_temp()

    def draw_image(self):
        status = weather_status.statuses[int(self.code)]
        img_name = status['file']
        filename = os.path.join(PIC_PATH, img_name)
        img = pygame.image.load(filename)
        self.blit(img, (0, 0))
        
    def draw_rect(self):
        dimens = [int(GX*0.3), int(GY*0.5), self.w - int(GX*0.3), GY * 2]
        pygame.draw.rect(self, RECT_COLOR, dimens)

    def draw_date(self):
        text = "{0}, {1} {2}".format(self.day, self.date.split(" ")[1], self.date.split(" ")[0])
        lbl = forecast_head_font.render(text, 1, TEXT_COLOR)
        self.blit(lbl, (int(GX * 1.0), int(GY * 0.08)))

    def draw_high_temp(self):
        text = "{0} *F".format(str(round(int(self.high) * 1.8 + 32, 1)))
        lbl = forecast_temp_font.render(text, 1, TEXT_COLOR)
        w = lbl.get_width()
        self.blit(lbl, (int(GX * 2.4 - w), int(GY * 0.6)))

    def draw_low_temp(self):
        text = "{0} *F".format(str(round(int(self.low) * 1.8 + 32, 1)))
        lbl = forecast_head_font.render(text, 1, TEXT_COLOR)
        w = lbl.get_width()
        self.blit(lbl, (int(GX * 2.3 - w), int(GY * 1.2)))

    def draw_forecast_text(self):
        text = "{0}".format(self.text)
        lbl = forecast_head_font.render(text, 1, TEXT_COLOR)
        self.blit(lbl, (int(GX * 0.4), int(GY * 1.8)))


