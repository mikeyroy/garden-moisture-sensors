#!/usr/bin/python

sensors = 6
readings = [0] * sensors
reading_delay = 2
plot_delay = 600
min_moisture = 966 #~3.11V instead of 1023@3.3V
max_moisture = 0
diff_moisture = min_moisture - max_moisture
plot_data = [''] * sensors