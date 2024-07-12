# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 13:02:04 2024

@author: ahmad
"""

import matplotlib.pyplot as plt

# Define the PQRST data for 5 heartbeats
ecg_pqrst_data = [
    # Heartbeat 1
    0.0, 0.1, 0.2, 0.1, 0.0, -0.1, 0.2, 0.6, 1.2, 0.7, 0.2, 0.1, 0.0, -0.1, -0.2, 0.0, 0.2, 0.0, 
    # Heartbeat 2
    0.0, 0.1, 0.2, 0.1, 0.0, -0.1, 0.2, 0.6, 1.2, 0.7, 0.2, 0.1, 0.0, -0.1, -0.2, 0.0, 0.2, 0.0, 
    # Heartbeat 3
    0.0, 0.1, 0.2, 0.1, 0.0, -0.1, 0.2, 0.6, 1.2, 0.7, 0.2, 0.1, 0.0, -0.1, -0.2, 0.0, 0.2, 0.0, 
    # Heartbeat 4
    0.0, 0.1, 0.2, 0.1, 0.0, -0.1, 0.2, 0.6, 1.2, 0.7, 0.2, 0.1, 0.0, -0.1, -0.2, 0.0, 0.2, 0.0, 
    # Heartbeat 5
    0.0, 0.1, 0.2, 0.1, 0.0, -0.1, 0.2, 0.6, 1.2, 0.7, 0.2, 0.1, 0.0, -0.1, -0.2, 0.0, 0.2, 0.0 
]

# Plot the PQRST complex data
plt.figure(figsize=(12, 5))
plt.plot(ecg_pqrst_data, label='PQRST Complex Signal')
plt.xlabel('Time (arbitrary units)')
plt.ylabel('Voltage (arbitrary units)')
plt.title('ECG Signal (PQRST Complex) for 5 Heartbeats')
plt.legend()
plt.grid(True)
plt.show()
