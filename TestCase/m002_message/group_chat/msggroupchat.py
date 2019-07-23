import random
import re
import time
import unittest
import uuid
import warnings

import preconditions
from pages.chat.ChatGroupSMS import ChatGroupSMSPage
from pages.components import BaseChatPage
from preconditions.BasePreconditions import  WorkbenchPreconditions
from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from pages.contacts.local_contact import localContactPage
from pages.workbench.create_group.CreateGroup import CreateGroupPage
from pages.workbench.create_group.SelectEnterpriseContacts import SelectEnterpriseContactsPage

class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def make_already_delete_my_group():
        """确保删掉所有群"""
        # 消息页面
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            flag = sc.wait_for_page_load()
            if not flag:
                sc.click_back()
                time.sleep(2)
                mess.click_add_icon()
                mess.click_group_chat()
                sc = SelectContactsPage()
            else:
                break
            n = n + 1
        sc.click_select_one_group()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        group_names = sog.get_group_name()
        # 有群删除，无群返回
        if len(group_names) == 0:
            sog.click_back()
            pass
        else:
            for group_name in group_names:
                sog.select_one_group_by_name(group_name)
                gcp = GroupChatPage()
                gcp.wait_for_page_load()
                gcp.click_setting()
                gcs = GroupChatSetPage()
                gcs.wait_for_page_load()
                gcs.click_delete_and_exit()
                # gcs.click_sure()
                mess.click_add_icon()
                mess.click_group_chat()
                sc.wait_for_page_load()
                sc.click_select_one_group()
            sog.click_back()
            # if not gcs.is_toast_exist("已退出群聊"):
            #     raise AssertionError("无退出群聊提示")
            # sc.click_back()


    @staticmethod
    def make_already_have_my_group(reset=False):
        """确保有群，没有群则创建群名为mygroup+电话号码后4位的群"""
        # 消息页面
        Preconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            flag = sc.wait_for_page_load()
            if not flag:
                sc.click_back()
                time.sleep(2)
                mess.click_add_icon()
                mess.click_group_chat()
                sc = SelectContactsPage()
            else:
                break
            n = n + 1
        time.sleep(3)
        sc.click_select_one_group()
        # 群名
        group_name = Preconditions.get_group_chat_name()
        # 获取已有群名
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        time.sleep(2)
        sog.input_search_keyword(group_name)
        time.sleep(2)
        if sog.is_element_exit("群聊名"):
            current_mobile().back()
            time.sleep(2)
            current_mobile().back()
            return
        current_mobile().back()
        time.sleep(2)
        current_mobile().back()
        sog.click_back()
        time.sleep(2)
        sc.click_back()
        mess.wait_for_page_load()
        # 点击 +
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 从本地联系人中选择成员创建群
        sc.click_local_contacts()
        time.sleep(2)
        slc = SelectLocalContactsPage()
        a = 0
        names = {}
        while a < 3:
            names = slc.get_contacts_name()
            num = len(names)
            if not names:
                raise AssertionError("No contacts, please add contacts in address book.")
            if num == 1:
                sog.page_up()
                a += 1
                if a == 3:
                    raise AssertionError("联系人只有一个，请再添加多个不同名字联系人组成群聊")
            else:
                break
        # 选择成员
        for name in names:
            slc.select_one_member_by_name(name)
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name(group_name)
        cgnp.click_sure()
        # 等待群聊页面加载
        GroupChatPage().wait_for_page_load()

    @staticmethod
    def enter_group_chat_page(reset=False):
        """进入群聊聊天会话页面"""
        # 确保已有群
        Preconditions.make_already_have_my_group(reset)
        # 如果有群，会在选择一个群页面，没有创建群后会在群聊页面
        scp = GroupChatPage()
        sogp = SelectOneGroupPage()
        if sogp.is_on_this_page():
            group_name = Preconditions.get_group_chat_name()
            # 点击群名，进入群聊页面
            sogp.click_one_contact(group_name)
            scp.wait_for_page_load()
        if scp.is_on_this_page():
            return
        else:
            raise AssertionError("Failure to enter group chat session page.")

    @staticmethod
    def get_group_chat_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "ag" + phone_number[-4:]
        return group_name

    @staticmethod
    def get_into_group_chat_page(name):
        """进入群聊聊天会话页面"""

        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击发起群聊
        mp.click_group_chat()
        scg = SelectContactsPage()
        times = 15
        n = 0
        # 重置应用时需要再次点击才会出现选择一个群
        while n < times:
            # 等待选择联系人页面加载
            flag = scg.wait_for_page_load()
            if not flag:
                scg.click_back()
                time.sleep(2)
                mp.click_add_icon()
                mp.click_group_chat()
            else:
                break
            n += 1
        scg.click_select_one_group()
        sog = SelectOneGroupPage()
        # 等待“选择一个群”页面加载
        sog.wait_for_page_load()
        # 选择一个普通群
        sog.selecting_one_group_by_name(name)
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @staticmethod
    def if_exists_multiple_enterprises_enter_group_chat():
        """选择团队联系人时存在多个团队时返回获取当前团队名，再进入群聊分享群二维码"""

        shc = SelectHeContactsDetailPage()
        # 测试号码是否存在多个团队
        if not shc.is_exist_corporate_grade():
            mp = MessagePage()
            scg = SelectContactsPage()
            gcp = GroupChatPage()
            shc.click_back()
            scg.wait_for_page_load()
            scg.click_back()
            gcp.wait_for_page_load()
            gcp.click_back()
            mp.wait_for_page_load()
            mp.open_workbench_page()
            wbp = WorkbenchPage()
            wbp.wait_for_workbench_page_load()
            time.sleep(2)
            # 获取当前团队名
            workbench_name = wbp.get_workbench_name()
            mp.open_message_page()
            mp.wait_for_page_load()
            group_name = "群聊1"
            Preconditions.get_into_group_chat_page(group_name)
            gcp.click_setting()
            gcs = GroupChatSetPage()
            gcs.wait_for_page_load()
            gcs.click_QRCode()
            n = 1
            while not gcs.page_should_contain_text2("该二维码7天内"):
                gcs.click_back()
                gcs.wait_for_page_load()
                gcs.click_QRCode()
                n += 1
                if n > 10:
                    break
            code_page = GroupChatSetSeeQRCodePage()
            code_page.wait_for_page_load()
            gcs.click_qecode_share_button()
            scg.wait_for_page_load()
            scg.click_he_contacts()
            shc.wait_for_he_contacts_page_load()
            # 选择当前团队
            shc.click_department_name(workbench_name)

    @staticmethod
    def background_app():
        """后台运行"""
        current_mobile().press_home_key()

    @staticmethod
    def enter_single_chat_page(name):
        """进入单聊聊天会话页面"""
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击 +
        mp.click_add_icon()
        # 点击“新建消息”
        mp.click_new_message()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 进入单聊会话页面
        slc.selecting_local_contacts_by_name(name)
        bcp = BaseChatPage()
        if bcp.is_exist_dialog():
            # 点击我已阅读
            bcp.click_i_have_read()
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()


