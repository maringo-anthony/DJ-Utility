#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType


class TestWebsite:
    # 1. Check browser configuration in browser_setup_and_teardown
    # 2. Run 'Selenium Tests' configuration
    # 3. Test report will be created in reports/ directory

    @pytest.fixture(autouse=True)
    def browser_setup_and_teardown(self):
        self.use_selenoid = False  # set to True to run tests with Selenoid

        if self.use_selenoid:
            self.browser = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities={
                    "browserName": "chrome",
                    "browserSize": "1920x1080"
                }
            )
        else:
            self.browser = webdriver.Chrome(
                executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

        self.browser.maximize_window()
        self.browser.implicitly_wait(10)
        self.browser.get("https://www.jetbrains.com/")

        yield

        self.browser.close()
        self.browser.quit()

    def test_tools_menu(self):
        """this test checks presence of Tools menu item"""
        tools_menu = self.browser.find_element_by_xpath(
            "//div[contains(@class, 'menu-main__item') and text() = 'Tools']")

        actions = webdriver.ActionChains(self.browser)
        actions.move_to_element(tools_menu)
        actions.perform()

        menu_popup = self.browser.find_element_by_class_name("menu-main__popup-wrapper")
        assert menu_popup is not None

    def test_navigation_to_all_tools(self):
        """this test checks navigation by See All Tools button"""
        see_all_tools_button = self.browser.find_element_by_css_selector("a.wt-button_mode_primary")
        see_all_tools_button.click()

        products_list = self.browser.find_element_by_class_name("products-list")
        assert products_list is not None
        assert self.browser.title == "All Developer Tools and Products by JetBrains"

    def test_search(self):
        """this test checks search from the main menu"""
        search_button = self.browser.find_element_by_css_selector("[data-test=menu-main-icon-search]")
        search_button.click()

        search_field = self.browser.find_element_by_id("header-search")
        search_field.send_keys("Selenium")

        submit_button = self.browser.find_element_by_xpath("//button[@type='submit' and text()='Search']")
        submit_button.click()

        search_page_field = self.browser.find_element_by_class_name("js-search-input")
        assert search_page_field.get_property("value") == "Selenium"
