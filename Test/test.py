#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from WebApp.CamelotKeyConverter import CamelotKeyConverter


def upload_rekordbox_xml(driver):
    # Upload rekordbox.xml
    choose_file = driver.find_element(by=By.NAME, value='file')
    submit = driver.find_element(by=By.XPATH, value="//input[@type='submit']")
    choose_file.send_keys(os.getcwd() + "/rekordbox.xml")
    driver.find_element(by=By.ID, value='yes').click()
    submit.click()


def wait_for_download(file_name):
    seconds = 0
    while seconds <= 2:
        if file_name not in os.listdir(str(Path.home() / "Downloads")):
            time.sleep(.5)
        seconds += .5


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
        upload_rekordbox_xml(driver)

        assert "File uploaded successfully" in driver.page_source

    def test_camelot_key_conversion(self):
        converter = CamelotKeyConverter()

        new_xml = converter.convertToCamelotKeys()

        old_keys = list(converter.camelot_conversions.keys())

        for key in old_keys:
            assert "Tonality=\"" + key + "\"" not in new_xml

    def test_uploaded_file_key_change(self, test_setup):
        upload_rekordbox_xml(driver)
        assert "rekordbox" in driver.page_source

        converter = CamelotKeyConverter()

        old_keys = list(converter.camelot_conversions.keys())

        for key in old_keys:
            assert "Tonality=\"" + key + "\"" not in driver.page_source


class TestCamelotHomePage:
    home_url = "http://localhost:5000/camelot"

    @pytest.fixture()
    def test_setup(self):
        global driver
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.home_url)
        yield driver
        driver.quit()

    def test_choose_file_clicked_submit_clicked_compression_yes_clicked(self, test_setup):
        self.execute_actions(True, True, "Yes")
        assert "Click to download converted and compressed rekordbox.zip" in driver.page_source

    def test_choose_file_clicked_submit_clicked_compression_no_clicked(self, test_setup):
        self.execute_actions(True, True, "No")
        assert "File uploaded successfully" in driver.page_source and "Click to download converted and compressed rekordbox.zip" not in driver.page_source

    def test_choose_file_clicked_submit_clicked_compression_none_clicked(self, test_setup):
        self.execute_actions(True, True, None)
        assert "File uploaded successfully" in driver.page_source and "Click to download converted and compressed rekordbox.zip" not in driver.page_source

    def test_choose_file_clicked_submit_NOT_clicked_compression_yes_clicked(self, test_setup):
        self.execute_actions(True, False, "Yes")
        assert driver.current_url == self.home_url

    def test_choose_file_NOT_clicked_submit_clicked_compression_yes_clicked(self, test_setup):
        self.execute_actions(False, True, "Yes")
        assert driver.current_url == self.home_url

    def execute_actions(self, choose_file, submit, compression):
        driver.get(self.home_url)

        if choose_file:
            choose_file_button = driver.find_element(by=By.NAME, value='file')
            choose_file_button.send_keys(os.getcwd() + "/rekordbox.xml")

        if compression == "Yes":
            driver.find_element(by=By.ID, value='yes').click()
        elif compression == "No":
            driver.find_element(by=By.ID, value='no').click()

        if submit:
            driver.find_element(by=By.XPATH, value="//input[@type='submit']").click()


class TestCamelotDownloadPage:
    home_url = "http://localhost:5000/"

    @pytest.fixture()
    def test_setup(self):
        global driver
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.home_url)

        upload_rekordbox_xml(driver)
        yield driver
        driver.quit()

        # Tear down
        download_path = str(Path.home() / "Downloads")
        files_to_delete = [x for x in os.listdir(download_path) if "rekordbox" in x]
        print(f'need to delete: {files_to_delete}')
        for file in files_to_delete:
            os.remove(str(download_path + "/" + file))

    def test_download_xml(self, test_setup):
        driver.find_element(By.PARTIAL_LINK_TEXT, "Click to download converted rekordbox.xml").click()
        file_name = "rekordbox.xml"
        wait_for_download(file_name)

        assert file_name in os.listdir(str(Path.home() / "Downloads"))

    def test_download_compressed_xml(self, test_setup):
        driver.find_element(By.PARTIAL_LINK_TEXT, "Click to download converted and compressed rekordbox.zip").click()
        file_name = "rekordbox.zip"
        wait_for_download(file_name)

        assert file_name in os.listdir(str(Path.home() / "Downloads"))

    def test_download_xml_and_compressed_xml(self, test_setup):
        driver.find_element(By.PARTIAL_LINK_TEXT, "Click to download converted rekordbox.xml").click()
        driver.find_element(By.PARTIAL_LINK_TEXT, "Click to download converted and compressed rekordbox.zip").click()

        file1_name = "rekordbox.xml"
        wait_for_download(file1_name)

        file2_name = "rekordbox.zip"
        wait_for_download(file2_name)

        assert file1_name in os.listdir(str(Path.home() / "Downloads")) and file2_name in os.listdir(
            str(Path.home() / "Downloads"))


