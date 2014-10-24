from datetime import datetime
import time
import os
import unittest
from selenium.webdriver import DesiredCapabilities, Remote
from tests.page_objects.page_object import AuthPage, CreatePage, CampaignsListPage, EditPage


class SeleniumTest(unittest.TestCase):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    BANNER_IMG = 'img.png'
    BANNER_URL = 'www.example.com'
    USER_NAME = 'tech-testing-ha2-2@bk.ru'
    PASS_WORD = os.environ['TTHA2PASSWORD']
    DOMAIN = '@bk.ru'
    PRODUCT_TYPE = 4
    SNG = 'sng'
    AGE_RESTRICT = '18+'

    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def tearDown(self):
        camp_list_page = CampaignsListPage(self.driver)
        camp_list_page.open()
        camp_list_page.campaigns_list.delete_all()
        self.driver.quit()

    def login(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()

        auth_form = auth_page.form
        auth_form.set_domain(self.DOMAIN)
        auth_form.set_login(self.USER_NAME)
        auth_form.set_password(self.PASS_WORD)
        auth_form.submit()

    def set_default_settings(self, create_page, camp_name):
        base_settings = create_page.base_settings
        base_settings.set_campaign_name(camp_name)
        base_settings.set_product_types(self.PRODUCT_TYPE)

        banner_form = create_page.banner_form
        banner_form.set_url(self.BANNER_URL)
        banner_form.set_image(os.path.join(self.BASE_DIR, self.BANNER_IMG))

    def test_login(self):
        self.login()

        camp_list_page = CampaignsListPage(self.driver)
        camp_list_page.open()
        user_name = camp_list_page.top_menu.get_email()

        self.assertEqual(self.USER_NAME, user_name)

    def test_create_company(self):
        self.login()

        camp_name = datetime.now().strftime("%Y.%m.%d %H:%M:%S")

        #Create page
        create_page = CreatePage(self.driver)
        create_page.open()

        self.set_default_settings(create_page, camp_name)

        create_page.create_button.create()

        #Campains list page
        camp_list_page = CampaignsListPage(self.driver)
        camp_list_page.open()

        campaigns_list = camp_list_page.campaigns_list
        is_campaign_exist = campaigns_list.is_campaign_exist(camp_name)

        self.assertTrue(is_campaign_exist, 'campaign not exist')

    def test_create_company_where(self):
        self.login()

        camp_name = datetime.now().strftime("%Y.%m.%d %H:%M:%S")

        #Create page
        create_page = CreatePage(self.driver)
        create_page.open()

        self.set_default_settings(create_page, camp_name)

        where_settings = create_page.where_settings
        where_settings.select_present(self.SNG)

        create_page.create_button.create()

        #Campains list page
        camp_list_page = CampaignsListPage(self.driver)
        camp_list_page.open()

        campaigns_list = camp_list_page.campaigns_list
        camp = campaigns_list.get_campaign(camp_name)
        camp_id = camp.get_campaign_id()

        #Edit page
        edit_page = EditPage(self.driver, camp_id)
        edit_page.open()

        selected_present = edit_page.where_settings.get_selected_present()

        self.assertEqual(self.SNG, selected_present)

    def test_create_company_age_restrictions(self):
        self.login()

        camp_name = datetime.now().strftime("%Y.%m.%d %H:%M:%S")

        #Create page
        create_page = CreatePage(self.driver)
        create_page.open()

        self.set_default_settings(create_page, camp_name)

        age_restrictions = create_page.age_restrictions
        age_restrictions.set_age_restrictions(self.AGE_RESTRICT)

        create_page.create_button.create()

        #Campains list page
        campaigns_list_page = CampaignsListPage(self.driver)
        camp = campaigns_list_page.campaigns_list.get_campaign(camp_name)
        camp_id = camp.get_campaign_id()

        #Edit page
        edit_page = EditPage(self.driver, camp_id)
        edit_page.open()

        expected_age = edit_page.age_restrictions.get_setting_value()
        self.assertEqual(self.AGE_RESTRICT, expected_age)