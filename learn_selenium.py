from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

import re

options = Options()
options.add_argument('--headless')  # Enable headless mode

# Optional: If geckodriver is not in your PATH
# service = Service(executable_path='/path/to/geckodriver')

driver = webdriver.Firefox(options=options)  # Or with service: driver = webdriver.Firefox(service=service, options=options)

driver.get("https://weathershopper.pythonanywhere.com/") # get the website

#Get the temperature
def getTemp():
    temp = driver.find_element("id", "temperature").text #Get the temperature
    temp = int((re.findall(r'\d+', temp))[0]) # Extract the integer value
    print(f"Temperature: {temp}")
    return temp

def testButton(temp):
    #Sunscreen Test Case
    if temp > 34:
        
        #Check if sunscreen button is there
        print("Need Sunscreen")
        test = driver.find_element(By.CSS_SELECTOR, ".offset-4 .btn").text
        print(test)

        #Click on sunscreen button
        driver.find_element(By.CSS_SELECTOR, ".offset-4 .btn").click()

    #Moisturizer Test Case
    elif temp < 19:

        #Check if Moisturizer button is there
        print("Need Moisturizer")
        test = driver.find_element(By.CSS_SELECTOR, ".text-center:nth-child(1) .btn").text
        print(test)

        #Click on moisturizer button
        driver.find_element(By.CSS_SELECTOR, ".text-center:nth-child(1) .btn").click()

def getNamesAndPrices():
    #Check if we are at right page
    title = driver.find_element(By.CSS_SELECTOR, "h2").text
    print(title)

    #Get names into array
    names = getNames()
    print(names)
    if title == 'Sunscreens': #Extract the the type #
        names = [x[-2:] for x in names]
    else: #Extract Aloe and Almond
        '''NOTE: MUST FIX CASING OF WORDS --> Max honey and almond moisturiser should be capitalized'''
        names = [word for s in names for word in ["Aloe", "Almond", "almond"] if word in s]
    print(names)

    #Get prices into array
    prices = getPrices()
    prices = [x[-3:] for x in prices]
    print(prices)

    return [names, prices]

def addItemsToCart(namesAndPrices):

    buttons = getButtons()

    title = driver.find_element(By.CSS_SELECTOR, "h2").text
    print(title)
    names = namesAndPrices[0]
    prices = namesAndPrices[1]
    if title == 'Sunscreens': #Choose lowest 30 and 50
        lowest50 = -1 #Fake price to compare
        lowest50index = -1
        lowest30 = -1 #Fake price to compare
        lowest30index = -1
        for i in range(len(names)): #Get the lowest prices
            if names[i] == '50' and (lowest50 == -1 or int(prices[i]) < int(lowest50)):
                lowest50index = i
                lowest50 = prices[i]
            elif names[i] == '30' and (lowest30 == -1 or int(prices[i]) < int(lowest30)):
                lowest30index = i
                lowest30 = prices[i]
        print(lowest50, lowest30)

        #Add To Cart
        buttons[lowest50index].click()
        buttons[lowest30index].click()

    else: #Choose lowest Almond and Aloe
        lowestAloe = -1 #Fake price to compare
        lowestAloeIndex = -1
        lowestAlmond = -1 #Fake price to compare
        lowestAlmondIndex = -1
        for i in range(len(names)): #Get the lowest prices
            if names[i] == 'Aloe' and (lowestAloe == -1 or int(prices[i]) < int(lowestAloe)):
                lowestAloeindex = i
                lowestAloe = prices[i]
            elif names[i].upper() == 'ALMOND' and (lowestAlmond == -1 or int(prices[i]) < int(lowestAlmond)):
                lowestAlmondindex = i
                lowestAlmond = prices[i]
        print(lowestAloe, lowestAlmond)

        #Add To Cart
        buttons[lowestAloeindex].click()
        buttons[lowestAlmondindex].click()

    #Check if the items were added to the cart
    cart = driver.find_element(By.XPATH, "//button").text
    print(cart)

    #Move to checkout
    driver.find_element(By.XPATH, "//button").click()

