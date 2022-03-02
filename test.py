#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class TestCamelotKeys:
    home_url = "http://localhost:5000/"

    @pytest.fixture()
    def test_setup(self):
        global driver
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.home_url)
        yield driver
        driver.quit()

    def test_server_running(self, test_setup):
        assert 'Hello, world!' == driver.title

    def test_file_upload(self, test_setup):
        driver.get(self.home_url + '/camelot')
        choose_file = driver.find_element_by_name('file')
        submit = driver.find_element_by_xpath("//input[@type='submit']")

        choose_file.send_keys(os.getcwd() + "/testTXT.txt")
        submit.click()

        assert "file uploaded successfully" in driver.page_source
