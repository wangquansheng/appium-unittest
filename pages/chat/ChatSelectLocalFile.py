from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatSelectLocalFilePage(BasePage):
    """选择本地文件页面聊天"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ChooseLocalFileActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                  'SD卡内存': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
                  '列表容器': (MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'),
                  'com.chinasofti.rcs:id/lv_choose': (MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'),
                  'com.chinasofti.rcs:id/rl_sd_file': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_sd_file'),
                  'com.chinasofti.rcs:id/iv_icon_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_icon_layout'),
                  'com.chinasofti.rcs:id/iv_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_icon'),
                  'sogou': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  'Xiaomi': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  '2018-11-09 11-06-18-722582.log': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  '410.0B': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_size'),
                  '10:18': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_create_time'),
                  'com.chinasofti.rcs:id/cb_choose_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/cb_choose_icon'),
                  'ReleaseChannel.txt': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  '14.0B': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_size'),
                  '11-09 10:07': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_create_time'),
                  'test_video.mp4': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  '2.2M': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_size'),
                  '文件大小': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_size'),
                  '选择文件大小': (MobileBy.XPATH, "//android.widget.CheckBox[@checked='true']/preceding-sibling::android.widget.RelativeLayout/*[@resource-id='com.chinasofti.rcs:id/textview_file_size']"),
                  '10:19': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_create_time'),
                  'txt文件': (MobileBy.XPATH, '//*[contains(@text,".txt")]'),
                  'jpg文件': (MobileBy.XPATH, '//*[contains(@text,".jpg")]'),
                  'xlsx文件': (MobileBy.XPATH, '//*[contains(@text,".xlsx")]'),
                  'pdf文件': (MobileBy.XPATH, '//*[contains(@text,".pdf")]'),
                  'mp4文件': (MobileBy.XPATH, '//*[contains(@text,".mp4")]'),
                  'docx文件': (MobileBy.XPATH, '//*[contains(@text,".docx")]'),
                  'avi文件': (MobileBy.XPATH, '//*[contains(@text,".avi")]'),
                  'BPG文件': (MobileBy.XPATH, '//*[contains(@text,".BPG")]'),
                  'com.chinasofti.rcs:id/rl_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_panel'),
                  '已选: 2.2M': (MobileBy.XPATH, '//*[contains(@text,"已选:")]'),
                  '发送': (MobileBy.ID, 'com.chinasofti.rcs:id/button_send'),
                  # 视频选择页面
                  '视频': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  # 照片选择页面
                  '照片': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  # 音乐选择页面
                  '音乐': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_file_name'),
                  }
    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log("下一页")
    def page_up(self):
        """向上滑动一页"""
        self.swipe_by_direction(self.__locators['列表容器'], 'up')

    @TestLogger.log()
    def find_element_by_swipe(self, locator, times=10):
        """找不到元素就滑动"""
        if self._is_element_present(locator):
            return self.get_element(locator)
        else:
            c = 0
            while c < times:
                self.page_up()
                if self._is_element_present(locator):
                    return self.get_element(locator)
                c += 1
            return None

    @TestLogger.log()
    def get_file_size(self):
        """获取选择的文件大小"""
        size_el = self.get_element(self.__class__.__locators['选择文件大小'])
        return size_el.text

    @TestLogger.log()
    def get_selected_file_size(self):
        """获取已选文件大小信息"""
        el = self.get_element(self.__class__.__locators['已选: 2.2M'])
        return el.text

    @TestLogger.log()
    def select_file(self, file_type):
        """选择文件"""
        el = self.find_element_by_swipe(self.__class__.__locators[file_type])
        if el:
            el.click()
            return el
        else:
            print("在SD卡根目录无%s类型的文件，请预置相应类型文件" % file_type)

    @TestLogger.log()
    def send_btn_is_enabled(self):
        """获取发送按钮状态是否可点击"""
        return self._is_enabled(self.__class__.__locators["发送"])

    @TestLogger.log()
    def click_send(self, timeout=4):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])
        time.sleep(timeout)
