import urlparse
from tests.page_objects.component import AuthForm, TopMenu, Slider, BaseSettings, BannerForm, CreateButton, \
    CampaignsList, WhereSettings


class Page(object):
    BASE_URL = 'https://target.mail.ru'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)


class AuthPage(Page):
    PATH = '/login'

    @property
    def form(self):
        return AuthForm(self.driver)


class CreatePage(Page):
    PATH = '/ads/create'

    @property
    def top_menu(self):
        return TopMenu(self.driver)

    @property
    def slider(self):
        return Slider(self.driver)

    @property
    def base_settings(self):
        return BaseSettings(self.driver)

    @property
    def banner_form(self):
        return BannerForm(self.driver)

    @property
    def create_button(self):
        return CreateButton(self.driver)

    @property
    def where_settings(self):
        return WhereSettings(self.driver)


class CampaignsListPage(Page):
    PATH = '/ads/campaigns/'

    @property
    def top_menu(self):
        return TopMenu(self.driver)

    @property
    def campaigns_list(self):
        return CampaignsList(self.driver)


class EditPage(Page):
    PATH = '/ads/campaigns/'
    SUF = '/edit/'

    def __init__(self, driver, campaign_id):
        super(EditPage, self).__init__(driver)
        self.PATH = urlparse.urljoin(self.PATH, str(campaign_id))
        self.PATH = urlparse.urljoin(self.PATH, self.SUF)

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