class MsgGroupChatTest(TestCase):
    """
    模块：消息->群聊
    文件位置：冒烟/冒烟测试用例-V20181225.01.xlsx
    表格：消息-群聊
    """

    @classmethod
    def setUpClass(cls):

        Preconditions.select_mobile('Android-移动')
        # 导入测试联系人、群聊
        fail_time1 = 0
        flag1 = False
        import dataproviders
        while fail_time1 < 3:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                current_mobile().hide_keyboard_if_display()
                Preconditions.make_already_in_message_page()
                conts.open_contacts_page()
                try:
                    if conts.is_text_present("发现SIM卡联系人"):
                        conts.click_text("显示")
                except:
                    pass
                for name, number in required_contacts:
                    # 创建联系人
                    conts.create_contacts_if_not_exits(name, number)
                required_group_chats = dataproviders.get_preset_group_chats()
                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name, members in required_group_chats:
                    group_list.wait_for_page_load()
                    # 创建群
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.click_back()
                conts.open_message_page()
                flag1 = True
            except:
                fail_time1 += 1
            if flag1:
                break

    def default_setUp(self):
        """确保每个用例运行前在群聊聊天会话页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_group_chat_page()
            return
        scp = GroupChatPage()
        if scp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_group_chat_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0001(self):
        """在群聊聊天会话页面，发送一段字符数等于“0”的文本字符"""
        # 1.在当前聊天会话页面，在输入框中不输入任何内容，输入框右边展示的按钮是否是语音按钮
        gcp = GroupChatPage()
        # 语音按钮检查
        gcp.page_should_contain_audio_btn()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0002(self):
        """在群聊聊天会话页面，发送一段字符数大于“0”的文本字符"""
        # 1.在当前聊天会话页面，在输入框中输入一段文本，字符数大于0
        gcp = GroupChatPage()
        info = "Hello everyone!"
        gcp.input_message(info)
        # 2.点击输入框右边高亮展示的发送按钮，发送此段文本
        gcp.page_should_contain_send_btn()
        gcp.send_message()
        gcp.page_should_contain_text(info)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0003(self):
        """在群聊聊天会话页面，发送一段字符数小于等于“5000”的文本字符"""
        # 1.在当前聊天会话页面，在输入框中输入一段文本，字符数小于5000
        gcp = GroupChatPage()
        info = "Hello everyone, Welcome to my group, I hope my group can bring you happy."
        gcp.input_message(info)
        # 2.点击输入框右边高亮展示的发送按钮，发送此段文本
        gcp.page_should_contain_send_btn()
        gcp.send_message()
        gcp.page_should_contain_text(info)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0004(self):
        """在群聊聊天会话页面，发送一段字符数等于“5000”的文本字符"""
        # 1.在当前聊天会话页面，在输入框中输入一段文本，字符数等于5000
        gcp = GroupChatPage()
        info = "哈哈" * 2500
        gcp.input_message(info)
        # 2.点击输入框右边高亮展示的发送按，发送此段文本
        gcp.page_should_contain_send_btn()
        gcp.send_message()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0005(self):
        """在群聊聊天会话页面，发送一段字符数大于“5000”的文本字符"""
        # 1.在当前聊天会话页面，在输入框中输入一段文本，字符数等于5000
        gcp = GroupChatPage()
        info = "呵呵" * 2501
        gcp.input_message(info)
        # 2.在输入框中不可以输入一段字符大于5000文本
        gcp.page_should_contain_send_btn()
        info = gcp.get_input_message()
        self.assertEqual(len(info), 5000)
        gcp.send_message()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0006(self):
        """在群聊聊天会话页面，发送相册内的图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        # 点击图片按钮
        gcp.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.不选择照片时，发送按钮是否置灰展示并且不可点击
        flag = cpg.send_btn_is_enabled()
        self.assertEquals(flag, False)
        # 回到聊天回话页面
        cpg.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0007(self):
        """在群聊聊天会话页面，发送相册内的图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        # 点击图片按钮
        gcp.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，点击右下角高亮展示的发送按钮，发送此照片
        cpg.select_pic()
        # 发送按钮可点击
        self.assertTrue(cpg.send_btn_is_enabled())
        cpg.click_send()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0011(self):
        """在群聊聊天会话页面，发送相册内的图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，直接点击当前选中的图片，是否会放大展示当前图片
        cpg.click_pic_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        # 3、当前放大图片的左上角是否会展示格式为：当前图片张数/当前相册的总张数
        preview_info = cppp.get_pic_preview_info()
        self.assertIsNotNone(re.match(r'预览\(\d+/\d+\)', preview_info))
        cppp.click_back()
        cpg.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0012(self):
        """在群聊聊天会话页面，发送相册内的图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、选择2张照片后，点击左下角的预览按钮，当前图片预览放大后，右上角的编辑按钮是否已隐藏
        cpp.select_pic(n=2)
        cpp.click_preview()
        pic_preview = ChatPicPreviewPage()
        pic_preview.wait_for_page_load()
        # 3、当前放大页面的右下角发送按钮，是否高亮展示并且展示当前已选择的图片数量
        send_num = pic_preview.get_pic_send_num()
        self.assertEqual(send_num, '2')
        # 4、点击发送按钮，能否进行发送
        pic_preview.click_send()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0013(self):
        """在群聊聊天会话页面，发送相册内的图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2.选择9张图片后，相册详情右下角的发送按钮上方是否会高亮展示，并且展示已选择的图片数量
        cpp.select_pic(n=9)
        self.assertTrue(cpp.send_btn_is_enabled())
        send_num = cpp.get_pic_send_num()
        self.assertEqual(send_num, '9')
        # 3.点击相册详情右下角的发送按钮，能否进行发送
        cpp.click_send(times=5)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0014(self):
        """在群聊聊天会话页面，发送相册内的图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、在当前页面选择第10张图片，是否会有提示
        cpp.select_pic(n=10)
        flag = cpp.is_toast_exist("最多只能选择9张照片")
        self.assertTrue(flag)
        cpp.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0015(self):
        """在群聊聊天会话页面，发送相册内的图片"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、在当前页面选择图片和视频时，是否会有提示
        cpp.select_pic()
        cpp.select_video()
        flag = cpp.is_toast_exist("不能同时选择照片和视频")
        self.assertTrue(flag)
        cpp.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0016(self):
        """在群聊聊天会话页面，发送相册内的视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、在当前相册详情页面，选择一个视频，右下角的发送按钮是否会高亮展示
        cpp.select_video()
        self.assertTrue(cpp.send_btn_is_enabled())
        cpp.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0017(self):
        """在群聊聊天会话页面，发送相册内的视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、在当前相册详情页面，相册详情中是否会展示其中视频的可播放长度
        times = cpp.get_video_times()
        for time in times:
            self.assertIsNotNone(re.match(r'\d+:\d+', time))
        cpp.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0018(self):
        """在群聊聊天会话页面，发送相册内的视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、在当前相册详情页面，选择一个视频后，点击左下角的预览按钮，是否会以预览模式放大展示当前视频
        cpp.select_video()
        cpp.click_preview()
        video_preview = ChatPicPreviewPage()
        video_preview.wait_for_video_preview_load()
        # 3、预览展示的视频页面中，是否存在点击可播放的三角形按钮
        self.assertTrue(video_preview.play_video_btn_is_enabled())
        # 4、预览播放视频中途，点击左上角的返回按钮，是否可以返回到上一级页面
        video_preview.play_video()
        video_preview.close_video()
        video_preview.click_back()
        cpp.wait_for_page_load()
        cpp.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0019(self):
        """在群聊聊天会话页面，发送相册内的视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2.在当前相册详情页面，选择2个视频，选择第二个视频时，是否会提示：最多只能选择1个视频的提示
        cpp.select_video(n=0)
        cpp.select_video(n=1)
        flag = cpp.is_toast_exist("最多只能选择1个视频")
        self.assertTrue(flag)
        cpp.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0020(self):
        """在群聊聊天会话页面，发送相册内的视频"""
        # 1、在当前聊天会话页面，点击输入框左上方的相册图标，进入到相册详情展示页面
        gcp = GroupChatPage()
        gcp.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、在当前相册详情页面，选择一张照片或者视频后，点击左上角的返回按钮，是否可以返回到聊天会话页面
        cpp.select_pic()
        cpp.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0022(self):
        """在群聊聊天会话页面，拍照发送照片"""
        # 1、在当前聊天会话页面，点击输入框上方的相机图标，进入到相机拍摄页面
        gcp = GroupChatPage()
        gcp.click_take_photo()
        # 2、在相机拍摄页面，轻触拍摄按钮，是否可以拍摄成功一张照片
        cpp = ChatPhotoPage()
        cpp.take_photo()
        # 3、照片拍摄成功后，点击左边的返回按钮，是否可以删除本次拍摄的照片
        cpp.click_back()
        # 4、重新拍摄一张照片后，点击右边的√按钮，是否可以发送这张照片
        cpp.take_photo()
        cpp.send_photo()

    @unittest.skip("无法实现")
    def test_msg_group_chat_0023(self):
        """在群聊聊天会话页面，拍照发送照片"""
        # 无法实现：appium执行按压1s操作服务器响应需要3s，在这3s时间内toast提示已消失，无法捕获提示
        # 1、在当前聊天会话页面，点击输入框上方的相机图标，进入到相机拍摄页面
        gcp = GroupChatPage()
        gcp.click_take_photo()
        # 2、在相机拍摄页面，长按拍摄按钮，是否可以进入到录像模式
        video = ChatPhotoPage()
        video.wait_for_page_load()
        video.record_video(times=1000)
        # 3.在录像模式下，长按录像按钮，1秒钟之后，松开手指，是否会提示：拍摄失败
        flag = video.is_toast_exist("拍摄失败", timeout=5, poll_frequency=0.01)
        self.assertTrue(flag)
        video.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0024(self):
        """在群聊聊天会话页面，拍照发送照片"""
        # 1、在当前聊天会话页面，点击输入框上方的相机图标，进入到相机拍摄页面
        gcp = GroupChatPage()
        gcp.click_take_photo()
        # 2、在相机拍摄页面，长按拍摄按钮，进入到录像模式
        video = ChatPhotoPage()
        video.wait_for_page_load()
        # 3.在录像模式下，长按录像按钮，10秒钟之后，松开手指，是否会展示并且自动播放当前录制的10秒录像
        video.record_video(times=11000)
        video.wait_for_record_video_after_page_load()
        # 4.在录像展示页面，点击左边的返回按钮，是否可以删除本次录像
        video.click_back()
        video.take_photo_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0025(self):
        """在群聊聊天会话页面，拍照发送照片"""
        # 1、在当前聊天会话页面，点击输入框上方的相机图标，进入到相机拍摄页面
        gcp = GroupChatPage()
        gcp.click_take_photo()
        # 2、在相机拍摄页面，长按拍摄按钮，进入到录像模式
        video = ChatPhotoPage()
        video.wait_for_page_load()
        # 3.在录像模式下，长按录像按钮，10秒钟之后，松开手指，是否会展示并且自动播放当前录制的10秒录像
        video.record_video(times=11000)
        video.wait_for_record_video_after_page_load()
        # 4.在录像展示页面，点击右边的√按钮，是否可以发送本次录像
        video.send_video()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0027(self):
        """在群聊聊天会话页面，拍照发送照片/录像"""
        # 1、在当前聊天会话页面，点击输入框上方的相机图标，进入到相机拍摄页面
        gcp = GroupChatPage()
        gcp.click_take_photo()
        # 2、在相机拍摄页面，点击左下角倒三角，是否可以返回到聊天会话页面
        video = ChatPhotoPage()
        video.wait_for_page_load()
        video.take_photo_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0028(self):
        """在群聊聊天会话页面，发送名片消息"""
        # 1.在当前聊天会话页面，点击输入框上方的名片图标，进入到名片详情页面
        gcp = GroupChatPage()
        gcp.click_profile()
        # 2.在名片详情页面，是否可以选择本地联系人名片，进行发送
        cpp = ChatProfilePage()
        cpp.wait_for_page_load()
        cpp.select_card()
        cpp.wait_for_card_page_load()
        cpp.send_card()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0029(self):
        """在群聊聊天会话页面，发送名片消息"""
        # 1.在当前聊天会话页面，点击输入框上方的名片图标，进入到名片详情页面
        gcp = GroupChatPage()
        gcp.click_profile()
        # 2.在名片详情页面，是否可以搜索选择本地联系人名片，进行发送
        cpp = ChatProfilePage()
        cpp.wait_for_page_load()
        # names = cpp.get_contacts_name()
        names = cpp.get_first_page_contacts_name()
        if "和通讯录" in names:
            names.remove("和通讯录")
        if "和飞信电话" in names:
            names.remove("和飞信电话")
        # 随机选择一个联系人，进行搜索发送
        cpp.search(random.choice(names))
        cpp.select_card()
        cpp.wait_for_card_page_load()
        cpp.send_card()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0030(self):
        """在群聊聊天会话页面，发送名片消息"""
        # 1.在当前聊天会话页面，点击输入框上方的名片图标，可进入到名片详情页面
        gcp = GroupChatPage()
        gcp.click_profile()
        # 2.在名片详情页面，不可以搜索选择陌生联系人名片，进行发送
        cpp = ChatProfilePage()
        cpp.wait_for_page_load()
        # names = cpp.get_contacts_name()
        names = cpp.get_first_page_contacts_name()
        # 构造陌生联系人名
        name = ""
        while True:
            info = "在名片详情页面，不可以搜索选择陌生联系人名片，进行发送"
            name = random.choices(info, k=3)
            if name not in names:
                break
        cpp.search(name)
        # flag = cpp.select_card()
        # self.assertFalse(flag)
        time.sleep(1)
        # 由于页面元素原因，拿“手机联系人”文本做判断是否搜索成功
        self.assertEquals(cpp.is_text_present("手机联系人"), False)
        cpp.click_back()
        time.sleep(1)
        cpp.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0033(self):
        """在群聊聊天会话页面，发送名片消息"""
        # 1.在当前聊天会话页面，点击输入框上方的名片图标，进入到名片详情页面
        gcp = GroupChatPage()
        gcp.click_profile()
        # 2.在名片详情页面，点击右侧的索引字母，索引字母定位搜索是否正常
        cpp = ChatProfilePage()
        cpp.wait_for_page_load()
        # 获取所有右侧索引字母，随机选择一个点击
        letters = cpp.get_letters_index()
        letter = random.choice(letters)
        cpp.click_letter_index(letter)
        left_lets = cpp.get_left_letters()
        if letter not in left_lets:
            raise AssertionError("在名片详情页面，点击右侧的索引字母，索引字母定位搜索异常")
        cpp.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0034(self):
        """在群聊聊天会话页面，发送GIF图片消息"""
        # 1.在当前聊天会话页面，点击输入框上方的GIF图标，进入到GIF图片展示页面
        gcp = GroupChatPage()
        gcp.click_gif()
        # 2、在GIF图片展示页面，直接点击上方展示的GIF图片，能否可以进行发送
        gif = ChatGIFPage()
        gif.wait_for_page_load()
        gif.send_gif()
        # 3.在GIF图片展示页面，多次点击上方展示的GIF图片，发送出去的GIF图片是否会展示多张
        gif.send_gif()
        gif.send_gif()
        # 4、点击输入框左上角的X按钮是否可以关闭GIF图片的展示
        gif.close_gif()
        gcp.page_should_not_contain_text("趣图搜搜")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0035(self):
        """在群聊聊天会话页面，发送GIF图片消息"""
        # 1.在当前聊天会话页面，点击输入框上方的GIF图标，进入到GIF图片展示页面
        gcp = GroupChatPage()
        gcp.click_gif()
        gif = ChatGIFPage()
        gif.wait_for_page_load()
        # 2、在输入框中输入英文、中文、字符、数字、表情，是否可以搜索出对应的GIF图片
        # 3、在输入框中输入的搜索条件，搜索不出对应的GIF图片时，是否会提示：无搜索结果,换个热词试试
        infos = ["appium", "哈哈", "a", "123456", "w(ﾟДﾟ)w"]
        try:
            for info in infos:
                gif.input_message(info)
                toast_flag = gif.is_toast_exist("无搜索结果，换个热词试试", timeout=4)
                gif_flag = gif.is_gif_exist()
                self.assertTrue(toast_flag or gif_flag)
        finally:
            gif.close_gif()
            gif.input_message("")
            gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0036(self):
        """在群聊聊天会话页面，发送GIF图片消息"""
        # 1.在当前聊天会话页面，点击输入框上方的GIF图标，进入到GIF图片展示页面
        gcp = GroupChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gcp.click_gif()
        gif.wait_for_page_load()
        # 2、在GIF图片展示页面，点击输入框右边的语音，是否可以切换到语音模式页面
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if gcp.is_text_present("请选择您偏好的语音发送模式"):
            audio.click_sure()
        audio.wait_for_page_load()
        audio.click_exit()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0037(self):
        """在群聊聊天会话页面，点击输入框右上角的+号，展示隐藏图标按钮"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，是否会展示隐藏功能图标
        gcp = GroupChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        if not gcp.is_open_more():
            gcp.click_more()
        time.sleep(1)
        gcp.page_should_contain_text("文件")
        gcp.page_should_contain_text("群短信")
        gcp.page_should_contain_text("位置")
        gcp.page_should_contain_text("红包")
        gcp.click_more()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0038(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，文件功能图标"""
        files = ['.txt', '.pdf', '.docx', '.jpg', '.xlsx', '.BPG', '.mp4', '.avi']
        for file_type in files:
            # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
            gcp = GroupChatPage()
            if not gcp.is_open_more():
                gcp.click_more()
            # 2.点击展示的隐藏功能图标，文件图标，进入到文件选择页面
            more_page = ChatMorePage()
            more_page.click_file()
            # 3、点击本地文件，进入到本地文件中，选择.txt,.pdf,.docx,.xlsx,.jpg,.BPG,.MP4,.AVI等格式的文件，
            # 选择完成后，右下角的发送按钮是否变成高亮展示
            csf = ChatSelectFilePage()
            csf.wait_for_page_load()
            csf.click_local_file()
            local_file = ChatSelectLocalFilePage()
            # 没有预置文件，则上传
            flag = local_file.push_preset_file()
            if flag:
                local_file.click_back()
                csf.click_local_file()
            # 进入预置文件目录，选择文件发送
            local_file.click_preset_file_dir()
            file = local_file.select_file(file_type)
            if file:
                self.assertTrue(local_file.send_btn_is_enabled())
                # 4.选择文件后，左下角是否会展示已选择文件的大小
                file_size = local_file.get_file_size()
                select_file_size = local_file.get_selected_file_size()
                self.assertIn(file_size, select_file_size)
                # 5.右下角的发送按钮高亮展示后，点击发送按钮，是否可以进行发送
                local_file.click_send()
            else:
                local_file.click_back()
                local_file.click_back()
                csf.click_back()
                gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0039(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，文件功能图标"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
        gcp = GroupChatPage()
        if not gcp.is_open_more():
            gcp.click_more()
        # 2.点击展示的隐藏功能图标，文件图标，进入到文件选择页面
        more_page = ChatMorePage()
        more_page.click_file()
        # 3.点击视频选择项，进入到本地视频详情展示页面。当前页面的发送按钮，是否默认置灰展示
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_video()
        local_file = ChatSelectLocalFilePage()
        self.assertFalse(local_file.send_btn_is_enabled())
        # 4.选择一个视频之后，左下角是否会展示当前选择视频的大小，右下角的发送按钮变成高亮展示
        el = local_file.select_file2("视频")
        if el:
            self.assertTrue(local_file.send_btn_is_enabled())
            # 5.点击右下角高亮展示的发送按钮，是否可以发送
            local_file.click_send()
        else:
            local_file.click_back()
            csf.click_back()
            gcp.wait_for_page_load()
            raise AssertionError("There is no video")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0040(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，文件功能图标"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
        gcp = GroupChatPage()
        if not gcp.is_open_more():
            gcp.click_more()
        # 2.点击展示的隐藏功能图标，文件图标，进入到文件选择页面
        more_page = ChatMorePage()
        more_page.click_file()
        # 3.点击照片选择项，进入到本地照片详情展示页面。当前页面的发送按钮，是否默认置灰展示
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_pic()
        time.sleep(2)
        local_file = ChatSelectLocalFilePage()
        self.assertFalse(local_file.send_btn_is_enabled())
        # 4、选择一张照片之后，左下角是否会展示当前选择照片的大小，右下角的发送按钮变成高亮展示
        el = local_file.select_file2("照片")
        if el:
            self.assertTrue(local_file.send_btn_is_enabled())
            # 5.点击右下角高亮展示的发送按钮，是否可以发送
            local_file.click_send()
        else:
            local_file.click_back()
            csf.click_back()
            gcp.wait_for_page_load()
            raise AssertionError("There is no picture")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0041(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，文件功能图标"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
        gcp = GroupChatPage()
        if not gcp.is_open_more():
            gcp.click_more()
        # 2.点击展示的隐藏功能图标，文件图标，进入到文件选择页面
        more_page = ChatMorePage()
        more_page.click_file()
        # 3.点击音乐选择项，进入到本地音乐文件详情展示页面。当前页面的发送按钮，是否默认置灰展示
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_music()
        local_file = ChatSelectLocalFilePage()
        self.assertFalse(local_file.send_btn_is_enabled())
        # 4.选择一个音乐文件之后，左下角是否会展示当前选择音乐文件的大小，右下角的发送按钮变成高亮展示
        el = local_file.select_file2("音乐")
        if el:
            self.assertTrue(local_file.send_btn_is_enabled())
            # 5.点击右下角高亮展示的发送按钮，是否可以发送
            local_file.click_send()
        else:
            local_file.click_back()
            csf.click_back()
            gcp.wait_for_page_load()
            raise AssertionError("There is no music")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG')
    def test_msg_group_chat_0043(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，位置功能图标"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
        gcp = GroupChatPage()
        if not gcp.is_open_more():
            gcp.click_more()
        # 2.点击展示的隐藏功能图标，位置功能图标，进入到位置详情展示页面
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 3.在当前页面底部展示的地标选择项中，是否会默认选中第一项。
        self.assertTrue(location_page.is_selected_first_item())
        # 4.位置底部，地标选择项是否可以手动切换选择项
        location_page.select_other_item()
        # 5.选择完成后，点击右上角的发送按钮，是否可以发送
        addr = location_page.get_location_info()
        location_page.click_send()
        gcp.wait_for_page_load()
        # gcp.wait_until(condition=lambda d: gcp.is_text_present(addr))

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat', 'DEBUG')
    def test_msg_group_chat_0044(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，位置功能图标"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        if not gcp.is_open_more():
            gcp.click_more()
        # 2.点击展示的隐藏功能图标，位置功能图标，进入到位置详情展示页面
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 3.在当前页面底部展示的地标选择项中，是否会默认选中第一项。
        self.assertTrue(location_page.is_selected_first_item())
        # 4、直接点击当前页面的右上角发送按钮，是否可以发送默认选择项位置
        addr = location_page.get_location_info()
        location_page.click_send()
        gcp.wait_for_page_load()
        # gcp.page_should_contain_text(addr)

    @staticmethod
    def setUp_test_msg_group_chat_0420():
        """重置应用后进入群聊聊天会话页面"""
        Preconditions.enter_group_chat_page(reset=True)
        # 确保每个用例运行前在群聊聊天会话页面
        scp = GroupChatPage()
        if scp.is_on_this_page():
            return
        else:
            current_mobile().disconnect_mobile()
            Preconditions.enter_group_chat_page(reset=True)

    @tags('ALL', 'SMOKE', 'CMCC_RESET', 'group_chat')
    def test_msg_group_chat_0420(self):
        """在群聊聊天会话页面，点击输入框右上角+，展示的隐藏功能图标，位置功能图标"""
        # 1.在当前聊天会话页面，点击输入框右上方的+号，展示隐藏功能图标后
        gcp = GroupChatPage()
        gcp.click_more()
        # 2.点击展示的隐藏功能图标，位置功能图标，是否会弹出权限允许申请弹窗
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_permission_message_load()
        location_page.wait_for_page_load()
        location_page.click_back()
        gcp.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_group_chat_0470():
        """重置应用后进入群聊聊天会话页面"""
        Preconditions.enter_group_chat_page(reset=True)
        # 确保每个用例运行前在群聊聊天会话页面
        scp = GroupChatPage()
        if scp.is_on_this_page():
            return
        else:
            current_mobile().disconnect_mobile()
            Preconditions.enter_group_chat_page(reset=True)

    @tags('ALL', 'SMOKE', 'CMCC_RESET', 'group_chat')
    def test_msg_group_chat_0470(self):
        """在群聊聊天会话页面，点击输入框右边的语音按钮"""
        # 1.在当前聊天会话页面，点击输入框右边的语音按钮，在未获取录音权限时，是否会弹出权限申请允许弹窗
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        if audio.wait_for_audio_type_select_page_load():
            audio.click_sure()
        # 权限申请允许弹窗判断
        flag = audio.wait_for_audio_allow_page_load()
        self.assertTrue(flag)
        audio.click_allow()
        audio.wait_until(condition=lambda d: audio.is_text_present("退出"))
        audio.click_exit()
        gcp.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_group_chat_0480():
        """重置应用后进入群聊聊天会话页面"""
        Preconditions.enter_group_chat_page(reset=True)
        # 确保每个用例运行前在群聊聊天会话页面
        scp = GroupChatPage()
        if scp.is_on_this_page():
            return
        else:
            current_mobile().disconnect_mobile()
            Preconditions.enter_group_chat_page(reset=True)

    @tags('ALL', 'SMOKE', 'CMCC_RESET', 'group_chat')
    def test_msg_group_chat_0480(self):
        """首次使用语音功能"""
        # 1、点击输入框右边的语音按钮，跳转到的页面是否是语音模式设置页面
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        audio = ChatAudioPage()
        flag = audio.wait_for_audio_type_select_page_load()
        self.assertTrue(flag)
        # 2、默认展示的选择项是否是，语音+文字模式
        info = audio.get_selected_item()
        self.assertIn("语音+文字", info)
        audio.click_sure()
        audio.wait_for_page_load()
        audio.click_exit()
        gcp.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_group_chat_0520():
        """重置应用后进入群聊聊天会话页面"""
        Preconditions.enter_group_chat_page(reset=True)
        # 确保每个用例运行前在群聊聊天会话页面
        scp = GroupChatPage()
        if scp.is_on_this_page():
            return
        else:
            current_mobile().disconnect_mobile()
            Preconditions.enter_group_chat_page(reset=True)

    @tags('ALL', 'SMOKE', 'CMCC_RESET', 'group_chat')
    def test_msg_group_chat_0520(self):
        """在群聊聊天会话页面，点击输入框右边的语音按钮"""
        # 1.在当前聊天会话页面，点击输入框右边的语音按钮，进入到语音录制页面
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        # 2.首次使用语音录制功能时，点击语音按钮是否会跳转到，语音模式选择页面
        audio = ChatAudioPage()
        flag = audio.wait_for_audio_type_select_page_load()
        self.assertTrue(flag)
        # 3.在语音模式选择页面，是否会默认展示已选择：同时发送语音+文字（语音识别）选择项
        info = audio.get_selected_item()
        self.assertIn("同时发送语音+文字(语音识别)", info)
        # 4.在语音模式选择页面，是否可以手动更改已选择的模式
        audio.select_other_audio_item()
        # 5.更改模式后，点击右下角的确定按钮，是否可以跳转到语音录制页面
        audio.click_sure()
        audio.wait_for_page_load()
        audio.click_exit()
        gcp.wait_for_page_load()

    @staticmethod
    def setUp_test_msg_group_chat_0530():
        """重置应用后进入群聊聊天会话页面"""
        Preconditions.enter_group_chat_page(reset=True)
        # 确保每个用例运行前在群聊聊天会话页面
        scp = GroupChatPage()
        if scp.is_on_this_page():
            return
        else:
            current_mobile().disconnect_mobile()
            Preconditions.enter_group_chat_page(reset=True)

    @tags('ALL', 'SMOKE', 'CMCC_RESET', 'group_chat')
    def test_msg_group_chat_0530(self):
        """在群聊聊天会话页面，点击输入框右边的语音按钮"""
        # 1.在当前聊天会话页面，点击输入框右边的语音按钮，进入到语音录制页面
        gcp = GroupChatPage()
        gcp.click_audio_btn()
        # 2.首次使用语音录制功能时，点击语音按钮会跳转到，语音模式选择页面
        audio = ChatAudioPage()
        flag = audio.wait_for_audio_type_select_page_load()
        self.assertTrue(flag)
        # 3.在语音模式选择页面，点击取消是否可以返回到聊天会话页面
        audio.click_cancel()
        audio.wait_for_page_load()
        audio.click_exit()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0058(self):
        """在群聊聊天设置页面"""
        # 1.在聊天设置页面，点击群成员展示的右边“>”三角形符号，是否可以展示群成员列表
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.click_group_member_show()
        group_member = GroupChatSetSeeMembersPage()
        group_member.wait_for_page_load()
        # 2.在展示的群成员列表上方是否会展示，未进群提示
        flag = group_member.is_others_not_in_group()
        if flag:
            # 3.点击未进群提示，是否可以进入到未进群成员展示列表
            group_member.click_invite_prompt()
            group_member.wait_for_invite_page_load()
            group_member.invite_back()
            group_set.click_group_member_show()
            group_member.wait_for_page_load()
        # 4.点击群成员列表中的成员，是否可以跳转到个人profile页
        group_member.click_group_member()
        if not group_member.is_toast_exist("该联系人不可选择", 3):
            group_member.wait_for_profile_page_load()
            group_member.profile_back()
            group_member.wait_for_page_load()
        # 5.在群成员列表上方的搜索框，通过英文（大、小写）、中文、等搜索条件，搜索出符合条件的结果
        names = group_member.get_all_group_member_names()
        group_member.search(names[0])
        results = group_member.get_all_group_member_names()
        self.assertIn(names[0], results)
        name1 = str(uuid.uuid1()) + "Name"
        group_member.search(name1)
        # results1 = group_member.get_all_group_member_names()
        # self.assertEqual(0, len(results1))
        time.sleep(1)
        self.assertEquals(group_member.is_text_present("无搜索结果"), True)
        name2 = str(uuid.uuid1()) + "中文"
        group_member.search(name2)
        # results2 = group_member.get_all_group_member_names()
        # self.assertEqual(0, len(results2))
        time.sleep(1)
        self.assertEquals(group_member.is_text_present("无搜索结果"), True)
        group_member.click_back()
        time.sleep(1)
        group_member.click_back()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0060(self):
        """在群聊聊天设置页面"""
        # 1.在聊天设置页面，点击群成员右下角展示+号，添加成员按钮，是否会跳转到联系人选择器页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_add_member()
        # 2.在联系人选择器页面，是否可以选择本地联系人
        # 3、在联系人选择器页面，是否可以选择和通讯录联系人
        # 4、在联系人选择器页面，未选择任何联系人时，右上角展示的确定按钮是否是置灰展示
        contacts_page = SelectLocalContactsPage()
        contacts_page.wait_for_page_load()
        # 选择与否获取的属性都是可点击
        # flag = contacts_page.sure_btn_is_enabled()
        # self.assertFalse(flag)
        # 5、选择联系人后，右上角的确定按钮上是否会展示已选择人数加剩余可选择人数，例：确定（2/462）
        names = contacts_page.get_contacts_name_list()
        for name in names:
            contacts_page.select_one_member_by_name(name)
        info = contacts_page.get_sure_btn_text()
        self.assertIsNotNone(re.match(r'确定\(\d+/\d+\)', info))
        # 返回聊天页面
        contacts_page.click_back()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0061(self):
        """在群聊聊天设置页面"""
        # 1.在聊天设置页面，点击群成员右下角展示+号，添加成员按钮，是否会跳转到联系人选择器页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_add_member()
        # 2.在联系人选择器页面，单击是否可以选择联系人
        contacts_page = SelectLocalContactsPage()
        contacts_page.wait_for_page_load()
        names = contacts_page.get_contacts_name_list()
        if "本机" in names:
            names.remove("本机")
        contacts_page.select_one_member_by_name(names[0])
        # flag = contacts_page.contacts_is_selected(names[0])
        time.sleep(1)
        flag = contacts_page.is_exist_select_contacts_name()
        if not flag:
            raise AssertionError("在联系人选择器页面，单击不可以选择联系人")
        # 3.在联系人选择器页面，点击是否可以取消联系人的选择状态
        contacts_page.select_one_member_by_name(names[0])
        # flag2 = contacts_page.contacts_is_selected(names[0])
        time.sleep(1)
        flag2 = contacts_page.is_exist_select_contacts_name()
        if flag2:
            raise AssertionError("在联系人选择器页面，单击不可以取消联系人的选择状态")
        contacts_page.click_back()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0062(self):
        """在群聊聊天设置页面"""
        # 1.在聊天设置页面，点击群成员右下角展示+号，添加成员按钮，跳转到联系人选择器页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_add_member()
        # 2.在联系人选择器页面，选择多个联系人之后，点击左上角的返回按钮，
        # 是否可以返回到聊天会话页面并且清除已选择的联系人选择状态
        contacts_page = SelectLocalContactsPage()
        contacts_page.wait_for_page_load()
        names = contacts_page.get_contacts_name_list()
        for name in names:
            contacts_page.select_one_member_by_name(name)
        contacts_page.click_back()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0063(self):
        """在群聊聊天设置页面"""
        # 1.在聊天设置页面，点击群成员右下角展示+号，添加成员按钮，跳转到联系人选择器页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_add_member()
        # 2.在联系人选择页面，把剩余可选择人数全部勾选上，点击右上角的确定按钮，是否可以发送邀请
        contacts_page = SelectLocalContactsPage()
        contacts_page.wait_for_page_load()
        names = contacts_page.get_contacts_name_list()
        contacts_page.swipe_to_top()
        for name in names:
            contacts_page.search_and_select_one_member_by_name(name)
        contacts_page.click_sure()
        gcp.wait_for_page_load()
        gcp.page_should_contain_text("发出群邀请")

    def msg_group_chat_0064_pre_condition(self):
        """test_msg_group_chat_0064执行前置条件"""
        # 从通讯录获取人数，如果人数不足510(一个群可以添加500人)则先创建联系人
        gcp = GroupChatPage()
        gcp.click_back()
        if gcp.is_text_present("选择一个群"):
            sogp = SelectOneGroupPage()
            sogp.click_back()
            sc = SelectContactsPage()
            sc.wait_for_page_load()
            sc.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.click_contacts()
        contacts_page = ContactsPage()
        contacts_page.wait_for_page_load()
        names = contacts_page.get_all_contacts_name()
        if "和通讯录" in names:
            names.remove("和通讯录")
        if "和飞信电话" in names:
            names.remove("和飞信电话")
        totals = len(names)
        if totals < 510:
            # 人数不足创建联系人
            nums = 510 - totals
            info = "abcdefghigklmnopqrstuvwxyz"
            bname = "z" + random.choice(info) + random.choice(info)
            bnumber = "1477" + str(time.time())[-4:]
            for n in range(1, nums + 1):
                name = bname + "%05d" % n
                names.append(name)
                number = bnumber + "%03d" % n
                contacts_page.click_add()
                ccp = CreateContactPage()
                ccp.wait_for_page_load()
                ccp.create_contact(name, number)
                cdp = ContactDetailsPage()
                cdp.wait_for_page_load()
                cdp.click_back_icon()
        # 人数足够回到群聊设置页面
        mess.open_message_page()
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        group_name = Preconditions.get_group_chat_name()
        sogp = SelectOneGroupPage()
        sogp.select_one_group_by_name(group_name)
        gcp.wait_for_page_load()
        gcp.click_setting()
        return names

    @tags('ALL', 'SMOKE', 'group_chat0064')
    def test_msg_group_chat_0064(self):
        """在群聊聊天设置页面，添加群成员"""
        names = self.msg_group_chat_0064_pre_condition()
        # 1.在聊天设置页面，点击群成员右下角展示+号，添加成员按钮，跳转到联系人选择器页面
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_add_member()
        contacts_page = SelectLocalContactsPage()
        contacts_page.wait_for_page_load()
        # 2.在联系人选择页面，勾选人数超出剩余可勾选人数，是否会提示
        for name in names:
            contacts_page.search_and_select_one_member_by_name(name)
        selected_nums, threshold_nums = contacts_page.get_selected_and_threshold_nums()
        if selected_nums > threshold_nums:
            name_list = contacts_page.get_contacts_name_list()
            if contacts_page.contacts_is_selected(name_list[0]):
                contacts_page.select_one_member_by_name(name_list[0])
            contacts_page.select_one_member_by_name(name_list[0])
            flag = contacts_page.is_toast_exist("最多只能选择" + str(threshold_nums) + "人", timeout=6)
            if not flag:
                raise AssertionError("勾选人数超出剩余可勾选人数无‘最多只能选择" + str(threshold_nums) + "人' 提示")
        else:
            raise AssertionError("没有选择超出剩余可勾选人数，请确定")
        contacts_page.click_sure()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'only_group_owner')
    def test_msg_group_chat_0065(self):
        """在群聊聊天设置页面，删除群成员"""
        # 1.在聊天设置页面，点击群成员右下角展示-号，移除群成员按钮，是否会跳转到群成员移除列表展示页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        nums = group_set.get_group_total_member()
        if nums != 1:
            print("当前群聊中只能有群主,请预置条件")
            group_set.click_back()
            gcp.wait_for_page_load()
            return
        group_set.click_del_member()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'group_chat_6_members')
    def test_msg_group_chat_0066(self):
        """在群聊聊天设置页面，删除群成员"""
        # 1.在聊天设置页面，点击群成员右下角展示-号，移除群成员按钮，是否可以跳转到群成员移除列表展示页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        nums = group_set.get_group_total_member()
        if nums < 3:
            print("当前群聊成员需要大于2,请预置条件")
            group_set.click_back()
            gcp.wait_for_page_load()
            return
        # 2.在群成员展示列表中，未选择需要进行移除的成员时，右上角的确定按钮是否默认置灰展示
        group_set.click_del_member()
        contacts = SelectLocalContactsPage()
        contacts.wait_for_page_load()
        # 3.在群成员展示列表中，点击勾选一个成员，右上角的确定是否会高亮展示并且展示已选择的移除数量
        names = contacts.get_contacts_name_list()
        contacts.select_one_member_by_name(names[0])
        info = contacts.get_sure_btn_text()
        self.assertIsNotNone(re.match(r'确定\(1/\d+\)', info))
        # 4.点击右上角高亮展示的确定按钮，是否可以移除当前成员
        contacts.click_sure()
        contacts.click_sure_del()
        group_set.wait_for_page_load()
        group_set.click_back()
        # 5.被移除的成员，是否会收到一条系统通知，你已被群主请出群聊
        # 6.在群聊聊天会话页面，是否会展示一条，XX被移除群聊的信息
        gcp.wait_for_page_load()
        gcp.page_should_contain_text("移出群")

    @tags('ALL', 'SMOKE', 'group_chat_6_members')
    def test_msg_group_chat_0067(self):
        """在群聊聊天设置页面，删除群成员"""
        # 1.在聊天设置页面，点击群成员右下角展示-号，移除群成员按钮，是否可以跳转到群成员移除列表展示页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        nums = group_set.get_group_total_member()
        if nums < 4:
            print("当前群聊成员需要大于3,请预置条件")
            group_set.click_back()
            gcp.wait_for_page_load()
            return
        group_set.click_del_member()
        # 2.在群成员展示列表中，未选择需要进行移除的成员时，右上角的确定按钮是否默认置灰展示
        contacts = SelectLocalContactsPage()
        contacts.wait_for_page_load()
        # 3.在群成员展示列表中，点击勾选2个成员，右上角的确定是否会高亮展示并且展示已选择的移除数量
        names = contacts.get_contacts_name_list()
        contacts.select_one_member_by_name(names[0])
        contacts.select_one_member_by_name(names[1])
        info = contacts.get_sure_btn_text()
        self.assertIsNotNone(re.match(r'确定\(2/\d+\)', info))
        # 4.点击右上角高亮展示的确定按钮，是否可以移除当前成员
        contacts.click_sure()
        contacts.click_sure_del()
        group_set.wait_for_page_load()
        group_set.click_back()
        # 5.被移除的成员，是否会收到一条系统通知，你已被群主请出群聊
        # 6.在群聊聊天会话页面，是否会展示一条，XX被移除群聊的信息
        gcp.wait_for_page_load()
        gcp.page_should_contain_text("移出群")

    @tags('ALL', 'SMOKE', 'group_chat_6_members')
    def test_msg_group_chat_0068(self):
        """在群聊聊天设置页面，删除群成员"""
        # 1.在聊天设置页面，点击群成员右下角展示-号，移除群成员按钮，是否可以跳转到群成员移除列表展示页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        nums = group_set.get_group_total_member()
        if nums != 3:
            print("当前群聊成员必须为3人,请预置条件")
            group_set.click_back()
            gcp.wait_for_page_load()
            return
        group_set.click_del_member()
        # 2.在群成员展示列表中，未选择需要进行移除的成员时，右上角的确定按钮是否默认置灰展示
        contacts = SelectLocalContactsPage()
        contacts.wait_for_page_load()
        # 3.在群成员展示列表中，点击勾选2个成员，右上角的确定是否会高亮展示并且展示已选择的移除数量
        names = contacts.get_contacts_name_list()
        contacts.select_one_member_by_name(names[0])
        contacts.select_one_member_by_name(names[1])
        info = contacts.get_sure_btn_text()
        self.assertIsNotNone(re.match(r'确定\(2/\d+\)', info))
        # 4.点击右上角高亮展示的确定按钮，是否可以移除当前成员
        contacts.click_sure()
        contacts.click_sure_del()
        # 5.被移除的成员，是否会收到一条系统通知，你已被群主请出群聊同时提示该群已解散
        # 6.在群聊聊天会话页面，是否会展示一条，XX被移除群聊的信息同时展示该群已解散
        flag = contacts.is_toast_exist("该群已解散")
        self.assertTrue(flag)

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0069(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，是否会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2.在群聊名称修改页面，点击左上角的“修改群聊名称”返回按钮，是否可以返回到聊天设置页面
        group_name.click_back()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0070(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2.在群聊名称修改页面，不修改直接点击右上角的保存按钮，是否可以进行保存
        group_name.click_save()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0071(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2、在群聊名称修改页面，录入29个英文（大小写）字母字符，点击右上角的保存按钮是否可以保存
        old_name = Preconditions.get_group_chat_name()
        new_name = "PreconditionsGetGroupChatName"
        group_name.input_group_name(new_name)
        group_name.click_save()
        flag = group_name.is_toast_exist("修改成功")
        self.assertTrue(flag)
        group_set.wait_for_page_load()
        # 改回之前的名字
        group_set.click_modify_group_name()
        group_name.input_group_name(old_name)
        group_name.click_save()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0072(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2.在群聊名称修改页面，不录入任何字符，右上角的保存按钮是否是置灰展示，不可点击
        group_name.input_group_name("")
        flag = group_name.save_btn_is_enabled()
        self.assertFalse(flag)
        # 回到群聊页面
        group_name.click_back()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0073(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2.在群聊名称修改页面，点击群名称右边的“X”符号，是否可以一次清除输入框中的群聊名称
        group_name.click_delete_group_name()
        # 3.群聊名称被清除后，右上角的保存按钮，是否会置灰展示不可点击
        flag = group_name.save_btn_is_enabled()
        self.assertFalse(flag)
        # 回到群聊页面
        group_name.click_back()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0074(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2.在群聊名称修改页面，录入30个英文（大小写）字母字符，点击右上角的保存按钮，是否可以保存
        old_name = Preconditions.get_group_chat_name()
        new_name = "PreconditionsGetGroupChatNameX"
        group_name.input_group_name(new_name)
        group_name.click_save()
        flag = group_name.is_toast_exist("修改成功")
        self.assertTrue(flag)
        group_set.wait_for_page_load()
        # 改回之前的名字
        group_set.click_modify_group_name()
        group_name.input_group_name(old_name)
        group_name.click_save()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0075(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2.在群名片修改页面，录入31个英文字符，不可以录入成功（只支持30个字符）
        new_name = "PreconditionsGetGroupChatNameXx"
        try:
            group_name.input_group_name(new_name)
        except:
            print("ok")
        else:
            name = group_name.get_input_group_name()
            if len(name) != 30:
                raise AssertionError("修改群名片录入31个英文字符，代码可以实现，请确认是否可以手动录入31个英文字符！")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0076(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2.在群聊名称修改页面，录入10个汉字，点击右上角的保存按钮，是否可以保存
        old_name = Preconditions.get_group_chat_name()
        new_name = "汉字群聊名称修改页面"
        group_name.input_group_name(new_name)
        group_name.click_save()
        flag = group_name.is_toast_exist("修改成功")
        self.assertTrue(flag)
        group_set.wait_for_page_load()
        # 改回之前的名字
        group_set.click_modify_group_name()
        group_name.input_group_name(old_name)
        group_name.click_save()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0077(self):
        """在聊天设置页面，修改群聊名称"""
        # 1.在聊天设置页面，点击群聊名称，会跳转到群聊名称修改页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_modify_group_name()
        group_name = GroupNamePage()
        group_name.wait_for_page_load()
        # 2.在群名片修改页面，不可以录入11个汉字（只能录入10个汉字）
        new_name = "汉字群聊名称修改页面字"
        try:
            group_name.input_group_name(new_name)
        except:
            print("ok")
        else:
            name = group_name.get_input_group_name()
            if len(name) != 10:
                raise AssertionError("修改群名片录入11个汉字，代码可以实现，请确认是否可以手动录入11个汉字！")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0078(self):
        """在聊天设置页面，分享群二维码"""
        # 1、在聊天设置页面，点击群二维码，是否会跳转到群聊二维码展示页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_QRCode()
        n = 1
        while not group_set.page_should_contain_text2("该二维码7天内"):
            group_set.click_back()
            group_set.wait_for_page_load()
            group_set.click_QRCode()
            n += 1
            if n > 10:
                break
        code_page = GroupChatSetSeeQRCodePage()
        code_page.wait_for_page_load()
        # 2、在当前群聊展示页面，点击左下角的分享按钮，是否会跳转到联系人选择器页面
        code_page.click_qecode_share_btn()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 3、在联系人选择器页面，选择一个群聊或者联系人，是否会弹出确认分享弹窗
        scp.select_local_contacts()
        local_contacts = SelectLocalContactsPage()
        names = local_contacts.get_contacts_name_list()
        if "本机" in names:
            names.remove("本机")
        local_contacts.select_one_member_by_name(names[0])
        # 4、点击确定是否可以分享成功
        local_contacts.click_sure_share()
        flag = code_page.is_toast_exist("已转发")
        self.assertTrue(flag)
        code_page.click_back()
        time.sleep(1)
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0079(self):
        """在聊天设置页面，分享群二维码"""
        # 1、在聊天设置页面，点击群二维码，是否会跳转到群聊二维码展示页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_QRCode()
        n = 1
        while not group_set.page_should_contain_text2("该二维码7天内"):
            group_set.click_back()
            group_set.wait_for_page_load()
            group_set.click_QRCode()
            n += 1
            if n > 10:
                break
        code_page = GroupChatSetSeeQRCodePage()
        code_page.wait_for_page_load()
        # 2、在当前群聊展示页面，点击右下角的下载按钮，是否会提示下载成功
        code_page.click_qecode_save_btn()
        flag = code_page.is_toast_exist("已保存")
        self.assertTrue(flag)
        # 3、点击左上角的“<”返回按钮，是否可以返回到聊天设置页面
        code_page.click_back()
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0080(self):
        """在聊天设置页面，修改我在本群的昵称"""
        # 1、在聊天设置页面，点击我在本群的昵称，是否会跳转到修改群名片页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_my_card()
        mycard = GroupChatSetModifyMyCardPage()
        mycard.wait_for_page_load()
        # 2、在修改群名片页面，输入新的名称，点击右上角的保存按钮，是否可以保存
        name = "w" + str(int(time.time()))
        mycard.input_my_name(name)
        mycard.click_save()
        flag = group_set.is_toast_exist("修改成功", timeout=8)
        if not flag:
            raise AssertionError("修改群名片后，无‘修改成功’提示")
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0081(self):
        """在聊天设置页面，修改我在本群的昵称"""
        # 1.在聊天设置页面，点击我在本群的昵称，会跳转到修改群名片页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_my_card()
        mycard = GroupChatSetModifyMyCardPage()
        mycard.wait_for_page_load()
        # 2.在修改群名片页面，点击输入框右边的“x”按钮，是否可以一次清除已存在的昵称
        mycard.click_delete_my_name()
        mycard.page_should_contain_text("设置你在群内显示的昵称")
        # 3.输入框中不存在内容后，右上角的保存按钮是否会置灰展示
        flag = mycard.save_btn_is_enabled()
        self.assertFalse(flag)
        # 4.输入框录入内容后，右上角的保存按钮，是否会高亮展示
        name = "w" + str(int(time.time()))
        mycard.input_my_name(name)
        flag = mycard.save_btn_is_enabled()
        self.assertTrue(flag)
        # 5.点击高亮展示的保存按钮，是否可以保存
        mycard.click_save()
        flag = group_set.is_toast_exist("修改成功")
        if not flag:
            raise AssertionError("修改群名片后，无‘修改成功’提示")
        group_set.wait_for_page_load()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0820(self):
        """在聊天设置—群管理页面，转让群主或者解散群"""
        # 1.点击群管理，是否可以跳转到群管理页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_group_manage()
        # 2.点击解散群，是否会弹窗提示解散群聊确认操作
        manage_page = GroupChatSetManagerPage()
        manage_page.click_group_disband()
        manage_page.click_confirm()
        # 3.点击确定，是否可以解散群聊
        flag = manage_page.is_toast_exist("该群已解散")
        self.assertTrue(flag)

    @tags('ALL', 'SMOKE', 'only_group_owner')
    def test_msg_group_chat_0083(self):
        """在聊天设置—群管理页面，转让群主或者解散群"""
        # 1.点击群管理，跳转到群管理页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.wait_for_page_load()
        nums = group_set.get_group_total_member()
        if nums != 1:
            print("当前群不能有群成员,请预置条件")
            group_set.click_back()
            gcp.wait_for_page_load()
            return
        group_set.click_group_manage()
        # 2.点击群主管理权转让，是否会弹出提示：暂无群成员
        manage_page = GroupChatSetManagerPage()
        manage_page.click_group_transfer()
        flag = manage_page.is_toast_exist("暂无群成员")
        self.assertTrue(flag)
        manage_page.click_back()
        group_set.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'transfer_group_owner')
    def test_msg_group_chat_1084(self):
        """在聊天设置—群管理页面，转让群主或者解散群"""
        # 1、点击群管理，跳转到群管理页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.wait_for_page_load()
        nums = group_set.get_group_total_member()
        if nums == 1:
            print("当前群只有群主,请添加成员")
            group_set.click_back()
            gcp.wait_for_page_load()
            return
        group_set.click_group_manage()
        # 2、点击群主管理权转让，是否会跳转到“新群主选择”页面
        manage_page = GroupChatSetManagerPage()
        manage_page.click_group_transfer()
        # 3、点击选择一个群成员，是否会弹出提示：是否确定XXX为新群主的确认提示
        contacts = SelectLocalContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name_list()
        contacts.select_one_member_by_name(names[0])
        contacts.page_should_contain_text("确定选择" + names[0] + "为新群主")
        # 4、点击取消，返回到上一级操作
        contacts.click_cancel_transfer()
        # 5、点击确定，群主转让成功同时在群聊天会话页面展示XXX已成为新群主
        contacts.select_one_member_by_name(names[0])
        contacts.page_should_contain_text("确定选择" + names[0] + "为新群主")
        contacts.click_sure_transfer()
        flag = group_set.is_toast_exist("已转让")
        self.assertTrue(flag)
        group_set.click_back()
        gcp.wait_for_page_load()
        gcp.page_should_contain_text(names[0] + " 已成为新群主")

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0085(self):
        """在聊天设置—设置免打扰"""
        # 1、点击消息免打扰的开关，是否可以打开消息免打扰开关
        gcp = GroupChatPage()
        # 点击前先发送一条消息
        info = "Hello everyone!"
        gcp.input_message(info)
        gcp.send_message()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        switch_status = group_set.get_switch_undisturb_status()
        if not switch_status:
            group_set.click_switch_undisturb()
            time.sleep(2)
        # 2、返回到聊天会话页面，页面上方是否会展示免打扰标志
        group_set.click_back()
        gcp.wait_for_page_load()
        flag = gcp.is_exist_undisturb()
        if not flag:
            raise AssertionError("在聊天会话页面，页面上方没有展示免打扰标志")
        gcp.click_back()
        sogp = SelectOneGroupPage()
        # sogp.click_back()
        scp = SelectContactsPage()
        # scp.click_back()
        # 3、返回到消息列表，开启免打扰的聊天窗口上是否会展示免打扰标志
        mess = MessagePage()
        mess.wait_for_page_load()
        group_name = Preconditions.get_group_chat_name()
        flag2 = mess.is_exist_undisturb(group_name)
        if not flag2:
            raise AssertionError("在消息列表，开启免打扰的聊天窗口上没有展示免打扰标志")
        # 回到群聊会话页面
        mess.click_add_icon()
        mess.click_group_chat()
        scp.click_select_one_group()
        sogp.select_one_group_by_name(group_name)
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0086(self):
        """在聊天设置—设置免打扰"""
        # 1.点击消息免打扰开关，是否可以关闭免打扰
        gcp = GroupChatPage()
        # 先发送一条消息
        info = "Hello"
        gcp.input_message(info)
        gcp.send_message()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        switch_status = group_set.get_switch_undisturb_status()
        # 如果开关打开则关闭
        if switch_status:
            group_set.click_switch_undisturb()
            time.sleep(2)
        # 2.返回到聊天会话页面，页面上方是否会隐藏免打扰标志
        group_set.click_back()
        flag = gcp.is_exist_undisturb()
        self.assertFalse(flag)
        gcp.click_back()
        sogp = SelectOneGroupPage()
        # sogp.click_back()
        scp = SelectContactsPage()
        # scp.click_back()
        # 3.返回到消息列表，关闭免打扰的聊天窗口上是否会隐藏免打扰标志
        mess = MessagePage()
        mess.wait_for_page_load()
        group_name = Preconditions.get_group_chat_name()
        flag = mess.is_exist_undisturb(group_name)
        self.assertFalse(flag)
        # 回到群聊会话页面
        mess.click_add_icon()
        mess.click_group_chat()
        scp.click_select_one_group()
        sogp.select_one_group_by_name(group_name)
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0087(self):
        """在聊天设置—设置置顶聊天 """
        # 1.点击置顶聊天的开关，是否可以开启置顶聊天开关
        gcp = GroupChatPage()
        # 先发送一条消息
        info = "hehe"
        gcp.input_message(info)
        gcp.send_message()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        top_switch = group_set.get_chat_set_to_top_switch_status()
        if not top_switch:
            group_set.click_chat_set_to_top_switch()
            time.sleep(1)
        # 2.返回到消息列表，当前打开置顶聊天功能的群聊是否成功置顶
        group_set.click_back()
        gcp.click_back()
        sogp = SelectOneGroupPage()
        # sogp.click_back()
        scp = SelectContactsPage()
        # scp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 给其他联系人发送一条消息，看群聊是否设置成功置顶
        mess.click_contacts()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        contacts.select_people_by_name(names[0])
        contact_detail = ContactDetailsPage()
        contact_detail.click_message_icon()
        chat = GroupChatPage()
        # 如果弹框用户须知则点击处理
        flag = chat.is_exist_dialog()
        if flag:
            chat.click_i_have_read()
        info = "您好"
        chat.input_message(info)
        chat.send_message()
        chat.click_back()
        contact_detail.click_back_icon()
        contacts.open_message_page()
        # 获取群名字
        group_name = Preconditions.get_group_chat_name()
        # 顶部消息群名
        top_name = mess.get_top_news_name()
        # 名字一致，则置顶成功
        self.assertEqual(group_name, top_name)
        # 回到群聊会话页面
        mess.click_add_icon()
        mess.click_group_chat()
        scp.click_select_one_group()
        sogp.select_one_group_by_name(group_name)
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0088(self):
        """在聊天设置—设置置顶聊天 """
        # 1.点击置顶聊天的开关，是否可以关闭置顶聊天开关
        gcp = GroupChatPage()
        # 先发送一条消息
        info = "hehe"
        gcp.input_message(info)
        gcp.send_message()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        top_switch = group_set.get_chat_set_to_top_switch_status()
        if top_switch:
            group_set.click_chat_set_to_top_switch()
            time.sleep(1)
        # 2.返回到消息列表，当前关闭置顶聊天功能的群聊，是否成功取消置顶
        group_set.click_back()
        gcp.click_back()
        sogp = SelectOneGroupPage()
        # sogp.click_back()
        scp = SelectContactsPage()
        # scp.click_back()
        mess = MessagePage()
        mess.wait_for_page_load()
        # 给其他联系人发送一条消息，看群聊是否成功取消置顶
        mess.click_contacts()
        contacts = ContactsPage()
        contacts.wait_for_page_load()
        names = contacts.get_contacts_name()
        contacts.select_people_by_name(names[0])
        contact_detail = ContactDetailsPage()
        contact_detail.click_message_icon()
        chat = GroupChatPage()
        # 如果弹框用户须知则点击处理
        flag = chat.is_exist_dialog()
        if flag:
            chat.click_i_have_read()
        info = "您好"
        chat.input_message(info)
        chat.send_message()
        chat.click_back()
        contact_detail.click_back_icon()
        contacts.open_message_page()
        # 获取群名字
        group_name = Preconditions.get_group_chat_name()
        # 顶部消息群名
        top_name = mess.get_top_news_name()
        # 名字不一致，则取消置顶成功
        self.assertNotEqual(group_name, top_name)
        # 回到群聊会话页面
        mess.click_add_icon()
        mess.click_group_chat()
        scp.click_select_one_group()
        sogp.select_one_group_by_name(group_name)
        gcp.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'group_chat')
    def test_msg_group_chat_0089(self):
        """在聊天设置—查找聊天内容 """
        # 1.点击查找聊天内容，是否可以跳转到聊天内容搜索展示页面
        gcp = GroupChatPage()
        gcp.click_setting()
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.scroll_to_bottom()
        group_set.click_find_chat_record()
        search_page = GroupChatSetFindChatContentPage()
        search_page.wait_for_page_load()
        # 2.在页面顶部搜索框中，输入搜索条件，无搜索结果，页面是否会展示文案：“无搜索结果”
        info = str(uuid.uuid1())
        search_page.search(info)
        search_page.page_should_contain_text("无搜索结果")
        # 3.搜索框中存在内容时，右边是否会展示一键清除输入框中内容按钮“X”
        # 4.点击“X”按钮是否可以清除输入框中内容并展示初始化页面
        search_page.click_x_icon()
        search_page.wait_for_page_load()
        search_page.page_should_contain_text("分类索引")
        search_page.page_should_contain_text("图片与视频")
        search_page.page_should_contain_text("文件")
        search_page.click_back()
        group_set.click_back()
        gcp.wait_for_page_load()

@unittest.skip("暂时跳过")
class MessageGroupChatAllTest(TestCase):

    @classmethod
    def setUpClass(cls):

        Preconditions.select_mobile('Android-移动')
        # 导入测试联系人、群聊
        fail_time1 = 0
        flag1 = False
        import dataproviders
        while fail_time1 < 3:
            try:
                required_contacts = dataproviders.get_preset_contacts()
                conts = ContactsPage()
                current_mobile().hide_keyboard_if_display()
                Preconditions.make_already_in_message_page()
                conts.open_contacts_page()
                try:
                    if conts.is_text_present("发现SIM卡联系人"):
                        conts.click_text("显示")
                except:
                    pass
                for name, number in required_contacts:
                    # 创建联系人
                    conts.create_contacts_if_not_exits(name, number)
                required_group_chats = dataproviders.get_preset_group_chats()
                conts.open_group_chat_list()
                group_list = GroupListPage()
                for group_name, members in required_group_chats:
                    group_list.wait_for_page_load()
                    # 创建群
                    group_list.create_group_chats_if_not_exits(group_name, members)
                group_list.click_back()
                conts.open_message_page()
                flag1 = True
            except:
                fail_time1 += 1
            if flag1:
                break

        # 导入团队联系人
        fail_time2 = 0
        flag2 = False
        while fail_time2 < 5:
            try:
                Preconditions.make_already_in_message_page()
                contact_names = ["大佬1", "大佬2", "大佬3", "大佬4"]
                Preconditions.create_he_contacts(contact_names)
                flag2 = True
            except:
                fail_time2 += 1
            if flag2:
                break

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、确保当前页面在群聊聊天会话页面
        """

        Preconditions.select_mobile('Android-移动')
        mp = MessagePage()
        name = "群聊1"
        if mp.is_on_this_page():
            Preconditions.get_into_group_chat_page(name)
            return
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page(name)

    @tags('ALL','CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0173(self):
        """分享群二维码——搜索选择一个群 """

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_QRCode()
        n = 1
        while not gcs.page_should_contain_text2("该二维码7天内"):
            gcs.click_back()
            gcs.wait_for_page_load()
            gcs.click_QRCode()
            n += 1
            if n > 10:
                break
        code_page = GroupChatSetSeeQRCodePage()
        code_page.wait_for_page_load()
        # 1、点击左下角的分享按钮，会跳转到联系人选择器页面
        gcs.click_qecode_share_button()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2、点击选择一个群，可以进入到群聊列表展示页面
        scp.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        sog.click_search_group()
        # 3、搜索选中一个群，会弹出确认弹窗
        name = "群聊2"
        sog.input_search_keyword(name)
        time.sleep(1)
        sog.selecting_one_group_by_name(name)
        time.sleep(1)
        self.assertEquals(gcp.is_text_present("确定"), True)
        # 4、点击取消，关闭弹窗，会停留在搜索结果展示页面
        sog.click_cancel_forward()
        time.sleep(1)
        self.assertEquals(sog.is_exists_group_search_box(), True)
        sog.selecting_one_group_by_name(name)
        # 5、点击确定，会关闭弹窗并弹出toast提示：已转发
        sog.click_sure_forward()
        self.assertEquals(gcp.is_exist_forward(), True)
        sog.click_back_by_android()
        gcs.wait_for_page_load()
        scp.click_back_by_android()
        gcp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0174(self):
        """分享群二维码到——选择一个群 """

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_QRCode()
        n = 1
        while not gcs.page_should_contain_text2("该二维码7天内"):
            gcs.click_back()
            gcs.wait_for_page_load()
            gcs.click_QRCode()
            n += 1
            if n > 10:
                break
        code_page = GroupChatSetSeeQRCodePage()
        code_page.wait_for_page_load()
        # 1、点击左下角的分享按钮，会跳转到联系人选择器页面
        gcs.click_qecode_share_button()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2、点击选择一个群，可以进入到群聊列表展示页面
        scp.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        # 3、点击选中一个群，会弹出确认弹窗
        name = "群聊2"
        sog.selecting_one_group_by_name(name)
        time.sleep(1)
        self.assertEquals(gcp.is_text_present("确定"), True)
        # 4、点击取消，关闭弹窗，会停留在群聊列表展示页面
        sog.click_cancel_forward()
        sog.wait_for_page_load()
        sog.selecting_one_group_by_name(name)
        # 5、点击确定，会关闭弹窗并弹出toast提示：已转发
        sog.click_sure_forward()
        self.assertEquals(gcp.is_exist_forward(), True)
        sog.click_back_by_android()
        gcs.wait_for_page_load()
        scp.click_back_by_android()
        gcp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0175(self):
        """分享群二维码到——选择选择团队联系人——搜索选择联系人 """

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_QRCode()
        n = 1
        while not gcs.page_should_contain_text2("该二维码7天内"):
            gcs.click_back()
            gcs.wait_for_page_load()
            gcs.click_QRCode()
            n += 1
            if n > 10:
                break
        code_page = GroupChatSetSeeQRCodePage()
        code_page.wait_for_page_load()
        # 1、点击左下角的分享按钮，会跳转到联系人选择器页面
        gcs.click_qecode_share_button()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2、点击选择团队联系人，可以进入到企业展示列表
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_enter_group_chat()
        # 3、搜索选择团队联系人，会弹出确认弹窗
        name = "大佬3"
        shc.input_search(name)
        shc.selecting_he_contacts_by_name(name)
        time.sleep(1)
        self.assertEquals(shc.is_text_present("确定"), True)
        # 4、点击取消，会关闭弹窗并停留在搜索结果展示页面
        scp.click_cancel_forward()
        time.sleep(1)
        self.assertEquals(shc.is_exists_search_box(), True)
        shc.selecting_he_contacts_by_name(name)
        # 5、点击确定，会返回到群二维码分享页面并弹出toast提示：已转发
        scp.click_sure_forward()
        self.assertEquals(gcp.is_exist_forward(), True)
        code_page.wait_for_page_load()
        scp.click_back_by_android()
        gcs.wait_for_page_load()
        scp.click_back_by_android()
        gcp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0176(self):
        """分享群二维码到——选择选择团队联系人——选择联系人 """

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_QRCode()
        n = 1
        while not gcs.page_should_contain_text2("该二维码7天内"):
            gcs.click_back()
            gcs.wait_for_page_load()
            gcs.click_QRCode()
            n += 1
            if n > 10:
                break
        code_page = GroupChatSetSeeQRCodePage()
        code_page.wait_for_page_load()
        # 1、点击左下角的分享按钮，会跳转到联系人选择器页面
        gcs.click_qecode_share_button()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2、点击选择团队联系人，可以进入到企业展示列表
        scp.click_he_contacts()
        shc = SelectHeContactsDetailPage()
        shc.wait_for_he_contacts_page_load()
        # 需要考虑测试号码存在多个团队的情况
        Preconditions.if_exists_multiple_enterprises_enter_group_chat()
        # 3、选择团队联系人，会弹出确认弹窗
        name = "大佬3"
        shc.selecting_he_contacts_by_name(name)
        time.sleep(1)
        self.assertEquals(shc.is_text_present("确定"), True)
        # 4、点击取消，会关闭弹窗并停留在搜索结果展示页面
        scp.click_cancel_forward()
        time.sleep(1)
        self.assertEquals(shc.is_exists_search_box(), True)
        shc.selecting_he_contacts_by_name(name)
        # 5、点击确定，会返回到群二维码分享页面并弹出toast提示：已转发
        scp.click_sure_forward()
        self.assertEquals(gcp.is_exist_forward(), True)
        code_page.wait_for_page_load()
        scp.click_back_by_android()
        gcs.wait_for_page_load()
        scp.click_back_by_android()
        gcp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0177(self):
        """分享群二维码到——选择手机联系人——搜索选择联系人 """

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_QRCode()
        n = 1
        while not gcs.page_should_contain_text2("该二维码7天内"):
            gcs.click_back()
            gcs.wait_for_page_load()
            gcs.click_QRCode()
            n += 1
            if n > 10:
                break
        code_page = GroupChatSetSeeQRCodePage()
        code_page.wait_for_page_load()
        # 1、点击左下角的分享按钮，是否会跳转到联系人选择器页面
        gcs.click_qecode_share_button()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2、点击选择手机联系人，是否会进入到手机联系人展示列表
        scp.select_local_contacts()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 3、搜索选择手机联系人，是否会弹出确认弹窗
        name = "大佬1"
        slc.input_search_keyword(name)
        time.sleep(1)
        slc.selecting_local_contacts_by_name(name)
        time.sleep(1)
        self.assertEquals(gcp.is_text_present("确定"), True)
        # 4、点击取消，会关闭弹窗，不会自动清除搜索结果
        scp.click_cancel_forward()
        time.sleep(1)
        self.assertEquals(slc.is_exists_local_contacts_by_name(name), True)
        slc.selecting_local_contacts_by_name(name)
        # 5、点击确定，会返回到群二维码分享页面并弹出toast提示：已转发
        scp.click_sure_forward()
        self.assertEquals(gcp.is_exist_forward(), True)
        code_page.wait_for_page_load()
        scp.click_back_by_android()
        gcs.wait_for_page_load()
        scp.click_back_by_android()
        gcp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0178(self):
        """分享群二维码到——选择手机联系人——选择手机联系人 """

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_QRCode()
        n = 1
        while not gcs.page_should_contain_text2("该二维码7天内"):
            gcs.click_back()
            gcs.wait_for_page_load()
            gcs.click_QRCode()
            n += 1
            if n > 10:
                break
        code_page = GroupChatSetSeeQRCodePage()
        code_page.wait_for_page_load()
        # 1、点击左下角的分享按钮，是否会跳转到联系人选择器页面
        gcs.click_qecode_share_button()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2、点击选择手机联系人，是否会进入到手机联系人展示列表
        scp.select_local_contacts()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 3、选择手机联系人，是否会弹出确认弹窗
        name = "大佬1"
        slc.selecting_local_contacts_by_name(name)
        time.sleep(1)
        self.assertEquals(gcp.is_text_present("确定"), True)
        # 4、点击取消，会关闭弹窗，不会自动清除搜索结果
        scp.click_cancel_forward()
        time.sleep(1)
        self.assertEquals(slc.is_exists_local_contacts_by_name(name), True)
        slc.selecting_local_contacts_by_name(name)
        # 5、点击确定，会返回到群二维码分享页面并弹出toast提示：已转发
        scp.click_sure_forward()
        self.assertEquals(gcp.is_exist_forward(), True)
        code_page.wait_for_page_load()
        scp.click_back_by_android()
        gcs.wait_for_page_load()
        scp.click_back_by_android()
        gcp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0179(self):
        """分享群二维码到——选择最近聊天 """

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 给当前会话页面发送消息,确保最近聊天中有记录
        gcp.input_text_message("111")
        gcp.send_text()
        time.sleep(2)
        # 解决发送消息后，最近聊天窗口没有记录，需要退出刷新的问题
        gcp.click_back()
        group_name = "群聊1"
        Preconditions.get_into_group_chat_page(group_name)
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_QRCode()
        n = 1
        while not gcs.page_should_contain_text2("该二维码7天内"):
            gcs.click_back()
            gcs.wait_for_page_load()
            gcs.click_QRCode()
            n += 1
            if n > 10:
                break
        code_page = GroupChatSetSeeQRCodePage()
        code_page.wait_for_page_load()
        # 1、点击左下角的分享按钮，是否会跳转到联系人选择器页面
        gcs.click_qecode_share_button()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        # 2、点击选择最近聊天的联系人或者群聊，会弹出确认弹窗
        scp.select_recent_chat_by_name(group_name)
        time.sleep(1)
        self.assertEquals(gcp.is_text_present("确定"), True)
        # 3、点击取消，会关闭弹窗，不会自动清除搜索结果
        scp.click_cancel_forward()
        time.sleep(1)
        self.assertEquals(scp.is_exists_recent_chat_by_name(group_name), True)
        scp.select_recent_chat_by_name(group_name)
        # 4、点击确定，会返回到群二维码分享页面并弹出toast提示：已转发
        scp.click_sure_forward()
        self.assertEquals(gcp.is_exist_forward(), True)
        code_page.wait_for_page_load()
        scp.click_back_by_android()
        gcs.wait_for_page_load()
        scp.click_back_by_android()
        gcp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0180(self):
        """聊天会话窗口中——长按识别二维码 """

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_QRCode()
        n = 1
        while not gcs.page_should_contain_text2("该二维码7天内"):
            gcs.click_back()
            gcs.wait_for_page_load()
            gcs.click_QRCode()
            n += 1
            if n > 10:
                break
        code_page = GroupChatSetSeeQRCodePage()
        code_page.wait_for_page_load()
        # 确保有群二维码图片可识别
        gcs.click_qecode_share_button()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        name = "群聊2"
        sog.selecting_one_group_by_name(name)
        scp.click_sure_forward()
        code_page.wait_for_page_load()
        scp.click_back_by_android()
        gcs.wait_for_page_load()
        scp.click_back_by_android()
        gcp.wait_for_page_load()
        scp.click_back_by_android()
        mp = MessagePage()
        mp.wait_for_page_load()
        mp.choose_chat_by_name(name)
        gcp.wait_for_page_load()
        # 1、点击放大二维码图片
        gcp.click_msg_image(-1)
        time.sleep(1)
        # 2、长按二维码图片，会弹出功能菜单列表
        gcp.press_xy()
        # 3、点击识别图中的二维码，识别成功后，会自动跳转到群聊会话页面
        gcp.click_text("识别图中二维码")
        gcp.wait_for_page_load()
        group_name = "群聊1"
        self.assertEquals(gcp.is_exists_group_by_name(group_name), True)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0182(self):
        """聊天会话窗口中——长按识别二维码 """

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_QRCode()
        n = 1
        while not gcs.page_should_contain_text2("该二维码7天内"):
            gcs.click_back()
            gcs.wait_for_page_load()
            gcs.click_QRCode()
            n += 1
            if n > 10:
                break
        code_page = GroupChatSetSeeQRCodePage()
        code_page.wait_for_page_load()
        # 确保有群二维码图片可识别
        gcs.click_qecode_share_button()
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.click_select_one_group()
        sog = SelectOneGroupPage()
        sog.wait_for_page_load()
        name = "群聊2"
        sog.selecting_one_group_by_name(name)
        scp.click_sure_forward()
        code_page.wait_for_page_load()
        scp.click_back_by_android()
        gcs.wait_for_page_load()
        gcs.click_delete_and_exit()
        mp = MessagePage()
        mp.wait_for_page_load()
        mp.choose_chat_by_name(name)
        gcp.wait_for_page_load()
        # 1、点击放大二维码图片
        gcp.click_msg_image(-1)
        time.sleep(1)
        # 2、长按二维码图片
        gcp.press_xy()
        # 3、点击识别图中的二维码，识别成功后，会自动跳转到：群聊邀请详情页并展示：群聊已解散的提示
        gcp.click_text("识别图中二维码")
        self.assertEquals(gcp.page_should_contain_text2("群已解散"), True)

    @staticmethod
    def tearDown_test_msg_():
        """恢复环境"""

        Preconditions.make_already_in_message_page()
        cp = ContactsPage()
        cp.open_contacts_page()
        if cp.is_text_present("发现SIM卡联系人"):
            cp.click_text("显示")
        cp.open_group_chat_list()
        glp = GroupListPage()
        glp.wait_for_page_load()
        group_name = "群聊1"
        glp.create_group_chats_if_not_exits(group_name, ['大佬1', '大佬2'])
        time.sleep(1)
        glp.click_back_by_android()
        cp.open_message_page()
        mp = MessagePage()
        mp.wait_for_page_load()
        Preconditions.get_into_group_chat_page(group_name)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0183():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        scp = SelectContactsPage()
        scp.create_message_group(text='bbb')

    @unittest.skip("用例有误，跳过")
    def test_msg_xiaoqiu_0183(self):
        """聊天会话窗口中——长按识别二维码 """

        gcp = GroupChatPage()
        scp = SelectContactsPage()
        gcp.click_setting()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_QRCode()
        group_set.click_qecode_download_button()
        time.sleep(2)
        scp.click_back_by_android()
        time.sleep(1)
        scp.page_up()
        time.sleep(1)
        group_set.click_delete_and_exit()
        time.sleep(3)
        group_set.click_sure()
        time.sleep(1)
        scp.create_message_group(text='aaa')
        gcp = GroupChatPage()
        # 点击图片按钮
        gcp.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic()
        time.sleep(1)
        cpg.click_send()
        time.sleep(2)
        scp.click_group_code()
        time.sleep(1)
        scp.press_xy()
        time.sleep(1)
        scp.click_recognize_code()
        time.sleep(6)
        scp.is_text_present("群已解散")
        scp.click_back_by_android(times=4)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0185():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        scp = SelectContactsPage()
        scp.create_message_group(text='bbb')

    @unittest.skip("用例有误，跳过")
    def test_msg_xiaoqiu_0185(self):
        """聊天会话窗口中——长按识别二维码"""

        gcp = GroupChatPage()
        scp = SelectContactsPage()
        gcp.click_setting()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_QRCode()
        group_set.click_qecode_download_button()
        time.sleep(2)
        scp.click_back_by_android()
        time.sleep(1)
        scp.page_up()
        time.sleep(1)
        group_set.click_delete_and_exit()
        time.sleep(3)
        group_set.click_sure()
        time.sleep(1)
        scp.create_message_group(text='aaa')
        gcp = GroupChatPage()
        # 点击图片按钮
        gcp.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        cpg.select_pic()
        time.sleep(1)
        cpg.click_send()
        time.sleep(2)
        scp.click_group_code()
        time.sleep(1)
        scp.press_xy()
        time.sleep(1)
        scp.click_recognize_code()
        time.sleep(6)
        scp.is_text_present("群已解散")
        scp.click_back_by_android(times=4)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0186(self):
        """群二维码详情页——保存二维码"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_QRCode()
        n = 1
        while not gcs.page_should_contain_text2("该二维码7天内"):
            gcs.click_back()
            gcs.wait_for_page_load()
            gcs.click_QRCode()
            n += 1
            if n > 10:
                break
        code_page = GroupChatSetSeeQRCodePage()
        code_page.wait_for_page_load()
        code_page.click_qecode_save_btn()
        # 1、在群二维码详情页，点击右下角的下载按钮，下载成功后，会弹出toast提示：已保存
        self.assertEquals(code_page.is_toast_exist("已保存"), True)
        code_page.click_back_by_android()
        gcs.wait_for_page_load()
        gcs.click_back_by_android()
        gcp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0188(self):
        """群聊设置页面——进入到群管理详情页"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        # 1、点击群管理，进入到群管理详情页
        gcs.click_group_manage()
        gcs.wait_for_group_manage_load()
        # 2、点击群主管理权转让，会弹出toast提示：暂无群成员并且停留在当前页
        gcs.click_group_manage_transfer_button()
        self.assertEquals(gcs.is_toast_exist("暂无群成员"), True)
        gcs.wait_for_group_manage_load()
        # 3、点击左上角的返回按钮，可以返回到群聊设置页
        gcs.click_group_manage_back_button()
        gcs.wait_for_page_load()
        gcs.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0195(self):
        """群聊设置页面——查找聊天内容"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        text = "12345"
        gcp.input_text_message(text)
        gcp.send_text()
        time.sleep(2)
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        gcf = GroupChatSetFindChatContentPage()
        gcf.wait_for_page_load()
        gcf.search(text)
        # 1、点击聊天内容入口，跳转到聊天内容页面
        gcf.select_message_record_by_text(text)
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        gcf.wait_for_page_load()
        # 2、点击顶部的搜索框，调起小键盘
        gcf.click_search_box()
        self.assertEquals(gcf.is_keyboard_shown(), True)
        gcf.click_back()
        gcs.wait_for_page_load()
        gcs.click_back()
        gcp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0197(self):
        """群聊设置页面——查找聊天内容——数字搜索——搜索结果展示"""

        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        text = "197197"
        gcp.input_text_message(text)
        gcp.send_text()
        time.sleep(2)
        gcp.click_setting()
        gcs = GroupChatSetPage()
        gcs.wait_for_page_load()
        gcs.click_find_chat_record()
        gcf = GroupChatSetFindChatContentPage()
        gcf.wait_for_page_load()
        gcf.search(text)
        time.sleep(2)
        # 1、在查找聊天内容页面，输入框中，输入数字搜索条件，存在搜索结果时，搜索结果展示为：发送人头像、发送人名称、发送的内容、发送的时间
        self.assertEquals(gcf.is_exists_sending_head(), True)
        self.assertEquals(gcf.is_exists_sending_name(), True)
        self.assertEquals(gcf.is_exists_send_content(), True)
        self.assertEquals(gcf.is_exists_send_time(), True)
        # 2、任意选中一条聊天记录，会跳转到聊天记录对应的位置
        gcf.select_message_record_by_text(text)
        gcp.wait_for_page_load()
        self.assertEquals(gcp.is_text_present(text), True)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0254(self):
        """消息列表——发起群聊——选择1个手机联系人"""

        current_mobile().launch_app()
        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_add_icon()
        mp.click_group_chat()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 选择1个手机联系人
        name = "大佬1"
        slc.selecting_local_contacts_by_name(name)
        slc.click_sure()
        time.sleep(2)
        chat = BaseChatPage()
        if chat.is_exist_dialog():
            # 点击我已阅读
            chat.click_i_have_read()
        scp = SingleChatPage()
        # 1.等待一对一聊天会话页面加载
        scp.wait_for_page_load()

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0255(self):
        """消息列表——发起群聊——选择5个手机联系人——创建群聊"""

        current_mobile().launch_app()
        mp = MessagePage()
        mp.wait_for_page_load()
        mp.click_add_icon()
        mp.click_group_chat()
        scg = SelectContactsPage()
        scg.wait_for_page_load()
        scg.select_local_contacts()
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 选择5个手机联系人
        names = ["大佬1", "大佬2", "大佬3", "大佬4", "给个红包1"]
        # 选择成员
        for name in names:
            slc.selecting_local_contacts_by_name(name)
        slc.click_sure()
        # 创建群
        cgnp = CreateGroupNamePage()
        cgnp.input_group_name("群聊255")
        cgnp.click_sure()
        # 等待群聊页面加载
        gcp = GroupChatPage()
        gcp.wait_for_page_load()

    # @staticmethod
    # def tearDown_test_msg_xiaoqiu_0255():
    #     """恢复环境"""
    #
    #     pass

    @staticmethod
    def setUp_test_msg_xiaoqiu_0256():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0256(self):
        """消息列表——发起群聊——选择50个手机联系人——创建群聊"""
        scp = SelectContactsPage()
        gcp = GroupChatPage()
        scp.create_multi_contacts_group(groupname='aaa',num=6,times=3)
        gcp.click_setting()
        time.sleep(1)
        group_set = GroupChatSetPage()
        scp.page_up()
        time.sleep(1)
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0258():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0258(self):
        """消息列表——发起群聊——选择501个手机联系人——创建群聊"""
        scp = SelectContactsPage()
        gcp = GroupChatPage()
        scp.create_multi_contacts_group(groupname='aaa',num=6,times=3)
        gcp.click_setting()
        time.sleep(1)
        group_set = GroupChatSetPage()
        scp.page_up()
        time.sleep(1)
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)



    @staticmethod
    def setUp_test_msg_xiaoqiu_0271():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0271(self):
        """通讯录——发起群聊——选择手机联系人"""
        scp = SelectContactsPage()
        scp.create_message_group()
        time.sleep(1)
        gcp = GroupChatPage()
        gcp.click_setting()
        time.sleep(1)
        group_set = GroupChatSetPage()
        scp.page_up()
        time.sleep(1)
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)


    @staticmethod
    def setUp_test_msg_xiaoqiu_0278():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0278(self):
        """通讯录——群聊——搜索——选择一个群"""
        scp = SelectContactsPage()
        scp.create_message_group(text='中软国际')
        time.sleep(1)
        gcp = GroupChatPage()
        gcp.click_setting()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_QRCode()
        time.sleep(1)
        group_set.click_qecode_share_button()
        time.sleep(1)
        scp = SelectContactsPage()
        scp.click_select_one_group()
        time.sleep(1)
        scp.click_group_search()
        scp.group_search(text="中软国际")
        time.sleep(1)
        scp.page_should_not_contain_text("无搜索结果")
        time.sleep(1)
        gcp.click_back_by_android(times=2)
        scp.page_up()
        time.sleep(1)
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0215():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0215(self):
        """群聊设置页面——关闭消息免打扰——网络异常"""
        scp = SelectContactsPage()
        scp.create_message_group()
        time.sleep(1)
        gcp = GroupChatPage()
        gcp.click_setting()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.wait_for_page_load()
        switch_status = group_set.get_switch_undisturb_status()
        # 如果关闭，则打开
        if not switch_status:
            group_set.click_switch_undisturb()
            time.sleep(2)

        group_set.set_network_status(1)
        time.sleep(3)
        #关闭
        group_set.click_switch_undisturb()
        group_set.is_toast_exist("没有网络，请连接网络再试")
        scp.page_up()
        time.sleep(1)
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)

    @staticmethod
    def tearDown_msg_xiaoqiu_0215():
        # 初始化,恢复app到默认状态
        group_set = GroupChatSetPage()
        group_set.set_network_status(6)
        group_set.click_back_by_android(1)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0216():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0216(self):
        """群聊设置页面——关闭消息免打扰——网络断网"""
        scp = SelectContactsPage()
        scp.create_message_group()
        time.sleep(1)
        gcp = GroupChatPage()
        gcp.click_setting()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.wait_for_page_load()
        switch_status = group_set.get_switch_undisturb_status()
        # 如果关闭，则打开
        if not switch_status:
            group_set.click_switch_undisturb()
            time.sleep(2)

        group_set.set_network_status(0)
        time.sleep(3)
        #关闭
        group_set.click_switch_undisturb()
        group_set.is_toast_exist("没有网络，请连接网络再试")
        scp.page_up()
        time.sleep(1)
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)

    @staticmethod
    def tearDown_msg_xiaoqiu_0216():
        # 初始化,恢复app到默认状态
        group_set = GroupChatSetPage()
        group_set.set_network_status(6)
        group_set.click_back_by_android(1)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0217():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0217(self):
        """群聊设置页面——开启消息免打扰——网络断网"""
        scp = SelectContactsPage()
        scp.create_message_group()
        time.sleep(1)
        gcp = GroupChatPage()
        gcp.click_setting()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.wait_for_page_load()
        switch_status = group_set.get_switch_undisturb_status()
        # 如果打开，则关闭
        if switch_status:
            group_set.click_switch_undisturb()
            time.sleep(2)

        group_set.set_network_status(0)
        time.sleep(3)
        # 关闭
        group_set.click_switch_undisturb()
        group_set.is_toast_exist("没有网络，请连接网络再试")
        scp.page_up()
        time.sleep(1)
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)

    @staticmethod
    def tearDown_msg_xiaoqiu_0217():
        # 初始化,恢复app到默认状态
        group_set = GroupChatSetPage()
        group_set.set_network_status(6)
        group_set.click_back_by_android(1)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0218():
        Preconditions.select_mobile('Android-移动')
        from settings.available_devices import TARGET_APP
        current_mobile().remove_app(TARGET_APP.get('APP_PACKAGE'))
        current_mobile().install_app(TARGET_APP.get('DOWNLOAD_URL'),
                                     replace=True)
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0218(self):
        """卸载重装——登录和飞信——查看置顶状态"""
        scp = SelectContactsPage()
        scp.create_message_group()
        time.sleep(1)
        gcp = GroupChatPage()
        gcp.click_setting()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        top_switch = group_set.get_chat_set_to_top_switch_status()
        self.assertTrue(top_switch==False)
        scp.page_up()
        time.sleep(1)
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0242():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0242(self):
        """消息草稿-聊天列表显示-输入文本信息"""
        scp = SelectContactsPage()
        scp.create_message_group()
        time.sleep(1)
        gcp = GroupChatPage()
        info = "Hello everyone"
        gcp.input_message(info)
        # 2.点击输入框右边高亮展示的发送按钮，发送此段文本
        gcp.send_message()
        gcp.input_message(info)
        gcp.click_back_by_android(times=2)
        gcp.page_should_contain_text("[草稿]")
        gcp.click_text("aaa")
        gcp.click_setting()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        scp.page_up()
        time.sleep(1)
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0243():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0243(self):
        """消息草稿-聊天列表显示-输入表情信息"""
        scp = SelectContactsPage()
        scp.create_message_group()
        time.sleep(1)
        gcp = GroupChatPage()
        infos = ["appium", "哈哈", "a", "123456", "w(ﾟДﾟ)w"]
        gcp.input_message(infos)
        # 2.点击输入框右边高亮展示的发送按钮，发送此段文本
        gcp.send_message()
        gcp.input_message(infos)
        gcp.click_back_by_android(times=2)
        gcp.page_should_contain_text("[草稿]")
        gcp.click_text("aaa")
        gcp.click_setting()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        scp.page_up()
        time.sleep(1)
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0245():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0245(self):
        """消息草稿-聊天列表显示-输入空格消息-网络异常"""
        scp = SelectContactsPage()
        scp.create_message_group()
        time.sleep(1)
        gcp = GroupChatPage()
        infos ="  "
        gcp.input_message("haha")
        # 2.点击输入框右边高亮展示的发送按钮，发送此段文本
        gcp.send_message()
        time.sleep(1)
        gcp.input_message(infos)
        gcp.click_back_by_android()
        gcp.page_should_not_contain_text("[草稿]")
        gcp.click_text("aaa")
        gcp.click_setting()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        scp.page_up()
        time.sleep(1)
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0246():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0246(self):
        """消息草稿-聊天列表显示-输入文本信息-网络异常"""
        scp = SelectContactsPage()
        scp.create_message_group()
        time.sleep(1)
        gcp = GroupChatPage()
        infos ="haha"
        gcp.input_message(infos)
        # 2.点击输入框右边高亮展示的发送按钮，发送此段文本
        gcp.send_message()
        time.sleep(1)
        gcp.input_message(infos)
        gcp.click_back_by_android(times=1)
        gcp.page_should_contain_text("[草稿]")
        gcp.click_text("aaa")
        gcp.click_setting()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        scp.page_up()
        time.sleep(1)
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)


    @staticmethod
    def setUp_test_msg_xiaoqiu_0247():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0247(self):
        """消息草稿-聊天列表显示-草稿信息发送成功"""
        scp = SelectContactsPage()
        scp.create_message_group()
        time.sleep(1)
        gcp = GroupChatPage()
        infos ="haha"
        gcp.input_message(infos)
        # 2.点击输入框右边高亮展示的发送按钮，发送此段文本
        gcp.send_message()
        time.sleep(1)
        gcp.input_message(infos)
        gcp.click_back_by_android()
        gcp.page_should_contain_text("[草稿]")
        gcp.click_text("aaa")
        time.sleep(1)
        gcp.send_message()
        time.sleep(1)
        group_set = GroupChatSetPage()
        gcp.click_setting()
        group_set.wait_for_page_load()
        scp.page_up()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)


    @staticmethod
    def setUp_test_msg_xiaoqiu_0247():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0247(self):
        """消息草稿-聊天列表显示-草稿信息删除"""
        scp = SelectContactsPage()
        scp.create_message_group()
        time.sleep(1)
        gcp = GroupChatPage()
        infos ="haha"
        gcp.input_message(infos)
        # 2.点击输入框右边高亮展示的发送按钮，发送此段文本
        gcp.send_message()
        time.sleep(1)
        gcp.input_message(infos)
        gcp.click_back_by_android()
        gcp.page_should_contain_text("[草稿]")
        gcp.click_text("aaa")
        time.sleep(1)
        gcp.send_message()
        time.sleep(1)
        group_set = GroupChatSetPage()
        gcp.click_setting()
        group_set.wait_for_page_load()
        scp.page_up()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)


    @staticmethod
    def setUp_test_msg_xiaoqiu_0248():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0248(self):
        """消息草稿-聊天列表显示-草稿信息删除"""
        scp = SelectContactsPage()
        scp.create_message_group()
        time.sleep(1)
        gcp = GroupChatPage()
        infos ="haha"
        gcp.input_message(infos)
        # 2.点击输入框右边高亮展示的发送按钮，发送此段文本
        gcp.send_message()
        time.sleep(1)
        gcp.input_message(infos)
        gcp.click_back_by_android(times=2)
        gcp.page_should_contain_text("[草稿]")
        gcp.click_text("aaa")
        time.sleep(1)
        for i in range(5):
            gcp.tap_coordinate([(1400,2145)])
        time.sleep(1)
        gcp.click_back_by_android()
        time.sleep(1)
        gcp.page_should_not_contain_text("[草稿]")
        group_set = GroupChatSetPage()
        gcp.click_text("aaa")
        time.sleep(1)
        gcp.click_setting()
        group_set.wait_for_page_load()
        scp.page_up()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)


    @staticmethod
    def setUp_test_msg_xiaoqiu_0269():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0269(self):
        """普通群——聊天会话页面——未进群联系人展示"""
        scp = SelectContactsPage()
        scp.create_message_group()
        time.sleep(1)
        gcp = GroupChatPage()
        group_set = GroupChatSetPage()
        infos ="haha"
        for i in range(3):
            gcp.input_message(infos)
            # 2.点击输入框右边高亮展示的发送按钮，发送此段文本
            gcp.send_message()
            time.sleep(1)
        num=group_set.get_element_count()
        self.assertTrue(num==3)
        time.sleep(1)
        gcp.click_setting()
        group_set.wait_for_page_load()
        scp.page_up()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0279():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        scp = SelectContactsPage()
        scp.del_message_group()
        scp.create_message_group2(text='中软国际')
      #  scp.create_message_group(text='中软国际')

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0279(self):
        """通讯录-群聊-中文模糊搜索——搜索结果展示"""
        time.sleep(1)
        gcp = GroupChatPage()
        gcp.click_setting()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        group_set.click_QRCode()
        time.sleep(1)
        group_set.click_qecode_share_button()
        time.sleep(1)
        scp = SelectContactsPage()
        scp.click_select_one_group()
        time.sleep(1)
        scp.click_group_search()
        scp.group_search(text="中国")
        time.sleep(1)
        scp.page_should_contain_text("无搜索结果")
        time.sleep(1)
        gcp.click_back_by_android(times=4)
        scp.page_up()
        time.sleep(1)
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0292():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)
        scp = SelectContactsPage()
        scp.del_message_group()
        groupname=["aaa","bbb","ccc","ddd","eee","fff","hhh","kkk"]
        for name in groupname:
            scp.create_message_group2(text=name)
            time.sleep(1)
            scp.click_back_by_android()

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0292(self):
        """通讯录-群聊-索引字母定位选择"""
        mess = MessagePage()
        mess.click_add_icon()
        # 点击 发起群聊
        mess.click_group_chat()
        # 选择联系人界面，选择一个群
        sc = SelectContactsPage()
        sc.click_select_one_group()
        time.sleep(1)

        cpp = ChatProfilePage()
        # 获取所有右侧索引字母，随机选择一个点击
        letters = cpp.get_letters_index()
        letter = letters[0]
        cpp.click_letter_index(letter)
        time.sleep(1)
        sc.page_should_contain_text("aaa")
        letters = cpp.get_letters_index()
        letter = letters[-1]
        cpp.click_letter_index(letter)
        time.sleep(1)
        sc.page_should_contain_text("kkk")
        sc.click_back_by_android(times=1)

    def tearDown_test_msg_xiaoqiu_0292(self):
        scp = SelectContactsPage()
        scp.del_message_group()


    @staticmethod
    def setUp_test_msg_xiaoqiu_0259():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        # Preconditions.make_already_delete_my_group()
        Preconditions.ensure_have_enterprise_group()


    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0259(self):
        """消息列表——发起群聊——选择选择团队联系人——创建群聊"""
        scp = SelectContactsPage()
        scp.create_message_group2()

    def tearDown_test_msg_xiaoqiu_0259(self):
        scp = SelectContactsPage()
        scp.del_message_group()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0219():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page(reset=True)
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0219(self):
        """清除数据——登录和飞信——查看置顶状态"""
        scp = SelectContactsPage()
        scp.create_message_group()
        time.sleep(1)
        gcp = GroupChatPage()
        gcp.click_setting()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.wait_for_page_load()
        top_switch = group_set.get_chat_set_to_top_switch_status()
        self.assertTrue(top_switch == False)
        scp.page_up()
        time.sleep(1)
        group_set.click_delete_and_exit()
        gcp.click_back_by_android(times=2)


    @staticmethod
    def setUp_test_msg_xiaoqiu_0228():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_xiaoqiu_0228(self):
        """聊天设置页面——删除并退出群聊——群主"""
        scp = SelectContactsPage()
        scp.create_message_group2()
        time.sleep(1)
        gcp = GroupChatPage()
        group_set = GroupChatSetPage()
        gcp.click_setting()
        group_set.wait_for_page_load()
        scp.page_up()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.click_delete_and_exit2()
        time.sleep(2)
        group_set.click_cancel()
        group_set.click_delete_and_exit2()
        time.sleep(2)
        group_set.click_sure()
        group_set.is_toast_exist("已退出群聊")
        gcp.click_back_by_android(times=2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0229():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat',"high")
    def test_msg_huangcaizui_C_0006(self):
        """聊天设置页面——删除并退出群聊——群主"""
        scp = SelectContactsPage()
        scp.create_message_group2()
        time.sleep(1)
        gcp = GroupChatPage()
        group_set = GroupChatSetPage()
        gcp.click_setting()
        group_set.wait_for_page_load()
        scp.page_up()
        time.sleep(1)
        group_set = GroupChatSetPage()
        group_set.click_delete_and_exit()
        group_set.is_toast_exist("已退出群聊")
        gcp.click_back_by_android(times=2)


class MessageGroupChatSendGroupMessage(TestCase):
    """
     模块：消息->群聊
     文件位置：
     表格：消息-群聊-群发短信
     """
    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)

    def default_setUp(self):
        """
        1、成功登录和飞信
        2、确保当前页面在群聊聊天会话页面
        """

        Preconditions.select_mobile('Android-移动')
        name = "群聊1"
        mp = MessagePage()
        if mp.is_on_this_page():
            Preconditions.get_into_group_chat_page(name)
            return
        gcp = GroupChatPage()
        if gcp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.get_into_group_chat_page(name)

    @staticmethod
    def setUp_test_msg_huangcaizui_C_0006():
        Preconditions.select_mobile('Android-移动')
        # current_mobile().reset_app()
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'group_chat', "high", "yx")
    def test_msg_huangcaizui_C_0006(self):
        """验证退出短信是否成功退出"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.（普通群群主、企业群/党群的成员或群主）已进入的群聊页面
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多富媒体按钮
        gcp.click_more()
        # 2.点击群短信
        gcp.click_group_sms()
        time.sleep(1)
        cgs = ChatGroupSMSPage()
        # 3.如果在资费介绍页，点击确定
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        time.sleep(1)
        # 3.点击返回
        cgs.wait_for_page_load()
        cgs.click_back()
        # 4.验证是否在群聊页面
        self.assertTrue(gcp.is_on_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_C_0008():
        Preconditions.select_mobile('Android-移动')
        # current_mobile().reset_app()
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'group_chat', "high", "yx")
    def test_msg_huangcaizui_C_0008(self):
        """验证退出短信是否成功退出"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.（普通群群主、企业群/党群的成员或群主）已进入的群聊页面
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多富媒体按钮
        gcp.click_more()
        # 2.点击群短信
        gcp.click_group_sms()
        time.sleep(1)
        cgs = ChatGroupSMSPage()
        # 3.如果在资费介绍页，点击确定
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        cgs.wait_for_page_load()
        # 4.点击发送短信框
        cgs.click_send_message()
        # 5.判断是否弹起键盘
        self.assertEqual(cgs.is_keyboard_shown(), True)
        # 6.输入文本消息
        cgs.input_text_message("测试测试")
        # 7.点击发送消息
        cgs.click_send()
        # 8.验证是否弹框提示'请选择收件人'
        self.assertTrue(cgs.is_toast_exist("请选择收件人"))
        time.sleep(1)

    @staticmethod
    def setUp_test_msg_huangcaizui_C_0010():
        Preconditions.select_mobile('Android-移动')
        # current_mobile().reset_app()
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'group_chat', "high", "yx")
    def test_msg_huangcaizui_C_0010(self):
        """群聊中群短信无记录"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.（普通群群主、企业群/党群的成员或群主）已进入的群聊页面
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多富媒体按钮
        gcp.click_more()
        # 2.是否存在更多选项
        time.sleep(1)
        self.assertTrue(gcp.is_exist_more_page())
        time.sleep(1)
        # 3.点击群短信
        gcp.click_group_sms()
        cgs = ChatGroupSMSPage()
        # 4.如果在资费介绍页，点击确定
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        # 5.判断有无显示记录
        cgs.wait_for_page_load()
        if not cgs.is_on_message_edit_this_page():
            raise AssertionError("当前页面不在群短信编辑页面")
        else:
            print("进入群短信编辑页面，显示记录")
        time.sleep(1)

    @staticmethod
    def setUp_test_msg_huangcaizui_C_0011():
        """先发送一条消息，确保有消息记录"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().reset_app()
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_more()
        gcp.click_group_sms()
        cgs = ChatGroupSMSPage()
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        cgs.wait_for_page_load()
        if cgs.is_on_message_edit_this_page():
            cgs.click_add_contact()
            cgs.click_first_contact()
            cgs.click_contact_sure()
            cgs.input_text_message("群短信测试")
            cgs.click_send()
            cgs.wait_for_record_page_load()
            cgs.click_back()
            gcp.click_more()
            time.sleep(1)

    @tags('ALL', 'CMCC', 'group_chat', "high", "yx")
    def test_msg_huangcaizui_C_0011(self):
        """群聊中群短信无记录"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.（普通群群主、企业群/党群的成员或群主）已进入的群聊页面
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击更多富媒体按钮
        gcp.click_more()
        # 2.是否存在更多选项
        self.assertTrue(gcp.is_exist_more_page())
        # 3.点击群短信
        gcp.click_group_sms()
        cgs = ChatGroupSMSPage()
        # 4.如果在资费介绍页，点击确定
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        # 4.判断有无显示记录
        if not cgs.is_on_message_record_this_page():
            raise AssertionError("当前页面不在历史群短信记录页面")
        else:
            cgs.wait_for_record_page_load()
            print("进入群短信编辑页面，显示记录")
        time.sleep(1)

    @staticmethod
    def setUp_test_msg_huangcaizui_C_0013():
        Preconditions.select_mobile('Android-移动')
        current_mobile().reset_app()
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'group_chat', "high", "yx")
    def test_msg_huangcaizui_C_0013(self):
        """群短信输入1个字符的文本内容进行发送"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.（普通群群主、企业群/党群的成员或群主）已进入的群聊页面
        gcp = GroupChatPage()
        # 1.点击更多富媒体按钮
        gcp.click_more()
        # 2.点击群短信
        gcp.click_group_sms()
        cgs = ChatGroupSMSPage()
        # 3.如果在资费介绍页，点击确定
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        cgs.wait_for_page_load()
        if cgs.is_on_message_edit_this_page():
            # 4.点击添加收件人
            cgs.click_add_contact()
            # 5.点击联系人列表第一个
            cgs.click_first_contact()
            # 6.点击确定
            cgs.click_contact_sure()
            # 7.输入文本a
            cgs.input_text_message("a")
            # 8.点击发送
            cgs.click_send()

    @tags('ALL', 'CMCC', 'group_chat', "high", "yx")
    def test_msg_huangcaizui_C_0016(self):
        """短信已发送多条的情况，查看群短信记录排序"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.（普通群群主、企业群/党群的成员或群主）已进入的群聊页面
        gcp = GroupChatPage()
        # 1.点击更多富媒体按钮
        gcp.click_more()
        # 2.点击群短信
        gcp.click_group_sms()
        cgs = ChatGroupSMSPage()
        # 3.如果在资费介绍页，点击确定
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        # 4.判断有无显示记录
        if not cgs.is_on_message_record_this_page():
            raise AssertionError("当前页面不在历史群短信记录页面")
        else:
            cgs.wait_for_record_page_load()
            print("进入群短信编辑页面，显示记录")
        time.sleep(1)

    @staticmethod
    def setUp_test_msg_huangcaizui_C_0017():
        Preconditions.select_mobile('Android-移动')
        current_mobile().reset_app()
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'group_chat', "high", "yx")
    def test_msg_huangcaizui_C_0017(self):
        """观察群短信内容以及群成员的展示"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.（普通群群主、企业群/党群的成员或群主）已进入的群聊页面
        gcp = GroupChatPage()
        # 1.点击更多富媒体按钮
        gcp.click_more()
        # 2.点击群短信
        gcp.click_group_sms()
        cgs = ChatGroupSMSPage()
        # 3.如果在资费介绍页，点击确定
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        cgs.wait_for_page_load()
        if cgs.is_on_message_edit_this_page():
            # 4.点击，添加收件人
            cgs.click_add_contact()
            cgs.click_first_contact()
            cgs.click_contact_sure()
            # 5.输入文本，点击发送
            cgs.input_text_message("群发短信测试")
            cgs.click_send()
            # 6.等待群短信记录加载
            cgs.wait_for_record_page_load()
        # 7.判断当前页面是否含有发送文本
        self.assertTrue(cgs.page_should_contain_text('群发短信测试'))
        self.assertTrue(cgs.page_should_contain_text("发送给:"))
        time.sleep(1)

    @tags('ALL', 'CMCC', 'group_chat', "high", "yx")
    def test_msg_huangcaizui_C_0019(self):
        """点击底部编辑按钮，是否跳转到编辑页面"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.（普通群群主、企业群/党群的成员或群主）已进入的群聊页面
        gcp = GroupChatPage()
        # 1.点击更多富媒体按钮
        gcp.click_more()
        # 2.点击群短信
        gcp.click_group_sms()
        cgs = ChatGroupSMSPage()
        # 3.如果在资费介绍页，点击确定
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        # 4.等待群短信记录页面加载
        cgs.wait_for_record_page_load()
        # 5.点击底部的编辑新短信的按钮
        cgs.click_add()
        # 6.验证是否跳转到群短信编辑页面
        cgs.wait_for_page_load()
        self.assertTrue(cgs.is_on_message_edit_this_page())
        time.sleep(1)

    @tags('ALL', 'CMCC', 'group_chat', "high", "yx")
    def test_msg_huangcaizui_C_0020(self):
        """点击左上角返回键时候返回群聊天页面"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.（普通群群主、企业群/党群的成员或群主）已进入的群聊页面
        gcp = GroupChatPage()
        # 1.点击更多富媒体按钮
        gcp.click_more()
        # 2.点击群短信
        gcp.click_group_sms()
        time.sleep(1)
        cgs = ChatGroupSMSPage()
        # 3.如果在资费介绍页，点击确定
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        time.sleep(1)
        # 3.点击返回
        cgs.click_back()
        # 4.验证是否在群聊页面
        self.assertTrue(gcp.is_on_this_page())

    @tags('ALL', 'CMCC', 'group_chat', "high", "yx")
    def test_msg_huangcaizui_C_0021(self):
        """从群短信列表进入群发短信页面"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.（普通群群主、企业群/党群的成员或群主）已进入的群聊页面
        gcp = GroupChatPage()
        # 1.点击更多富媒体按钮
        gcp.click_more()
        # 2.点击群短信
        gcp.click_group_sms()
        cgs = ChatGroupSMSPage()
        # 3.如果在资费介绍页，点击确定
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        # 4.等待群短信记录页面加载
        cgs.wait_for_record_page_load()
        # 5.点击底部的编辑新短信的按钮
        cgs.click_add()
        # 6.验证是否跳转到群短信编辑页面
        cgs.wait_for_page_load()
        self.assertTrue(cgs.is_on_message_edit_this_page())
        time.sleep(1)

    @staticmethod
    def setUp_test_msg_huangcaizui_C_0025():
        Preconditions.select_mobile('Android-移动')
        current_mobile().reset_app()
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'group_chat', "high", "yx")
    def test_msg_huangcaizui_C_0025(self):
        """进入群短信收件人联系人选择器"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.（普通群群主、企业群/党群的成员或群主）已进入的群聊页面
        gcp = GroupChatPage()
        # 1.点击更多富媒体按钮
        gcp.click_more()
        # 2.点击群短信
        gcp.click_group_sms()
        cgs = ChatGroupSMSPage()
        # 3.如果在资费介绍页，点击确定
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        cgs.wait_for_page_load()
        # 4.输入文本消息
        cgs.input_text_message("测试测试")
        # 5.点击发送消息
        cgs.click_send()
        # 6.验证是否弹框提示'请选择收件人'
        self.assertTrue(cgs.is_toast_exist("请选择收件人"))
        # 7.点击接收人右边头像按钮
        cgs.click_add_contact()
        cgs.wait_for_select_contact_page_load()
        # 8.验证是否存在全选按钮
        self.assertTrue(cgs.is_exist_select_all())
        # 9.选择第一个联系人
        cgs.click_first_contact()
        # 10.验证是否存在已选择人数和可选择的最高上限人数显示
        self.assertTrue(cgs.is_exist_select_and_all())
        time.sleep(2)

    @tags('ALL', 'CMCC', 'group_chat', "high", "yx")
    def test_msg_huangcaizui_C_0026(self):
        """进入群短信收件人联系人选择器"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.（普通群群主、企业群/党群的成员或群主）已进入的群聊页面
        gcp = GroupChatPage()
        # 1.点击更多富媒体按钮
        gcp.click_more()
        # 2.点击群短信
        gcp.click_group_sms()
        cgs = ChatGroupSMSPage()
        # 3.如果在资费介绍页，点击确定
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        cgs.wait_for_page_load()
        # 4.点击接收人右边头像按钮
        cgs.click_add_contact()
        cgs.wait_for_select_contact_page_load()
        # 5.点击全选
        cgs.click_select_all()
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_huangcaizui_C_0033():
        Preconditions.select_mobile('Android-移动')
        current_mobile().reset_app()
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'group_chat', "high", "yx")
    def test_msg_huangcaizui_C_0033(self):
        """昵称搜索群成员"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.（普通群群主、企业群/党群的成员或群主）已进入的群聊页面
        gcp = GroupChatPage()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击第一个群成员头像
        gcsp.click_first_group_member_avatar()
        cdp = ContactDetailsPage()
        # 3.获取群成员名字
        name = cdp.get_people_name()
        time.sleep(1)
        # 4.点击返回群聊页面
        cdp.click_back_icon()
        gcsp.click_back()
        gcp.wait_for_page_load()
        # 5.点击更多富媒体按钮
        gcp.click_more()
        # 6.点击群短信
        gcp.click_group_sms()
        cgs = ChatGroupSMSPage()
        # 7.如果在资费介绍页，点击确定
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        cgs.wait_for_page_load()
        # 8.输入文本消息
        cgs.input_text_message("测试测试")
        # 9.点击发送消息
        cgs.click_send()
        # 10.验证是否弹框提示'请选择收件人'
        self.assertTrue(cgs.is_toast_exist("请选择收件人"))
        # 11.点击接收人右边头像按钮
        cgs.click_add_contact()
        # 12.点击搜索成员，用昵称搜索群成员
        cgs.input_search_message(name)
        # 13.验证是否有搜索结果
        if cgs.page_should_contain_text("无搜索结果"):
            print("无搜索结果，不能用昵称搜索群成员")

    @staticmethod
    def setUp_test_msg_huangcaizui_C_0034():
        Preconditions.select_mobile('Android-移动')
        current_mobile().reset_app()
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'group_chat', "high", "yx")
    def test_msg_huangcaizui_C_0034(self):
        """昵称搜索群成员"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.（普通群群主、企业群/党群的成员或群主）已进入的群聊页面
        gcp = GroupChatPage()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击第一个群成员头像
        gcsp.click_first_group_member_avatar()
        cdp = ContactDetailsPage()
        # 3.获取群成员手机号
        phone_number = cdp.get_people_number()
        time.sleep(1)
        # 4.点击返回群聊页面
        cdp.click_back_icon()
        gcsp.click_back()
        gcp.wait_for_page_load()
        # 5.点击更多富媒体按钮
        gcp.click_more()
        # 6.点击群短信
        gcp.click_group_sms()
        cgs = ChatGroupSMSPage()
        # 7.如果在资费介绍页，点击确定
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        cgs.wait_for_page_load()
        # 8.输入文本消息
        cgs.input_text_message("测试测试")
        # 9.点击发送消息
        cgs.click_send()
        # 10.验证是否弹框提示'请选择收件人'
        self.assertTrue(cgs.is_toast_exist("请选择收件人"))
        # 11.点击接收人右边头像按钮
        cgs.click_add_contact()
        # 12.点击搜索成员，用手机号搜索群成员
        cgs.input_search_message(phone_number)
        # 13.验证是否有搜索结果
        if cgs.page_should_contain_text("无搜索结果"):
            print("无搜索结果，不能用昵称搜索群成员")

    @tags('ALL', 'CMCC', 'group_chat', "high", "yx")
    def test_msg_huangcaizui_C_0035(self):
        """选择群成员后返回去查看，是否可以从新选择"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.（普通群群主、企业群/党群的成员或群主）已进入的群聊页面
        gcp = GroupChatPage()
        # 1.点击更多富媒体按钮
        gcp.click_more()
        # 2.点击群短信
        gcp.click_group_sms()
        cgs = ChatGroupSMSPage()
        # 3.如果在资费介绍页，点击确定
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        cgs.wait_for_page_load()
        # 4.输入文本消息
        cgs.input_text_message("测试测试")
        # 5.点击发送消息
        cgs.click_send()
        # 6.验证是否弹框提示'请选择收件人'
        self.assertTrue(cgs.is_toast_exist("请选择收件人"))
        # 7.点击接收人右边头像按钮
        cgs.click_add_contact()
        cgs.wait_for_select_contact_page_load()
        # 8.选择第一个联系人
        cgs.click_first_contact()
        # 9.点击确定
        cgs.click_contact_sure()
        # 10.再次点击接收人右边头像按钮
        cgs.click_add_contact()
        cgs.wait_for_select_contact_page_load()
        # 11.点击选择第二个联系人
        cgs.click_second_contact()
        # 12.是否可以重新选择联系人
        self.assertTrue(cgs.is_exist_renew_select())
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_huangcaizui_C_0037():
        Preconditions.select_mobile('Android-移动')
        current_mobile().reset_app()
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'group_chat', "high", "yx")
    def test_msg_huangcaizui_C_0037(self):
        """编辑群短信字符数为1"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.（普通群群主、企业群/党群的成员或群主）已进入的群聊页面
        gcp = GroupChatPage()
        # 1.点击更多富媒体按钮
        gcp.click_more()
        # 2.点击群短信
        gcp.click_group_sms()
        cgs = ChatGroupSMSPage()
        # 3.如果在资费介绍页，点击确定
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        cgs.wait_for_page_load()
        if cgs.is_on_message_edit_this_page():
            # 4.点击添加收件人
            cgs.click_add_contact()
            # 5.点击联系人列表第一个
            cgs.click_first_contact()
            # 6.点击确定
            cgs.click_contact_sure()
            # 7.输入1
            cgs.input_text_message("1")
            # 8.点击发送
            cgs.click_send()
        # 9.验证是否提示发送成功
        self.assertTrue(cgs.is_toast_exist("发送成功"))
        # 10.验证是否进入短信列表页面
        cgs.wait_for_record_page_load()
        self.assertTrue(cgs.is_on_message_record_this_page())

    @staticmethod
    def setUp_test_msg_huangcaizui_C_0040():
        Preconditions.select_mobile('Android-移动')
        current_mobile().reset_app()
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'group_chat', "high", "yx")
    def test_msg_huangcaizui_C_0040(self):
        """编辑群短信字符数为1"""
        # 1.网络正常，本网用户
        # 2.客户端已登录
        # 3.首次使用发送短信，短信设置开关已开启
        # 4.（普通群群主、企业群/党群的成员或群主）已进入的群聊页面
        gcp = GroupChatPage()
        # 1.点击更多富媒体按钮
        gcp.click_more()
        # 2.点击群短信
        gcp.click_group_sms()
        cgs = ChatGroupSMSPage()
        # 3.如果在资费介绍页，点击确定
        if cgs.is_on_this_page():
            cgs.click_coordinate()
        cgs.wait_for_page_load()
        if cgs.is_on_message_edit_this_page():
            # 4.点击添加收件人
            cgs.click_add_contact()
            # 5.点击联系人列表第一个
            cgs.click_first_contact()
            # 6.点击确定
            cgs.click_contact_sure()
            # 7.输入发送信息
            cgs.input_text_message("群发短信测试，群发短信测试。")
            # 8.点击发送
            cgs.click_send()
        # 9.验证是否提示发送成功
        self.assertTrue(cgs.is_toast_exist("发送成功"))
        # 10.验证是否进入短信列表页面
        cgs.wait_for_record_page_load()
        self.assertTrue(cgs.is_on_message_record_this_page())

    @staticmethod
    def setUp_test_msg_xiaoqiu_0615():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0615(self):
        """首次创建群聊桌面快捷方式"""
        # 1、手机存在桌面快捷方式权限
        # 2、已开启此权限或者此权限默认为开启状态
        # 3、登录和飞信
        # 4、进入到群聊设置页面
        # 5、勾选弹窗中复选框
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击添加桌面快捷方式
        gcsp.click_add_destop_link()
        # 3.点击不再提醒
        if gcsp.is_text_present("我知道了"):
            gcsp.click_no_show_again()
            gcsp.click_text("我知道了")
        time.sleep(3)
        if gcsp.is_text_present("添加到主屏幕"):
            gcsp.click_sure_add_desktop_shortcut()
        # 4.再次点击添加桌面快捷方式
        gcsp.wait_for_page_load()
        gcsp.click_add_destop_link()
        # 5.验证是否再次弹框提示‘已尝试添加到桌面’
        self.assertFalse(gcsp.is_text_present("我知道了"))

    @staticmethod
    def setUp_test_msg_xiaoqiu_0616():
        Preconditions.select_mobile('Android-移动')
        current_mobile().launch_app()
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0616(self):
        """首次创建群聊桌面快捷方式"""
        # 1、手机存在桌面快捷方式权限
        # 2、已开启此权限或者此权限默认为开启状态
        # 3、登录和飞信
        # 4、进入到群聊设置页面
        # 5、勾选弹窗中复选框
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击添加桌面快捷方式
        gcsp.click_add_destop_link()
        # 3.点击不再提醒
        if gcsp.is_text_present("我知道了"):
            gcsp.click_no_show_again()
            gcsp.click_text("我知道了")
        time.sleep(3)
        if gcsp.is_text_present("添加到主屏幕"):
            gcsp.click_sure_add_desktop_shortcut()
        # 4.重置APP
        Preconditions.select_mobile('Android-移动')
        current_mobile().launch_app()
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 5.点击添加桌面快捷方式
        gcsp.click_add_destop_link()
        # 6.点击不再提醒
        if gcsp.is_text_present("我知道了"):
            gcsp.click_no_show_again()
            gcsp.click_text("我知道了")
        time.sleep(3)
        if gcsp.is_text_present("添加到主屏幕"):
            gcsp.click_sure_add_desktop_shortcut()

    @staticmethod
    def setUp_test_msg_xiaoqiu_0617():
        """进入群聊创建快捷方式，退出登录"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击添加桌面快捷方式
        gcsp.click_add_destop_link()
        # 3.点击不再提醒
        if gcsp.is_text_present("我知道了"):
            gcsp.click_no_show_again()
            gcsp.click_text("我知道了")
        if gcsp.is_text_present("添加到主屏幕"):
            gcsp.click_sure_add_desktop_shortcut()
        # 4.点击返回消息页面
        gcsp.click_back()
        gcp.click_back()
        mess = MessagePage()
        mess.click_me_icon()
        # 5.点击我
        me_page = MePage()
        me_page.click_setting_menu()
        setting = SettingPage()
        # 6.点击退出登录
        setting.click_logout()
        setting.click_ok_of_alert()
        time.sleep(3)

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0617(self):
        """退出登录，点击桌面已创建成功的桌面快捷方式"""
        # 1、当前桌面已存在和飞信群聊的快捷方式
        # 2、和飞信是退出登录状态
        Preconditions.background_app()
        gcp = GroupChatPage()
        time.sleep(2)
        # 1.点击桌面已存在的群聊快捷方式
        gcp.is_element_present_on_desktop("群聊1")
        gcp.click_text("群聊1")
        time.sleep(2)
        one_key = OneKeyLoginPage()
        # 2.验证是否会跳转到和飞信登录页
        one_key.is_on_this_page()
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0617():
        # 1.重新登录
        one_key = OneKeyLoginPage()
        one_key.wait_for_page_load()
        one_key.click_one_key_login()
        mess = MessagePage()
        mess.wait_login_success(60)
        Preconditions.background_app()
        time.sleep(2)
        # 2.长按删除桌面已存在的群聊快捷方式
        mess.is_element_present_on_desktop("群聊1")
        mess.press_text("群聊1")
        mess.click_text("移除")
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0618():
        """进入群聊创建快捷方式，退出登录"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_add_destop_link()
        if gcsp.is_text_present("我知道了"):
            gcsp.click_no_show_again()
            gcsp.click_text("我知道了")
        if gcsp.is_text_present("添加到主屏幕"):
            gcsp.click_sure_add_desktop_shortcut()
        gcsp.click_back()
        gcp.click_back()
        mess = MessagePage()
        mess.click_me_icon()
        me_page = MePage()
        me_page.click_setting_menu()
        setting = SettingPage()
        setting.click_logout()
        setting.click_ok_of_alert()
        time.sleep(3)

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0618(self):
        """退出登录，点击桌面已创建成功的桌面快捷方式"""
        # 1、当前桌面已存在和飞信群聊的快捷方式
        # 2、和飞信是退出登录状态
        Preconditions.background_app()
        contact_detail = ContactDetailsPage()
        time.sleep(2)
        # 1.点击桌面已存在的群聊快捷方式
        contact_detail.is_element_present_on_desktop("群聊1")
        contact_detail.click_text("群聊1")
        time.sleep(2)
        one_key = OneKeyLoginPage()
        one_key.wait_for_page_load()
        # 2.点击一键登录
        one_key.click_one_key_login()
        mess = MessagePage()
        mess.wait_login_success(60)
        # 3.验证是否在消息页面
        self.assertTrue(mess.is_on_this_page())
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0618():
        mess = MessagePage()
        Preconditions.background_app()
        time.sleep(2)
        # 长按删除桌面已存在的群聊快捷方式
        mess.is_element_present_on_desktop("群聊1")
        mess.press_text("群聊1")
        mess.click_text("移除")
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0619():
        """创建群，创建快捷方式，退出群聊"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        # 1.点击通讯录
        mess.click_contacts_only()
        contact = ContactsPage()
        if contact.is_text_present('始终允许'):
            contact.click_text('始终允许')
        # 2.点击群聊
        contact.click_group_chat()
        glp = GroupListPage()
        glp.wait_for_page_load()
        # 3.点击新建群
        glp.click_create_group()
        # 4.点击选择团队联系人
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        scp.click_group_contact()
        # 5.选择团队联系人
        scp.input_search_keyword("大佬1")
        scp.selecting_contacts_by_name("大佬1")
        scp.input_search_keyword("大佬2")
        scp.selecting_contacts_by_name("大佬2")
        # 6.点击确定
        scp.click_sure_forward()
        cgnp = CreateGroupNamePage()
        cgnp.wait_for_page_load()
        # 7.输入群名
        cgnp.input_group_name("创建快捷方式群聊1")
        time.sleep(2)
        # 8.点击确定
        cgnp.click_sure()
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 9.点击添加快捷方式
        gcsp.click_add_destop_link()
        if gcsp.is_text_present("我知道了"):
            gcsp.click_no_show_again()
            gcsp.click_text("我知道了")
        time.sleep(3)
        if gcsp.is_text_present("添加到主屏幕"):
            gcsp.click_sure_add_desktop_shortcut()
        time.sleep(3)
        gcsp.wait_for_page_load()
        # 10.点击删除并退出
        gcsp.click_delete_and_exit2()
        gcsp.click_sure()
        gcsp.click_first_group_member_avatar()
        gcsp.click_sure()

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0619(self):
        """退出当前创建快捷方式的群聊"""
        # 1、当前桌面已存在和飞信群聊的快捷方式
        # 2、已登录和飞信
        Preconditions.background_app()
        gcp = GroupChatPage()
        time.sleep(2)
        # 1.点击桌面已存在的群聊快捷方式
        gcp.is_element_present_on_desktop("创建快捷方式群聊1")
        time.sleep(2)
        gcp.click_text("创建快捷方式群聊1")
        time.sleep(3)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0619():
        mess = MessagePage()
        Preconditions.background_app()
        time.sleep(2)
        # 长按删除桌面已存在的群聊快捷方式
        mess.is_element_present_on_desktop("创建快捷方式群聊1")
        mess.press_text("创建快捷方式群聊1")
        mess.click_text("移除")
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0620():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0620(self):
        """杀死和飞信后，点击桌面快捷方式"""
        # 1、当前桌面已存在和飞信群聊的快捷方式
        # 2、已登录和飞信
        # 3、登录未失效
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击添加桌面快捷方式
        gcsp.click_add_destop_link()
        # 3.点击不再提醒
        if gcsp.is_text_present("我知道了"):
            gcsp.click_no_show_again()
            gcsp.click_text("我知道了")
        time.sleep(2)
        if gcsp.is_text_present("添加到主屏幕"):
            gcsp.click_sure_add_desktop_shortcut()
        # 4.返回群聊页面
        gcsp.click_back()
        gcp.wait_for_page_load()
        # 5.杀掉进程
        current_mobile().launch_app()
        Preconditions.background_app()
        contact_detail = ContactDetailsPage()
        time.sleep(2)
        # 6.点击桌面已存在的群聊快捷方式
        contact_detail.is_element_present_on_desktop("群聊1")
        contact_detail.click_text("群聊1")
        # 7.验证是否在群聊会话页面
        gcp.wait_for_page_load()
        self.assertTrue(gcp.is_on_this_page())
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0620():
        mess = MessagePage()
        Preconditions.background_app()
        time.sleep(2)
        # 长按删除桌面已存在的群聊快捷方式
        mess.is_element_present_on_desktop("群聊1")
        mess.press_text("群聊1")
        mess.click_text("移除")
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0621():
        """进入群聊创建快捷方式，杀死和飞信进程（退出和飞信）"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_add_destop_link()
        if gcsp.is_text_present("我知道了"):
            gcsp.click_no_show_again()
            gcsp.click_text("我知道了")
        time.sleep(2)
        if gcsp.is_text_present("添加到主屏幕"):
            gcsp.click_sure_add_desktop_shortcut()
        gcsp.click_back()
        gcp.click_back()
        mess = MessagePage()
        mess.click_me_icon()
        me_page = MePage()
        me_page.click_setting_menu()
        setting = SettingPage()
        setting.click_logout()
        setting.click_ok_of_alert()
        time.sleep(3)

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0621(self):
        """杀死和飞信后，点击桌面快捷方式"""
        # 1、当前桌面已存在和飞信群聊的快捷方式
        # 2、已登录和飞信
        # 3、登录已失效
        Preconditions.background_app()
        contact_detail = ContactDetailsPage()
        time.sleep(2)
        # 1.点击桌面已存在的群聊快捷方式
        contact_detail.is_element_present_on_desktop("群聊1")
        contact_detail.click_text("群聊1")
        time.sleep(2)
        one_key = OneKeyLoginPage()
        one_key.wait_for_page_load()
        # 2.点击一键登录
        one_key.click_one_key_login()
        mess = MessagePage()
        mess.wait_login_success(60)
        # 3.验证是否在消息页面
        self.assertTrue(mess.is_on_this_page())
        time.sleep(2)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0621():
        mess = MessagePage()
        Preconditions.background_app()
        time.sleep(2)
        # 长按删除桌面已存在的群聊快捷方式
        mess.is_element_present_on_desktop("群聊1")
        mess.press_text("群聊1")
        mess.click_text("移除")
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0622():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0622(self):
        """不杀死和飞信后，点击桌面快捷方式"""
        # 1、当前桌面已存在和飞信群聊的快捷方式
        # 2、已登录和飞信
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击添加桌面快捷方式
        gcsp.click_add_destop_link()
        # 3.点击不再提醒
        if gcsp.is_text_present("我知道了"):
            gcsp.click_no_show_again()
            gcsp.click_text("我知道了")
        time.sleep(2)
        if gcsp.is_text_present("添加到主屏幕"):
            gcsp.click_sure_add_desktop_shortcut()
        # 4.返回群聊页面
        gcsp.click_back()
        gcp.wait_for_page_load()
        Preconditions.background_app()
        contact_detail = ContactDetailsPage()
        time.sleep(2)
        # 5.点击桌面已存在的群聊快捷方式
        contact_detail.is_element_present_on_desktop("群聊1")
        contact_detail.click_text("群聊1")
        # 7.验证是否在群聊会话页面
        self.assertTrue(gcp.is_on_this_page())

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0622():
        mess = MessagePage()
        Preconditions.background_app()
        time.sleep(2)
        # 长按删除桌面已存在的群聊快捷方式
        mess.is_element_present_on_desktop("群聊1")
        mess.press_text("群聊1")
        mess.click_text("移除")
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0624():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0624(self):
        """无网络状态下，打开已创建的桌面快捷方式"""
        # 1、当前桌面已存在和飞信群聊的快捷方式
        # 2、已登录和飞信
        # 3、无网络状态
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击添加桌面快捷方式
        gcsp.click_add_destop_link()
        # 3.点击不再提醒
        if gcsp.is_text_present("我知道了"):
            gcsp.click_no_show_again()
            gcsp.click_text("我知道了")
        time.sleep(2)
        if gcsp.is_text_present("添加到主屏幕"):
            gcsp.click_sure_add_desktop_shortcut()
        # 4.返回群聊页面
        gcsp.click_back()
        gcp.wait_for_page_load()
        # 5.断开网络
        gcp.set_network_status(0)
        Preconditions.background_app()
        contact_detail = ContactDetailsPage()
        time.sleep(2)
        # 6.点击桌面已存在的群聊快捷方式
        contact_detail.is_element_present_on_desktop("群聊1")
        contact_detail.click_text("群聊1")
        # 8.验证是否在群聊会话页面
        gcp.wait_for_page_load()
        self.assertTrue(gcp.is_on_this_page())
        time.sleep(3)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0624():
        # 重新连接网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)
        Preconditions.background_app()
        time.sleep(2)
        # 长按删除桌面已存在的群聊快捷方式
        mess = MessagePage()
        mess.is_element_present_on_desktop("群聊1")
        mess.press_text("群聊1")
        mess.click_text("移除")
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0625():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0625(self):
        """无网络状态下，创建的桌面快捷方式"""
        # 1、当前桌面已存在和飞信群聊的快捷方式
        # 2、已登录和飞信
        # 3、无网络状态
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.断开网络
        gcsp.set_network_status(0)
        # 3.点击添加桌面快捷方式
        gcsp.click_add_destop_link()
        # 4.点击不再提醒
        if gcsp.is_text_present("我知道了"):
            gcsp.click_no_show_again()
            gcsp.click_text("我知道了")
        time.sleep(3)
        if gcsp.is_text_present("添加到主屏幕"):
            gcsp.click_sure_add_desktop_shortcut()

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0625():
        # 重新连接网络
        gcsp = GroupChatSetPage()
        gcsp.set_network_status(6)
        Preconditions.background_app()
        time.sleep(2)
        # 长按删除桌面已存在的群聊快捷方式
        mess = MessagePage()
        mess.is_element_present_on_desktop("群聊1")
        mess.press_text("群聊1")
        mess.click_text("移除")
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0626():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0626(self):
        """无网络状态下，创建的桌面快捷方式"""
        # 1、当前桌面已存在和飞信群聊的快捷方式
        # 2、已登录和飞信
        # 3、无网络状态
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        # 1.点击设置
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        # 2.点击添加桌面快捷方式
        gcsp.click_add_destop_link()
        # 3.点击不再提醒
        if gcsp.is_text_present("我知道了"):
            gcsp.click_no_show_again()
            gcsp.click_text("我知道了")
        time.sleep(3)
        if gcsp.is_text_present("添加到主屏幕"):
            gcsp.click_sure_add_desktop_shortcut()
        # 4.再次点击添加桌面快捷方式
        gcsp.click_add_destop_link()

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0626():
        Preconditions.background_app()
        time.sleep(2)
        # 长按删除桌面已存在的群聊快捷方式
        mess = MessagePage()
        mess.is_element_present_on_desktop("群聊1")
        mess.press_text("群聊1")
        mess.click_text("移除")
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0627():
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0627(self):
        """不同的群，相同的名称，创建快捷方式"""
        # 1、当前桌面已存在和飞信群聊的快捷方式
        # 2、已登录和飞信
        Preconditions.make_already_in_message_page()
        # 创建相同名字的群，创建快捷方式
        for i in range(2):
            mess = MessagePage()
            # 1.点击通讯录
            mess.click_contacts_only()
            contact = ContactsPage()
            if contact.is_text_present('始终允许'):
                contact.click_text('始终允许')
            # 2.点击群聊
            contact.click_group_chat()
            glp = GroupListPage()
            glp.wait_for_page_load()
            # 3.点击新建群
            glp.click_create_group()
            # 4.点击选择团队联系人
            scp = SelectContactsPage()
            scp.wait_for_page_load()
            scp.click_group_contact()
            # 5.选择团队联系人
            scp.input_search_keyword("大佬1")
            scp.selecting_contacts_by_name("大佬1")
            scp.input_search_keyword("大佬2")
            scp.selecting_contacts_by_name("大佬2")
            # 6.点击确定
            scp.click_sure_forward()
            cgnp = CreateGroupNamePage()
            cgnp.wait_for_page_load()
            # 7.输入群名
            cgnp.input_group_name("创建快捷方式群聊")
            time.sleep(2)
            # 8.点击确定
            cgnp.click_sure()
            gcp = GroupChatPage()
            gcp.wait_for_page_load()
            gcp.click_setting()
            gcsp = GroupChatSetPage()
            gcsp.wait_for_page_load()
            # 9.点击添加快捷方式
            gcsp.click_add_destop_link()
            if gcsp.is_text_present("我知道了"):
                gcsp.click_no_show_again()
                gcsp.click_text("我知道了")
            time.sleep(3)
            if gcsp.is_text_present("添加到主屏幕"):
                gcsp.click_sure_add_desktop_shortcut()
            time.sleep(3)
            # 10.点击群管理,解散群
            gcsp.click_group_manage()
            gcsp.click_group_manage_disband_button()
            gcsp.click_sure()
            time.sleep(1)
            # 11.返回消息列表页面
            gcp.click_back()
            glp = GroupListPage()
            time.sleep(1)
            glp.click_back()
            contacts = ContactsPage()
            contacts.click_message_icon()

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0627():
        for i in range(2):
            Preconditions.background_app()
            time.sleep(2)
            # 长按删除桌面已存在的群聊快捷方式
            mess = MessagePage()
            mess.is_element_present_on_desktop("创建快捷方式群聊")
            mess.press_text("创建快捷方式群聊")
            mess.click_text("移除")
            time.sleep(2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0632():
        """创建快捷方式"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("给个红包4")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_add_destop_link()
        if gcsp.is_text_present("我知道了"):
            gcsp.click_no_show_again()
            gcsp.click_text("我知道了")
        time.sleep(2)
        if gcsp.is_text_present("添加到主屏幕"):
            gcsp.click_sure_add_desktop_shortcut()

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0632(self):
        """创建A群聊桌面快捷方式后，修改当前A群聊的昵称"""
        # 1、当前桌面已存在和飞信群聊的快捷方式
        # 2、已登录和飞信
        gcsp = GroupChatSetPage()
        # 1.修改群名
        gcsp.click_modify_group_name()
        gcsp.input_new_group_name("修改-给个红包4")
        gcsp.save_group_name()
        self.assertEquals(gcsp.is_toast_exist("修改成功"), True)
        gcsp.wait_for_page_load()
        Preconditions.background_app()
        contact_detail = ContactDetailsPage()
        time.sleep(2)
        # 2.点击桌面未修改名字前创建的群聊快捷方式
        contact_detail.is_element_present_on_desktop("给个红包4")
        contact_detail.click_text("给个红包4")
        # 3.验证是否进入群聊会话页面
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        self.assertTrue(gcp.is_on_this_page())
        time.sleep(3)

    @staticmethod
    def tearDown_test_msg_xiaoqiu_0632():
        """恢复修改前群名"""
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.click_modify_group_name()
        gcsp.input_new_group_name("给个红包4")
        gcsp.save_group_name()
        gcsp.wait_for_page_load()
        Preconditions.background_app()
        time.sleep(2)
        # 长按删除桌面已存在的群聊快捷方式
        mess = MessagePage()
        mess.is_element_present_on_desktop("给个红包4")
        mess.press_text("给个红包4")
        mess.click_text("移除")
        time.sleep(2)

    @staticmethod
    def setUp_test_msg_xiaoqiu_0634():
        """创建快捷方式"""
        Preconditions.select_mobile('Android-移动')
        Preconditions.make_already_in_message_page()
        Preconditions.get_into_group_chat_page("群聊1")
        gcp = GroupChatPage()
        gcp.wait_for_page_load()
        gcp.click_setting()
        gcsp = GroupChatSetPage()
        gcsp.wait_for_page_load()
        gcsp.click_add_destop_link()
        if gcsp.is_text_present("我知道了"):
            gcsp.click_no_show_again()
            gcsp.click_text("我知道了")
        time.sleep(2)
        if gcsp.is_text_present("添加到主屏幕"):
            gcsp.click_sure_add_desktop_shortcut()

    @tags('ALL', 'CMCC', 'yx')
    def test_msg_xiaoqiu_0634(self):
        """桌面快捷方式，删除操作"""
        # 1、当前桌面已存在和飞信群聊的快捷方式
        # 2、已登录和飞信
        Preconditions.background_app()
        contact_detail = ContactDetailsPage()
        time.sleep(2)
        # 1.长按桌面已存在的群聊快捷方式
        contact_detail.is_element_present_on_desktop("群聊1")
        contact_detail.press_text("群聊1")
        # 2.点击移除
        contact_detail.click_text("移除")
        # 3.验证桌面是否还存在群聊1的群聊快捷方式
        self.assertFalse(contact_detail.is_element_present_on_desktop("群聊1"))
        time.sleep(2)