import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
from pages.components.keyboard import Keyboard


class CreateContactPage(Keyboard, BasePage):
    """新建联系人"""
    ACTIVITY = 'com.cmicc.module_contact.activitys.NewContactActivity'

    __locators = {
        '返回': (MobileBy.XPATH, '//*[contains(@resource-id, "back")]'),
        '新建联系人': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'),
        '保存': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_save_or_sure'),

        '姓名': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_name"]//android.widget.TextView'),
        '输入姓名': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_name"]//android.widget.EditText'),

        '电话': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_number"]//android.widget.TextView'),
        '输入号码': (MobileBy.XPATH,'//*[@resource-id="com.chinasofti.rcs:id/item_number"]//android.widget.EditText'),
        '电话号码': (MobileBy.XPATH, '//*[@text="电话"]/../android.widget.EditText[@resource-id="com.chinasofti.rcs:id/et"]'),

        '公司': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_company"]//android.widget.TextView'),
        '输入公司': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_company"]//android.widget.EditText'),

        '职位': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_job"]//android.widget.TextView'),
        '输入职位': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_job"]//android.widget.EditText'),

        '邮箱': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_email"]//android.widget.TextView'),
        '输入邮箱': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/item_email"]//android.widget.EditText'),
        '允许': (MobileBy.XPATH, '//*[@text="允许"]'),

        '输入公司2': (MobileBy.XPATH, "//*[contains(@text, '输入公司')]"),
        '输入职位2': (MobileBy.XPATH, "//*[contains(@text, '输入职位')]"),
        '输入邮箱2': (MobileBy.XPATH, "//*[contains(@text, '输入邮箱')]"),
    }

    @TestLogger.log('点击保存')
    def click_save(self):
        """点击保存"""
        self.click_element(self.__locators['保存'])

    @TestLogger.log("点击允许权限")
    def click_allow_button(self):
        time.sleep(2)
        if self._is_element_present(self.__class__.__locators['允许']):
            self.click_element(self.__class__.__locators['允许'])
        return True

    @TestLogger.log('判断保存按钮是否不可点击')
    def assert_save_button_should_not_be_clickable(self):
        if self._is_enabled(self.__locators['保存']):
            raise AssertionError("ensure_button_should_not_be_clickable")

    @TestLogger.log('')
    def click_input_name(self):
        self.click_element(self.__locators['输入姓名'])

    @TestLogger.log('')
    def input_name(self, name):
        self.input_text(self.__locators['输入姓名'], name)

    @TestLogger.log('')
    def click_input_number(self):
        self.click_element(self.__locators['输入号码'])

    @TestLogger.log('')
    def input_number(self, name):
        self.input_text(self.__locators['输入号码'], name)

    @TestLogger.log('')
    def get_contant_number(self):
        return self.get_element(self.__locators['输入号码'])

    @TestLogger.log('')
    def click_input_company(self):
        self.click_element(self.__locators['输入公司'])

    @TestLogger.log('')
    def input_company(self, name):
        self.input_text(self.__locators['输入公司'], name)

    @TestLogger.log('')
    def click_input_company(self, name):
        self.click_element(self.__locators['输入公司'], name)

    @TestLogger.log('')
    def input_company(self, name):
        self.input_text(self.__locators['输入公司'], name)

    @TestLogger.log('')
    def click_input_position(self, name):
        self.click_element(self.__locators['输入职位'], name)

    @TestLogger.log('')
    def input_position(self, name):
        self.input_text(self.__locators['输入职位'], name)

    @TestLogger.log('')
    def click_input_email_address(self, name):
        self.click_element(self.__locators['输入邮箱'], name)

    @TestLogger.log('')
    def get_text_of_box(self, locator='输入公司'):
        return self.get_text(self.__locators[locator])

    @TestLogger.log('输入邮箱')
    def input_email_address(self, name):
        self.input_text(self.__locators['输入邮箱'], name)

    @TestLogger.log('')
    def click_company2(self):
        self.click_element(self.__locators['输入公司2'])

    @TestLogger.log('')
    def input_company2(self, name):
        self.input_text(self.__locators['输入公司2'], name)

    @TestLogger.log('')
    def click_position2(self):
        self.click_element(self.__locators['输入职位2'])

    @TestLogger.log('')
    def input_position2(self, name):
        self.input_text(self.__locators['输入职位2'], name)

    @TestLogger.log('')
    def click_email_address2(self):
        self.click_element(self.__locators['输入邮箱2'])

    @TestLogger.log('')
    def input_email_address2(self, name):
        self.input_text(self.__locators['输入邮箱2'], name)

    @TestLogger.log('点击保存')
    def save_contact(self):
        self.click_element(self.__locators['保存'])

    @TestLogger.log('保存按钮是否可点击')
    def is_save_icon_is_clickable(self):
        """保存按钮是否可点击"""
        self._is_clickable(self.__locators['保存'])

    @TestLogger.log('')
    def is_save_icon_is_clickable2(self):
        """保存按钮是否可点击"""
        el = self.get_element(self.__locators['保存'])
        if el:
            if el.get_attribute("enabled")=='true':
                return True
            else:
                return False
        else:
            return False

    @TestLogger.log('点击返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('创建联系人')
    def create_contact(self, name, number, company='', position='', email=''):
        if name:
            self.hide_keyboard_if_display()
            self.input_name(name)
        if number:
            self.hide_keyboard_if_display()
            self.input_number(number)
        if company:
            self.hide_keyboard_if_display()
            self.input_company(company)
        if position:
            self.hide_keyboard_if_display()
            self.input_position(position)
        if email:
            self.hide_keyboard_if_display()
            self.input_email_address(email)
        self.hide_keyboard_if_display()
        self.save_contact()

    @TestLogger.log('创建只有姓名的联系人')
    def create_name_only_contact(self, name, number='', company='', position='', email=''):
        if name:
            self.hide_keyboard_if_display()
            self.input_name(name)
        self.hide_keyboard_if_display()
        self.input_number(number)
        if company:
            self.hide_keyboard_if_display()
            self.input_company(company)
        if position:
            self.hide_keyboard_if_display()
            self.input_position(position)
        if email:
            self.hide_keyboard_if_display()
            self.input_email_address(email)
        self.hide_keyboard_if_display()
        self.save_contact()

    @TestLogger.log('等待页面加载')
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        self.wait_until(
            condition=lambda d: self._is_element_present(self.__locators['输入姓名'])
        )

    @TestLogger.log("更改手机号码")
    def change_mobile_number(self,text='13800138005'):
        return self.input_text(self.__locators["电话号码"],text)
