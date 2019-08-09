from library.core.BasePage import BasePage
from appium.webdriver.common.mobileby import MobileBy
from library.core.TestLogger import TestLogger
import time


class AddTeamContacrH5Page(BasePage):
    """团队详细信息"""
    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '添加联系人': (MobileBy.ID, 'c_nav_contact_add'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),

    }

    @TestLogger.log("点击返回")
    def click_back_button(self):
        """点击返回"""
        self.click_element(self.__locators['返回'])

    @TestLogger.log("点击添加联系人")
    def click_add_contacter(self):
        """点击添加联系人"""
        self.click_text('添加联系人')

    @TestLogger.log("点击手动输入添加")
    def click_manually_add(self):
        """点击手动输入添加"""
        self.click_text('手动输入添加')

    @TestLogger.log("点击从手机通讯录添加")
    def click_add_contact_by_phone(self):
        """点击从手机通讯录添加"""
        self.click_text('从手机通讯录添加')

    @TestLogger.log("添加联系人信息")
    def add_contacter(self, name, number):
        """添加联系人信息"""
        self.click_add_contact_by_phone()

    @TestLogger.log("添加联系人信息")
    def input_team_name(self, name):
        """添加联系人信息"""
        self.click_text('团队名称')
        self.input_text((MobileBy.ID, "qy_name"), name)

