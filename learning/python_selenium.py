from selenium import webdriver

'''
driver = webdriver.PhantomJS(executable_path="C:\phantomjs.exe")  
driver.get("http://tianqi.2345.com/wea_history/50936.htm")  
RQ=driver.find_element_by_name("")
print(RQ)


'''
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys



driver = webdriver.PhantomJS(executable_path="C:\phantomjs.exe")   
driver.get("http://tianqi.2345.com/wea_history/50936.htm")  

'''
driver.find_element_by_class_name("prev").click() 
'''
RQ=driver.find_element_by_css_selector("> table > tbody > tr:nth-child(3) > td:nth-child(1)")

print(RQ)
'''
assert "百度" in driver.title  
elem = driver.find_element_by_name("wd")  
elem.send_keys("Eastmount")  
elem.send_keys(Keys.RETURN)  
assert "谷歌" in driver.title  
driver.save_screenshot('baidu.png')  
driver.close()  
driver.quit()  
'''#weather_tab 