def checkCart():
    #Check if we are in the cart
    title = driver.find_element(By.CSS_SELECTOR, "h2").text
    print(title)

    #Check if the correct items are in the cart
    item1name = driver.find_element(By.XPATH, "//td").text
    item2name = driver.find_element(By.XPATH, "//tr[2]/td").text
    item1price = driver.find_element(By.XPATH, "//td[2]").text
    item2price = driver.find_element(By.XPATH, "//tr[2]/td[2]").text
    print(item1name, item2name)
    print(item1price, item2price)

    #Check if price is equal to the sum of the two items
    assert int(item1price) + int(item2price) == int((driver.find_element(By.XPATH, "//p").text)[-3:])
    print("Price and Items are correct")

    #Go to payment
    driver.find_element(By.XPATH, "//button/span").click()

'''
def pay():
    #Switch to IFrame
    driver.switch_to.frame(0)

    #Check if at IFrame
    title = driver.find_element(By.CSS_SELECTOR, "h1").text
    print(title)

    #Enter Info
    driver.find_element(By.ID, "email").click()
    driver.find_element(By.ID, "email").send_keys("test@email.com")
    driver.find_element(By.ID, "card_number").click()
    driver.find_element(By.ID, "card_number").send_keys("4242424242424242")
    driver.find_element(By.ID, "cc-exp").click()
    driver.find_element(By.ID, "cc-exp").send_keys("1234")
    driver.find_element(By.ID, "cc-csc").click()
    driver.find_element(By.ID, "cc-csc").send_keys("567")
    driver.find_element(By.ID, "billing-zip").click()
    driver.find_element(By.ID, "billing-zip").send_keys("12345")

    #Checkout
    driver.find_element(By.CSS_SELECTOR, ".iconTick").click()

    #Check if payment went through
    title = driver.find_element(By.CSS_SELECTOR, "h1").text
    print(title)
'''

def getButtons():
    
    #prep the buttons
    elem1 = driver.find_element(By.XPATH, "//div/button")
    elem2 = driver.find_element(By.XPATH, "//div[2]/button")
    elem3 = driver.find_element(By.XPATH, "//div[3]/button")
    elem4 = driver.find_element(By.XPATH, "//div[3]/div/button")
    elem5 = driver.find_element(By.XPATH, "//div[3]/div[2]/button")
    elem6 = driver.find_element(By.XPATH, "//div[3]/div[3]/button")
    return [elem1, elem2, elem3, elem4, elem5, elem6]

def getNames():

    #Get names into array
    elem1 = driver.find_element(By.XPATH, "//p").text
    elem2 = driver.find_element(By.XPATH, "//div[2]/p").text
    elem3 = driver.find_element(By.XPATH, "//div[3]/p").text
    elem4 = driver.find_element(By.XPATH, "//div[3]/div/p").text
    elem5 = driver.find_element(By.XPATH, "//div[3]/div[2]/p").text
    elem6 = driver.find_element(By.XPATH, "//div[3]/div[3]/p").text
    return [elem1, elem2, elem3, elem4, elem5, elem6]

def getPrices():
    #Get prices into array
    elem1 = driver.find_element(By.XPATH, "//p[2]").text
    elem2 = driver.find_element(By.XPATH, "//div[2]/p[2]").text
    elem3 = driver.find_element(By.XPATH, "//div[3]/p[2]").text
    elem4 = driver.find_element(By.XPATH, "//div[3]/div/p[2]").text
    elem5 = driver.find_element(By.XPATH, "//div[3]/div[2]/p[2]").text
    elem6 = driver.find_element(By.XPATH, "//div[3]/div[3]/p[2]").text
    return [elem1, elem2, elem3, elem4, elem5, elem6]

temp = getTemp()
testButton(temp)
namesAndPrices = getNamesAndPrices()
addItemsToCart(namesAndPrices)
checkCart()
#pay()

driver.quit()