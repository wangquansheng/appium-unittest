from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class CreateGroupNamePage(BasePage):
    """创建群聊名称页面"""
    ACTIVITY = 'com.cmicc.module_message.ui.activity.EditGroupPageActivity'

    __locators = {
        'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
        'android:id/content': (MobileBy.ID, 'android:id/content'),
        '删除': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_del'),
        '群聊名输入框': (MobileBy.ID, 'com.chinasofti.rcs:id/et_group_name'),
        '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_sure'),
        '为你的群创建一个群名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_expanded'),
    }

    @TestLogger.log()
    def input_group_name(self, group_name):
        """输入群聊名称"""
        self.input_text(self.__class__.__locators["群聊名输入框"], group_name)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log('检查当前搜索框内容')
    def assert_current_search_keyword_is(self, keyword):
        """检查当前搜索框内容"""
        self.element_text_should_be(self.__locators['群聊名输入框'], keyword)
        return self
