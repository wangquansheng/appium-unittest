from library.core.BasePage import BasePage
from appium.webdriver.common.mobileby import MobileBy
from library.core.TestLogger import TestLogger
import time


class EnterPrisePage(BasePage):
    """团队详细信息"""
    ACTIVITY = 'com.cmicc.module_contact.enterprise.ui.activity.EnterPriseActivity'

    __locators = {
        '更多控件': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_more'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '团队名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
        '团队管理': (MobileBy.ID, 'com.chinasofti.rcs:id/quit_confirm_tv'),
        '解散团队': (MobileBy.ID, 'com.chinasofti.rcs:id/quit_cancel_tv'),
        '联系人名称标签': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name_personal_contactlist'),

    }

    @TestLogger.log("点击返回")
    def click_back_button(self):
        """点击返回"""
        self.click_element(self.__locators['返回'])

    @TestLogger.log("点击更多")
    def click_more(self):
        """点击更多"""
        self.click_element(self.__locators['更多控件'])

    @TestLogger.log("点击团队管理")
    def click_group_mgmt(self):
        """点击团队管理"""
        self.click_element(self.__locators['团队管理'])
        time.sleep(10)

    @TestLogger.log("点击解散团队")
    def click_dissolve_group(self):
        """点击解散团队"""
        self.click_element(self.__locators['解散团队'])

    @TestLogger.log("查找是否存在某联系人")
    def search_user_is_exsit(self, user_name):
        """查找是否存在某联系人"""
        i = 0
        while True:
            el = self.get_elements(self.__locators['联系人名称标签'])
            if len(el) < 1:
                return False
            current_el = el[len(el) - 1].text
            for e in el:
                if e.text == user_name:
                    print("搜索到名称为:%s的联系人" % user_name)
                    return True
            if i != 0:
                if tmp_last_el == current_el:
                    print("已到达最尾页")
                    return False
            tmp_last_el = current_el
            self.page_up()
            i = i + 1

