from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from plyer import gps
from math import radians, cos, sin, asin, sqrt
import time


class SpeedTrackerApp(App):
    def build(self):
        # Main layout
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Speed label to show the current speed
        self.speed_label = Label(text="Speed: 0.0 km/h", font_size=32)
        self.layout.add_widget(self.speed_label)

        # Button to start or stop the GPS tracking
        self.toggle_button = Button(text="Start Tracking", on_press=self.toggle_gps, font_size=24)
        self.layout.add_widget(self.toggle_button)

        # Variables to store previous location and time
        self.previous_latitude = None
        self.previous_longitude = None
        self.previous_time = None

        # Flag to track whether GPS tracking is active
        self.tracking_active = False

        return self.layout

    def toggle_gps(self, instance):
        """Toggles GPS tracking on or off."""
        if not self.tracking_active:
            # Start GPS tracking
            gps.configure(on_location=self.update_location)
            gps.start(minTime=1000, minDistance=1)  # Updates every 1 second or when moved 1 meter
            self.toggle_button.text = "Stop Tracking"
            self.tracking_active = True
        else:
            # Stop GPS tracking
            gps.stop()
            self.toggle_button.text = "Start Tracking"
            self.tracking_active = False

    def update_location(self, **kwargs):
        """Callback function that gets called when GPS location updates."""
        latitude = kwargs['lat']
        longitude = kwargs['lon']
        current_time = time.time()

        # If we have a previous location, calculate the speed
        if self.previous_latitude is not None and self.previous_longitude is not None:
            distance = self.haversine(self.previous_latitude, self.previous_longitude, latitude, longitude)
            time_diff = current_time - self.previous_time

            # Calculate speed in meters per second, convert to km/h
            speed = (distance / time_diff) * 3.6  # m/s to km/h

            # Update the label with the current speed
            self.speed_label.text = f"Speed: {speed:.2f} km/h"

        # Update the previous location and time for the next calculation
        self.previous_latitude = latitude
        self.previous_longitude = longitude
        self.previous_time = current_time

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        """
        Calculate the great-circle distance between two points on the Earth
        using their latitude and longitude (Haversine formula).
        """
        R = 6371000  # Radius of the Earth in meters
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        distance = R * c  # Distance in meters

        return distance

    def on_stop(self):
        """Stop the GPS tracking when the app is closed."""
        if self.tracking_active:
            gps.stop()


if __name__ == '__main__':
    SpeedTrackerApp().run()
