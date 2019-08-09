from library.core.BasePage import BasePage
from appium.webdriver.common.mobileby import MobileBy
from library.core.TestLogger import TestLogger


class EnterPriseHomeListPage(BasePage):
    """团队列表"""
    ACTIVITY = 'com.cmicc.module_contact.enterprise.ui.activity.EnterPriseHomeListActivity'

    __locators = {
        '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_back_actionbar'),
        '全部团队': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title_actionbar'),
        '团队名称标签': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'),


    }

    @TestLogger.log("点击返回")
    def click_back_button(self):
        """点击返回"""
        self.click_element(self.__locators['返回'])

    @TestLogger.log("查找是否存在某团队")
    def search_group_is_exsit(self, team_name):
        """查找是否存在某团队"""
        i = 0
        while True:
            el = self.get_elements(self.__locators['团队名称标签'])
            if len(el) < 1:
                return False
            current_el = el[len(el)-1].text
            for e in el:
                if e.text == team_name:
                    print("搜索到名称为:%s的团队" % team_name)
                    return True
            if i != 0:
                if tmp_last_el == current_el:
                    print("已到达最尾页")
                    return False
            tmp_last_el = current_el
            self.page_up()
            i = i + 1

    @TestLogger.log("查找并点击某个团队")
    def click_the_group(self, team_name):
        """查找并点击某个团队"""
        if not self.search_group_is_exsit(team_name):
            return False
        tmp_path = "//android.widget.TextView[@text='%s']" % team_name
        tmp = (MobileBy.XPATH, tmp_path)
        self.click_element(tmp)
        return True
