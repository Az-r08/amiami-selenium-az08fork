import selenium 
from selenium import webdriver
#from webdriver_manager.firefox import GeckoDriverManager
#from selenium.webdriver.firefox.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("user-data-dir=/home/admin/.config/chromium/")
options.add_argument("--profile-directory = Default");
options.add_experimental_option("detach", True)
# Not specifying executable_path results in weird errors on Windows
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

with open( 'config.json') as file_config:
        # Read from configuration files
        config = json.load(file_config)
        credentials = config['credentials']SSS
        #driver_path = config['driverPath']
        #if sys.argv[1] == "action":
            #products = config["actionItems"]
        #else:  # testing
            #products = config["testItems"]

        #for product in products:
            #query_product(product, credentials, driver_path)

driver.get("https://www.amiami.com/eng/detail?gcode=GOODS-04235079")
filtered = []

while len(filtered) == 0:
    
    try:
        driver.implicitly_wait(60)
    except:
        print("timed out")
        pass
            # print("Page opened")
    try:
        elem_list = cart = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "btn-cart"))) 
        filtered = list(filter(lambda element: 
            element.get_attribute("style") == "", elem_list))
    except:
        pass


    if len(filtered) == 0: #the length of the table will be different to 0 if the button has been filtered, so if the length is still 0, refresh the page
        print("adding to cart failed, refreshing")
        driver.refresh()
    else:
        pass
        
filtered[0].click() #click the add to cart
print("added to cart successfully")



#print(filtered[0].text)
#-----------------------------------------------------------------------------------


#advance to the cart


while True:
        while True:
            try:
                cart = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "cart"))) 
                #check if the cart button has loaded yet
                break #if the button done loading, break the loop
             
            except:
                print("timed out on checkout, refreshing") 
                #if the time runs out, refresh the site and continue the loop(if the timer runs out, it will raise an exception)
                driver.refresh()
        
        cart.submit() #submit to checkout
        
        try: 
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.xpath('//button[text()="Confirm"]')))).click()
            #if the server got flooded, it will have the popup that says something about access restriction, 
            #the button to close it has the "Confirm" text on it, i don't have the element name nor any attributes 
            #of it cause the last time i bought a fumo on the site was august last year, so i used xpath and find by 
            #the element's text
        except:
            break

print("broketheloop")

#------------------------------------------------------------------------------------------------------



#login page
email_field = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "email")))


#the code below DOES NOT WORK, amiami has developed an anti pasting login page, which means that you can't paste, or use send_keys() to type in your credentials in the box anymore.
#doing so will trigger an error message and if you trigger it 5 times, your account will be locked for an hour

#email_field.send_keys(Keys.CONTROL + "a") #using this to clear the field since .clear() will also clear it's type and will cause an error
#email_field.send_keys(Keys.DELETE)
#email_field.send_keys(credentials["email"])
#password_field = driver.find_element(By.NAME, "password" )
#password_field.send_keys(credentials["password"])

#Weirdly, Firefox webdriver auto fill will trigger the mechanism while Chromium webdriver autofill don't, so we need to setup an auto fill, i've done that by importing my chromium 
#options to the webdriver at the beginning of the script

submitbtn = driver.find_element(By.CLASS_NAME, "btn-submit")
submitbtn.submit()

while True:
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.xpath("//*[text()='Confirm how to combine the items']"))))
        print("detected")
        break    
    except:
        submitbtn.submit()

 
#while True:
    #try:
            #WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'shipping-method1')))
            #driver.execute_script("document.getElementById('shipping-method19').click()")
           # break
            #submitbtn = driver.find_element_by_class_name("btn-submit").click()
            #if submitbtn.is_displayed() == True:
                #pass
            #else:
                #break
    #except:
            #pass



#https://stackoverflow.com/questions/663034/can-selenium-handle-autocomplete
#https://stackoverflow.com/questions/37488390/can-you-tell-me-why-this-web-scraper-isnt-able-to-log-in-correctly
# <h2 class="item-detail__error-title">Access Restriction Notice</h2> access restriction
#driver.find_element(By.NAME, "email").send_keys(username)
#driver.find_element(By.NAME, "password").send_keys(password)
#driver.find_element(By.CLASS_NAME, "btn-submit").click()
