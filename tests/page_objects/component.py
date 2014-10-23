from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver import ActionChains, DesiredCapabilities, Remote
from selenium.webdriver.support.ui import Select, WebDriverWait
import time


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class AuthForm(Component):
    LOGIN = '#id_Login'
    PASSWORD = '#id_Password'
    DOMAIN = '#id_Domain'
    SUBMIT = '#gogogo>input'

    def set_login(self, login):
        self.driver.find_element_by_css_selector(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_css_selector(self.PASSWORD).send_keys(pwd)

    def set_domain(self, domain):
        select = self.driver.find_element_by_css_selector(self.DOMAIN)
        Select(select).select_by_visible_text(domain)

    def submit(self):
        self.driver.find_element_by_css_selector(self.SUBMIT).click()


class TopMenu(Component):
    EMAIL = '#PH_user-email'

    def get_email(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.EMAIL).text
        )


class Slider(Component):
    SLIDER = '.price-slider__begunok'

    def move(self, offset):
        element = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.SLIDER)
        )
        ac = ActionChains(self.driver)
        ac.click_and_hold(element).move_by_offset(offset, 0).perform()


class BaseSettings(Component):
    BASE_SETTINGS_FORM = '.base-setting'
    CAMPAIGN_NAME_INPUT = '.base-setting__campaign-name__input'
    PRODUCT_TYPES = {1: '#product-type-5205',
                     2: '#product-type-5212',
                     3: '#product-type-5208',
                     4: '#product-type-6043',
                     5: '#product-type-6039'}

    def __init__(self, driver):
        super(BaseSettings, self).__init__(driver)
        self.base_settings_form = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.BASE_SETTINGS_FORM)
        )

    def set_campaign_name(self, name):
        element = WebDriverWait(self.base_settings_form, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.CAMPAIGN_NAME_INPUT)
        )
        element.clear()
        element.send_keys(name)

    def set_product_types(self, type_number):
        element = WebDriverWait(self.base_settings_form, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.PRODUCT_TYPES[type_number])
        )
        element.click()


class BannerForm(Component):
    BANNER_FORM = '.banner-form'
    URL_INPUT = '.banner-form__input'
    BANNER_IMG_INPUT = '.banner-form__img-file'
    SAVE_IMAGE_BUTTON = '.image-cropper__save'

    def __init__(self, driver):
        super(BannerForm, self).__init__(driver)
        self.banner_form = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.BANNER_FORM)
        )

    def set_url(self, url):
        url_inputs = WebDriverWait(self.banner_form, 30, 0.1).until(
            lambda d: d.find_elements_by_css_selector(self.URL_INPUT)
        )
        for url_input in url_inputs:
            if url_input.is_displayed():
                url_input.send_keys(url)

    def set_image(self, img_path):
        banner_input_form = WebDriverWait(self.banner_form, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.BANNER_IMG_INPUT)
        )
        banner_input_form.send_keys(img_path)
        save_img_button = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.SAVE_IMAGE_BUTTON)
        )
        save_img_button.click()


class CreateButton(Component):
    CREATE_BUTTON = '.main-button-new'

    def create(self):
        element = WebDriverWait(self.driver, 30, 0.1).until(self.check_button)
        element.click()

    def check_button(self, d):
        button = d.find_element_by_css_selector(self.CREATE_BUTTON)
        if button.is_displayed():
            return button


class CampaignsList(Component):
    CAMPAIGNS_UL = '.campaigns-page__campaigns'
    CAMPAIGN_LI = '.campaign-row'
    campaigns_list = []

    def __init__(self, driver):
        super(CampaignsList, self).__init__(driver)

        self.campaigns_ul = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.CAMPAIGNS_UL)
        )

        element_list = WebDriverWait(self.campaigns_ul, 30, 0.1).until(
            lambda d: d.find_elements_by_css_selector(self.CAMPAIGN_LI)
        )
        self.campaigns_list = []
        for element in element_list:
            if element.get_attribute("data-type") == 'active':
                self.campaigns_list.append(Campaign(self.driver, element))

    def get_campaign(self, name):
        for camp in self.campaigns_list:
            if camp.campaign_name() == name:
                return camp

    def is_campaign_exist(self, name):
        for camp in self.campaigns_list:
            if camp.campaign_name() == name:
                return True
        return False

    def delete_all(self):
        for camp in self.campaigns_list:
            camp.delete_campaign()


class Campaign(Component):
    CAMPAIGN_TITLE_DIV = '.campaign-title__name'
    DELETE_BUTTON = '.control__preset_delete'
    name = None

    def __init__(self, driver, campaign_li):
        super(Campaign, self).__init__(driver)

        self.campaign_li = campaign_li

    def campaign_name(self):
        if not self.name:
            self.name = WebDriverWait(self.campaign_li, 30, 0.1).until(
                lambda d: d.find_element_by_css_selector(self.CAMPAIGN_TITLE_DIV).text
            )
        return self.name

    def delete_campaign(self):
        delete_button = WebDriverWait(self.campaign_li, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.DELETE_BUTTON)
        )
        delete_button.click()


class WhereSettings(Component):
    PRESENT_LIST_UI = '.campaign-setting__preset-list'
    PRESENT_LI = '.campaign-setting__preset'

    def __init__(self, driver):
        super(WhereSettings, self).__init__(driver)
        self.context = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.PRESENT_LIST_UI) if d.find_element_by_css_selector(
                self.PRESENT_LIST_UI).is_displayed() else None
        )

    def select_present(self, data_name):
        presents_list = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_elements_by_css_selector(self.PRESENT_LI)
        )
        for present in presents_list:
            if present.get_attribute("data-name") == data_name:
                present.click()