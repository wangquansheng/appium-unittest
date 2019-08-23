from selenium.webdriver.remote.webelement import WebElement
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException

from library.core.TestLogger import TestLogger
from pages.message import ChatWindowPage
from pages.components.BaseChat import BaseChatPage
import time


class SingleChatPage(BaseChatPage):
    """单聊会话页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.MessageDetailActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  'com.chinasofti.rcs:id/back': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back_arrow'),
                  'axzq': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  '打电话图标': (MobileBy.ID, 'com.chinasofti.rcs:id/action_call'),
                  '设置': (MobileBy.ID, 'com.chinasofti.rcs:id/action_setting'),
                  'com.chinasofti.rcs:id/view_line': (MobileBy.ID, 'com.chinasofti.rcs:id/view_line'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/message_editor_layout': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/message_editor_layout'),
                  'com.chinasofti.rcs:id/rv_message_chat': (MobileBy.ID, 'com.chinasofti.rcs:id/rv_message_chat'),
                  'com.chinasofti.rcs:id/linearLayout': (MobileBy.ID, 'com.chinasofti.rcs:id/linearLayout'),
                  '10:57': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
                  'com.chinasofti.rcs:id/ll_msg': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_msg'),
                  'com.chinasofti.rcs:id/iv_file_icon': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_file_icon'),
                  '67.0KB': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_size'),
                  '和飞信测试用例.xlsx': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_name'),
                  'com.chinasofti.rcs:id/img_message_down_file': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/img_message_down_file'),
                  '对方离线，已提醒': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_has_read'),
                  'com.chinasofti.rcs:id/iv_send_status': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_send_status'),
                  'com.chinasofti.rcs:id/imgae_fl': (MobileBy.ID, 'com.chinasofti.rcs:id/imgae_fl'),
                  'com.chinasofti.rcs:id/layout_loading': (MobileBy.ID, 'com.chinasofti.rcs:id/layout_loading'),
                  'com.chinasofti.rcs:id/imageview_msg_image': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_image'),
                  'hello': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_message'),
                  'com.chinasofti.rcs:id/svd_head': (MobileBy.ID, 'com.chinasofti.rcs:id/svd_head'),
                  '选择短信': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_btn'),
                  '语音消息体': (MobileBy.ID, 'com.chinasofti.rcs:id/img_audio_play_icon'),
                  '消息图片': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_image'),
                  '消息视频': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_video_time'),
                  '选择照片': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_pic'),
                  '短信发送按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_sms_send'),
                  '短信输入框': (MobileBy.ID, 'com.chinasofti.rcs:id/et_sms'),
                  '短信资费提醒': (MobileBy.XPATH, '//*[@text="资费提醒"]'),
                  "文本输入框": (MobileBy.ID, "com.chinasofti.rcs:id/et_message"),
                  "文本发送按钮": (MobileBy.ID, "com.chinasofti.rcs:id/ib_send"),
                  "语音发送按钮": (MobileBy.ID, "com.chinasofti.rcs:id/ib_audio"),
                  "消息免打扰图标": (MobileBy.ID, "com.chinasofti.rcs:id/iv_slient"),
                  '重发按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_send_failed'),
                  '确定': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_ok'),
                  '取消': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_cancel'),
                  '文件名称': (MobileBy.ID, 'com.chinasofti.rcs:id/textview_file_name'),
                  '和飞信电话（免费）': (MobileBy.XPATH, '//*[@text="和飞信电话（免费）"]'),
                  '飞信电话（免费）': (MobileBy.XPATH, '//*[@text="飞信电话（免费）"]'),
                  '名片消息名称': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_card_name'),
                  '更多': (MobileBy.ID, 'com.chinasofti.rcs:id/ib_more'),
                  '选择名片': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iocn_tv" and @text="名片"]'),
                  '视频播放': (MobileBy.ID, 'com.chinasofti.rcs:id/video_play'),
                  '关闭视频': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_close'),
                  '消息文件': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_msg'),
                  '文件下载图标': (MobileBy.ID, 'com.chinasofti.rcs:id/img_message_down_file'),
                  '收藏': (MobileBy.XPATH, "//*[contains(@text, '收藏')]"),
                  '转发': (MobileBy.XPATH, "//*[contains(@text, '转发')]"),
                  '删除': (MobileBy.XPATH, "//*[contains(@text, '删除')]"),
                  '撤回': (MobileBy.XPATH, "//*[contains(@text, '撤回')]"),
                  '多选': (MobileBy.XPATH, "//*[contains(@text, '多选')]"),
                  '复制': (MobileBy.XPATH, "//*[contains(@text, '复制')]"),
                  '编辑': (MobileBy.XPATH, "//*[contains(@text, '编辑')]"),
                  '消息位置': (MobileBy.ID, 'com.chinasofti.rcs:id/lloc_famous_address_text'),
                  '文件': ('id', 'com.chinasofti.rcs:id/ib_file'),
                  '下拉菜单箭头': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/drop_down_image"]'),
                  '下拉菜单选项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/albumTitle"]'),
                  '列表': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/recyclerView_gallery"]'),
                  '列表项': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/recyclerView_gallery"]/*['
                                          '@resource-id="com.chinasofti.rcs:id/rl_img"]'),
                  '选择': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iv_select"]'),
                  '原图': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/cb_original_photo"]'),
                  '预览': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_preview"]'),
                  '发送失败标识': (MobileBy.ID, 'com.chinasofti.rcs:id/imageview_msg_send_failed'),
                  '保存图片': (MobileBy.XPATH, "//*[contains(@text, '保存图片')]"),
                  '发送': (MobileBy.ID, "com.chinasofti.rcs:id/button_send"),
                  '文件列表': (MobileBy.ID, "com.chinasofti.rcs:id/lv_choose"),
                  '文件项': (MobileBy.ID, "com.chinasofti.rcs:id/rl_sd_file"),
                  '文件名称项': (MobileBy.ID, "com.chinasofti.rcs:id/tv_file_name"),
                  '关闭表情': (MobileBy.ID, "com.chinasofti.rcs:id/ib_expression"),
                  }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待单聊会话页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["打电话图标"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_sms(self):
        """点击选择短信"""
        self.click_element(self.__class__.__locators["选择短信"])

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在单聊会话页面"""
        el = self.get_elements(self.__locators['打电话图标'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def click_setting(self):
        """点击 设置"""
        self.click_element(self.__class__.__locators['设置'])
        time.sleep(1)

    @TestLogger.log()
    def is_audio_exist(self):
        """是否存在语音消息"""
        return self._is_element_present(self.__class__.__locators['语音消息体'])

    def is_exist_msg_videos(self):
        """当前页面是否有发视频消息"""
        el = self.get_elements(self.__class__.__locators['消息视频'])
        return len(el) > 0

    def is_exist_msg_image(self):
        """当前页面是否有发图片消息"""
        el = self.get_elements(self.__class__.__locators['消息图片'])
        return len(el) > 0

    @TestLogger.log()
    def click_picture(self):
        """点击选择照片"""
        self.click_element(self.__class__.__locators["选择照片"])

    @TestLogger.log()
    def is_exist_forward(self):
        """是否存在消息已转发"""
        return self.is_toast_exist("已转发")

    @TestLogger.log()
    def is_enabled_sms_send_btn(self):
        """短信发送按钮是否可点击"""
        return self._is_enabled(self.__class__.__locators['短信发送按钮'])

    @TestLogger.log()
    def input_sms_message(self, message):
        """输入短信信息"""
        self.input_text(self.__class__.__locators["短信输入框"], message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def send_sms(self):
        """发送短信"""
        self.click_element(self.__class__.__locators["短信发送按钮"])
        time.sleep(1)

    @TestLogger.log()
    def is_present_sms_fee_remind(self, timeout=3, auto_accept_alerts=True):
        """是否出现短信资费提醒窗"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["短信资费提醒"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def input_text_message(self, message):
        """输入文本信息"""
        self.input_text(self.__class__.__locators["文本输入框"], message)
        try:
            self.driver.hide_keyboard()
        except:
            pass
        return self

    @TestLogger.log()
    def send_text(self):
        """发送文本"""
        self.click_element(self.__class__.__locators["文本发送按钮"])
        time.sleep(1)

    @TestLogger.log()
    def send_text_if_not_exist(self, mess):
        """发送消息如果当前页不存在该消息"""
        if not self._is_element_present((MobileBy.XPATH, '//*[@text ="%s"]' % mess)):
            self.input_text_message(mess)
            self.send_text()

    @TestLogger.log()
    def is_exist_no_disturb_icon(self):
        """是否存在消息免打扰图标"""
        return self._is_element_present(self.__class__.__locators["消息免打扰图标"])

    @TestLogger.log()
    def is_exist_file_by_type(self, file_type):
        """是否存在指定类型文件"""
        locator = (
            MobileBy.XPATH,
            '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and contains(@text,"%s")]' % file_type)
        return self._is_element_present(locator)

    @TestLogger.log()
    def is_exist_msg_send_failed_button(self):
        """是否存在重发按钮"""
        return self._is_element_present(self.__class__.__locators["重发按钮"])

    @TestLogger.log()
    def click_msg_send_failed_button(self, number):
        """点击重发按钮"""
        if self._is_element_present(self.__class__.__locators['重发按钮']):
            els = self.get_elements(self.__class__.__locators["重发按钮"])
            els[number].click()

    @TestLogger.log()
    def click_sure(self):
        """点击确定"""
        self.click_element(self.__class__.__locators["确定"])

    @TestLogger.log()
    def click_cancel(self):
        """点击取消"""
        self.click_element(self.__class__.__locators["取消"])

    @TestLogger.log()
    def is_exist_cancel_button(self):
        """是否存在资费提醒取消按钮"""
        return self._is_element_present(self.__locators["取消"])

    @TestLogger.log()
    def is_exist_send_audio_button(self):
        """是否存在语音发送按钮"""
        return self._is_element_present(self.__locators["语音发送按钮"])

    @TestLogger.log()
    def is_exist_send_txt_button(self):
        """是否存在文本发送按钮"""
        return self._is_element_present(self.__locators["文本发送按钮"])

    @TestLogger.log("页面元素判断")
    def is_exist_element(self, locator):
        self.page_should_contain_element(self.__class__.__locators[locator])

    @TestLogger.log()
    def close_chat_expression(self):
        """关闭表情"""
        self.click_element(self.__class__.__locators["关闭表情"])

    @TestLogger.log()
    def get_current_file_name(self):
        """获取刚刚发送的文件名称"""
        els = self.get_elements(self.__class__.__locators["文件名称"])
        file_name = els[-1].text
        return file_name

    @TestLogger.log("确认短信弹框页面是否有两个按键")
    def check_cmcc_msg_two_button(self):
        btn_list = [('id','com.chinasofti.rcs:id/sure_btn'),('id','com.chinasofti.rcs:id/cancle_btn')]
        for btn in btn_list:
            if not self._is_enabled(btn):
                return False
        return True
    @TestLogger.log()
    def click_action_call(self):
        """点击打电话图标"""
        self.click_element(self.__class__.__locators["打电话图标"])

    @TestLogger.log()
    def press_card_name_by_number(self, number):
        """按压名片消息"""
        els = self.get_elements(self.__class__.__locators["名片消息名称"])
        self.press(els[number])

    @TestLogger.log()
    def click_card_name_by_number(self, number):
        """点击名片消息"""
        els = self.get_elements(self.__class__.__locators["名片消息名称"])
        els[number].click()

    @TestLogger.log()
    def click_more(self):
        """点击更多富媒体按钮"""
        self.click_element(self.__class__.__locators["更多"])

    @TestLogger.log()
    def click_profile(self):
        """点击选择名片"""
        self.click_element(self.__class__.__locators["选择名片"])
		
    @TestLogger.log()
    def is_exist_inputtext(self):
        """是否存在消息输入框"""
        return self._is_element_present(self.__class__.__locators["文本输入框"])

    @TestLogger.log()
    def clear_inputtext(self):
        """清空消息输入框"""
        time.sleep(2)
        self.click_element(self.__class__.__locators["短信输入框"])
        el = self.get_element(self.__class__.__locators["短信输入框"])
        el.clear()

    @TestLogger.log()
    def click_hefeixinfree_call(self):
        """点击和飞信电话（免费）"""
        self.click_element(self.__class__.__locators["和飞信电话（免费）"])

    @TestLogger.log()
    def click_hefeixinfree_call_631(self):
        """点击飞信电话（免费）"""
        self.click_element(self.__class__.__locators["飞信电话（免费）"])

    @TestLogger.log()
    def click_back_tubiao(self):
        """点击返回图标"""
        self.click_element(self.__class__.__locators["com.chinasofti.rcs:id/back"])

    @TestLogger.log()
    def click_element_(self, text):
        """点击元素"""
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def press_element_(self, text,times):
        """长按元素"""
        el=self.get_element(self.__class__.__locators[text])
        self.press(el,times)

    @TestLogger.log()
    def is_element_exit_(self, text):
        """指定元素是否存在"""
        return self._is_element_present(self.__class__.__locators[text])

    @TestLogger.log()
    def wait_for_video_load(self, timeout=60, auto_accept_alerts=True):
        """等待群聊视频加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["视频播放"])
            )
        except:
            message = "视频在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_file_load(self, timeout=8, auto_accept_alerts=True):
        """等待文件加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["文件下载图标"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(message)
        return self

    @TestLogger.log()
    def press_message_to_do(self, text):
        """长按指定信息进行操作"""
        el = self.get_element((MobileBy.ID, 'com.chinasofti.rcs:id/lloc_famous_address_text'))
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def press_file_to_do(self, file, text):
        """长按指定文件进行操作"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def click_file(self):
        """点击文件"""
        self.click_element(self.__class__.__locators["文件"])

    @TestLogger.log()
    def press_last_file_to_do(self, text):
        """长按最后一个文件进行操作"""
        el = self.get_elements(('id', 'com.chinasofti.rcs:id/ll_msg'))[-1]
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def press_last_picture_to_do(self, text):
        """长按最后一个图片文件进行操作"""
        el = self.get_elements(('id', 'com.chinasofti.rcs:id/layout_loading'))[-1]
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log()
    def press_last_video_to_do(self, text):
        """长按最后一个视频文件进行操作"""
        el = self.get_elements(('id', 'com.chinasofti.rcs:id/video_thumb'))[-1]
        self.press(el)
        self.click_element(self.__class__.__locators[text])

    @TestLogger.log('切换到指定文件夹')
    def switch_to_given_folder(self, path):
        import re
        if not self.get_elements(self.__locators['下拉菜单选项']):
            self.click_element(self.__locators['下拉菜单箭头'])
        menu_list = ['xpath', '//*[@resource-id="com.chinasofti.rcs:id/list_select"]']
        self.swipe_by_direction(menu_list, 'down', 600)
        menu_item = ['xpath', '//*[@resource-id="com.chinasofti.rcs:id/list_select"]/*']
        for i in self.mobile.list_iterator(menu_list, menu_item):
            del i
            menus = self.get_elements(self.__locators['下拉菜单选项'])
            for menu in menus:
                menu_text = menu.text
                assert re.match(r'.+\(\d+\)', menu_text), r'Assert menu text match Regex:."+\(\d+\)"'
                display_name, total = re.findall(r'(.+)\((\d+)\)', menu_text)[0]
                if len(display_name) > 3:
                    result = re.findall(r'(.+)([.]{3})$', display_name)
                    if result:
                        if path.find(result[0][0]) == 0:
                            menu.click()
                            return result[0][0], int(total)
                    else:
                        if path.find(display_name) == 0:
                            menu.click()
                            return display_name, int(total)
                else:
                    if display_name == path:
                        menu.click()
                        return path, int(total)
        raise NoSuchElementException('下拉菜单没有找到名称为"{}"的目录'.format(path))

    @TestLogger.log('选择指定序号的图片（视频）')
    def select_items_by_given_orders(self, *orders):
        orders = sorted(list(set(orders)))
        offset = 1
        for i in self.mobile.list_iterator(self.__locators['列表'], self.__locators['列表项']):
            if offset in orders:
                if not self.is_list_item_selected(i):
                    el = i.find_element(*self.__locators['选择'])
                    el.click()
                orders.remove(offset)
            offset += 1
            if not orders:
                break

    @TestLogger.log('获取列表项已选状态')
    def is_list_item_selected(self, item):
        if isinstance(item, (list, tuple)):
            item = self.get_element(item)
        elif isinstance(item, WebElement):
            pass
        else:
            raise ValueError('参数类型错误')

        selector = item.find_element(*self.__locators['选择'])
        color = self.get_coordinate_color_of_element(selector, 5, 50, True)
        white = (255, 255, 255, 255)
        blue = (21, 124, 248, 255)
        if color == white:
            # 未选择状态为不透明白色
            return False
        elif color == blue:
            # 已选状态为不透明蓝色
            return True
        else:
            raise RuntimeError('RGBA颜色{}无法识别勾选状态'.format(color))

    @TestLogger.log('点击预览')
    def click_preview(self):
        """点击预览"""
        self.click_element(self.__locators['预览'])

    @TestLogger.log()
    def is_send_sucess(self):
        """当前页面是否有发送失败标识"""
        el = self.get_elements(self.__locators['发送失败标识'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def click_msg_image(self, number):
        """点击图片消息"""
        els = self.get_elements(self.__class__.__locators["消息图片"])
        els[number].click()

    @TestLogger.log()
    def is_exist_picture_edit_page(self):
        """长按消息"""
        for option in ["转发", "编辑", "保存图片"]:
            el = self.get_elements(self.__locators[option])
            if len(el) == 0:
                return False
        return True

    @TestLogger.log()
    def click_edit(self):
        """点击编辑"""
        self.click_element(self.__class__.__locators["编辑"])

    @TestLogger.log()
    def click_original_photo(self):
        """点击原图"""
        self.click_element(self.__class__.__locators["原图"])

    @TestLogger.log()
    def press_last_message_to_do(self, text):
        """长按最后一个文本消息进行操作"""
        el = self.get_elements(('id', 'com.chinasofti.rcs:id/tv_message'))[-1]
        self.press(el)
        self.click_element(self.__class__.__locators[text])

        # (//*[contains(@resource-id,"com.chinasofti.rcs:id/multi_check")])[4]

    @TestLogger.log()
    def click_select_many_messages(self):
        """点击选择多条消息"""
        time.sleep(1)
        self.click_element((MobileBy.XPATH, '(//*[contains(@resource-id,"com.chinasofti.rcs:id/multi_check")])[1]'))
        time.sleep(1)
        self.click_element((MobileBy.XPATH, '(//*[contains(@resource-id,"com.chinasofti.rcs:id/multi_check")])[2]'))
        time.sleep(1)

    @TestLogger.log()
    def send_file_messages(self, path, file_name):
        """单聊发送文件"""
        chatWindowPage = ChatWindowPage()
        for i in range(1, 10):
            chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'down', 600)
        elements = chatWindowPage.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找文件目录
        while len(elements) == 0:
            chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up', 600)
            time.sleep(1)
            elements = chatWindowPage.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % path))
        # 文件系统找文件
        time.sleep(2)
        for i in range(1, 10):
            chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'down', 600)
        elements = chatWindowPage.get_elements(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))

        while len(elements) == 0:
            chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'up')
            time.sleep(1)
            elements = chatWindowPage.get_elements(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/tv_file_name" and @text="%s"]' % file_name))
        # 发送
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)

    @TestLogger.log()
    def re_send_file_messages(self, file_name):
        """单聊转发文件"""
        chatWindowPage = ChatWindowPage()
        file_elements = chatWindowPage.get_elements(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/textview_file_name" and @text="%s"]' % file_name))
        file_elements[0].click()
        # 点击文件右上方的 ... 图标
        chatWindowPage.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/menu"]'))
        chatWindowPage.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/forward"  and @text="转发"]'))
        # 点击联系人名称
        chatWindowPage.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @index="0"]'))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        chatWindowPage.is_toast_exist("已转发")

    @TestLogger.log()
    def search_chat_record_file(self, file_name):
        self.click_element((MobileBy.XPATH,'//*[@text="查找聊天内容"]'))
        self.click_element((MobileBy.XPATH, '//*[@text="文件"]'))
        self.click_element((MobileBy.XPATH, '//*[@text="%s"]' % file_name))

    @TestLogger.log()
    def assert_collect_record_file(self):
        self.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/menu"]'))
        self.click_element((MobileBy.XPATH, '//*[@text="收藏"]'))
        if not self.is_toast_exist("已收藏"):
            raise AssertionError("收藏失败")

    @TestLogger.log()
    def assert_transmit_record_file(self):
        chatWindowPage = ChatWindowPage()
        chatWindowPage.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/menu"]'))
        chatWindowPage.click_element(
            (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/forward"  and @text="转发"]'))
        # 点击联系人名称
        chatWindowPage.click_element(
            (MobileBy.XPATH,
             '//*[@resource-id="com.chinasofti.rcs:id/tv_name" and @index="0"]'))
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/btn_ok" and @text="确定"]'))
        if not self.is_toast_exist("已转发"):
            raise AssertionError("转发失败")

    @TestLogger.log()
    def other_app_open_file(self):
        self.click_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/menu"]'))
        self.click_element((MobileBy.XPATH, '//*[@text="其他应用打开"]'))
        self.click_back_by_android()

    @TestLogger.log()
    def more_select_item(self):
        self.click_element(self.__locators['多选'])

    @TestLogger.log()
    def select_collect_item(self):
        self.click_element(self.__locators['收藏'])

    @TestLogger.log()
    def assert_id_menu_more(self):
        time.sleep(4)
        self.page_should_contain_element((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/menu"]'))

    @TestLogger.log('选择文件目录')
    def select_local_file_directory(self, *file_directory_list):
        name_list = list(file_directory_list)
        self.wait_until(
            condition=lambda d: self._is_element_present((MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text"]'))
        )
        for cont in self.mobile.list_iterator(self.__locators['文件列表'], self.__locators['文件项']):
            name = cont.find_element(*self.__locators['文件名称项']).text
            if name in name_list:
                cont.click()
                name_list.remove(name)
            if not name_list:
                break
        if name_list:
            print('没有找到以下文件目录：{}'.format(name_list))
            return False
        return True

    @TestLogger.log('选择文件')
    def select_local_file(self, *file_list):
        name_list = list(file_list)
        self.wait_until(
            condition=lambda d: self._is_element_present(
                (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text"]'))
        )
        for cont in self.mobile.list_iterator(self.__locators['文件列表'], self.__locators['文件项']):
            name = cont.find_element(*self.__locators['文件名称项']).text
            if name in name_list:
                cont.click()
                name_list.remove(name)
            if not name_list:
                break
        if name_list:
            print('没有找到以下联系人：{}'.format(name_list))
            return False
        return True

    @TestLogger.log()
    def send_file_messages_631(self, path, file_name):
        """单聊发送文件"""
        chatWindowPage = ChatWindowPage()
        for i in range(1, 5):
            chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'down', 600)
        self.select_local_file_directory(path)
        self.click_text_or_description('resource')
        # 文件系统找文件
        time.sleep(2)
        for i in range(1, 5):
            chatWindowPage.swipe_by_direction((MobileBy.ID, 'com.chinasofti.rcs:id/lv_choose'), 'down', 600)
        self.select_local_file(file_name)
        # 发送
        chatWindowPage.click_element((MobileBy.XPATH,
                                      '//*[@resource-id="com.chinasofti.rcs:id/button_send" and @text="发送"]'))
        time.sleep(1)

    @TestLogger.log()
    def click_mess_text(self, mess):
        """发送消息如果当前页不存在该消息"""
        self.click_element((MobileBy.XPATH, '//*[@text ="%s"]' % mess))

