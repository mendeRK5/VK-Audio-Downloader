from sys import platform
from os import path, getcwd
from re import match
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Controller:
    def __init__(self):
        if platform.startswith('win'):
            driver_location = 'driver/windows/chromedriver.exe'

        elif platform.startswith('darwin'):
            driver_location = 'driver/mac/chromedriver'

        elif platform.startswith('linux'):
            driver_location = 'driver/linux/chromedriver'

        options = Options()
        options.add_argument("user-data-dir=" + path.abspath(path.join(getcwd(), "data")))

        self.driver = webdriver.Chrome(executable_path=driver_location, chrome_options=options)

    def start(self):
        self.driver.get("about:blank")
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get("https://vk.com/")

    def get_audio(self):
        while not match(r"^https:\/\/vk\.com\/audios(.*)", self.driver.current_url):
            sleep(1)

        self.driver.execute_script(open('jsModules/scrollDown.js').read())
        WebDriverWait(self.driver, 9999).until(
             EC.alert_is_present()
        )

        self.driver.switch_to.alert.accept()
        self.driver.switch_to.window(self.driver.window_handles[0])

        track_names = self.driver.execute_script(open('jsModules/createTrackList.js').read())
        print("Now connect to proxy (localhost:8080)\n")
        return track_names

    def switch_track(self):
        is_switched = self.driver.execute_script(open('jsModules/switchTrack.js').read())
        return is_switched

    def restore_track_position(self, position):
        self.driver.execute_script("window.__noPlayback = true;")
        for _ in range(position):
            self.switch_track()

        self.driver.execute_script("window.__noPlayback = false;")

    def finish(self):
        self.driver.quit()