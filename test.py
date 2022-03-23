#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# from WebApp.MP3_Processing import MP3Processor

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
        driver.get(self.home_url + '/camelot')
        choose_file = driver.find_element_by_name('file')
        submit = driver.find_element_by_xpath("//input[@type='submit']")

        choose_file.send_keys(os.getcwd() + "/rekordbox.xml")
        submit.click()

        assert "File uploaded successfully" in driver.page_source

    def test_camelot_key_conversion(self):
        converter = CamelotKeyConverter()

        new_xml = converter.convertToCamelotKeys()

        old_keys = list(converter.camelot_conversions.keys())

        for key in old_keys:
            assert "Tonality=\"" + key + "\"" not in new_xml

    def test_uploaded_file_key_change(self, test_setup):  # TODO: Update this test for the downloading file
        driver.get(self.home_url + '/camelot')
        choose_file = driver.find_element_by_name('file')
        submit = driver.find_element_by_xpath("//input[@type='submit']")

        choose_file.send_keys(os.getcwd() + "/rekordbox.xml")
        submit.click()
        assert "rekordbox" in driver.page_source  # TODO: make this a better check

        converter = CamelotKeyConverter()

        old_keys = list(converter.camelot_conversions.keys())

        for key in old_keys:
            assert "Tonality=\"" + key + "\"" not in driver.page_source

    def test_upload_mp3(self, test_setup):
        driver.get(self.home_url + '/process_mp3')
        choose_file = driver.find_element_by_name('file')
        submit = driver.find_element_by_xpath("//input[@type='submit']")

        mp3_file = "riptide.mp3"
        choose_file.send_keys(os.getcwd() + '/' + mp3_file)
        submit.click()

        web_app_dir = 'WebApp/'
        assert mp3_file in os.listdir(web_app_dir)
        os.remove(web_app_dir + mp3_file)

    def test_song_finger_printing(self):

        mp3_file = os.path.join(os.getcwd(), 'riptide.mp3')
        print('THE meta data is: ')

        print(MP3Processor.newAttemptAtMetaData(mp3_file))

