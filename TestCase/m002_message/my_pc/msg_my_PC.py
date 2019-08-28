import time

from selenium.common.exceptions import TimeoutException

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.workbench.group_messenger.SelectCompanyContacts import SelectCompanyContactsPage
from preconditions.BasePreconditions import LoginPreconditions, WorkbenchPreconditions

REQUIRED_MOBILES = {
    'Android-移动': 'M960BDQN229CH',
    'Android-XX': ''  # 用来发短信
}


class Preconditions(WorkbenchPreconditions):
    """前置条件"""
    @staticmethod
    def enter_my_PC_chat_page(reset=False):
        """进入我的电脑会话页面"""
        # 登录进入消息页面
        Preconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 点击搜索我的电脑
        if mess.is_text_present('我的电脑'):
            mess.choose_chat_by_name('我的电脑')
        else:
            mess.click_search()
            SearchPage().input_search_keyword('我的电脑')
            mess.choose_chat_by_name('我的电脑')

    @staticmethod
    def make_sure_chatwindow_exist_file():
        """确保我的电脑页面有文件记录"""
        chat=ChatWindowPage()
        time.sleep(2)
        # if chat.is_element_present_file():
        #     chat.wait_for_page_load()
        # else:
        chat.click_more()
        ChatMorePage().click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.txt')
        local_file.click_send()
        chat.wait_for_page_load()

    @staticmethod
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "aatest" + phone_number[-4:]
        return group_name

    @staticmethod
    def make_already_in_message_page2(reset=False):
        """确保应用在消息页面"""
        Preconditions.select_mobile('Android-移动', reset)
        current_mobile().hide_keyboard_if_display()
        time.sleep(1)
        # 如果在消息页，不做任何操作
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        # 进入一键登录页
        else:
            try:
                current_mobile().launch_app()
                mess.wait_for_page_load()
            except:
                # 进入一键登录页
                Preconditions.make_already_in_one_key_login_page()
                #  从一键登录页面登录
                Preconditions.login_by_one_key_login()


