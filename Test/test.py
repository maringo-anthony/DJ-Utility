#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from WebApp.CamelotKeyConverter import CamelotKeyConverter


# TODO: TEST THE BACK BUTTON
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

    def test_file_upload(self, test_setup):  # TODO: DELETE THE FILE FROM THE DIRECTORY THEN UPLOAD IT
        self.upload_rekordboxxml()

        assert "File uploaded successfully" in driver.page_source

    def test_camelot_key_conversion(self):
        converter = CamelotKeyConverter()

        new_xml = converter.convertToCamelotKeys()

        old_keys = list(converter.camelot_conversions.keys())

        for key in old_keys:
            assert "Tonality=\"" + key + "\"" not in new_xml

    def test_uploaded_file_key_change(self, test_setup):  # TODO: Update this test for the downloading file
        self.upload_rekordboxxml()
        assert "rekordbox" in driver.page_source  # TODO: make this a better check

        converter = CamelotKeyConverter()

        old_keys = list(converter.camelot_conversions.keys())

        for key in old_keys:
            assert "Tonality=\"" + key + "\"" not in driver.page_source

    def upload_rekordboxxml(self):
        driver.get(self.home_url + '/camelot')
        choose_file = driver.find_element(by=By.NAME, value='file')
        submit = driver.find_element(by=By.XPATH, value="//input[@type='submit']")
        choose_file.send_keys(os.getcwd() + "/rekordbox.xml")
        submit.click()
