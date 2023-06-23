from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import re
from webhooks import *

webhook_url_general = '' # Replace with your webhook url
webhook_url_important = '' # Replace with your webhook url


def read_txt_file(file_path):
    emails = []
    order_numbers = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            email, order_number = line.split(':')
            emails.append(email)
            order_numbers.append(order_number)
    return emails, order_numbers

# Replace 'file_path.txt' with the actual path to your text file
# file_path = 'Adidas.txt'
file_path = 'Adidas.txt'


email_list, order_number_list = read_txt_file(file_path)

allorders= len(order_number_list)

prog = 0
ship = 0
deli = 0
dela = 0
sleepcounter =0
date = datetime.datetime.now()
now = date.strftime("%m-%d-%y %I:%M:%S %p")
embed = {
"title": "New Order Tracking Task",
"description": "",
"color": 0000,
"fields": [
    {
        "name": "Total Orders",
        "value": allorders,
        "inline": True
    },
    ],
    "footer": {
        "text": "Adidas Order Tracker by Jihxdul - "+ now,
    }
}
send_discord_webhook(webhook_url_general, embed)
send_discord_webhook(webhook_url_important, embed)

for i in range(allorders):
    
    # Broswer Mode
    
    # PATH = "chromedriver.exe"
    # driver = webdriver.Chrome(PATH)
    # driver.get('https://www.adidas.com/us/order-tracker')

    # Headless / non browser Mode
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("--force-device-scale-factor=0.5")
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    driver.get('https://www.adidas.com/us/order-tracker')
    
    OrdNum = order_number_list[i]
    mail = email_list[i]
    orderNumber = driver.find_element(By.ID,'order-tracker-page-order-number-field')
    email = driver.find_element(By.ID,'order-tracker-page-email-field')

    orderNumber.send_keys(OrdNum)
    time.sleep(3)
    email.send_keys(mail)
    time.sleep(2)
    email.submit()
    time.sleep(10)
    date = datetime.datetime.now()
    now = date.strftime("%m-%d-%y %I:%M:%S %p")


    element = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div[1]/div/div/div[4]/div/div/div[1]/div[1]/section[2]/div/section/div/div[2]")
    status =element.text
    # print(status)

    if status == "DELAYED":
        element = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[1]/div[1]/div/div/div[4]/div/div/div[1]/div[1]/section[2]/div/div[1]/div/div[2]/span")
        expected = element.text
        dela = dela +1
       
    elif status == "DELIVERED":
        element = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[1]/div[1]/div/div/div[4]/div/div/div[1]/div[1]/section[2]/div/div[1]/div/div[2]/span")
        expected = element.text
        deli = deli+1
        
    else:

        element = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[1]/div[1]/div/div/div[4]/div/div/div[1]/div[1]/section[2]/div/div[1]/div[2]/div/span")
        expected = element.text
        

    if status == "IN PROGRESS":
        prog = prog+1

    element = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[1]/div[1]/div/div/div[4]/div/div/div[1]/div[1]/section[2]/div/div[3]/div[2]/h3")
    product = element.text



    element = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[1]/div[1]/div/div/div[4]/div/div/div[1]/div[1]/section[2]/div/div[3]/div[2]/dl/dd[1]")
    size = element.text

    element = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[1]/div[1]/div/div/div[4]/div/div/div[1]/section[2]/div/div[1]/address/ul[1]")
    address = element.text
 

    
    tracking = "No Tracking Available"
    if status == "ON ITS WAY":
        element = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[1]/div[1]/div/div/div[4]/div/div/div[1]/div[1]/section[2]/div/section/div/div[4]/p")
        tracking = element.text
        tracking = re.sub(r"\D", "", tracking)
        ship = ship+1
        embed = {
        "title": status,
        "description": expected,
        "color": 65280,
        "fields": [
            {
                "name": "Order Number",
                "value": OrdNum,
                "inline": True
            },
            {
                "name": "Email",
                "value": mail,
                "inline": False
            },       
            {
                "name": "Product",
                "value": product,
                "inline": True
            },
            {
                "name": "Size",
                "value": size,
                "inline": True
            },
            {
                "name": "Address",
                "value": address,
                "inline": False
            },
            {
                "name": "Tracking Number",
                "value": tracking,
                "inline": True
            },
        ],
            "footer": {
                "text": "Adidas Order Tracker by Jihxdul - "+ now,
            }
        }
        send_discord_webhook(webhook_url_general, embed)
    elif status == "DELIVERED":
        element = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[1]/div[1]/div/div/div[4]/div/div/div[1]/div[1]/section[2]/div/section/div/div[4]/p")
        tracking = element.text
        tracking = re.sub(r"\D", "", tracking)
        embed = {
        "title": status,
        "description": expected,
        "color": 0000,
        "fields": [
            {
                "name": "Order Number",
                "value": OrdNum,
                "inline": True
            },
            {
                "name": "Email",
                "value": mail,
                "inline": False
            },       
            {
                "name": "Product",
                "value": product,
                "inline": True
            },
            {
                "name": "Size",
                "value": size,
                "inline": True
            },
            {
                "name": "Address",
                "value": address,
                "inline": False
            },
            {
                "name": "Tracking Number",
                "value": tracking,
                "inline": True
            },
        ],
            "footer": {
                "text": "Adidas Order Tracker by Jihxdul - "+ now,
            }
        }
        send_discord_webhook(webhook_url_general, embed)
    elif status == "DELAYED":
        embed = {
        "title": status,
        "description": expected,
        "color": 2552550,
        "fields": [
            {
                "name": "Order Number",
                "value": OrdNum,
                "inline": True
            },
            {
                "name": "Email",
                "value": mail,
                "inline": False
            },       
            {
                "name": "Product",
                "value": product,
                "inline": True
            },
            {
                "name": "Size",
                "value": size,
                "inline": True
            },
            {
                "name": "Address",
                "value": address,
                "inline": False
            },
            {
                "name": "Tracking Number",
                "value": tracking,
                "inline": True
            },
        ],
            "footer": {
                "text": "Adidas Order Tracker by Jihxdul - "+ now,
            }
        }
        send_discord_webhook(webhook_url_general, embed)
    else:
        embed = {
        "title": status,
        "description": expected,
        "color": 255,
        "fields": [
            {
                "name": "Order Number",
                "value": OrdNum,
                "inline": True
            },
            {
                "name": "Email",
                "value": mail,
                "inline": False
            },       
            {
                "name": "Product",
                "value": product,
                "inline": True
            },
            {
                "name": "Size",
                "value": size,
                "inline": True
            },
            {
                "name": "Address",
                "value": address,
                "inline": False
            },
            {
                "name": "Tracking Number",
                "value": tracking,
                "inline": True
            },
        ],
            "footer": {
                "text": "Adidas Order Tracker by Jihxdul - "+ now,
            }
        }
        send_discord_webhook(webhook_url_general, embed)
    driver.quit()

    sleepcounter = sleepcounter +1 
    if sleepcounter % 3 == 0:
        embed = {
        "title": "Sleeping...",
        "description": "30 Seconds",
        "color": 0000,
        "fields": [
            {
                "name": "",
                "value": ":sleeping::zzz:",
                "inline": True
            },
        ],
            "footer": {
                "text": "Adidas Order Tracker by Jihxdul - "+ now,
            }
        }
        send_discord_webhook(webhook_url_general, embed)
        # time.sleep(30)
  
    
embed = {
    
    "title": "Order Tracking Task Complete",
    "description": "Statistics Below",
    "color": 800080,
    "fields": [
        {
            "name": "In Progress",
            "value": prog,
            "inline": True
        },
        {
            "name": "Delayed",
            "value": dela,
            "inline": False
        },
        {
            "name": "Shipped",
            "value": ship,
            "inline": True
        },
        {
            "name": "Delivered",
            "value": deli,
            "inline": False
        }
    ],
    "footer": {
        "text": "Adidas Order Tracker by Jihxdul - " + now,
    }
}

send_discord_webhook(webhook_url_important, embed)


            
            