class TestYoutubeSearchPage:
    url = "http://localhost:5000/youtube_search"

    @pytest.fixture()
    def test_setup(self):
        global driver
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.url)

        yield driver
        driver.quit()

    def test_not_empty_submit_button_clicked_yes_look_for_remix(self, test_setup):
        self.execute_actions("Riptide", True, "Yes")
        assert "Click to download your song!" in driver.page_source and "Click to download remixed version of your song!" in driver.page_source

    def test_not_empty_submit_button_clicked_none_look_for_remix(self, test_setup):
        self.execute_actions("Riptide", True, None)
        assert "Click to download your song!" in driver.page_source and "Click to download remixed version of your song!" not in driver.page_source

    def test_not_empty_submit_button_clicked_no_look_for_remix(self, test_setup):
        self.execute_actions("Riptide", True, "No")
        assert "Click to download your song!" in driver.page_source and "Click to download remixed version of your song!" not in driver.page_source

    def test_not_empty_submit_button_NOT_clicked_yes_look_for_remix(self, test_setup):
        self.execute_actions("Riptide", False, "Yes")
        assert driver.current_url == self.url

    def test_empty_submit_button_clicked_yes_look_for_remix(self, test_setup):
        self.execute_actions("", True, "Yes")
        assert driver.current_url == self.url

    def execute_actions(self, textbox_content, submit, remix):
        driver.get(self.url)

        if textbox_content:
            textbox = driver.find_element(By.NAME, "song-name")
            textbox.send_keys(textbox_content)

        if remix == "Yes":
            driver.find_element(by=By.NAME, value='remix_radio.yes').click()
        elif remix == "No":
            driver.find_element(by=By.NAME, value='remix_radio').click()

        if submit:
            driver.find_element(by=By.XPATH, value="//input[@type='submit']").click()


class TestYoutubeDownloadPage:
    url = "http://localhost:5000/youtube_search"
    song_name = "Riptide"

    @pytest.fixture()
    def test_setup(self):
        global driver
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.url)

        # Search for youtube video
        textbox = driver.find_element(By.NAME, "song-name")
        textbox.send_keys(self.song_name)
        driver.find_element(by=By.NAME, value='remix_radio.yes').click()
        driver.find_element(by=By.XPATH, value="//input[@type='submit']").click()

        yield driver
        driver.quit()

        # Tear down
        download_path = str(Path.home() / "Downloads")
        files_to_delete = [x for x in os.listdir(download_path) if self.song_name in x]
        print(f'need to delete: {files_to_delete}')
        for file in files_to_delete:
            os.remove(str(download_path + "/" + file))

    def test_normal_version_download_remix_download(self, test_setup):
        driver.find_element(By.PARTIAL_LINK_TEXT, "Click to download your song!").click()
        driver.find_element(By.PARTIAL_LINK_TEXT, "Click to download remixed version of your song!").click()
        wait_for_download(self.song_name)
        wait_for_download(self.song_name + "-remix")

        original_downloaded = False
        remix_downloaded = False

        # Look for the downloaded files
        for file in os.listdir(str(Path.home() / "Downloads")):
            if self.song_name in file and "remix" not in file:
                original_downloaded = True
            if self.song_name in file and "remix" in file:
                remix_downloaded = True
            if original_downloaded and remix_downloaded:
                break

        assert original_downloaded and remix_downloaded

    def test_normal_version_download_remix_NOT_download(self, test_setup):
        driver.find_element(By.PARTIAL_LINK_TEXT, "Click to download your song!").click()
        wait_for_download(self.song_name)

        original_downloaded = False

        # Look for the downloaded files
        for file in os.listdir(str(Path.home() / "Downloads")):
            if self.song_name in file:
                original_downloaded = True
                break

        assert original_downloaded

    def test_normal_version_NOT_downloaded_remix_download(self, test_setup):
        driver.find_element(By.PARTIAL_LINK_TEXT, "Click to download remixed version of your song!").click()
        wait_for_download(self.song_name + "-remix")

        remix_downloaded = False

        # Look for the downloaded files
        for file in os.listdir(str(Path.home() / "Downloads")):
            if self.song_name in file and "-remix" in file:
                remix_downloaded = True
                break

        assert remix_downloaded


class TestNavigationBar:
    home_url = "http://localhost:5000/camelot"

    @pytest.fixture()
    def test_setup(self):
        global driver
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.home_url)
        yield driver
        driver.quit()

    def test_camelot_page_and_youtube_search_page(self, test_setup):
        driver.find_element(By.PARTIAL_LINK_TEXT, "Camelot Keys").click()
        driver.find_element(By.PARTIAL_LINK_TEXT, "Youtube Search").click()

        assert "Enter the song you would like to download" in driver.page_source

    def test_camelot_page(self, test_setup):
        driver.find_element(By.PARTIAL_LINK_TEXT, "Camelot Keys").click()
        assert "Upload your rekordbox.xml to covert keys to camelot keys!" in driver.page_source

    def test_youtube_search(self, test_setup):
        driver.find_element(By.PARTIAL_LINK_TEXT, "Youtube Search").click()

        assert "Enter the song you would like to download" in driver.page_source


class TestHomeMutations:
    home_url = "http://localhost:5000/camelot"

    @pytest.fixture()
    def test_setup(self):
        global driver
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.home_url)
        upload_rekordbox_xml(driver)
        yield driver
        driver.quit()

    def test_file_upload_inverted_if_mutant(self, test_setup):
        assert "File uploaded successfully" in driver.page_source

    def test_file_compression_inverted_if_mutatnt(self, test_setup):
        assert "Click to download converted and compressed rekordbox.zip" in driver.page_source