class MsgMyPCChating(TestCase):
    """我的电脑-文件"""

    @classmethod
    def setUpClass(cls):
        # 备注：脚本中已判断预支文件是否存在
        Preconditions.select_mobile('Android-移动')

    def default_setUp(self):
        """确保每个用例运行前在我的电脑会话页面"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.enter_my_PC_chat_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0253(self):
        """我的电脑预览文件页面,右上角显示更多选项"""
        #确保页面有.txt文件
        chat=ChatWindowPage()
        chat.click_more()
        ChatMorePage().click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.push_preset_file()
        local_file.click_preset_file_dir()
        local_file.select_file('.txt')
        local_file.click_send()
        #打开文件
        file_name=chat.get_file_info('文件名')
        chat.open_file_in_chat_page(file_name)
        chat.wait_for_open_file()
        chat.page_contain_element_more()
        #返回聊天页面
        chat.click_back_in_open_file_page()

    @tags('ALL', 'CMCC',  'my_PC')
    def test_msg_weifenglian_PC_0254(self):
        """我的电脑预览文件页面,点击更多"""
        chat=ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        file_name=chat.get_file_info('文件名')
        chat.open_file_in_chat_page(file_name)
        chat.wait_for_open_file()
        chat.click_more_Preview()
        time.sleep(1)
        chat.page_should_contain_text('转发')
        chat.page_should_contain_text('收藏')
        chat.page_should_contain_text('其他应用打开')

    @tags('ALL', 'CMCC',  'my_PC')
    def test_msg_weifenglian_PC_0256(self):
        """我的电脑预览文件页面,点击转发"""
        chat=ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        file_name=chat.get_file_info('文件名')
        chat.open_file_in_chat_page(file_name)
        chat.wait_for_open_file()
        chat.click_more_Preview()
        time.sleep(1)
        chat.click_forward_Preview()
        #选择联系人
        scp = SelectContactsPage()
        scp.is_on_this_page()
        scp.click_phone_contact()
        scp.click_one_contact('给个红包1')
        scp.click_sure_forward()
        time.sleep(2)
        self.assertTrue(chat.is_toast_exist('已转发'))
        chat.page_contain_element_more()

    @tags('ALL', 'CMCC',  'my_PC')
    def test_msg_weifenglian_PC_0257(self):
        """我的电脑预览文件页面,点击收藏"""
        chat=ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        file_name=chat.get_file_info('文件名')
        chat.open_file_in_chat_page(file_name)
        chat.wait_for_open_file()
        chat.click_more_Preview()
        time.sleep(2)
        chat.click_collection_Preview()
        self.assertTrue(chat.is_toast_exist('已收藏'))
        chat.click_back_in_open_file_page()

    @tags('ALL', 'CMCC',  'my_PC')
    def test_msg_weifenglian_PC_0258(self):
        """我的电脑预览文件页面,点击其他应用打开"""
        chat=ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        file_name=chat.get_file_info('文件名')
        chat.open_file_in_chat_page(file_name)
        chat.wait_for_open_file()
        chat.click_more_Preview()
        time.sleep(2)
        chat.click_other_App_open()
        chat.page_should_contain_text('使用以下方式打开')

    @tags('ALL', 'CMCC',  'my_PC')
    def test_msg_weifenglian_PC_0302(self):
        """断网,我的电脑预览文件页面,右上角显示更多选项"""
        chat=ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        chat.set_network_status(0)
        file_name=chat.get_file_info('文件名')
        chat.open_file_in_chat_page(file_name)
        chat.wait_for_open_file()
        chat.page_contain_element_more()
        #返回聊天页面
        chat.click_back_in_open_file_page()

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0302():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0306(self):
        """断网 我的电脑预览文件页面,点击收藏"""
        chat=ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        chat.set_network_status(0)
        file_name=chat.get_file_info('文件名')
        chat.open_file_in_chat_page(file_name)
        chat.wait_for_open_file()
        chat.click_more_Preview()
        time.sleep(2)
        chat.click_collection_Preview()
        self.assertTrue(chat.is_toast_exist('已收藏'))
        chat.click_back_in_open_file_page()

    @tags('ALL', 'CMCC', 'DEBUG_1', 'my_PC')
    def test_msg_weifenglian_PC_0307(self):
        """断网 我的电脑预览文件页面,点击其他应用打开"""
        chat=ChatWindowPage()
        Preconditions.make_sure_chatwindow_exist_file()
        chat.set_network_status(0)
        file_name=chat.get_file_info('文件名')
        chat.open_file_in_chat_page(file_name)
        chat.wait_for_open_file()
        chat.click_more_Preview()
        time.sleep(2)
        chat.click_other_App_open()
        chat.page_should_contain_text('使用以下方式打开')

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0307():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep = MePage()
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0532(self):
        """放大发送表情文本"""
        #选择表情
        chat=ChatWindowPage()
        chat.open_expression()
        chat.select_expression(n=5)
        #放大发送表情
        time.sleep(1)
        chat.press_and_move_up('发送按钮')
        # 验证是否发送成功
        try:
            chat.wait_for_msg_send_status_become_to('发送成功', 10)
        except TimeoutException:
            raise AssertionError('消息在 {}s 内没有发送成功'.format(10))
        # 判断是否放大,一个表情文本框信息正常宽度为107
        if not chat.get_width_of_msg_of_text() > 107:
            raise AssertionError("表情没有放大展示")
        chat.close_expression2()
        chat.hide_keyboard()

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0014(self):
        """我的电脑-本地照片发送"""
        #进入选择照片文件夹
        chat = ChatWindowPage()
        chat.click_more()
        ChatMorePage().click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_pic()
        #选择照片
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.jpg')
        local_file.click_send()
        chat.wait_for_msg_send_status_become_to('发送成功', 10)
        #返回消息页面
        chat.click_back_by_android()
        time.sleep(2)
        MessagePage().page_should_contain_text('图片')

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0028(self):
        """我的电脑-本地视频发送"""
        #进入选择视频文件夹
        chat = ChatWindowPage()
        chat.click_more()
        ChatMorePage().click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_video()
        #选择视频
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.mp4')
        local_file.click_send()
        chat.wait_for_msg_send_status_become_to('发送成功', 10)
        #返回消息页面
        chat.click_back_by_android()
        time.sleep(2)
        MessagePage().page_should_contain_text('视频')

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0042(self):
        """我的电脑-本地音乐发送"""
        #进入选择音乐文件夹
        chat = ChatWindowPage()
        chat.click_more()
        ChatMorePage().click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_music()
        #选择音乐
        local_file = ChatSelectLocalFilePage()
        local_file.select_file('.mp3')
        local_file.click_send()
        chat.wait_for_msg_send_status_become_to('发送成功', 10)
        #返回消息页面
        chat.click_back_by_android()
        time.sleep(2)
        MessagePage().page_should_contain_text('文件')


class MsgMyPcTest(TestCase):
    """我的电脑-文件"""

    @classmethod
    def setUpClass(cls):
        # 备注：脚本中已判断预支文件是否存在
        Preconditions.select_mobile('Android-移动')

    def default_setUp(self):
        """确保每个用例运行前在我的电脑会话页面"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        msg_page = MessagePage()
        msg_page.wait_for_page_load()
        if msg_page.message_list_is_exist_name('我的电脑', max_try=3):
            try:
                msg_page.choose_chat_by_name('我的电脑')
                self.wait_for_MyPc_page_load()
            except:
                msg_page.click_search()
                SearchPage().input_search_keyword('我的电脑')
                msg_page.choose_chat_by_name('我的电脑')
                self.wait_for_MyPc_page_load()
        else:
            try:
                msg_page.clear_message_record()
            except Exception as e:
                print(e)
            msg_page.click_search()
            SearchPage().input_search_keyword('我的电脑')
            msg_page.choose_chat_by_name('我的电脑')
            self.wait_for_MyPc_page_load()

    @staticmethod
    def wait_for_MyPc_page_load():
        """等待我的电脑页面加载，也可判断是否在我的电脑页面，return True"""
        return current_mobile().wait_until(condition=lambda x: current_mobile().is_text_present('我的电脑'))

    def public_select_folder(self):
        chat_more = ChatMorePage()
        chat_more.click_file()

    def public_select_file(self, file_type=".xlsx"):
        """聊天页面选择文件"""
        self.public_select_folder()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_local_file()
        local_file = ChatSelectLocalFilePage()
        local_file.enter_preset_file_dir()
        local_file.select_file(file_type)

    def public_select_file_send(self, file_type=".xlsx"):
        """聊天页面选择文件发送"""
        self.public_select_file(file_type)
        time.sleep(3)
        ChatSelectLocalFilePage().click_send()
        time.sleep(2)

    def public_send_GT_2M_file(self, file_type="2M_data.json"):
        """发送大于2M的文件"""
        current_mobile().turn_off_wifi()
        self.public_select_file(file_type)
        ChatSelectLocalFilePage().click_single_send()

    def public_make_sure_have_faild_massege(self, file_type=".xlsx"):
        """确保页面有发送失败的消息"""
        MessagePage().set_network_status(0)
        self.public_select_file_send(file_type)

    def public_select_pic(self, file_type=".jpg"):
        self.public_select_folder()
        #  选择文件夹类型
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_pic()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(file_type)

    def public_select_pic_send(self, file_type='.jpg'):
        self.public_select_pic(file_type)
        ChatSelectLocalFilePage().click_send()

    def public_select_music(self, file_name = '28618718.mp3'):
        self.public_select_folder()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_music()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(file_name)

    def public_select_music_send(self, file_name='28618718.mp3'):
        self.public_select_music(file_name)
        ChatSelectLocalFilePage().click_send()

    def public_select_video(self, file_name='.mp4'):
        self.public_select_folder()
        select_file_type = ChatSelectFilePage()
        select_file_type.wait_for_page_load()
        select_file_type.click_video()
        # 3， 选择图片发送
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(file_name)

    def public_select_video_send(self, file_name='.mp4'):
        self.public_select_video(file_name)
        ChatSelectLocalFilePage().click_send()

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0001(self):
        """勾选本地文件内任意文件点击发送按钮"""
        self.public_select_file_send()
        msg_page = MessagePage()
        print(msg_page.wait_until(condition=lambda x: msg_page.is_text_present('测试用例.xlsx')))
        ChatWindowPage().click_back1()

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0002(self):
        """网络异常时勾选本地文件内任意文件点击发送按钮"""
        self.public_make_sure_have_faild_massege()
        self.assertTrue(GroupChatPage().is_exist_msg_send_failed_button())

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0002():
        MessagePage().set_network_status(6)

    @staticmethod
    def setUp_test_msg_weifenglian_PC_0003():
        Preconditions.make_already_in_message_page2()
        msg_page = MessagePage()
        msg_page.wait_for_page_load()
        if msg_page.message_list_is_exist_name('我的电脑', max_try=3):
            try:
                msg_page.choose_chat_by_name('我的电脑')
                time.sleep(3)
            except:
                msg_page.click_search()
                SearchPage().input_search_keyword('我的电脑')
                msg_page.choose_chat_by_name('我的电脑')
                time.sleep(3)
        else:
            try:
                msg_page.clear_message_record()
            except Exception as e:
                print(e)
            msg_page.click_search()
            SearchPage().input_search_keyword('我的电脑')
            msg_page.choose_chat_by_name('我的电脑')
            time.sleep(3)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0003(self):
        """会话页面有文件发送失败时查看消息列表是否有消息发送失败的标识"""
        mess = MessagePage()
        mess.set_network_status(0)
        self.wait_for_MyPc_page_load()
        if GroupChatPage().is_exist_msg_send_failed_button():
            pass
        else:
            self.public_make_sure_have_faild_massege()
        self.wait_for_MyPc_page_load()
        ChatWindowPage().click_back1()
        time.sleep(3)
        result = mess.is_iv_fail_status_present()
        self.assertTrue(result)

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0003():
        mess = MessagePage()
        mess.set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0004(self):
        """对发送失败的文件进行重发"""
        self.wait_for_MyPc_page_load()
        if GroupChatPage().is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_PC_0002()
            MessagePage().set_network_status(6)
            self.wait_for_MyPc_page_load()
        chat_page = GroupChatPage()
        chat_page.click_msg_send_failed_button()
        chat_page.click_resend_confirm()
        self.wait_for_MyPc_page_load()
        chat_page.wait_for_message_down_file()
        self.assertTrue(chat_page.check_message_resend_success())

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0004():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0005(self):
        """对发送失败的文件进行重发后，消息列表页面的消息发送失败的标识消失"""
        self.test_msg_weifenglian_PC_0004()
        ChatWindowPage().click_back1()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertFalse(message_page.is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0005():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0006(self):
        """点击取消重发文件消失，停留在当前页面"""
        chat_page = GroupChatPage()
        self.wait_for_MyPc_page_load()
        if chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.public_make_sure_have_faild_massege()
            chat_page.mobile.turn_on_wifi()
            chat_page.mobile.turn_on_mobile_data()
        chat_page.click_msg_send_failed_button()
        chat_page.click_multiple_selection_delete_cancel()
        self.wait_for_MyPc_page_load()
        self.assertTrue((chat_page.wait_until(condition=lambda x: chat_page.is_text_present('我的电脑'))))
        ChatWindowPage().click_back1()

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0006():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC-skip', 'my_PC')
    def test_msg_weifenglian_PC_0007(self):
        """未订购每月10G的用户发送大于2M的文件时有弹窗提示"""
        self.public_send_GT_2M_file(file_type="2M_data.json")
        local_file = ChatSelectLocalFilePage()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        local_file.click_back()
        ChatSelectFilePage().click_back()

    @tags('ALL', 'CMCC-skip', 'my_PC')
    def test_msg_weifenglian_PC_0008(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""
        current_mobile().turn_off_wifi()
        self.public_select_file_send('2M_data.json')
        self.test_msg_weifenglian_PC_0007()
        ChatWindowPage().click_back1()
        MessagePage().wait_for_page_load()
        MessagePage().clear_message_record()

    @tags('ALL', 'CMCC-skip', 'my_PC')
    def test_msg_weifenglian_PC_0010(self):
        """点击订购免流特权后可正常返回"""
        self.public_send_GT_2M_file(file_type="2M_data.json")
        local_file = ChatSelectLocalFilePage()
        local_file.click_free_data_button()
        bol = local_file.wait_until(lambda x: ChatSelectLocalFilePage().is_text_present('和飞信'),
                                    auto_accept_permission_alert=False)
        self.assertTrue(bol)
        local_file.click_free_data_back()
        self.assertTrue(local_file.check_10G_free_data_page())
        # 返回到消息页面
        local_file.click_outside_element()
        local_file.click_back()
        local_file.click_back()
        ChatSelectFilePage().click_back()
        ChatWindowPage().click_back1()

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0010():
        current_mobile().turn_on_wifi()

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0012(self):
        """在文件列表页选择文件后再点击取消按钮，停留在当前页面"""
        self.public_select_file()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".xlsx")
        self.assertTrue(local_file.is_on_this_page())
        # 返回到消息页面
        local_file.click_back()
        local_file.click_back()
        ChatSelectFilePage().click_back()
        ChatWindowPage().click_back1()

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0013(self):
        """在文件列表页点击返回按钮时可正常逐步返回到会话页面"""
        self.public_select_file()
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".xlsx")
        self.assertTrue(local_file.is_on_this_page())
        # 返回到消息页面
        local_file.click_back()
        local_file.click_back()
        ChatSelectFilePage().click_back()
        self.assertTrue(self.wait_for_MyPc_page_load())

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0015(self):
        """网络异常时勾选本地照片内任意相册的图片点击发送按钮"""
        MessagePage().set_network_status(0)
        self.public_select_pic_send('23e.jpg')
        self.wait_for_MyPc_page_load()
        self.assertTrue(GroupChatPage().is_exist_msg_send_failed_button())

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0015():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0016(self):
        """会话页面有图片发送失败时查看消息列表是否有消息发送失败的标识"""
        chat_page = GroupChatPage()
        if chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            MessagePage().set_network_status(0)
            self.public_select_pic_send('.jpg')
            self.wait_for_MyPc_page_load()
        ChatWindowPage().click_back1()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertTrue(message_page.is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0016():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0017(self):
        """对发送失败的图片文件进行重发"""
        pc_chat_page = GroupChatPage()
        if pc_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            MessagePage().set_network_status(0)
            time.sleep(1)
            self.public_select_pic_send('.jpg')
            time.sleep(1)
            MessagePage().set_network_status(6)
            self.wait_for_MyPc_page_load()
        time.sleep(2)
        pc_chat_page.click_msg_send_failed_button()
        time.sleep(2)
        pc_chat_page.click_resend_confirm()
        time.sleep(1)
        self.wait_for_MyPc_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0017():
        MessagePage().set_network_status(6)

    @staticmethod
    def setUp_test_msg_weifenglian_PC_0018():
        Preconditions.make_already_in_message_page2()
        msg_page = MessagePage()
        msg_page.wait_for_page_load()
        if msg_page.message_list_is_exist_name('我的电脑', max_try=3):
            try:
                msg_page.choose_chat_by_name('我的电脑')
                time.sleep(3)
            except:
                msg_page.click_search()
                SearchPage().input_search_keyword('我的电脑')
                msg_page.choose_chat_by_name('我的电脑')
                time.sleep(3)
        else:
            try:
                msg_page.clear_message_record()
            except Exception as e:
                print(e)
            msg_page.click_search()
            SearchPage().input_search_keyword('我的电脑')
            msg_page.choose_chat_by_name('我的电脑')
            time.sleep(3)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0018(self):
        """对发送失败的图片进行重发后，消息列表页面的消息发送失败的标识消失"""
        pc_chat_page = GroupChatPage()
        if pc_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            mess = MessagePage()
            mess.set_network_status(0)
            self.public_select_pic_send('23e.jpg')
            mess.set_network_status(6)
            self.wait_for_MyPc_page_load()
        pc_chat_page.click_msg_send_failed_button()
        pc_chat_page.click_resend_confirm()
        self.wait_for_MyPc_page_load()
        ChatWindowPage().click_back1()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertFalse(message_page.is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0018():
        mess = MessagePage()
        mess.set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0019(self):
        """点击取消重发图片消息，停留在当前页面"""
        pc_chat_page = GroupChatPage()
        if pc_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            MessagePage().set_network_status(0)
            self.public_select_pic_send('23e.jpg')
            MessagePage().set_network_status(6)
            self.wait_for_MyPc_page_load()
        pc_chat_page.click_msg_send_failed_button()
        pc_chat_page.click_multiple_selection_delete_cancel()
        bol = current_mobile().wait_until(condition=lambda x: current_mobile().is_text_present('我的电脑'))
        self.assertTrue(bol)

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0019():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC-skip', 'my_PC')
    def test_msg_weifenglian_PC_0020(self):
        """未订购每月10G的用户发送大于2M的文件时有弹窗提示"""
        # 关闭wifi发送文件
        current_mobile().turn_off_wifi()
        self.public_select_pic('2M_pic.jpg')
        local_file = ChatSelectLocalFilePage()
        local_file.click_single_send()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        ChatSelectFilePage().click_back()
        ChatWindowPage().click_back1()

    @tags('ALL', 'CMCC-skip', 'my_PC')
    def test_msg_weifenglian_PC_0021(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""
        current_mobile().turn_off_wifi()
        self.public_select_pic('2M_pic.jpg')
        local_file = ChatSelectLocalFilePage()
        local_file.click_send()
        self.test_msg_weifenglian_PC_0020()
        MessagePage().wait_for_page_load()
        MessagePage().clear_message_record()

    @tags('ALL', 'CMCC-skip', 'my_PC')
    def test_msg_weifenglian_PC_0023(self):
        """点击订购免流特权后可正常返回"""
        current_mobile().turn_off_wifi()
        self.public_select_pic('2M_pic.jpg')
        local_file = ChatSelectLocalFilePage()
        local_file.click_single_send()
        local_file.click_free_data_button()
        bol = local_file.wait_until(lambda x: ChatSelectLocalFilePage().is_text_present('和飞信'), timeout=15,
                                    auto_accept_permission_alert=False)
        self.assertTrue(bol)
        local_file.click_free_data_back()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        ChatSelectFilePage().click_back()
        ChatWindowPage().click_back1()

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0023():
        current_mobile().turn_on_wifi()

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0025(self):
        """在选择图片页面选择文件后再点击取消按钮，停留在当前页面"""
        self.public_select_pic('23e.jpg')
        local_file = ChatSelectLocalFilePage()
        local_file.select_file("23e.jpg")
        self.assertTrue(local_file.is_on_this_page())
        # 返回到消息页面
        local_file.click_back()
        ChatSelectLocalFilePage().click_back()
        ChatWindowPage().click_back1()

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0026(self):
        """在选择图片页面点击返回按钮时可正常逐步返回到会话页面"""
        self.public_select_pic('23e.jpg')
        local_file = ChatSelectLocalFilePage()
        local_file.select_file("23e.jpg")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        ChatSelectLocalFilePage().click_back()
        bol = current_mobile().wait_until(condition=lambda x: current_mobile().is_text_present('我的电脑'))
        self.assertTrue(bol)
        # 返回到消息页面
        ChatWindowPage().click_back1()

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0029(self):
        """网络异常时勾选本地文件内任意视频点击发送按钮"""
        MessagePage().set_network_status(0)
        self.public_select_video_send()
        self.wait_for_MyPc_page_load()
        self.assertTrue(GroupChatPage().is_exist_msg_send_failed_button())

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0029():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0030(self):
        """会话页面有视频发送失败时查看消息列表是否有消息发送失败的标识"""
        self.wait_for_MyPc_page_load()
        pc_chat_page = GroupChatPage()
        if pc_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_PC_0029()
        pc_chat_page.click_back()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        self.assertTrue(message_page.is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0030():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0031(self):
        """对发送失败的视频进行重发"""
        self.wait_for_MyPc_page_load()
        pc_chat_page = GroupChatPage()
        if pc_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_PC_0029()
            time.sleep(3)
            MessagePage().set_network_status(6)
        time.sleep(2)
        pc_chat_page.click_msg_send_failed_button()
        time.sleep(2)
        pc_chat_page.click_resend_confirm()
        time.sleep(1)
        self.wait_for_MyPc_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0031():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0032(self):
        """对发送失败的视频进行重发后，消息列表页面的消息发送失败的标识消失"""
        self.test_msg_weifenglian_PC_0031()
        MessagePage().wait_for_page_load()
        self.assertFalse(MessagePage().is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0032():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0033(self):
        """点击取消重发视频文件消失，停留在当前页面"""
        self.wait_for_MyPc_page_load()
        pc_chat_page = GroupChatPage()
        if pc_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.test_msg_weifenglian_PC_0029()
            MessagePage().set_network_status(6)
            time.sleep(2)
        pc_chat_page.click_msg_send_failed_button()
        pc_chat_page.click_multiple_selection_delete_cancel()
        bol = self.wait_for_MyPc_page_load()
        self.assertTrue(bol)

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0033():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC-skip', 'my_PC')
    def test_msg_weifenglian_PC_0034(self):
        """未订购每月10G的用户发送大于2M的视频时有弹窗提示"""
        self.wait_for_MyPc_page_load()
        current_mobile().turn_off_wifi()
        self.public_select_video('2M_vedio.mp4')
        local_file = ChatSelectLocalFilePage()
        local_file.click_single_send()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        ChatSelectFilePage().click_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0034():
        current_mobile().turn_on_wifi()

    @tags('ALL', 'CMCC-skip', 'my_PC')
    def test_msg_weifenglian_PC_0035(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示"""
        current_mobile().turn_off_wifi()
        self.public_select_video_send('2M_vedio.mp4')
        self.public_select_video('2M_vedio.mp4')
        local_file = ChatSelectLocalFilePage()
        local_file.click_single_send()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        ChatSelectFilePage().click_back()
        ChatWindowPage().click_back1()
        MessagePage().wait_for_page_load()
        MessagePage().clear_message_record()

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0035():
        current_mobile().turn_on_wifi()

    @staticmethod
    def setUp_test_msg_weifenglian_PC_0037():
        Preconditions.make_already_in_message_page2()
        msg_page = MessagePage()
        msg_page.wait_for_page_load()
        if msg_page.message_list_is_exist_name('我的电脑', max_try=3):
            try:
                msg_page.choose_chat_by_name('我的电脑')
                time.sleep(3)
            except:
                msg_page.click_search()
                SearchPage().input_search_keyword('我的电脑')
                msg_page.choose_chat_by_name('我的电脑')
                time.sleep(3)
        else:
            try:
                msg_page.clear_message_record()
            except Exception as e:
                print(e)
            msg_page.click_search()
            SearchPage().input_search_keyword('我的电脑')
            msg_page.choose_chat_by_name('我的电脑')
            time.sleep(3)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0037(self):
        """点击订购免流特权后可正常返回”"""
        mess = MessagePage()
        mess.set_network_status(0)
        self.public_select_video('2M_vedio.mp4')
        local_file = ChatSelectLocalFilePage()
        local_file.click_single_send()
        local_file.click_free_data_button()
        time.sleep(3)
        bol = local_file.wait_until(lambda x: ChatSelectLocalFilePage().is_text_present('网页无法打开'), timeout=15,
                                    auto_accept_permission_alert=False)
        self.assertTrue(bol)
        local_file.click_free_data_back()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        ChatSelectFilePage().click_back()

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0037():
        mess = MessagePage()
        mess.set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0039(self):
        """在视频列表页选择文件后再点击取消按钮，停留在当前页面”"""
        self.public_select_video('.mp4')
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".mp4")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        ChatSelectFilePage().click_back()

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0040(self):
        """在视频列表页点击返回按钮时可正常逐步返回到会话页面”"""
        self.public_select_video('.mp4')
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".mp4")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        ChatSelectFilePage().wait_for_page_load()
        ChatSelectFilePage().click_back()
        bol = self.wait_for_MyPc_page_load()
        self.assertTrue(bol)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0043(self):
        """网络异常时勾选音乐列表页面任意音乐点击发送按钮”"""
        MessagePage().set_network_status(0)
        self.public_select_music_send('.mp3')
        is_on_Pc_Chat_Page = self.wait_for_MyPc_page_load()
        self.assertTrue(is_on_Pc_Chat_Page)
        self.assertTrue(GroupChatPage().is_exist_msg_send_failed_button())

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0043():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0044(self):
        """会话页面有音乐文件发送失败时查看消息列表是否有消息发送失败的标识”"""
        if GroupChatPage().is_exist_msg_send_failed_button():
            pass
        else:
            MessagePage().set_network_status(0)
            self.public_select_music_send('.mp3')
        self.wait_for_MyPc_page_load()
        ChatWindowPage().click_back1()
        MessagePage().wait_for_page_load()
        self.assertTrue(MessagePage().is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0044():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0045(self):
        """对发送失败的音乐进行重发”"""
        if GroupChatPage().is_exist_msg_send_failed_button():
            pass
        else:
            MessagePage().set_network_status(0)
            self.public_select_music_send('.mp3')
            time.sleep(2)
        MessagePage().set_network_status(6)
        self.wait_for_MyPc_page_load()
        time.sleep(2)
        GroupChatPage().click_msg_send_failed_button()
        time.sleep(2)
        GroupChatPage().click_resend_confirm()
        time.sleep(2)
        self.wait_for_MyPc_page_load()

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0045():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0046(self):
        """对发送失败的音乐进行重发后，消息列表页面的消息发送失败的标识消失”"""
        self.test_msg_weifenglian_PC_0045()
        ChatWindowPage().click_back1()
        MessagePage().wait_for_page_load()
        self.assertFalse(MessagePage().is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0046():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0047(self):
        """点击取消重发音乐文件消失，停留在当前页面”"""
        if GroupChatPage().is_exist_msg_send_failed_button():
            pass
        else:
            MessagePage().set_network_status(0)
            self.public_select_music_send('28618718.mp3')
            MessagePage().set_network_status(6)
            time.sleep(2)
        GroupChatPage().click_msg_send_failed_button()
        GroupChatPage().click_multiple_selection_delete_cancel()
        pc_chat_page = self.wait_for_MyPc_page_load()
        self.assertTrue(pc_chat_page)

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0047():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC-skip', 'my_PC')
    def test_msg_weifenglian_PC_0048(self):
        """未订购每月10G的用户发送大于2M的音乐时有弹窗提示”"""
        current_mobile().turn_off_wifi()
        self.public_select_music('喜欢你.mp3')
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.click_single_send()
        self.assertTrue(local_file.check_10G_free_data_page())

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0048():
        current_mobile().turn_on_wifi()

    @tags('ALL', 'CMCC-skip', 'my_PC')
    def test_msg_weifenglian_PC_0049(self):
        """直接点击“继续发送”：关闭弹窗，拨出，下次继续提示”"""
        current_mobile().turn_off_wifi()
        self.public_select_music_send('喜欢你.mp3')
        self.test_msg_weifenglian_PC_0048()

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0049():
        current_mobile().turn_on_wifi()

    @tags('ALL', 'CMCC-skip', 'my_PC')
    def test_msg_weifenglian_PC_0051(self):
        """点击订购免流特权后可正常返回"""
        current_mobile().turn_off_wifi()
        self.public_select_music('喜欢你.mp3')
        local_file = ChatSelectLocalFilePage()
        local_file.click_single_send()
        local_file.click_free_data_button()
        bol = local_file.wait_until(lambda x: ChatSelectLocalFilePage().is_text_present('和飞信'), timeout=15,
                                    auto_accept_permission_alert=False)
        self.assertTrue(bol)
        local_file.click_free_data_back()
        self.assertTrue(local_file.check_10G_free_data_page())
        local_file.click_outside_element()
        local_file.click_back()
        ChatSelectFilePage().click_back()
        ChatWindowPage().click_back1()
        MessagePage().wait_for_page_load()
        MessagePage().clear_message_record()

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0051():
        current_mobile().turn_on_wifi()

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0053(self):
        """在音乐列表页选择文件后再点击取消按钮，停留在当前页面"""
        self.public_select_music('.mp3')
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".mp3")
        self.assertTrue(local_file.is_on_this_page())

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0054(self):
        """在音乐列表页点击返回按钮时可正常逐步返回到会话页面"""
        self.public_select_music('.mp3')
        local_file = ChatSelectLocalFilePage()
        local_file.select_file(".mp3")
        self.assertTrue(local_file.is_on_this_page())
        local_file.click_back()
        ChatSelectFilePage().click_back()
        pc_chat_page = self.wait_for_MyPc_page_load()
        self.assertTrue(pc_chat_page)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0074(self):
        """在我的电脑将自己发送的文件转发到当前会话窗口"""
        self.public_select_file_send(".xlsx")
        self.wait_for_MyPc_page_load()
        ChatFilePage().forward_file(".xlsx")
        SelectContactsPage().wait_for_page_load()
        SelectContactsPage().select_one_recently_contact_by_name('我的电脑')
        time.sleep(2)
        SelectContactsPage().click_sure_forward()
        time.sleep(2)
        self.assertTrue(GroupChatPage().is_exist_forward())

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0075(self):
        """将自己发送的文件转发到普通群"""
        pc_chat_page = GroupChatPage()
        if pc_chat_page.is_exist_msg_file():
            pass
        else:
            self.public_select_file_send('.xlsx')
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        SelectContactsPage().click_select_one_group()
        group_name = Preconditions.get_group_chat_name()
        SelectOneGroupPage().select_one_group_by_name(group_name)
        SelectOneGroupPage().click_sure_forward()
        # 转发成功并回到聊天页面
        self.assertTrue(GroupChatPage().is_exist_forward())
        pc_chat_page = self.wait_for_MyPc_page_load()
        self.assertTrue(pc_chat_page)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0077(self):
        """将自己发送的文件转发到普通群时失败"""
        MessagePage().set_network_status(0)
        pc_chat_page = GroupChatPage()
        if pc_chat_page.is_exist_msg_file():
            pass
        else:
            self.public_select_file_send('.xlsx')
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        SelectContactsPage().click_select_one_group()
        group_name = Preconditions.get_group_chat_name()
        SelectOneGroupPage().select_one_group_by_name(group_name)
        SelectOneGroupPage().click_sure_forward()
        # 转发成功并回到聊天页面
        self.assertTrue(GroupChatPage().is_exist_forward())
        ChatWindowPage().click_back1()
        MessagePage().wait_for_page_load()
        self.assertTrue(MessagePage().is_iv_fail_status_present())

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0077():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0076(self):
        """将自己发送的文件转发到企业群"""
        pc_chat_page = GroupChatPage()
        if pc_chat_page.is_exist_msg_file():
            pass
        else:
            self.public_select_file_send('.xlsx')
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        SelectContactsPage().click_select_one_group()
        SelectOneGroupPage().select_one_enterprise_group()
        time.sleep(2)
        SelectOneGroupPage().click_sure_forward()
        # 转发成功并回到聊天页面
        self.assertTrue(GroupChatPage().is_exist_forward())
        self.assertTrue(self.wait_for_MyPc_page_load())

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0078(self):
        """将自己发送的文件转发到企业群"""
        MessagePage().set_network_status(0)
        pc_chat_page = GroupChatPage()
        if pc_chat_page.is_exist_msg_file():
            pass
        else:
            self.public_select_file_send('.xlsx')
        # 转发xls文件
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        time.sleep(2)
        SelectContactsPage().click_select_one_group()
        SelectOneGroupPage().select_one_enterprise_group()
        time.sleep(2)
        SelectOneGroupPage().click_sure_forward()
        # 转发成功并回到聊天页面
        self.assertTrue(GroupChatPage().is_exist_forward())
        ChatWindowPage().click_back1()
        MessagePage().wait_for_page_load()
        self.assertTrue(MessagePage().is_iv_fail_status_present())
        MessagePage().clear_fail_in_send_message()

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0078():
        MessagePage().set_network_status(6)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0079(self):
        """将自己发送的文件转发到普通群时点击取消转发"""
        pc_chat_page = GroupChatPage()
        if pc_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.public_select_file_send('.xlsx')
            self.wait_for_MyPc_page_load()
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        SelectContactsPage().click_select_one_group()
        group_name = Preconditions.get_group_chat_name()
        SelectOneGroupPage().select_one_group_by_name(group_name)
        SelectOneGroupPage().click_cancel_forward()
        # 点击取消留在当前页面
        SelectOneGroupPage().wait_for_page_load()
        self.assertTrue(SelectOneGroupPage().is_on_this_page())

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0080(self):
        """将自己发送的文件转发到企业群时点击取消转发 """
        pc_chat_page = GroupChatPage()
        if pc_chat_page.is_exist_msg_send_failed_button():
            pass
        else:
            self.public_select_file_send('.xlsx')
            self.wait_for_MyPc_page_load()
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()
        # 需要转发的群
        SelectContactsPage().click_select_one_group()
        SelectOneGroupPage().select_one_enterprise_group()
        # 点击取消留在当前页面
        SelectOneGroupPage().click_cancel_forward()
        # 点击取消留在当前页面
        SelectOneGroupPage().wait_for_page_load()
        self.assertTrue(SelectOneGroupPage().is_on_this_page())

    def long_press_file(self):
        """ 长按文件(.xlsx) """
        pc_chat_page = GroupChatPage()
        if pc_chat_page.is_exist_msg_file():
            pass
        else:
            self.public_select_file_send()
            self.wait_for_MyPc_page_load()
        time.sleep(2)

    def public_forward_file(self):
        """ 转发文件 """
        self.long_press_file()
        # 转发xls文件
        time.sleep(2)
        ChatFilePage().forward_file('.xlsx')
        SelectContactsPage().wait_for_page_load()

    def public_select_Group_search_by_text(self, text):
        """ 进入选择一个群并通过文本搜索 """
        self.public_forward_file()
        SelectContactsPage().click_select_one_group()
        SelectOneGroupPage().wait_for_page_load()
        SelectOneGroupPage().click_search_group()
        time.sleep(2)
        SelectOneGroupPage().input_search_keyword(text)
        time.sleep(3)
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            SelectOneGroupPage().click_search_result()
            time.sleep(2)
            SelectOneGroupPage().click_sure_forward()
            # 转发成功并回到聊天页面
            self.assertTrue(GroupChatPage().is_exist_forward())
            self.assertTrue(self.wait_for_MyPc_page_load())

    def public_select_TeamListContacts_search_by_text(self, text):
        """ 进入团队联系人列表并通过文本搜索 """
        # 需要转发的群
        self.public_forward_file()
        SelectContactsPage().click_he_contacts()
        SelectHeContactsPage().wait_for_page_load()
        SelectHeContactsPage().input_search_keywords(text)
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            SelectHeContactsDetailPage().click_search_team_contacts()
            SelectHeContactsDetailPage().click_sure_forward()
            # 转发成功并回到聊天页面
            self.assertTrue(GroupChatPage().is_exist_forward())
            self.assertTrue(self.wait_for_MyPc_page_load())

    def public_select_TeamSingleContacts_search_by_text(self, text):
        """ 进入团队联系人内并通过文本搜索 """
        # 需要转发的群
        self.public_forward_file()
        SelectContactsPage().click_he_contacts()
        shcp = SelectHeContactsPage()
        teams = shcp.get_team_names()
        detail_page = SelectHeContactsDetailPage()
        if teams:
            shcp.select_one_team_by_name(teams[0])
            time.sleep(2)
        detail_page.input_search(text)
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            SelectHeContactsDetailPage().click_search_team_contacts()
            SelectHeContactsDetailPage().click_sure_forward()
            # 转发成功并回到聊天页面
            self.assertTrue(GroupChatPage().is_exist_forward())
            self.assertTrue(self.wait_for_MyPc_page_load())

    def public_select_PhoneContacts_search_by_text(self, text):
        """ 进入手机联系人并通过文本搜索 """
        self.public_forward_file()
        SelectContactsPage().select_local_contacts()
        SelectLocalContactsPage().wait_for_page_load()
        search_contact = SelectLocalContactsPage()
        search_contact.search(text)
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            search_contact.click_search_phone_contacts()
            search_contact.click_sure_forward()
            # 转发成功并回到聊天页面
            self.assertTrue(GroupChatPage().is_exist_forward())
            self.assertTrue(self.wait_for_MyPc_page_load())

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0081(self):
        """将自己发送的文件转发到在搜索框输入文字搜索到的群"""
        self.public_select_Group_search_by_text('群聊')

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0082(self):
        """将自己发送的文件转发到在搜索框输入英文字母搜索到的群"""
        self.public_select_Group_search_by_text('test')

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0083(self):
        """将自己发送的文件转发到在搜索框输入数字搜索到的群"""
        self.public_select_Group_search_by_text('2345')

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0084(self):
        """将自己发送的文件转发到在搜索框输入标点符号搜索到的群"""
        self.public_select_Group_search_by_text('.;,')

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0085(self):
        """将自己发送的文件转发到在搜索框输入特殊字符搜索到的群"""
        self.public_select_Group_search_by_text('αβγ')

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0086(self):
        """将自己发送的文件转发到在搜索框输入空格搜索到的群"""
        self.public_select_Group_search_by_text('    ')

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0087(self):
        """将自己发送的文件转发到在搜索框输入多种字符搜索到的群"""
        self.public_select_Group_search_by_text('int123')

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0088(self):
        """将自己发送的文件转发到在搜索框输入多种字符搜索到的群"""
        self.public_select_Group_search_by_text('float0.123')

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0090(self):
        """将自己发送的文件转发到搜索到的群时点击取消转发"""
        self.public_forward_file()
        SelectContactsPage().click_select_one_group()
        SelectOneGroupPage().wait_for_page_load()
        SelectOneGroupPage().click_search_group()
        SelectOneGroupPage().input_search_keyword('test')
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            SelectOneGroupPage().click_search_result()
            SelectOneGroupPage().click_cancel_forward()
            bol = SelectOneGroupPage().wait_until(lambda x: SelectOneGroupPage().is_text_present('群聊'),
                                                  auto_accept_permission_alert=False)
            self.assertTrue(bol)

    @tags('ALL', 'CMCC', 'my_PC')
    def test_msg_weifenglian_PC_0091(self):
        """将自己发送的文件转发到滑动右边字母导航栏定位查找的群"""
        self.public_forward_file()
        SelectContactsPage().click_select_one_group()
        SelectOneGroupPage().wait_for_page_load()
        SelectOneGroupPage().choose_index_bar_click_element()
        SelectOneGroupPage().click_sure_forward()
        self.assertTrue(GroupChatPage().is_exist_forward())
        self.assertTrue(self.wait_for_MyPc_page_load())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0092(self):
        """将自己发送的文件转发到手机联系人"""
        self.public_forward_file()
        SelectContactsPage().select_local_contacts()
        SelectLocalContactsPage().wait_for_page_load()
        phone_contacts = SelectLocalContactsPage()
        phone_contacts.click_first_phone_contacts()
        phone_contacts.click_sure_forward()
        # 转发成功并回到聊天页面
        gcp = GroupChatPage()
        result = gcp.is_exist_forward()
        self.assertTrue(result)
        result = gcp.is_exist_setting_btn()
        self.assertTrue(result)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0093(self):
        """将自己发送的文件转发到手机联系人时点击取消转发"""
        self.public_forward_file()
        SelectContactsPage().select_local_contacts()
        SelectLocalContactsPage().wait_for_page_load()
        phone_contacts = SelectLocalContactsPage()
        phone_contacts.click_first_phone_contacts()
        phone_contacts.click_cancel_forward()
        phone_contacts.wait_for_page_load()
        self.assertTrue(phone_contacts.is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0094(self):
        """将自己发送的文件转发到手机联系人时发送失败"""
        MessagePage().set_network_status(0)
        self.public_forward_file()
        SelectContactsPage().select_local_contacts()
        SelectLocalContactsPage().wait_for_page_load()
        phone_contacts = SelectLocalContactsPage()
        phone_contacts.click_first_phone_contacts()
        phone_contacts.click_sure_forward()
        ChatWindowPage().click_back1()
        MessagePage().wait_for_page_load()
        self.assertTrue(MessagePage().is_iv_fail_status_present())
        MessagePage().clear_fail_in_send_message()

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0094():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0095(self):
        """将自己发送的文件转发到在搜索框输入多种字符搜索到的手机联系人"""
        self.public_select_PhoneContacts_search_by_text('给个红包1')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0096(self):
        """将自己发送的文件转发到在搜索框输入数字搜索到的手机联系人"""
        self.public_select_PhoneContacts_search_by_text('23579')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0097(self):
        """将自己发送的文件转发到在搜索框输入标点符号搜索到的手机联系人"""
        self.public_select_PhoneContacts_search_by_text('.;,')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0098(self):
        """将自己发送的文件转发到在搜索框输入字母搜索到的手机联系人"""
        self.public_select_PhoneContacts_search_by_text('abc')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0099(self):
        """将自己发送的文件转发到在搜索框输入空格搜索到的手机联系人"""
        self.public_select_PhoneContacts_search_by_text('   ')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0101(self):
        """将自己发送的文件转发到在搜索框输入号码搜索到的手机联系人"""
        self.public_select_PhoneContacts_search_by_text('13800138005')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0102(self):
        """将自己发送的文件转发到在搜索框进行搜索到的手机联系人时取消转发"""
        self.public_forward_file()
        SelectContactsPage().select_local_contacts()
        SelectLocalContactsPage().wait_for_page_load()
        search_contact = SelectLocalContactsPage()
        search_contact.search('13800138005')
        if search_contact.is_text_present('无搜索结果'):
            pass
        else:
            search_contact.click_search_phone_contacts()
            search_contact.click_cancel_forward()
            search_contact.wait_for_page_load()
            self.assertTrue(search_contact.is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0103(self):
        """将自己发送的文件转发到滑动右边字母导航栏定位查找的手机联系人"""
        self.public_forward_file()
        SelectContactsPage().select_local_contacts()
        SelectLocalContactsPage().wait_for_page_load()
        SelectOneGroupPage().choose_index_bar_click_element()
        SelectOneGroupPage().click_sure_forward()
        self.assertTrue(GroupChatPage().is_exist_forward())
        self.assertTrue(self.wait_for_MyPc_page_load())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0104(self):
        """将自己发送的文件转发到滑动右边字母导航栏定位查找的手机联系人时点击取消转发"""
        self.public_forward_file()
        SelectContactsPage().select_local_contacts()
        SelectLocalContactsPage().wait_for_page_load()
        SelectOneGroupPage().choose_index_bar_click_element()
        SelectOneGroupPage().click_cancel_forward()
        SelectLocalContactsPage().wait_for_page_load()
        self.assertTrue(SelectLocalContactsPage().is_on_this_page())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0107(self):
        """将自己发送的文件转发到团队未置灰的联系人时点击取消转发"""
        self.public_forward_file()
        SelectContactsPage().click_he_contacts()
        shcp = SelectHeContactsPage()
        shcp.wait_for_page_load()
        teams = shcp.get_team_names()
        if teams:
            shcp.select_one_team_by_name(teams[0])
            detail_page = SelectHeContactsDetailPage()
            time.sleep(1)
            names = detail_page.get_contacts_names()
            if not names:
                print("WARN: Please add m005_contacts in %s." % teams[0])
            for name in names:
                detail_page.select_one_linkman(name)
                flag = detail_page.is_toast_exist("该联系人不可选择", timeout=3)
                if not flag:
                    break
            detail_page.click_cancel_forward()
            detail_page.wait_for_he_contacts_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0109(self):
        """将自己发送的文件转发到在企业列表搜索框输入多种字符搜索到的团队联系人"""
        self.public_select_TeamListContacts_search_by_text('float0.123')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0110(self):
        """将自己发送的文件转发到在企业内搜索框输入多种字符搜索到的团队联系人"""
        self.public_select_TeamSingleContacts_search_by_text('float0.123')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0111(self):
        """将自己发送的文件转发到在企业列表搜索框输入数字搜索到的团队联系人"""
        self.public_select_TeamListContacts_search_by_text('2345')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0112(self):
        """将自己发送的文件转发到在企业内搜索框输入数字搜索到的团队联系人"""
        self.public_select_TeamSingleContacts_search_by_text('2345')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0113(self):
        """将自己发送的文件转发到在企业列表搜索框输入标点符号搜索到的团队联系人"""
        self.public_select_TeamListContacts_search_by_text('.;,')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0114(self):
        """将自己发送的文件转发到在企业内搜索框输入标点符号搜索到的团队联系人"""
        self.public_select_TeamSingleContacts_search_by_text('.;,')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0115(self):
        """将自己发送的文件转发到在企业列表搜索框输入字母搜索到的团队联系人"""
        self.public_select_TeamSingleContacts_search_by_text('test')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0116(self):
        """将自己发送的文件转发到在企业内搜索框输入字母搜索到的团队联系人"""
        self.public_select_TeamListContacts_search_by_text('test')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0117(self):
        """将自己发送的文件转发到在企业列表搜索框输入空格搜索到的团队联系人"""
        self.public_select_TeamListContacts_search_by_text('   .')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0118(self):
        """将自己发送的文件转发到在企业内搜索框输入空格搜索到的团队联系人"""
        self.public_select_TeamSingleContacts_search_by_text('   .')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0121(self):
        """将自己发送的文件转发到在企业列表搜索框输入号码搜索到的团队联系人"""
        self.public_select_TeamSingleContacts_search_by_text('13800138005')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0122(self):
        """将自己发送的文件转发到在企业内搜索框输入号码搜索到的团队联系人"""
        self.public_select_TeamSingleContacts_search_by_text('13800138005')

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0123(self):
        """将自己发送的文件转发到在企业列表搜索框进行搜索到的团队联系人时取消转发"""
        self.public_forward_file()
        SelectContactsPage().click_he_contacts()
        SelectHeContactsPage().wait_for_page_load()
        SelectHeContactsPage().input_search_keywords('13800138005')
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            SelectHeContactsDetailPage().click_search_team_contacts()
            SelectHeContactsDetailPage().click_cancel_forward()
            bol = SelectHeContactsDetailPage().wait_for_he_contacts_page_load()
            self.assertTrue(bol)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0124(self):
        """将自己发送的文件转发到在企业内搜索框进行搜索到的团队联系人时取消转发"""
        self.public_forward_file()
        shcp = SelectHeContactsPage()
        SelectContactsPage().click_he_contacts()
        teams = shcp.get_team_names()
        detail_page = SelectHeContactsDetailPage()
        if teams:
            shcp.select_one_team_by_name(teams[0])
            detail_page.wait_for_page_load()
        detail_page.input_search("13800138005")
        if SelectOneGroupPage().is_text_present('无搜索结果'):
            pass
        else:
            SelectHeContactsDetailPage().click_search_team_contacts()
            SelectHeContactsDetailPage().click_cancel_forward()
            bol = SelectHeContactsDetailPage().wait_for_he_contacts_page_load()
            self.assertTrue(bol)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0125(self):
        """将自己发送的文件转发到我的电脑"""
        self.public_forward_file()
        SelectContactsPage().search('我的电脑')
        SelectContactsPage().select_one_contact_by_name('我的电脑')
        SelectContactsPage().click_sure_forward()
        # 转发成功并回到聊天页面
        self.assertTrue(GroupChatPage().is_exist_forward())
        self.assertTrue(self.wait_for_MyPc_page_load())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0126(self):
        """将自己发送的文件转发到最近聊天"""
        self.public_forward_file()
        select_recent_chat = SelectContactsPage()
        select_recent_chat.wait_for_page_load()
        select_recent_chat.select_recent_chat_by_number(0)
        SelectContactsPage().click_sure_forward()
        # 转发成功并回到聊天页面
        self.assertTrue(GroupChatPage().is_exist_forward())
        self.assertTrue(self.wait_for_MyPc_page_load())

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0127(self):
        """将自己发送的文件转发到最近聊天时点击取消转发"""
        self.public_forward_file()
        select_recent_chat = SelectContactsPage()
        select_recent_chat.wait_for_page_load()
        select_recent_chat.select_recent_chat_by_number(0)
        SelectContactsPage().click_cancel_forward()
        self.assertTrue(select_recent_chat.is_on_this_page())
        select_recent_chat.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0128(self):
        """将自己发送的文件转发到最近聊天时转发失败"""
        MessagePage().set_network_status(0)
        self.public_forward_file()
        select_recent_chat = SelectContactsPage()
        select_recent_chat.wait_for_page_load()
        select_recent_chat.select_recent_chat_by_number(0)
        SelectContactsPage().click_sure_forward()
        GroupChatPage().click_back()
        MessagePage().wait_for_page_load()
        self.assertTrue(MessagePage().is_iv_fail_status_present())
        MessagePage().clear_fail_in_send_message()

    @staticmethod
    def tearDown_test_msg_weifenglian_PC_0128():
        MessagePage().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0129(self):
        """对自己发送出去的文件消息进行删除"""
        self.long_press_file()
        GroupChatPage().delete_group_all_file()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0131(self):
        """对自己发送出去的文件消息进行收藏"""
        self.public_select_file_send(".xlsx")
        # self.long_press_file()
        ChatFilePage().collection_file(".xlsx")
        # 已收藏 toast 判断
        result = GroupChatPage().is_exist_collection()
        self.assertTrue(result)
        ChatWindowPage().click_back1()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()
        MePage().is_on_this_page()
        # 点击我的收藏,进入收藏页面
        MePage().click_collection()
        collection_page = MeCollectionPage()
        collection_page.wait_for_page_load()
        collection_page.is_text_present('.xlsx')
        MePage().click_back()
        MePage().open_message_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_weifenglian_PC_0190(self):
        """在收藏页面查看在我的电脑会话窗口收藏自己发送的文件"""
        self.public_select_file_send(".xlsx")
        ChatFilePage().collection_file(".xlsx")
        GroupChatPage().is_exist_collection()
        ChatWindowPage().click_back1()
        message_page = MessagePage()
        message_page.wait_for_page_load()
        message_page.open_me_page()
        MePage().is_on_this_page()
        # 点击我的收藏,进入收藏页面
        MePage().click_collection()
        collection_page = MeCollectionPage()
        collection_page.wait_for_page_load()
        collection_page.is_text_present('.xlsx')
        self.assertTrue(collection_page.get_width_of_collection('文件名', 2))
        self.assertTrue(collection_page.page_contain_element('文件大小'))
        file_names = collection_page.get_all_file_names()
        self.assertTrue(file_names[0].endswith(".xlsx"))
        file_ele = collection_page.get_all_collection()
        for i in range(len(file_ele)):
            collection_page.press_and_move_left()
            if collection_page.is_delete_element_present():
                collection_page.click_delete_collection()
                collection_page.click_sure_forward()
        MePage().click_back()
        MePage().wait_for_page_load()
        MePage().open_message_page()


class MsgXiaoQiu(TestCase):
    """我的电脑-群聊"""
    @classmethod
    def setUpClass(cls):
        # 备注：脚本中已判断预支文件是否存在
        Preconditions.select_mobile('Android-移动')

    def default_setUp(self):
        """确保每个用例运行前在我的电脑会话页面"""
        Preconditions.select_mobile('Android-移动')
        LoginPreconditions.make_already_in_message_page()
        msg_page = MessagePage()
        msg_page.wait_for_page_load()
        msg_page.click_add_icon()
        msg_page.click_group_chat()
        SelectContactsPage().click_he_contacts()

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0637(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面的文案展示"""
        self.assertTrue(current_mobile().is_text_present('选择联系人'))

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0638(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面搜索框中默认文案展示"""
        self.assertEquals(SelectContactsPage().get_element_text('搜索或输入手机号'), '搜索或输入手机号')

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0639(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-点击搜索框"""
        SelectContactsPage().click_search_keyword()
        time.sleep(3)
        self.assertTrue(current_mobile().is_keyboard_shown())
        current_mobile().hide_keyboard()
        self.assertFalse(current_mobile().is_keyboard_shown())

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0640(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-搜索框为空时"""
        self.assertFalse(SelectContactsPage().is_element_present_by_locator('X'))

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0641(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入框存在内容时"""
        SelectContactsPage().search('123')
        self.assertTrue(SelectContactsPage().is_element_present_by_locator('X'))

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0642(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-搜索联系人"""
        scp = SelectContactsPage()
        scp.search('a')
        time.sleep(6)
        sccp = SelectCompanyContactsPage()
        result = sccp.is_search_contacts_name_match2('a')
        self.assertTrue(result)
        elements = current_mobile().get_elements(('id', 'com.chinasofti.rcs:id/tv_name_personal_contactlist'))
        time.sleep(6)
        first_page_element = [el.text for el in elements]
        scp.page_up()
        elements2 = current_mobile().get_elements(('id', 'com.chinasofti.rcs:id/tv_name_personal_contactlist'))
        sec_page_element = [el.text for el in elements2]
        self.assertFalse(first_page_element == sec_page_element)

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0643(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-上滑联系人"""
        shcp = SelectHeContactsPage()
        time.sleep(3)
        teams = shcp.get_team_names()
        print(teams)
        if teams:
            shcp.select_one_team_by_name(teams[0])
            time.sleep(2)
        shcp.page_up()
        self.assertTrue(SelectContactsPage().is_element_present_by_locator('搜索或输入手机号'))

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0644(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入一个大写字母搜索联系人"""
        SelectContactsPage().search('A')
        time.sleep(6)
        sccp = SelectCompanyContactsPage()
        result = sccp.is_exist_search_match()
        self.assertTrue(result)
        time.sleep(1)
        SelectHeContactsDetailPage().click_search_team_contacts()

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0645(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入一个大写字母搜索联系人"""
        # 备注：无法构造无查询结果的数据。
        SelectContactsPage().search('X')
        time.sleep(6)
        self.assertFalse(SelectCompanyContactsPage().is_text_present('无搜索结果'))

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0646(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入2个大写字母搜索联系人"""
        SelectContactsPage().search('AA')
        time.sleep(6)
        sccp = SelectCompanyContactsPage()
        result = sccp.is_exist_search_match()
        self.assertTrue(result)
        time.sleep(1)
        SelectHeContactsDetailPage().click_search_team_contacts()

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0647(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入2个大写字母搜索联系人"""
        # 备注：无法构造无查询结果的数据。
        SelectContactsPage().search('XX')
        time.sleep(6)
        self.assertFalse(SelectCompanyContactsPage().is_text_present('无搜索结果'))

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0648(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入一个小写字母搜索联系人"""
        SelectContactsPage().search('a')
        time.sleep(6)
        sccp = SelectCompanyContactsPage()
        result = sccp.is_exist_search_match()
        self.assertTrue(result)
        time.sleep(1)
        SelectHeContactsDetailPage().click_search_team_contacts()

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0649(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入一个小写字母搜索联系人"""
        # 备注：无法构造无查询结果的数据。
        SelectContactsPage().search('x')
        time.sleep(6)
        self.assertFalse(SelectCompanyContactsPage().is_text_present('无搜索结果'))

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0650(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入2个小写字母搜索联系人"""
        SelectContactsPage().search('aa')
        time.sleep(6)
        sccp = SelectCompanyContactsPage()
        result = sccp.is_exist_search_match()
        self.assertTrue(result)
        time.sleep(1)
        SelectHeContactsDetailPage().click_search_team_contacts()

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0651(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入2个小写字母搜索联系人"""
        # 备注：无法构造无查询结果的数据。
        SelectContactsPage().search('xx')
        time.sleep(6)
        self.assertFalse(SelectCompanyContactsPage().is_text_present('无搜索结果'))

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0652(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入联系人的姓名拼音"""
        SelectContactsPage().search('dalao')
        time.sleep(6)
        elements = current_mobile().get_elements(('id', 'com.chinasofti.rcs:id/tv_name_personal_contactlist'))
        first_page_element = [el.text for el in elements]
        time.sleep(3)
        SelectContactsPage().page_up()
        time.sleep(3)
        elements2 = current_mobile().get_elements(('id', 'com.chinasofti.rcs:id/tv_name_personal_contactlist'))
        sec_page_element = [el.text for el in elements2]
        time.sleep(3)
        self.assertFalse(first_page_element == sec_page_element)
        SelectHeContactsDetailPage().click_search_team_contacts()

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0653(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入联系人的姓名拼音-搜索"""
        SelectContactsPage().search('caixukunkun')
        time.sleep(6)
        self.assertTrue(SelectCompanyContactsPage().is_text_present('无搜索结果'))

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0654(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入任何一个汉字——搜索"""
        SelectContactsPage().search('大')
        time.sleep(6)
        sccp = SelectCompanyContactsPage()
        result = sccp.is_exist_search_match()
        self.assertTrue(result)
        time.sleep(1)
        # self.assertTrue(SelectCompanyContactsPage().is_search_contacts_name_match('大'))
        SelectHeContactsDetailPage().click_search_team_contacts()

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0655(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-企业列表页面-输入任何一个汉字——搜索"""
        SelectContactsPage().search('死')
        time.sleep(6)
        sccp = SelectCompanyContactsPage()
        result = sccp.is_text_present('无搜索结果')
        self.assertTrue(result)

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0656(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入号码规则的3位数字——搜索"""
        SelectContactsPage().search('138')
        time.sleep(8)
        SelectHeContactsDetailPage().click_search_team_contacts()

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0657(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-企业列表页面-输入号码规则的3位数字——搜索"""
        # 备注：无法构造无查询结果的数据。
        SelectContactsPage().search('999')
        time.sleep(6)
        self.assertTrue(SelectCompanyContactsPage().is_text_present('无搜索结果'))

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0658(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入号码规则的6位数字——搜索"""
        SelectContactsPage().search('138001')
        time.sleep(6)
        SelectHeContactsDetailPage().click_search_team_contacts()

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0659(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-企业列表页面-输入号码规则的6位数字——搜索"""
        # 备注：无法构造无查询结果的数据。
        SelectContactsPage().search('654321')
        time.sleep(6)
        self.assertTrue(SelectCompanyContactsPage().is_text_present('无搜索结果'))

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0660(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-输入号码规则的11位数字——搜索"""
        SelectContactsPage().search('13800137001')
        time.sleep(6)
        SelectHeContactsDetailPage().click_search_team_contacts()

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0661(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-企业列表页面-输入号码规则的11位数字——搜索"""
        SelectContactsPage().search('12345678912')
        time.sleep(6)
        self.assertTrue(SelectCompanyContactsPage().is_text_present('无搜索结果'))

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0662(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-企业列表页面-输入号码规则的11位数字——搜索"""
        SelectContactsPage().search('1234567891')
        time.sleep(6)
        self.assertTrue(SelectCompanyContactsPage().is_text_present('无搜索结果'))

    @tags('ALL', 'CMCC', 'MSG')
    def test_msg_xiaoqiu_0663(self):
        """发起群聊/添加群成员/转发-选择团队联系人-企业列表页面-企业列表页面-输入号码规则的12位数字——搜索"""
        SelectContactsPage().search('123456789123')
        time.sleep(6)
        self.assertTrue(SelectCompanyContactsPage().is_text_present('无搜索结果'))

