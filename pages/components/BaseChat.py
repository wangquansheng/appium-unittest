from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class BaseChatPage(BasePage):
    """聊天基类抽取"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/iv_bkg': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_bkg'),
                  'com.chinasofti.rcs:id/input_and_menu': (MobileBy.ID, 'com.chinasofti.rcs:id/input_and_menu'),
                  'com.chinasofti.rcs:id/ll_text_input': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_text_input'),
                  'com.chinasofti.rcs:id/layout_for_message': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_for_message'),
                  'com.chinasofti.rcs:id/ll_rich_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_rich_panel'),
                  '选择图片': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_pic'),
                  '选择相机': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_take_photo'),
                  '选择名片': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_profile'),
                  '选择gif': (MobileBy.ID, 'com.chinasofti.rcs:id/rel_gif'),
                  '选择更多': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'),
                  'com.chinasofti.rcs:id/input_divider_inside': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/input_divider_inside'),
                  'com.chinasofti.rcs:id/input_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/input_layout'),
                  'com.chinasofti.rcs:id/fl_edit_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_edit_panel'),
                  '说点什么...': (MobileBy.ID, 'com.chinasofti.rcs:id/et_message'),
                  'com.chinasofti.rcs:id/ib_expression': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression'),
                  '语音按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_audio'),
                  '发送按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_send'),
                  'com.chinasofti.rcs:id/ib_record_red_dot': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_record_red_dot'),
                  # 消息长按弹窗
                  '收藏': (MobileBy.XPATH, "//*[contains(@text, '收藏')]"),
                  '转发': (MobileBy.XPATH, "//*[contains(@text, '转发')]"),
                  '撤回': (MobileBy.XPATH, "//*[contains(@text, '撤回')]"),
                  '转为短信发送': (MobileBy.XPATH, "//*[contains(@text, '转为短信发送')]"),
                  '删除': (MobileBy.XPATH, "//*[contains(@text, '删除')]"),
                  '复制': (MobileBy.XPATH, "//*[contains(@text, '复制')]"),
                  '多选': (MobileBy.XPATH, "//*[contains(@text, '多选')]"),
                  # 撤回消息时的弹窗
                  '我知道了': (MobileBy.XPATH, "//*[contains(@text, '知道了')]"),
                  # 用户须知
                  '用户须知': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_title'),
                  '我已阅读': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_check'),
                  '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_btn_ok'),
                  # 在聊天会话页面点击不可阅读文件时的弹窗
                  '打开方式': (MobileBy.XPATH, "//*[contains(@text,'方式')] | //*[contains(@text,'打开')]"),
                  '取消': (MobileBy.ID, 'android:id/button2'),
                  # 位置信息
                  '深圳市龙岗区交叉口': (MobileBy.ID, 'com.chinasofti.rcs:id/lloc_famous_address_text'),
                  # 消息图片
                  '消息图片': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_image'),
                  # 消息视频
                  '消息视频': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_video_time'),
                  '视频播放按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/video_play'),
                  '视频关闭按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_close'),
                  # 打开位置页面元素
                  "导航按钮": (MobileBy.ID, 'com.chinasofti.rcs:id/location_nativ_btn'),
                  # 打开gif图片后元素
                  "gif图片元素列表": (MobileBy.ID, 'com.chinasofti.rcs:id/stickers_container'),
                  "gif群聊会话中的元素": (MobileBy.ID, 'com.chinasofti.rcs:id/layout_loading'),
                  "gif趣图搜索框": (MobileBy.ID, 'com.chinasofti.rcs:id/et_message'),
                  "关闭gif趣图聊天框": (MobileBy.ID, 'com.chinasofti.rcs:id/iv_cancel_gif'),
                  # 消息发送失败 重发弹窗
                  "是否重发该条信息": (MobileBy.ID, 'com.chinasofti.rcs:id/dialog_message'),
                  "确定重发": (MobileBy.XPATH, '//*[@text="确定"]'),
                  "取消重发": (MobileBy.XPATH, '//*[@text="取消"]'),
                  "发送失败icon": (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_send_failed'),
                  # 消息文件
                  "文件名": (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_name'),
                  "文件大小": (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_size'),
                  '消息文本内容': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  "粘贴": (MobileBy.XPATH, '//*[@text="粘贴"]'),
                  '打开表情': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression'),
                  '关闭表情': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_expression'),
                  '表情id': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_expression_image'),
                  '表情集选择栏': (MobileBy.ID, 'com.chinasofti.rcs:id/lltButton'),
                  '表情集选择栏btn1': (MobileBy.ID, 'com.chinasofti.rcs:id/first_emoji'),
                  '表情集选择栏btn2': (MobileBy.ID, 'com.chinasofti.rcs:id/sec_emoji'),
                  '翻页小圆点': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/pcv_expression"]/android.widget.ImageView'),
                  '删除表情按钮': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iv_expression_image" and contains(@text,"删除")]'),
                  '短信编辑': (MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'),
                  '发送': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
                  '退出短信': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_exitsms'),
                  '发送短信': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'),
                  #预览文件页面
                  '预览文件标题': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  '预览文件-更多':(MobileBy.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.ImageView'),
                  '预览文件-转发': (MobileBy.XPATH, "//*[contains(@text, '转发')]"),
                  '预览文件-收藏': (MobileBy.XPATH, "//*[contains(@text, '收藏')]"),
                  '其他应用打开': (MobileBy.XPATH, "//*[contains(@text, '其他应用打开')]"),
                  "未读消息气泡": (MobileBy.ID, "com.chinasofti.rcs:id/rnMessageBadge"),
                  '视频消息': (MobileBy.ID, 'com.chinasofti.rcs:id/video_thumb')
                  }

    @TestLogger.log('文件是否存在')
    def is_element_present_file(self):
        return self._is_element_present(self.__locators['文件名'])

    @TestLogger.log()
    def is_msg_send_fail(self):
        """消息是否发送失败"""
        return self._is_element_present(self.__class__.__locators['发送失败icon'])

    @TestLogger.log()
    def repeat_send_msg(self):
        """重发消息"""
        self.click_element(self.__class__.__locators['发送失败icon'])

    @TestLogger.log()
    def click_sure_repeat_msg(self):
        """点击 确定 重发消息"""
        self.click_element(self.__class__.__locators['确定重发'])

    @TestLogger.log()
    def click_not_repeat_msg(self):
        """点击 取消 重发消息"""
        self.click_element(self.__class__.__locators['取消重发'])

    @TestLogger.log()
    def click_addr_info(self):
        """点击位置信息"""
        self.click_element(self.__class__.__locators["深圳市龙岗区交叉口"])

    @TestLogger.log()
    def wait_for_location_page_load(self, timeout=8, auto_accept_alerts=True):
        """点击位置信息后，等待位置页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/location_title'))
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log()
    def click_nav_btn(self):
        """点击位置页面右下角导航按钮"""
        self.click_element(self.__class__.__locators['导航按钮'])

    @TestLogger.log()
    def click_i_have_read(self):
        """点击我已阅读"""
        self.click_element(self.__class__.__locators["我已阅读"])
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def collection_file(self, file):
        """收藏文件"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)
        self.click_element(self.__class__.__locators['收藏'])

    @TestLogger.log()
    def forward_file(self, file):
        """转发文件"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)
        time.sleep(3)
        self.click_element(self.__class__.__locators['转发'])

    @TestLogger.log()
    def forward_pic(self):
        """转发图片消息"""
        el = self.get_element(self.__class__.__locators['消息图片'])
        self.press(el)
        self.click_element(self.__class__.__locators['转发'])

    @TestLogger.log()
    def forward_video(self):
        """转发视频消息"""
        el = self.get_element(self.__class__.__locators['消息视频'])
        self.press(el)
        self.click_element(self.__class__.__locators['转发'])

    @TestLogger.log()
    def delete_mess(self, mess):
        """删除消息"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % mess))
        self.press(el)
        self.click_element(self.__class__.__locators['删除'])

    @TestLogger.log()
    def click_delete(self):
        """点击删除"""
        self.click_element(self.__class__.__locators['删除'])
        time.sleep(1)

    @TestLogger.log()
    def click_forward(self):
        """点击转发"""
        self.click_element(self.__class__.__locators['转发'])

    @TestLogger.log()
    def click_collection(self):
        """点击收藏"""
        self.click_element(self.__class__.__locators['收藏'])

    @TestLogger.log()
    def click_recall(self):
        """点击撤回"""
        self.click_element(self.__class__.__locators['撤回'])

    @TestLogger.log()
    def recall_mess(self, mess):
        """撤回消息"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % mess))
        self.press(el)
        self.click_element(self.__class__.__locators['撤回'])

    @TestLogger.log()
    def if_exist_i_know_click(self):
        """撤回消息时，弹窗处理，点击 我知道了"""
        time.sleep(2)
        if self._is_element_present(self.__class__.__locators["我知道了"]):
            self.click_element(self.__class__.__locators["我知道了"])

    @TestLogger.log()
    def click_i_know(self):
        """撤回消息时，弹窗处理，点击 我知道了"""
        self.click_element(self.__class__.__locators["我知道了"])

    @TestLogger.log()
    def send_for_sms(self, mess):
        """转为短信发送"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % mess))
        self.press(el)
        self.click_element(self.__class__.__locators['转为短信发送'])

    @TestLogger.log()
    def press_mess(self, mess):
        """长按消息"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % mess))
        self.press(el)

    @TestLogger.log()
    def press_pic(self):
        """长按图片"""
        el = self.get_element(self.__class__.__locators['消息图片'])
        self.press(el)
        time.sleep(1)

    @TestLogger.log()
    def press_video(self):
        """长按视频"""
        el = self.get_element(self.__class__.__locators['消息视频'])
        self.press(el)

    @TestLogger.log()
    def click_pic(self):
        """点击选择图片"""
        self.click_element(self.__class__.__locators["选择图片"])

    @TestLogger.log()
    def click_take_photo(self):
        """点击选择相机"""
        self.click_element(self.__class__.__locators["选择相机"])

    @TestLogger.log()
    def click_name_card(self):
        """点击选择名片"""
        self.click_element(self.__class__.__locators["选择名片"])

    @TestLogger.log()
    def click_free_msg(self):
        """点击免费短信"""
        self.click_element(self.__class__.__locators["选择名片"])

    @TestLogger.log()
    def click_gif(self):
        """点击选择gif"""
        self.click_element(self.__class__.__locators["选择gif"])
        time.sleep(1)

    @TestLogger.log()
    def click_more(self):
        """点击选择更多 +"""
        self.click_element(self.__class__.__locators["选择更多"])
        time.sleep(1)

    @TestLogger.log()
    def is_open_more(self):
        """是否打开 更多+ (通过判断是否有位置元素来判断是否有打开 更多+)"""
        els = self.get_elements((MobileBy.XPATH, '//*[@text="位置"]'))
        return len(els) > 0

    @TestLogger.log()
    def input_message(self, message):
        """输入聊天信息"""
        self.input_text(self.__class__.__locators["说点什么..."], message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def input_free_message(self, message):
        """输入短信信息"""
        self.input_text(self.__class__.__locators["短信编辑"], message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def get_input_message(self):
        """获取输入框的信息"""
        el = self.get_element(self.__class__.__locators["说点什么..."])
        return el.text

    @TestLogger.log()
    def get_name_card(self):
        """获取个人卡名信息"""
        el = self.get_element([MobileBy.ID, 'com.chinasofti.rcs:id/tv_card_name'])
        return el.text

    @TestLogger.log()
    def get_file_info(self, locator):
        """获最近一次发送文件信息"""
        el = self.get_elements(self.__class__.__locators[locator])
        el = el[-1]
        return el.text

    @TestLogger.log()
    def get_location(self):
        """获最近一次发送位置信息"""
        el = self.get_elements(self.__class__.__locators["深圳市龙岗区交叉口"])
        el = el[-1]
        return el.text

    @TestLogger.log()
    def send_message(self):
        """发送聊天信息"""
        self.click_element(self.__class__.__locators["发送按钮"])
        time.sleep(1)

    @TestLogger.log()
    def page_should_contain_audio_btn(self):
        """语音按钮检查"""
        self.page_should_contain_element(self.__locators["语音按钮"])

    @TestLogger.log()
    def page_should_contain_send_btn(self):
        """发送按钮检查"""
        self.page_should_contain_element(self.__locators["发送按钮"])

    @TestLogger.log()
    def click_send_btn(self):
        """点击发送按钮"""
        self.click_element(self.__locators["发送按钮"])

    @TestLogger.log()
    def click_audio_btn(self):
        """点击语音按钮"""
        self.click_element(self.__class__.__locators["语音按钮"])

    @TestLogger.log()
    def click_back(self):
        """点击返回按钮"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def is_exist_undisturb(self):
        """是否存在消息免打扰标志"""
        return self._is_element_present(self.__class__.__locators["消息免打扰"])

    @TestLogger.log()
    def is_exist_dialog(self, timeout=3, auto_accept_alerts=False):
        """是否存在 用户须知 弹框"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["用户须知"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def open_file_in_chat_page(self, file):
        """在聊天会话页面打开文件"""
        self.click_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))

    @TestLogger.log()
    def wait_for_open_file(self, timeout=8, auto_accept_alerts=True):
        """等待打开文件页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present((MobileBy.ID, 'com.chinasofti.rcs:id/menu'))
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log()
    def click_back_in_open_file_page(self):
        """在打开文件页面点击返回"""
        try:
            self.click_element((MobileBy.ID, "com.chinasofti.rcs:id/back"))
        except:
            self.click_element(self.__class__.__locators['返回'])

    @TestLogger.log()
    def wait_for_call_sys_app_page(self, timeout=8, auto_accept_alerts=True):
        """等待调起系统应用页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators['打开方式'])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log()
    def click_cancle(self):
        """点击取消"""
        self.click_element(self.__class__.__locators['取消'])

    @TestLogger.log()
    def play_video(self):
        """在聊天会话页面点击视频播放"""
        self.click_element(self.__class__.__locators['视频播放按钮'], default_timeout=30)

    @TestLogger.log()
    def close_video(self):
        """关闭视频播放"""
        self.click_element(self.__class__.__locators['视频关闭按钮'])

    @TestLogger.log()
    def wait_for_play_video_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待视频播放页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators['视频关闭按钮'])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log()
    def wait_for_play_video_button_load(self, timeout=8, auto_accept_alerts=True):
        """等待视频播放页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators['视频播放按钮'])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log()
    def wait_for_gif_ele_load(self, timeout=8, auto_accept_alerts=True):
        """等待gif图片页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators['gif图片元素列表'])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)

    @TestLogger.log()
    def send_gif(self):
        """点击选择发送gif图片"""
        self.click_element(self.__class__.__locators['gif图片元素列表'])
        time.sleep(1)

    @TestLogger.log()
    def is_send_gif(self):
        """检验会话窗口是否有gif图片"""
        return self.page_should_contain_element(self.__class__.__locators["gif群聊会话中的元素"])

    @TestLogger.log()
    def press_and_move_down(self, element):
        """按住并向下滑动"""
        # b=self.get_element_attribute(self.__class__.__locators[element],"bounds")
        self.press_and_move_to_down(self.__class__.__locators[element])

    @TestLogger.log()
    def press_and_move_up(self, element):
        """按住并向上滑动"""
        # b=self.get_element_attribute(self.__class__.__locators[element],"bounds")
        self.press_and_move_to_up(self.__class__.__locators[element])

    @TestLogger.log()
    def input_gif(self, message):
        """输入gif搜索框信息"""
        self.input_text(self.__class__.__locators["gif趣图搜索框"], message)
        self.driver.hide_keyboard()
        return self

    @TestLogger.log()
    def is_gif_exist_toast(self):
        """是否有趣图无搜索结果提示"""
        return self.is_toast_exist("无搜索结果，换个热词试试")

    @TestLogger.log()
    def click_cancel_gif(self):
        """点击关闭gif图片框"""
        self.click_element((self.__class__.__locators['关闭gif趣图聊天框']))

    @TestLogger.log()
    def edit_clear(self, text):
        """清楚输入框内容"""
        self.driver.keyevent(123)
        for i in range(0, len(text)):
            self.driver.keyevent(67)

    @TestLogger.log()
    def is_exist_gif_ele(self):
        """当前页面是否有gif框的消息"""
        el = self.get_elements(self.__class__.__locators['gif图片元素列表'])
        return len(el) > 0

    @TestLogger.log()
    def is_exist_video_msg(self):
        """是否存在视频消息"""
        return self._is_element_present(self.__class__.__locators['消息视频'])

    @TestLogger.log()
    def is_exist_video_record(self):
        """是否存在视频消息"""
        return self._is_element_present(self.__class__.__locators['视频消息'])

    @TestLogger.log()
    def is_exist_pic_msg(self):
        """是否存在图片消息"""
        return self._is_element_present(self.__class__.__locators['消息图片'])

    @TestLogger.log()
    def clear_msg(self):
        """清除会话窗的消息"""
        current = 0
        while True:
            current += 1
            if current > 20:
                return
            els = self.get_elements(self.__class__.__locators["消息文本内容"])
            if not els:
                break
            for el in els:
                self.press(el)
                self.click_element(self.__class__.__locators["删除"])

    @TestLogger.log()
    def click_cancel_repeat_msg(self):
        """点击 取消 重发消息"""
        self.click_element(self.__class__.__locators['取消重发'])

    @TestLogger.log()
    def press_input(self):
        """长按文本输入框"""
        el = self.get_element(self.__class__.__locators['说点什么...'])
        self.press(el)

    @TestLogger.log()
    def click_to_do(self, text):
        """根据文本text去点击操作 """
        self.click_element((MobileBy.XPATH, '//*[@text="%s"]' % text))

    @TestLogger.log()
    def is_open_expression(self):
        """是否打开表情"""
        return self._is_element_present(self.__class__.__locators['表情id'])

    @TestLogger.log()
    def open_expression(self):
        """打开表情"""
        self.click_element(self.__class__.__locators["打开表情"])

    @TestLogger.log()
    def close_expression(self):
        """关闭表情"""
        self.click_element(self.__class__.__locators["关闭表情"])

    @TestLogger.log()
    def close_expression2(self):
        """关闭表情"""
        self.click_element(self.__class__.__locators["打开表情"])

    @TestLogger.log()
    def select_expression(self, n=1):
        """选择表情"""
        els = self.get_elements(self.__class__.__locators['表情id'])
        texts = []
        if n > len(els):
            raise AssertionError("表情选择过多，没有 %s 个表情" % n)
        for i in range(n):
            els[i].click()
            texts.append(els[i].text)
        return texts

    @TestLogger.log("页面元素判断")
    def page_should_contains_element(self, locator):
        self.page_should_contain_element(self.__class__.__locators[locator])

    @TestLogger.log()
    def click_msg_input_box(self):
        """点击消息编辑框"""
        self.click_element(self.__locators["说点什么..."])

    @TestLogger.log()
    def delete_expression(self):
        """删除表情"""
        self.click_element(self.__locators["删除表情按钮"])

    @TestLogger.log()
    def is_audio_btn_exit(self):
        """语音按钮是否存在"""
        return self._is_element_present(self.__locators["语音按钮"])

    @TestLogger.log()
    def is_exist_send_button(self):
        """是否存在资费提醒发送按钮"""
        return self._is_element_present(self.__locators["发送"])

    @TestLogger.log()
    def click_send_button(self):
        """点击确认发送按钮"""
        self.click_element(self.__class__.__locators["发送"])

    @TestLogger.log()
    def is_exist_exit_sms(self):
        """是否存在退出短信"""
        return self._is_element_present(self.__locators["退出短信"])

    @TestLogger.log()
    def click_exit_sms(self):
        """点击退出短信"""
        self.click_element(self.__class__.__locators["退出短信"])

    @TestLogger.log()
    def click_send_sms(self):
        """点击发送短信"""
        self.click_element(self.__class__.__locators["发送短信"])

    @TestLogger.log()
    def click_copy(self):
        """点击复制"""
        self.click_element(self.__class__.__locators["复制"])

    @TestLogger.log()
    def click_multiple_selection(self):
        """点击多选"""
        self.click_element(self.__class__.__locators["多选"])

    @TestLogger.log("检查消息弹框是否有2个按钮")
    def check_element_enabled(self, locator):
        return self._is_enabled(self.__locators[locator])

    @TestLogger.log("点击我已阅读")
    def click_only_i_have_read(self):
        self.click_element(self.__class__.__locators["我已阅读"])

    @TestLogger.log("点击消息确定")
    def click_only_sure_button(self):
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def page_contain_element_more(self):
        """预览文件页面-页面应该包含更多"""
        self.page_should_contain_element(self.__locators["预览文件-更多"])

    @TestLogger.log("点击预览文件页面-更多按钮")
    def click_more_Preview(self):
        self.click_element(self.__class__.__locators["预览文件-更多"])


    @TestLogger.log("点击预览文件页面-转发")
    def click_forward_Preview(self):
        self.click_element(self.__class__.__locators["预览文件-转发"])


    @TestLogger.log("点击预览文件页面-收藏")
    def click_collection_Preview(self):
        self.click_element(self.__class__.__locators["预览文件-收藏"])

    @TestLogger.log("点击其他应用打开")
    def click_other_App_open(self):
        self.click_element(self.__class__.__locators["其他应用打开"])

    @TestLogger.log()
    def get_width_of_msg_of_text(self):
        """获取最近一条聊天记录文本信息框的大小"""
        time.sleep(1)
        els=self.get_element((MobileBy.ID,'com.chinasofti.rcs:id/tv_message'))
        rect=els.rect
        return rect["width"]

    @TestLogger.log()
    def get_width_of_last_msg_of_text(self):
        """获取最近一条聊天记录文本信息框的大小"""
        time.sleep(1)
        el = self.get_elements((MobileBy.ID,'com.chinasofti.rcs:id/tv_message'))[-1]
        rect = el.rect
        return rect["width"]

    @TestLogger.log()
    def click_open_file(self, file):
        """点击打开指定文件"""
        self.click_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
















