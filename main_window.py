import pygame

pygame.init()

from weather_gui import WeatherScreen

DISPLAY_SIZE = (896, 576)

GX = int(DISPLAY_SIZE[0] / 14) # Grid unit
GY = int(DISPLAY_SIZE[1] / 9) # Grid unit

ROTATE_SCREENS = 30 # seconds

class MainWindow(pygame.Surface):
    current_window = None
    current_surface = None
    window_list = ["weather", "calendar", "gmail"]
    
    def __init__(self, dimension):
        pygame.Surface.__init__(self, dimension)
        self.dimension = dimension
        self.screen = pygame.display.set_mode(DISPLAY_SIZE)
        self.windows = {}
        self.current_surface = None
        self.current_window = None
        pygame.time.set_timer(pygame.USEREVENT+1, ROTATE_SCREENS * 1000)
        
    def display_weather(self, event):
        if self.current_surface is None:
            self.current_surface = WeatherScreen(self.dimension)
        ws = self.current_surface
        self.blit(ws, (0,0))
        ws.display(event)
        self.current_window = "weather"
        
    def display_calendar(self, event):
        if self.current_surface is None:
            self.current_surface = WeatherScreen(self.dimension)
        ws = self.current_surface
        self.blit(ws, (0,0))
        ws.display(event)
        self.current_window = "weather"
        
    def display(self, event):
        if self.current_window is None:
            self.current_window = "weather"
        if self.current_window == "weather":
            self.display_weather(event)
        elif self.current_window == "calendar":
            self.display_calendar(event)
            
    def next_window(self):
        cw = self.current_window
        i_cw = self.window_list.index(cw)
        if i_cw == len(self.window_list) - 1:
            self.current_window = self.window_list[0]
        else:
            self.current_window = self.window_list[i_cw + 1]
        self.current_surface = None
        print(self.current_window)
        
    def mainloop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                
            self.display(event)
            
            if event.type == pygame.USEREVENT+1:
                self.next_window()
            
        self.screen.blit(self, (0,0))
        pygame.display.update()