from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class FindChatRecordPage(BasePage):
    """查找聊天内容页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageSearchActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_back'),
                  'com.chinasofti.rcs:id/iv_back': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_back'),
                  '输入关键词快速搜索': (MobileBy.ID, 'com.chinasofti.rcs:id/edit_query'),
                  '分类索引': (MobileBy.ID, 'com.chinasofti.rcs:id/text_hint_2'),
                  'com.chinasofti.rcs:id/layout_file_search': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_file_search'),
                  '文件': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_search'),
                  'com.chinasofti.rcs:id/layout_video_img_search': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/layout_video_img_search'),
                  '图片与视频': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_video_img_search'),
                  'com.chinasofti.rcs:id/result_list': (MobileBy.ID, 'com.chinasofti.rcs:id/result_list'),
                  '发送人头像': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
                  '发送人名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_conv_name'),
                  '发送的内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_content'),
                  '发送的时间': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_date'),
                  }

    @TestLogger.log()
    def click_back(self):
        """点击 返回"""
        self.click_element(self.__class__.__locators['返回'])
        time.sleep(1)

    @TestLogger.log()
    def click_file(self):
        """点击 文件"""
        self.click_element(self.__class__.__locators['文件'])
        time.sleep(1)

    @TestLogger.log()
    def click_pic_video(self):
        """点击 图片与视频"""
        self.click_element(self.__class__.__locators['图片与视频'])
        time.sleep(1)

    @TestLogger.log()
    def click_edit_query(self):
        """点击 输入关键词快速搜索"""
        self.click_element(self.__class__.__locators['输入关键词快速搜索'])

    @TestLogger.log()
    def input_search_message(self, message):
        """输入搜索信息"""
        self.input_text(self.__class__.__locators["输入关键词快速搜索"], message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def is_element_exit(self,keyName):
        """判断指定元素是否存在"""
        if self.get_element(self.__class__.__locators[keyName]):
            return True
        else:
            return False

    @TestLogger.log()
    def click_record(self):
        """点击 记录"""
        self.click_element(self.__class__.__locators['发送的内容'])

    @TestLogger.log()
    def wait_for_page_loads(self, timeout=60):
        """等待 页面加载"""
        try:
            self.wait_until(
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["文件"]),
                timeout=timeout
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self