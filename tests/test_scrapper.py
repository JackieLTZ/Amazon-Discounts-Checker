from api.scrapper import Scrapper


def test_scrapper():
    browser = "safari"
    url = "https://www.amazon.de/TY-7146128-Peppa-Schwein-rotem/dp/B001ENZ43K?pf_rd_p=b7b797ed-078a-4a5b-91a4-303c74775994&pf_rd_r=D0VN0RMV5J7JM2MQX3XM&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&th=1"

    scrap_test = Scrapper(None)
    scrap_test.set_driver(browser=browser, url=url)

    try:
        data = scrap_test.check_original_price(2)
        assert data.original_price, "Original price is empty"
        assert data.discount_price, "Discount price is empty"

    finally:
        if scrap_test._driver:
            scrap_test._driver.quit()
