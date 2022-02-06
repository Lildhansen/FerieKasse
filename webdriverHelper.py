def acceptCookies(webDriver):
    #time.sleep(3)#wait for it to show up
    try:
        webDriver.find_element_by_css_selector("#onetrust-reject-all-handler").click()
    except:
        pass