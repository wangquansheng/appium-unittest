from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class RemoveMember(BasePage):
    """打开的网页消息界面"""
    # ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.QRCodeActivity'

    __locators = {
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
        'OK': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
        '已解散': (MobileBy.XPATH, '//android.widget.TextView[@text="该群已解散"]'),

    }

    @TestLogger.log('等待加载完毕')
    def wait_for_loading_animation_end(self):
        self.mobile.wait_until(
            condition=lambda d: self.get_element(self.__locators['com.chinasofti.rcs:id/title']),
            timeout=60
        )

    @TestLogger.log('返回')
    def click_back(self):
        self.click_element(self.__locators['返回'])

    @TestLogger.log('确定')
    def click_sure(self):
        self.click_element(self.__locators['确定'])

    @TestLogger.log('确定')
    def click_ok(self):
        self.click_element(self.__locators['OK'])

    @TestLogger.log('选择一个成员')
    def select_member_by_name(self, name):
        # self.click_element(MobileBy.XPATH, '//android.widget.TextView[@text={}]' , name)
        self.driver.find_elements(MobileBy.XPATH, '//android.widget.TextView[@text="%s"]' % name)[-1].click()

    @TestLogger.log()
    def is_element_exist(self, text):
        """当前页面是否包含此元素"""
        return self._is_element_present(self.__class__.__locators['已解散'])

    @TestLogger.log()
    def delete_all_members(self):
        """删除所有成员"""
        locator = (MobileBy.ID, 'com.chinasofti.rcs:id/contact_list_item')
        import time
        time.sleep(1)
        for el in self.get_elements(locator):
            el.click()
            time.sleep(1)
        self.click_element(self.__locators['确定'])
        time.sleep(1)
        self.click_element(self.__locators['OK'])
        time.sleep(1)
