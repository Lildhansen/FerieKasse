#accepts cookies when using the selenium webdriver - not sure if it is neccessary
#on slower machines this might require time.sleep() - for some time (not more than half a second - otherwise it is slow af)
def acceptCookies(webDriver):
    try:
        webDriver.find_element_by_css_selector("#onetrust-reject-all-handler").click()
    except:
        pass