def acceptCookies(webDriver):
    try:
        webDriver.find_element_by_css_selector("#onetrust-reject-all-handler").click()
    except:
        pass