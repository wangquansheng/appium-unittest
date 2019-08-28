import random
import re
import time

from library.core.TestCase import TestCase
from library.core.common.simcardtype import CardType
from library.core.utils.applicationcache import current_mobile
from library.core.utils.testcasefilter import tags
from pages import *
from preconditions.BasePreconditions import LoginPreconditions


class Preconditions(WorkbenchPreconditions):
    """前置条件"""

    @staticmethod
    def enter_label_grouping_chat_page(reset=False):
        """进入标签分组会话页面"""
        # 登录进入消息页面
        Preconditions.make_already_in_message_page(reset)
        mess = MessagePage()
        # 点击‘通讯录’
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(1)
        contacts.click_mobile_contacts()
        contacts.click_label_grouping()
        label_grouping = LabelGroupingPage()
        label_grouping.wait_for_page_load()
        # 不存在标签分组则创建
        group_name = Preconditions.get_label_grouping_name()
        group_names = label_grouping.get_label_grouping_names()
        time.sleep(1)
        if not group_names:
            label_grouping.click_new_create_group()
            label_grouping.wait_for_create_label_grouping_page_load()
            label_grouping.input_label_grouping_name(group_name)
            label_grouping.click_sure()
            # 选择成员
            slc = SelectLocalContactsPage()
            slc.wait_for_page_load()
            names = slc.get_contacts_name()
            if not names:
                raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
            for name in names:
                slc.select_one_member_by_name(name)
            slc.click_sure()
            label_grouping.wait_for_page_load()
            label_grouping.select_group(group_name)
        else:
            # 选择一个标签分组
            label_grouping.select_group(group_names[0])
        lgdp = LableGroupDetailPage()
        time.sleep(1)
        # 标签分组成员小于2人，需要添加成员
        members_name = lgdp.get_members_names()
        if lgdp.is_text_present("该标签分组内暂无成员") or len(members_name) < 2:
            lgdp.click_add_members()
            # 选择成员
            slc = SelectLocalContactsPage()
            slc.wait_for_page_load()
            names = slc.get_contacts_name()
            if not names:
                raise AssertionError("No m005_contacts, please add m005_contacts in address book.")
            for name in names:
                slc.select_one_member_by_name(name)
            slc.click_sure()
        # 点击群发信息
        lgdp.click_send_group_info()
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()

    @staticmethod
    def get_label_grouping_name():
        """获取群名"""
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        group_name = "alg" + phone_number[-4:]
        return group_name


class MsgLabelGroupingTest(TestCase):
    """息-标签分组文件、位置 + 消息-单聊视频_图片"""
    @classmethod
    def setUpClass(cls):
        # 备注：脚本中已判断预支文件是否存在
        Preconditions.select_mobile('Android-移动')

    def default_setUp(self):
        """确保每个用例运行前在标签分组会话页面"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_label_grouping_chat_page()
            return
        chat = LabelGroupingChatPage()
        if chat.is_on_this_page():
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_label_grouping_chat_page()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0001(self):
        """标签分组会话页面，不勾选本地文件内文件点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        if not chat.is_open_more():
            chat.click_more()
        # 2、点击本地文件
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 3、不选择文件，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0002(self):
        """标签分组会话页面，勾选本地文件内文件点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        if not chat.is_open_more():
            chat.click_more()
        # 2、点击本地文件
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        time.sleep(1)
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.click_preset_file_dir()
        file = local_file.select_file(".txt")
        time.sleep(1)
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0003(self):
        """标签分组会话页面，不勾选本地视频文件内视频点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        if not chat.is_open_more():
            chat.click_more()
        # 2、点击视频
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_video()
        # 3、不选择视频，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0004(self):
        """标签分组会话页面，勾选本地视频文件内视频点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        if not chat.is_open_more():
            chat.click_more()
        # 2、点击视频
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_video()
        time.sleep(3)
        # 3、选择视频，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 页面没有加载出视频，则循环6次
        for i in range(6):
            el = local_file.select_file2("视频")
            if el:
                local_file.click_send()
                # chat.wait_for_page_load()
                return
            else:
                local_file.click_back()
                csf.click_video()
            time.sleep(1)
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0005(self):
        """标签分组会话页面，不勾选本地照片文件内照片点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        if not chat.is_open_more():
            chat.click_more()
        # 2、点击照片
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_pic()
        # 3、不选择照片，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0006(self):
        """标签分组会话页面，勾选本地照片文件内照片点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        if not chat.is_open_more():
            chat.click_more()
        # 2、点击照片
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_pic()
        time.sleep(3)
        # 3、选择照片，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 页面没有加载出照片，则循环6次
        for i in range(6):
            el = local_file.select_file2("照片")
            if el:
                local_file.click_send()
                chat.wait_for_page_load()
                return
            else:
                local_file.click_back()
                csf.click_pic()
            time.sleep(1)
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()
        raise AssertionError("There is no pic")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0007(self):
        """标签分组会话页面，不勾选本地音乐文件内音乐点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        if not chat.is_open_more():
            chat.click_more()
        # 2、点击音乐
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_music()
        # 3、不选择音乐，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        flag = local_file.send_btn_is_enabled()
        self.assertFalse(flag)
        # 返回聊天会话页面
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0008(self):
        """标签分组会话页面，勾选本地音乐文件内音乐点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        if not chat.is_open_more():
            chat.click_more()
        # 2、点击音乐
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_music()
        time.sleep(3)
        # 3、选择音乐，直接点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 页面没有加载出照片，则循环6次
        for i in range(6):
            el = local_file.select_file2("音乐")
            if el:
                local_file.click_send()
                chat.wait_for_page_load()
                return
            else:
                local_file.click_back()
                csf.click_music()
            time.sleep(1)
        local_file.click_back()
        csf.click_back()
        chat.wait_for_page_load()
        raise AssertionError("There is no music")

    @staticmethod
    def public_open_file(file_type):
        """在聊天会话页面打开文件"""
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        # 进入到文件选择页面
        if not chat.is_open_more():
            chat.click_more()
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击本地文件，进入到本地文件中
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
            local_file.click_send()
            # 打开文件
            chat.open_file_in_chat_page(file_type)
            chat.wait_for_open_file()
            chat.click_back_in_open_file_page()
            chat.wait_for_page_load()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
            chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0009(self):
        """标签分组会话页面，点击格式为格式为doc的文件可以正常查阅"""
        # 1、在当前聊天会话页面点击格式为doc的文件
        self.public_open_file(".doc")
        print("test_msg_label_grouping_0009")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0010(self):
        """标签分组会话页面，点击格式为格式为docx的文件可以正常查阅"""
        # 1、在当前聊天会话页面点击格式为docx的文件
        self.public_open_file(".docx")
        print("test_msg_label_grouping_0010")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0011(self):
        """标签分组会话页面，点击格式为格式为ppt的文件可以正常查阅"""
        # 1、在当前聊天会话页面点击格式为ppt的文件
        self.public_open_file(".ppt")
        print("test_msg_label_grouping_0011")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0012(self):
        """标签分组会话页面，点击格式为格式为pptx的文件可以正常查阅"""
        # 1、在当前聊天会话页面点击格式为pptx的文件
        self.public_open_file(".pptx")
        print("test_msg_label_grouping_0012")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0013(self):
        """标签分组会话页面，点击格式为格式为pdf的文件可以正常查阅"""
        # 1、在当前聊天会话页面点击格式为pdf的文件
        self.public_open_file(".pdf")
        print("test_msg_label_grouping_0013")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0014(self):
        """标签分组会话页面，点击格式为格式为xls的文件可以正常查阅"""
        # 1、在当前聊天会话页面点击格式为xls的文件
        self.public_open_file(".xls")
        print("test_msg_label_grouping_0014")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0015(self):
        """标签分组会话页面，点击格式为格式为xlsx的文件可以正常查阅"""
        # 1、在当前聊天会话页面点击格式为xlsx的文件
        self.public_open_file(".xlsx")
        print("test_msg_label_grouping_0015")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0016(self):
        """标签分组会话页面，点击格式为格式为txt的文件可以正常查阅"""
        # 1、在当前聊天会话页面点击格式为txt的文件
        self.public_open_file(".txt")
        print("test_msg_label_grouping_0016")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0017(self):
        """标签分组会话页面，点击不能直接打开的文件调起系统应用打开查阅"""
        # 1、在当前聊天会话页面点击不能直接打开的文件
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        # 进入到文件选择页面
        if not chat.is_open_more():
            chat.click_more()
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击本地文件，进入到本地文件中
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
        file = local_file.select_file(".html")
        if file:
            local_file.click_send()
            # 打开文件
            chat.open_file_in_chat_page(".html")
            chat.wait_for_call_sys_app_page()
            # chat.click_cancle()
            chat.driver.back()
            chat.wait_for_page_load()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
            chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0018(self):
        """标签分组天会话页面，长按文件转发到任意群"""
        # 1、在当前群聊天会话页面长按任意文件
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        # 进入到文件选择页面
        if not chat.is_open_more():
            chat.click_more()
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击本地文件，进入到本地文件中
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 2、选择转发，选择一个群
            chat.forward_file(".txt")
            scp = SelectContactsPage()
            scp.click_select_one_group()
            sogp = SelectOneGroupPage()
            sogp.wait_for_page_load()
            names = sogp.get_group_name()
            if names:
                sogp.select_one_group_by_name(names[0])
                # 3、点击确定
                sogp.click_sure_forward()
                flag = sogp.is_toast_exist("已转发")
                self.assertTrue(flag)
            else:
                print("WARN: There is no group.")
                sogp.click_back()
                scp.click_back()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0019(self):
        """标签分组天会话页面，长按文件取消转发到任意群"""
        # 1、在当前群聊天会话页面长按任意文件
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        # 进入到文件选择页面
        if not chat.is_open_more():
            chat.click_more()
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击本地文件，进入到本地文件中
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 2、选择转发，选择一个群
            chat.forward_file(".txt")
            scp = SelectContactsPage()
            scp.click_select_one_group()
            sogp = SelectOneGroupPage()
            sogp.wait_for_page_load()
            names = sogp.get_group_name()
            if names:
                sogp.select_one_group_by_name(names[0])
                # 3、点击取消
                sogp.click_cancel_forward()
            else:
                print("WARN: There is no group.")
            sogp.click_back()
            scp.click_back()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0020(self):
        """标签分组天会话页面，长按文件转发到任意和通讯录联系人"""
        # 1、在当前群聊天会话页面长按任意文件
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        # 进入到文件选择页面
        if not chat.is_open_more():
            chat.click_more()
        more_page = ChatMorePage()
        more_page.click_file()
        time.sleep(1)
        # 点击本地文件，进入到本地文件中
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        time.sleep(3)
        local_file = ChatSelectLocalFilePage()
        # 没有预置文件，则上传
        flag = local_file.push_preset_file()
        if flag:
            local_file.click_back()
            csf.click_local_file()
        # 进入预置文件目录，选择文件发送
        local_file.click_preset_file_dir()
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 2、选择转发，选择一个和通讯录联系人
            chat.forward_file(".txt")
            time.sleep(1)
            scp = SelectContactsPage()
            scp.click_he_contacts()
            shcp = SelectHeContactsPage()
            shcp.wait_for_page_load()
            teams = shcp.get_team_names()
            if teams:
                # shcp.select_one_team_by_name(teams[0])
                sog = SelectOneGroupPage()
                sog.selecting_one_group_by_name2("ateam7272")
                time.sleep(2)
                detail_page = SelectHeContactsDetailPage()
                # detail_page.wait_for_page_load()
                names = detail_page.get_contacts_names()
                if not names:
                    print("WARN: Please add m005_contacts in %s." % teams[0])
                for name in names:
                    detail_page.select_one_linkman(name)
                    time.sleep(0.5)
                    if detail_page.is_text_present("确定"):
                        break
                    flag = detail_page.is_toast_exist("该联系人不可选", timeout=3)
                    if not flag:
                        break
                # 3、点击确定
                detail_page.click_sure_forward()
                flag2 = detail_page.is_toast_exist("已转发")
                self.assertTrue(flag2)
            else:
                print("WARN: Please create a team and add m005_contacts.")
                shcp.click_back()
                scp.click_back()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0021(self):
        """标签分组天会话页面，长按文件取消转发到任意和通讯录联系人"""
        # 1、在当前群聊天会话页面长按任意文件
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        # 进入到文件选择页面
        if not chat.is_open_more():
            chat.click_more()
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击本地文件，进入到本地文件中
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 2、选择转发，选择一个和通讯录联系人
            chat.forward_file(".txt")
            scp = SelectContactsPage()
            scp.click_he_contacts()
            shcp = SelectHeContactsPage()
            shcp.wait_for_page_load()
            teams = shcp.get_team_names()
            if teams:
                # shcp.select_one_team_by_name(teams[0])
                sog = SelectOneGroupPage()
                sog.selecting_one_group_by_name2("ateam7272")
                time.sleep(2)
                detail_page = SelectHeContactsDetailPage()
                # detail_page.wait_for_page_load()
                names = detail_page.get_contacts_names()
                if not names:
                    print("WARN: Please add m005_contacts in %s." % teams[0])
                for name in names:
                    detail_page.select_one_linkman(name)
                    time.sleep(0.5)
                    if detail_page.is_text_present("确定"):
                        break
                    flag = detail_page.is_toast_exist("该联系人不可选择", timeout=3)
                    if not flag:
                        break
                # 3、点击取消
                time.sleep(3)
                detail_page.click_cancel_forward()
                detail_page.click_back()
            else:
                print("WARN: Please create a team and add m005_contacts.")
            shcp.click_back()
            scp.click_back()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0022(self):
        """标签分组天会话页面，长按文件转发到任意本地通讯录联系人"""
        # 1、在当前群聊天会话页面长按任意文件
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        # 进入到文件选择页面
        if not chat.is_open_more():
            chat.click_more()
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击本地文件，进入到本地文件中
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            time.sleep(1)
            # 2、选择转发，选择一个本地通讯录联系人
            chat.forward_file(".txt")
            scp = SelectContactsPage()
            scp.select_local_contacts()
            slcp = SelectLocalContactsPage()
            # slcp.wait_for_page_load()
            names = slcp.get_contacts_name2()
            if names:
                slcp.select_one_member_by_name(names[0])
                time.sleep(1)
                # 3、点击确定
                slcp.click_sure_forward()
                flag = slcp.is_toast_exist("已转发")
                self.assertTrue(flag)
            else:
                print("WARN: There is no linkman.")
                slcp.click_back()
                scp.click_back()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0023(self):
        """标签分组会话页面，长按文件取消转发到任意本地通讯录联系人"""
        # 1、在当前群聊天会话页面长按任意文件
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        # 进入到文件选择页面
        if not chat.is_open_more():
            chat.click_more()
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击本地文件，进入到本地文件中
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 2、选择转发，选择一个本地通讯录联系人
            chat.forward_file(".txt")
            scp = SelectContactsPage()
            scp.select_local_contacts()
            slcp = SelectLocalContactsPage()
            slcp.wait_for_page_load()
            names = slcp.get_contacts_name2()
            if names:
                slcp.select_one_member_by_name(names[0])
                time.sleep(1)
                # 3、点击取消
                slcp.click_cancel_forward()
            else:
                print("WARN: There is no linkman.")
            slcp.click_back()
            scp.click_back()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0024(self):
        """标签分组会话页面，长按文件进行收藏"""
        # 1、在当前群聊天会话页面长按任意文件
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        # 进入到文件选择页面
        if not chat.is_open_more():
            chat.click_more()
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击本地文件，进入到本地文件中
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 2.收藏文件
            chat.collection_file(".txt")
            flag = chat.is_toast_exist("已收藏", timeout=10)
            self.assertTrue(flag)
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0025(self):
        """标签分组天会话页面，长按文件进行删除"""
        # 1、在当前群聊天会话页面长按任意文件
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        # 进入到文件选择页面
        if not chat.is_open_more():
            chat.click_more()
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击本地文件，进入到本地文件中
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 2.删除文件
            chat.delete_mess(".txt")
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0026(self):
        """标签分组天会话页面，长按自己发送的文件，十分钟内撤回"""
        # 1、在当前群聊天会话页面长按任意文件
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        # 进入到文件选择页面
        if not chat.is_open_more():
            chat.click_more()
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击本地文件，进入到本地文件中
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 2.撤回文件
            chat.recall_mess(".txt")
            time.sleep(1)
            if chat.is_text_present("知道了"):
                chat.click_i_know()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'SLOW')
    def test_msg_label_grouping_0027(self):
        """标签分组天会话页面，长按自己发送的文件，超过十分钟撤回"""
        # 1、在当前群聊天会话页面长按任意文件
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        # 进入到文件选择页面
        if not chat.is_open_more():
            chat.click_more()
        more_page = ChatMorePage()
        more_page.click_file()
        # 点击本地文件，进入到本地文件中
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
        file = local_file.select_file(".txt")
        if file:
            local_file.click_send()
            # 长按自己发送的文件，超过十分钟撤回，没有撤回菜单按钮
            for i in range(122):
                time.sleep(2)
                text = chat.driver.page_source
                del text
                time.sleep(3)
                tmp = chat.driver.current_activity
                del tmp
            chat.press_mess(".txt")
            flag = chat.is_text_present("撤回")
            self.assertFalse(flag)
            # 删除文件，关闭弹框菜单
            chat.click_delete()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0028(self):
        """标签分组会话页面，点击位置，再返回到会话页面"""
        # 1、在当前会话窗口点击位置
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        if not chat.is_open_more():
            chat.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 2、点击左上角的返回按钮
        location_page.click_back()
        chat.click_more()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0029(self):
        """标签分组会话页面，点击位置，默认当前位置直接发送"""
        # 1、在当前会话窗口点击位置
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        if not chat.is_open_more():
            chat.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 2、点击右上角的发送按钮
        location_page.click_send()
        chat.wait_for_page_load()
        chat.click_more()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0030(self):
        """标签分组会话页面，点击位置，选择500米内的其他位置发送"""
        # 1、在当前会话窗口点击位置
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        if not chat.is_open_more():
            chat.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 2、滑动500米内的位置列表，选择其他位置
        location_page.select_other_item()
        # 3、点击右上角的发送按钮
        location_page.click_send()
        chat.wait_for_page_load()
        chat.click_more()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0031(self):
        """标签分组会话页面，点击位置，选择500米内的其他位置后返回到会话窗口"""
        # 1、在当前会话窗口点击位置
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        if not chat.is_open_more():
            chat.click_more()
        more_page = ChatMorePage()
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 2、滑动500米内的位置列表，选择其他位置
        location_page.select_other_item()
        # 3、点击左上角的返回按钮
        location_page.click_back()
        chat.wait_for_page_load()
        chat.click_more()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0032(self):
        """标签分组会话页面，长按位置消息体进行转发到本地通讯录联系人"""
        # 1、长按位置消息体
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        info = "Hello"
        chat.input_message(info)
        chat.send_message()
        # 2、选择转发，选择一个本地通讯录联系人
        chat.forward_file(info)
        scp = SelectContactsPage()
        scp.select_local_contacts()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = slcp.get_contacts_name2()
        if names:
            slcp.select_one_member_by_name(names[0])
            time.sleep(1)
            # 3、点击确定
            slcp.click_sure_forward()
            flag = slcp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            print("WARN: There is no linkman.")
            slcp.click_back()
            scp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0033(self):
        """标签分组会话页面，长按位置消息体进行转发到和通讯录联系人"""
        # 1、在当前群聊天会话页面长按长按位置消息体
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        info = "Hello"
        chat.input_message(info)
        chat.send_message()
        # 2、选择一个和通讯录联系人转发
        chat.forward_file(info)
        scp = SelectContactsPage()
        scp.click_he_contacts()
        shcp = SelectHeContactsPage()
        shcp.wait_for_page_load()
        teams = shcp.get_team_names()
        if teams:
            # shcp.select_one_team_by_name(teams[0])
            sog = SelectOneGroupPage()
            sog.selecting_one_group_by_name2("ateam7272")
            time.sleep(2)
            detail_page = SelectHeContactsDetailPage()
            # detail_page.wait_for_page_load()
            names = detail_page.get_contacts_names()
            if not names:
                raise AssertionError("Please add linkman in HeContacts %s." % teams[0])
            for name in names:
                detail_page.select_one_linkman(name)
                time.sleep(0.5)
                if detail_page.is_text_present("确定"):
                    break
                flag = detail_page.is_toast_exist("该联系人不可选择", timeout=3)
                if not flag:
                    break
            # 3、点击确定
            detail_page.click_sure_forward()
            flag2 = detail_page.is_toast_exist("已转发")
            self.assertTrue(flag2)
        else:
            raise AssertionError("WARN: Please create a team and add m005_contacts.")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0034(self):
        """标签分组会话页面，长按位置消息体进行转发到群"""
        # 1、在当前群聊天会话页面长按位置消息体
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        info = "Hello"
        chat.input_message(info)
        chat.send_message()
        # 2、选择一个群转发
        chat.forward_file(info)
        scp = SelectContactsPage()
        scp.click_select_one_group()
        sogp = SelectOneGroupPage()
        sogp.wait_for_page_load()
        names = sogp.get_group_name()
        if names:
            sogp.select_one_group_by_name(names[0])
            # 3、点击确定
            sogp.click_sure_forward()
            flag = sogp.is_toast_exist("已转发")
            self.assertTrue(flag)
        else:
            raise AssertionError("WARN: There is no group.")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_msg_label_grouping_0035(self):
        """标签分组会话页面点击位置消息体，在位置界面点击右下角按钮进行导航"""
        # 1、在当前页面点击位置消息体
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        # 点击更多
        if not chat.is_open_more():
            chat.click_more()
        more_page = ChatMorePage()
        # 点击位置
        more_page.click_location()
        location_page = ChatLocationPage()
        location_page.wait_for_page_load()
        # 点击发送
        location_page.click_send()
        chat.wait_for_page_load()
        # 再一次点击，关闭更多
        chat.click_more()
        chat.wait_for_page_load()
        # 点击位置消息体
        chat.click_addr_info()
        # 2、点击右下角按钮
        chat.click_nav_btn()
        toast_flag = chat.is_toast_exist("未发现手机导航应用", timeout=3)
        map_flag = chat.is_text_present("地图")
        self.assertTrue(toast_flag or map_flag)
        chat.driver.back()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0066(self):
        """标签分组会话窗，不勾选相册内图片点击发送按钮"""
        # 1、在标签分组会话窗，点击输入框左上方的相册图标
        chat = LabelGroupingChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.不选择照片，直接点击发送按钮
        flag = cpg.send_btn_is_enabled()
        if flag:
            raise AssertionError("未选择照片时，发送按钮可点击")
        # 回到聊天回话页面
        cpg.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0067(self):
        """标签分组会话窗，勾选相册内一张图片发送"""
        # 1、在标签分组会话窗，点击输入框左上方的相册图标
        chat = LabelGroupingChatPage()
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，点击发送按钮
        cpg.select_pic()
        cpg.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0068(self):
        """标签分组会话窗，预览相册内图片"""
        # 1、在标签分组会话窗，点击输入框左上方的相册图标
        chat = LabelGroupingChatPage()
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，点击左下角的预览按钮
        cpg.select_pic()
        cpg.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        cppp.click_back()
        cpg.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0069(self):
        """标签分组会话窗，预览相册内图片，不勾选原图发送"""
        # 1、在标签分组会话窗，点击输入框左上方的相册图标
        chat = LabelGroupingChatPage()
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，点击左下角的预览按钮
        cpg.select_pic()
        cpg.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        # 3.直接点击发送按钮
        cppp.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0070(self):
        """标签分组会话窗，预览相册数量与发送按钮数量一致"""
        # 1、在标签分组会话窗，点击输入框左上方的相册图标
        chat = LabelGroupingChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2.选择多张照片，点击左下角的预览按钮
        cpp.select_pic(n=4)
        cpp.click_preview()
        pic_preview = ChatPicPreviewPage()
        pic_preview.wait_for_page_load()
        # 3.查看发送按钮数字
        send_num = pic_preview.get_pic_send_num()
        self.assertEqual(send_num, '4')
        pic_preview.click_back()
        cpp.click_back()
        chat.wait_for_page_load()

    @staticmethod
    def public_edit_pic(edit_text="文本编辑"):
        """图片编辑操作"""
        # 1.在标签分组会话窗，点击输入框左上方的相册图标
        chat = LabelGroupingChatPage()
        # 点击图片按钮
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，点击右上角编辑按钮，进行涂鸦、马赛克、文本编辑
        cpg.select_pic()
        cpg.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        cppp.click_edit()
        pic = ChatPicEditPage()
        # 涂鸦
        pic.click_doodle()
        pic.do_doodle()
        # 马赛克
        pic.click_mosaic()
        pic.do_mosaic()
        # 文本编辑
        pic.click_text_edit_btn()
        pic.input_pic_text(edit_text)
        # 完成
        pic.click_save()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0071(self):
        """标签分组会话窗，编辑图片发送"""
        self.public_edit_pic("VideoPic_0071")
        chat = LabelGroupingChatPage()
        pic = ChatPicEditPage()
        # 3.点击保存按钮
        pic.click_save()
        # 4.点击发送
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0072(self):
        """标签分组会话窗，编辑图片不保存发送"""
        self.public_edit_pic("VideoPic_0072")
        chat = LabelGroupingChatPage()
        pic = ChatPicEditPage()
        # 点击发送按钮
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0073(self):
        """标签分组会话窗，编辑图片中途直接发送"""
        self.public_edit_pic("VideoPic_0073")
        chat = LabelGroupingChatPage()
        pic = ChatPicEditPage()
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0074(self):
        """标签分组会话窗，编辑图片保存"""
        self.public_edit_pic("VideoPic_0074")
        chat = LabelGroupingChatPage()
        pic = ChatPicEditPage()
        # 3.点击保存
        pic.click_save()
        flag = pic.is_toast_exist("保存成功")
        if not flag:
            raise AssertionError("保存编辑图片时没有弹出“保存成功”提示")
        # 返回分组会话窗
        pic.click_cancle()
        cppp = ChatPicPreviewPage()
        cppp.click_back()
        cpg = ChatPicPage()
        cpg.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0075(self):
        """标签分组会话窗，取消编辑图片"""
        self.public_edit_pic("VideoPic_0075")
        chat = LabelGroupingChatPage()
        pic = ChatPicEditPage()
        # 3.点击取消按钮
        pic.click_cancle()
        # 返回分组会话窗
        cppp = ChatPicPreviewPage()
        cppp.click_back()
        cpg = ChatPicPage()
        cpg.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0076(self):
        """标签分组会话窗，取消编辑图片，点击发送按钮"""
        self.public_edit_pic("VideoPic_0076")
        chat = LabelGroupingChatPage()
        pic = ChatPicEditPage()
        # 3.点击取消按钮
        pic.click_cancle()
        # 4.点击发送按钮
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0077(self):
        """标签分组会话窗，发送相册内的图片"""
        # 1.在标签分组会话窗，点击输入框左上方的相册图标
        chat = LabelGroupingChatPage()
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择一张照片，直接点击当前选中的图片，放大展示当前图片
        cpg.select_pic()
        cpg.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        preview_info = cppp.get_pic_preview_info()
        if not re.match(r'预览\(\d+/\d+\)', preview_info):
            raise AssertionError("左上角展示的格式不是：预览(当前图片张数/当前相册的总张数)")
        cppp.click_back()
        cpg.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0078(self):
        """标签分组会话窗，预览已选中的图片，隐藏编辑按钮"""
        # 1、在标签分组会话窗，点击输入框左上方的相册图标
        chat = LabelGroupingChatPage()
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2、选择2张照片后，点击左下角的预览按钮
        cpg.select_pic(n=2)
        cpg.click_preview()
        cppp = ChatPicPreviewPage()
        cppp.wait_for_page_load()
        cppp.click_edit()
        # 备注 版本有修改
        flag = cppp.is_toast_exist("仅支持勾选单张图片时进行编辑")
        if flag:
            raise AssertionError("勾选多张图片时编辑按钮没有隐藏,点击‘编辑’按钮无‘仅支持勾选单张图片时进行编辑’提示")
        time.sleep(1)
        cppp.click_back_by_android()
        time.sleep(1)
        cpg.click_back_by_android()
        time.sleep(1)
        cpg.click_back_by_android()
        time.sleep(1)
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0079(self):
        """标签分组会话窗，勾选9张相册内图片发送"""
        # 1.在标签分组会话窗，点击输入框左上方的相册图标
        chat = LabelGroupingChatPage()
        chat.click_pic()
        cpg = ChatPicPage()
        cpg.wait_for_page_load()
        # 2.选择9张图片，点击发送
        cpg.select_pic(n=9)
        cpg.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0080(self):
        """标签分组会话窗，勾选超9张相册内图片发送"""
        # 1.在标签分组会话窗，点击输入框左上方的相册图标
        chat = LabelGroupingChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2.选择超9张图片
        cpp.select_pic(n=10)
        flag = cpp.is_toast_exist("最多只能选择9张照片")
        if not flag:
            raise AssertionError("选择超过9张图片时无‘最多只能选择9张照片’提示")
        cpp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0081(self):
        """标签分组会话窗，同时发送相册中的图片和视屏"""
        # 1、在标签分组会话窗，点击输入框左上方的相册图标
        chat = LabelGroupingChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        # 2、在当前页面选择图片和视频
        cpp.select_pic()
        cpp.select_video()
        flag = cpp.is_toast_exist("不能同时选择照片和视频")
        if not flag:
            raise AssertionError("同时选择照片和视频时无‘不能同时选择照片和视频’提示")
        cpp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0082(self):
        """标签分组会话窗，使用拍照功能并发送照片"""
        # 1、在标签分组会话窗，点击富媒体行拍照图标
        chat = LabelGroupingChatPage()
        chat.click_take_photo()
        # 2、拍摄照片，点击“√”
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        cpp.send_photo()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0083(self):
        """标签分组会话窗，使用拍照功能并发送照片"""
        # 1.在标签分组会话窗，点击富媒体行拍照图标
        chat = LabelGroupingChatPage()
        chat.click_take_photo()
        # 2.拍摄照片，点击编辑图标，编辑该图片
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        cpp.click_edit_pic()
        pic = ChatPicEditPage()
        pic.click_doodle()
        pic.do_doodle()
        # 3.点击"发送"
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0084(self):
        """标签分组会话窗，使用拍照功能拍照之后编辑并保存"""
        # 1、在标签分组会话窗，点击富媒体行拍照图标
        chat = LabelGroupingChatPage()
        chat.click_take_photo()
        # 2、拍摄照片，点击编辑图标，编辑该图片
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        cpp.click_edit_pic()
        pic = ChatPicEditPage()
        pic.click_text_edit_btn()
        pic.input_pic_text(text="VideoPic_0084")
        pic.click_save()
        # 3、点击“保存”
        pic.click_save()
        # 4、点击“发送”
        pic.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0085(self):
        """标签分组会话窗，使用拍照功能拍照编辑图片，再取消编辑并发送"""
        # 1、在标签分组会话窗，点击富媒体行拍照图标
        chat = LabelGroupingChatPage()
        chat.click_take_photo()
        # 2、拍摄照片，点击编辑图标，编辑该图片
        cpp = ChatPhotoPage()
        cpp.wait_for_page_load()
        cpp.take_photo()
        cpp.click_edit_pic()
        pic = ChatPicEditPage()
        pic.click_doodle()
        pic.do_doodle()
        # 3.点击"取消"
        pic.click_cancle()
        # 4.点击“发送”
        cpp.send_photo()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0086(self):
        """标签分组会话窗，打开拍照，立刻返回会话窗口"""
        # 1、在标签分组会话窗，点击富媒体行拍照图标
        chat = LabelGroupingChatPage()
        chat.click_take_photo()
        cpp = ChatPhotoPage()
        cpp.take_photo()
        # 2、点击“∨”
        cpp.send_photo()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0087(self):
        """标签分组会话窗，打开拍照，拍照之后返回会话窗口"""
        # 1、在标签分组会话窗，点击富媒体行拍照图标
        chat = LabelGroupingChatPage()
        chat.click_take_photo()
        # 2、打开照相机，点击“返回图标”
        cpp = ChatPhotoPage()
        cpp.take_photo_back()
        chat.wait_for_page_load()

    @staticmethod
    def public_send_pic():
        """在标签分组会话页面发送一张图片"""
        chat = LabelGroupingChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        cpp.wait_for_page_load()
        cpp.select_pic()
        cpp.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0088(self):
        """标签分组会话窗，转发自己发送的图片给本地联系人"""
        self.public_send_pic()
        # 1、在标签分组会话窗，长按自己发送的图片
        chat = LabelGroupingChatPage()
        # 2、点击转发
        chat.forward_pic()
        # 3、选择任意本地联系人
        scp = SelectContactsPage()
        scp.select_local_contacts()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        # names = slcp.get_contacts_name()
        names = slcp.get_contacts_name2()
        if names:
            slcp.select_one_member_by_name(names[0])
            # 3、点击确定
            slcp.click_sure_forward()
            flag = slcp.is_toast_exist("已转发")
            if not flag:
                raise AssertionError("在标签分组会话页面转发图片时，没有‘已转发’提示")
        else:
            print("WARN: There is no linkman.")
            slcp.click_back_by_android()
            scp.click_back_by_android()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0089(self):
        """标签分组会话窗，转发自己发送的图片给和通讯录联系人"""
        # 1、在标签分组会话窗，长按自己发送的图片
        self.public_send_pic()
        chat = LabelGroupingChatPage()
        # 2、点击转发
        chat.forward_pic()
        # 3、选择任意和通讯录联系人
        scp = SelectContactsPage()
        scp.click_he_contacts()
        shcp = SelectHeContactsPage()
        shcp.wait_for_page_load()
        teams = shcp.get_team_names()
        if teams:
            # ateam7272
            # shcp.select_one_team_by_name("ateam7272")
            sog = SelectOneGroupPage()
            sog.selecting_one_group_by_name2("ateam7272")
            time.sleep(2)
            detail_page = SelectHeContactsDetailPage()
            # detail_page.wait_for_page_load()
            names = detail_page.get_contacts_names()
            if not names:
                print("WARN: Please add m005_contacts in %s." % teams[0])
            for name in names:
                detail_page.select_one_linkman(name)
                time.sleep(0.5)
                if detail_page.is_text_present("确定"):
                    break
                flag = detail_page.is_toast_exist("该联系人不可选择", timeout=3)
                if not flag:
                    break
            # 3、点击确定
            detail_page.click_sure_forward()
            flag2 = detail_page.is_toast_exist("已转发")
            if not flag2:
                raise AssertionError("标签分组会话窗，转发自己发送的图片给和通讯录联系人无‘已转发’提示")
        else:
            raise AssertionError("WARN: Please create a team and add m005_contacts.")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0090(self):
        """标签分组会话窗，转发自己发送的图片给陌生人"""
        # 1、在标签分组会话窗，长按自己发送的图片
        self.public_send_pic()
        chat = LabelGroupingChatPage()
        chat.press_pic()
        # 2、点击转发
        chat.click_forward()
        # 3、选择任意陌生人
        scp = SelectContactsPage()
        times = 600
        while times > 0:
            tel = "147752" + str(random.randint(10000, 99999))
            scp.search(tel)
            # 构造陌生号码发送
            if scp.is_present_unknown_member():
                scp.click_unknown_member()
                scp.click_sure_forward()
                flag = scp.is_toast_exist("已转发", timeout=5)
                if not flag:
                    raise AssertionError("标签分组会话窗，转发自己发送的图片给陌生人无‘已转发’提示")
                chat.wait_for_page_load()
                break
            times = times - 1

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0091(self):
        """标签分组会话窗，删除自己发送的图片"""
        # 1、在标签分组会话窗，长按自己发送的图片
        self.public_send_pic()
        chat = LabelGroupingChatPage()
        chat.press_pic()
        # 2、点击删除
        chat.click_delete()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0092(self):
        """标签分组会话窗，收藏自己发送的照片"""
        # 1、在标签分组会话窗，长按自己发送的图片
        self.public_send_pic()
        chat = LabelGroupingChatPage()
        chat.press_pic()
        # 2.收藏该图片
        chat.click_collection()
        flag = chat.is_toast_exist("已收藏", timeout=6)
        if not flag:
            raise AssertionError("标签分组会话窗，收藏自己发送的照片无‘已收藏’提示")
        # 去我模块中看是否收藏
        chat.click_back_by_android()
        time.sleep(1)
        ldgp = LableGroupDetailPage()
        ldgp.click_back_by_android()
        time.sleep(1)
        label_grouping = LabelGroupingPage()
        label_grouping.click_back_by_android()
        time.sleep(1)
        label_grouping.click_back_by_android()
        time.sleep(1)
        contacts_page = ContactsPage()
        # 点击‘我’
        contacts_page.open_me_page()
        me_page = MePage()
        me_page.click_menu("收藏")
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        have_pic = mcp.have_collection_pic()
        if not have_pic:
            raise AssertionError("在我收藏模块没有收藏图片")
        # 回到标签分组会话窗
        try:
            mcp.click_back()
            me_page.open_contacts_page()
            contacts_page.click_label_grouping()
            label_grouping.wait_for_page_load()
            group_names = label_grouping.get_label_grouping_names()
            label_grouping.select_group(group_names[0])
            lgdp = LableGroupDetailPage()
            lgdp.click_send_group_info()
            chat.wait_for_page_load()
        except:
            pass

    @staticmethod
    def public_send_video():
        """在标签分组会话窗发送视频"""
        chat = LabelGroupingChatPage()
        chat.click_pic()
        chat_pic_page = ChatPicPage()
        chat_pic_page.wait_for_page_load()
        chat_pic_page.select_video()
        chat_pic_page.click_send()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0093(self):
        """标签分组会话窗，转发自己发送的视频给本地联系人"""
        # 1、在标签分组会话窗，长按自己发送的视频
        self.public_send_video()
        chat = LabelGroupingChatPage()
        chat.press_video()
        # 2、点击转发
        chat.click_forward()
        # 3、选择任意本地联系人
        scp = SelectContactsPage()
        scp.select_local_contacts()
        slcp = SelectLocalContactsPage()
        slcp.wait_for_page_load()
        names = slcp.get_contacts_name2()
        if names:
            slcp.select_one_member_by_name(names[0])
            # 3、点击确定
            slcp.click_sure_forward()
            flag = slcp.is_toast_exist("已转发")
            if not flag:
                raise AssertionError("在标签分组会话页面转发视频时，没有‘已转发’提示")
        else:
            print("WARN: There is no local linkman.")
            slcp.click_back()
            scp.click_back()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0094(self):
        """标签分组会话窗，转发自己发送的视频给和通讯录联系人"""
        # 1、在标签分组会话窗，长按自己发送的视频
        self.public_send_video()
        chat = LabelGroupingChatPage()
        chat.press_video()
        # 2、点击转发
        chat.click_forward()
        # 3、选择任意和通讯录联系人
        scp = SelectContactsPage()
        scp.click_he_contacts()
        shcp = SelectHeContactsPage()
        shcp.wait_for_page_load()
        teams = shcp.get_team_names()
        if teams:
            # shcp.select_one_team_by_name(teams[0])
            sog = SelectOneGroupPage()
            sog.selecting_one_group_by_name2("ateam7272")
            time.sleep(2)
            detail = SelectHeContactsDetailPage()
            # detail.wait_for_page_load()
            names = detail.get_contacts_names()
            if not names:
                raise AssertionError("Please add linkman in HeContacts %s." % teams[0])
            for name in names:
                detail.select_one_linkman(name)
                time.sleep(0.5)
                if detail.is_text_present("确定"):
                    break
                flag = detail.is_toast_exist("该联系人不可选择", timeout=3)
                if not flag:
                    break
            # 点击确定
            detail.click_sure_forward()
            if not detail.is_toast_exist("已转发", timeout=8):
                raise AssertionError("标签分组会话窗，转发自己发送的视频给和通讯录联系人时无‘已转发’提示")
        else:
            raise AssertionError("无和通讯录联系人，请创建和通讯录")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0095(self):
        """标签分组会话窗，转发自己发送的视频给陌生人"""
        # 1、在标签分组会话窗，长按自己发送的视频
        self.public_send_video()
        chat = LabelGroupingChatPage()
        chat.press_video()
        # 2、点击转发
        chat.click_forward()
        # 3、选择任意陌生人
        scp = SelectContactsPage()
        scp.wait_for_page_load()
        times = 600
        while times > 0:
            tel = "14775" + str(random.randint(100000, 999999))
            scp.search(tel)
            if scp.is_present_unknown_member():
                scp.click_unknown_member()
                scp.click_sure_forward()
                if not chat.is_toast_exist("已转发", timeout=5):
                    raise AssertionError("在标签分组会话窗，转发自己发送的视频给陌生人时无‘已转发’提示")
                chat.wait_for_page_load()
                break
            times = times - 1

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0096(self):
        """标签分组会话窗，删除自己发送的视频"""
        # 删除会话窗口之前发送的视频消息
        chat = LabelGroupingChatPage()
        current = 0
        while True:
            current += 1
            if current > 20:
                return
            chat.wait_for_page_load()
            if not chat.is_exist_video_msg():
                break
            chat.press_video()
            chat.click_delete()
        # 1、在标签分组会话窗，长按自己发送的视频
        self.public_send_video()
        chat.wait_for_page_load()
        chat.press_video()
        # 2、点击删除
        chat.click_delete()
        chat.wait_for_page_load()
        if chat.is_exist_video_msg():
            raise AssertionError("在标签分组会话窗，删除自己发送的视频失败！")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0097(self):
        """标签分组会话窗，收藏自己发送的视频"""
        # 1、在标签分组会话窗，长按自己发送的视频
        self.public_send_video()
        chat = LabelGroupingChatPage()
        chat.press_video()
        # 2、收藏该视频
        chat.click_collection()
        if not chat.is_toast_exist("已收藏", timeout=5):
            raise AssertionError("在标签分组会话窗，收藏自己发送的视频没有提示‘已收藏’")
        # 在我模块中的收藏可见
        chat.click_back_by_android()
        time.sleep(1)
        ldgp = LableGroupDetailPage()
        ldgp.click_back_by_android()
        time.sleep(1)
        label_group = LabelGroupingPage()
        label_group.click_back_by_android()
        time.sleep(1)
        label_group.click_back_by_android()
        time.sleep(1)
        contacts = ContactsPage()
        contacts.open_me_page()
        me = MePage()
        me.click_menu("收藏")
        mcp = MeCollectionPage()
        mcp.wait_for_page_load()
        if not mcp.have_collection_video():
            raise AssertionError("在标签分组会话窗，收藏自己发送的视频后在‘我’收藏中不可见")
        # 回到标签分组会话窗
        mcp.click_back()
        time.sleep(1)
        me.open_contacts_page()
        time.sleep(1)
        contacts.click_mobile_contacts()
        time.sleep(1)
        contacts.click_label_grouping()
        label_group.wait_for_page_load()
        names = label_group.get_label_grouping_names()
        label_group.select_group(names[0])
        ldgp.click_send_group_info()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0098(self):
        """标签分组会话窗，发送相册内的视频"""
        # 1、在标签分组会话窗，点击输入框左上方的相册图标
        chat = LabelGroupingChatPage()
        chat.click_pic()
        cpp = ChatPicPage()
        # 2、选择一个视屏
        cpp.select_video()
        # 发送按钮可点击
        if not cpp.send_btn_is_enabled():
            raise AssertionError("选择视频后，发送按钮不可点击")
        time_infos = cpp.get_video_times()
        res = re.match(r'\d+:\d+', time_infos[0])
        if not res:
            raise AssertionError("视频显示格式异常，不是‘xx:xx’类型格式！")
        cpp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0099(self):
        """标签分组会话窗，发送相册内一个视频"""
        # 1、在标签分组会话窗，点击输入框左上方的相册图标
        chat = LabelGroupingChatPage()
        chat.click_pic()
        # 2、选中一个视屏，点击发送
        cpp = ChatPicPage()
        cpp.select_video()
        cpp.click_send()
        chat.wait_for_page_load()
        # 发送成功，会话窗口可见可播放
        chat.play_video()
        chat.wait_for_play_video_page_load()
        chat.close_video()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0100(self):
        """标签分组会话窗，发送相册内多个视频"""
        # 1、在标签分组会话窗，点击输入框左上方的相册图标
        chat = LabelGroupingChatPage()
        chat.click_pic()
        # 2、选中多个视屏
        cpp = ChatPicPage()
        cpp.select_video(n=1)
        cpp.select_video(n=2)
        # 提示最多只能选择1个视频
        if not cpp.is_toast_exist("最多只能选择1个视频", timeout=5):
            raise AssertionError("选择多个视频时，无‘最多只能选择1个视频’提示")
        cpp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0101(self):
        """标签分组会话窗，同时发送相册内视频和图片"""
        # 1、在标签分组会话窗，点击输入框左上方的相册图标
        chat = LabelGroupingChatPage()
        chat.click_pic()
        # 2、选中一个视频和一个图片
        cpp = ChatPicPage()
        cpp.select_video()
        cpp.select_pic()
        # toast提示“不能同时选择照片和视频”
        if not cpp.is_toast_exist("不能同时选择照片和视频", timeout=5):
            raise AssertionError("")
        cpp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0102(self):
        """标签分组会话窗，发送视频时预览视频"""
        # 1、在标签分组会话窗，点击输入框左上方的相册图标
        chat = LabelGroupingChatPage()
        chat.click_pic()
        # 2、选中一个视频点击预览
        cpp = ChatPicPage()
        cpp.select_video()
        cpp.click_preview()
        # 可正常预览
        preview = ChatPicPreviewPage()
        preview.wait_for_page_load()
        preview.click_back()
        cpp.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0105(self):
        """标签分组会话窗，验证点击趣图搜搜入口"""
        # 1、进入标签分组会话窗
        chat = LabelGroupingChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        # 2、点击GIF--先点击表情
        gc = GroupChatPage()
        gc.click_expression_button()
        time.sleep(1)
        chat.click_gif()
        # 进入趣图选择页面
        gif.wait_for_page_load(timeout=60)
        gif.close_gif()
        current_mobile().hide_keyboard_if_display()
        chat.wait_for_page_load()

    @staticmethod
    def delete_media_msg():
        """删除标签分组会话窗的图片，gif消息"""
        chat = LabelGroupingChatPage()
        current = 0
        while True:
            current += 1
            if current > 20:
                return
            chat.wait_for_page_load()
            if not chat.is_exist_pic_msg():
                break
            chat.press_pic()
            chat.click_delete()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0106(self):
        """标签分组会话窗，验证点击趣图搜搜入口"""
        self.delete_media_msg()
        # 1、进入标签分组会话窗
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        # 2、点击GIF
        gc = GroupChatPage()
        gc.click_expression_button()
        time.sleep(1)
        chat = LabelGroupingChatPage()
        chat.click_gif()
        # 3、选择表情点击
        gif.wait_for_page_load(timeout=60)
        gif.send_gif()
        time.sleep(1)
        gif.close_gif()
        current_mobile().hide_keyboard_if_display()
        if not chat.is_exist_pic_msg():
            raise AssertionError("发送gif后，在标签分组会话窗无gif")
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0107(self):
        """标签分组会话窗，断网情况下发送表情搜搜"""
        # 1、进入标签分组会话窗
        chat = LabelGroupingChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        current_mobile().set_network_status(0)
        # 2、点击GIF
        gc = GroupChatPage()
        gc.click_expression_button()
        time.sleep(1)
        chat.click_gif()
        # 提示：“网络异常，请重新设置网络”
        if not chat.is_toast_exist("请检查网络设置", timeout=10):
            raise AssertionError("断网情况下点击GIF无 ‘请检查网络设置’提示")

    @staticmethod
    def tearDown_test_Msg_PrivateChat_VideoPic_0107():
        current_mobile().set_network_status(6)

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0108(self):
        """标签分组会话窗，搜索数字关键字选择发送趣图"""
        self.delete_media_msg()
        # 1、点击GIF图标
        chat = LabelGroupingChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gc = GroupChatPage()
        gc.click_expression_button()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、搜索框输入数字
        gif.input_message(1)
        if gif.is_toast_exist("无搜索结果，换个热词试试", timeout=4):
            raise AssertionError("输入数字 1 无gif趣图 ")
        # 3、点击选择表情
        gif.send_gif()
        time.sleep(1)
        gif.input_message("")
        gif.close_gif()
        current_mobile().hide_keyboard_if_display()
        if not chat.is_exist_pic_msg():
            raise AssertionError("发送gif后，在标签分组会话窗无gif")
        chat.wait_for_page_load()

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0109(self):
        """标签分组会话窗，搜索特殊字符关键字发送趣图"""
        self.delete_media_msg()
        # 1、点击GIF图标
        chat = LabelGroupingChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gc = GroupChatPage()
        gc.click_expression_button()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、搜索框输入特殊字符 @ ? ...
        chars = ['@', '?', '...']
        for msg in chars:
            gif.input_message(msg)
            if not gif.is_toast_exist("无搜索结果，换个热词试试", timeout=4):
                # 3、点击选择表情
                gif.send_gif()
                time.sleep(1)
                if not chat.is_exist_pic_msg():
                    raise AssertionError("发送gif后，在标签分组会话窗无gif")
                gif.input_message("")
                gif.close_gif()
                current_mobile().hide_keyboard_if_display()
                chat.wait_for_page_load()
                return
        raise AssertionError("搜索框输入特殊字符" + "、".join(chars) + "无gif搜索结果")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0110(self):
        """标签分组会话窗，搜索无结果的趣图"""
        self.delete_media_msg()
        # 1、点击GIF图标
        chat = LabelGroupingChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gc = GroupChatPage()
        gc.click_expression_button()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、搜索框输入关键字
        chars = ['appium', 'xxxx', 'a', '123456', '*']
        # 提示无搜索结果，换个关键词试试
        for msg in chars:
            gif.input_message(msg)
            if gif.is_toast_exist("无搜索结果，换个热词试试", timeout=4):
                gif.input_message("")
                gif.close_gif()
                current_mobile().hide_keyboard_if_display()
                chat.wait_for_page_load()
                return
        raise AssertionError("搜索框输入关键字" + "、".join(chars) + "有gif搜索结果，请换输入关键字试试")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0111(self):
        """标签分组会话窗，搜索趣图过程中返回至消息列表重新进入"""
        # 1、点击GIF图标
        chat = LabelGroupingChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gc = GroupChatPage()
        gc.click_expression_button()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、搜索框输入关键字匹配到对应结果后点击返回
        chars = ['ok', 'o', '哈哈', 'no', 'yes']
        for msg in chars:
            gif.input_message(msg)
            if not gif.is_toast_exist("无搜索结果，换个热词试试", timeout=4):
                chat.click_back()
                # 3、再次进入该会话页面
                lgdp = LableGroupDetailPage()
                lgdp.click_send_group_info()
                chat.wait_for_page_load()
                if gif.is_gif_exist():
                    raise AssertionError("gif搜索到对应结果后点击返回,再次进入该会话页面时gif存在")
                return
        raise AssertionError("搜索框输入特殊字符" + "、".join(chars) + "无gif搜索结果")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0112(self):
        """标签分组会话窗，趣图发送成功后搜索结果依然保留"""
        self.delete_media_msg()
        # 1、点击GIF图标
        chat = LabelGroupingChatPage()
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gc = GroupChatPage()
        gc.click_expression_button()
        time.sleep(1)
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、搜索框输入关键字匹配到对应结果后点击发送
        chars = ['ok', 'o', '哈哈', 'no', 'yes']
        for msg in chars:
            gif.input_message(msg)
            if not gif.is_toast_exist("无搜索结果，换个热词试试", timeout=4):
                gif.send_gif()
                time.sleep(1)
                if not chat.is_exist_pic_msg():
                    raise AssertionError("发送gif后，在标签分组会话窗无gif")
                if not gif.is_gif_exist():
                    raise AssertionError("gif发送后，gif的搜索内容不存在")
                gif.input_message("")
                gif.close_gif()
                current_mobile().hide_keyboard_if_display()
                chat.wait_for_page_load()
                return
        raise AssertionError("搜索框输入特殊字符" + "、".join(chars) + "无gif搜索结果")

    @tags('ALL', 'SMOKE', 'CMCC', 'label_grouping')
    def test_Msg_PrivateChat_VideoPic_0114(self):
        """标签分组会话窗，关闭GIF搜索框"""
        # 1、点击GIF图标
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()
        gc = GroupChatPage()
        gc.click_expression_button()
        time.sleep(1)
        chat = LabelGroupingChatPage()
        chat.click_gif()
        gif.wait_for_page_load()
        # 2、点击搜索框左方×
        gif.close_gif()
        if gif.is_gif_exist():
            raise AssertionError("点击左方× gif关闭后趣图页面还存在")
        current_mobile().hide_keyboard_if_display()
        chat.wait_for_page_load()

    @staticmethod
    def tearDown_test_Msg_PrivateChat_VideoPic_0114():
        """如果gif存在是打开的，则关闭"""
        gif = ChatGIFPage()
        if gif.is_gif_exist():
            gif.close_gif()


class MsgLabelGroupingTestAll(TestCase):
    """模块：消息-标签分组"""

    @classmethod
    def setUpClass(cls):
        # 备注：脚本中已判断预支文件是否存在
        Preconditions.select_mobile('Android-移动')

    def default_setUp(self):
        """确保每个用例运行前在标签分组会话页面"""
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_label_grouping_chat_page()
            return
        chat = LabelGroupingChatPage()
        if chat.is_on_this_page():
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_label_grouping_chat_page()

    def default_tearDown(self):
        pass

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0001(self):
        """勾选本地文件内任意文件点击发送按钮"""
        # 1、在当前聊天会话页面，点击更多富媒体的文件按钮
        chat = LabelGroupingChatPage()
        chat.wait_for_page_load()
        if not chat.is_open_more():
            chat.click_more()
        # 2、点击本地文件
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.click_preset_file_dir()
        file = local_file.select_file(".xls")
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0002(self):
        """网络异常时勾选本地文件内任意文件点击发送按钮"""
        # 1、在当前聊天会话页面，断开网络，点击更多富媒体的文件按钮
        chat = LabelGroupingChatPage()
        chat.set_network_status(0)
        chat.wait_for_page_load()
        if not chat.is_open_more():
            chat.click_more()
        # 2、点击本地文件
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.click_preset_file_dir()
        file = local_file.select_file(".xls")
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()
        # 5.验证是否有发送失败的标示
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0002():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0003(self):
        """会话页面有文件发送失败时查看消息列表是否有消息发送失败的标识"""
        # 1、在当前聊天会话页面，断开网络，点击更多富媒体的文件按钮
        chat = LabelGroupingChatPage()
        chat.set_network_status(0)
        chat.wait_for_page_load()
        if not chat.is_open_more():
            chat.click_more()
        # 2、点击本地文件
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.click_preset_file_dir()
        file = local_file.select_file(".xls")
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()
        # 5.验证是否有发送失败的标示
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        # 6.返回消息列表是否有重发的标示
        label_name = chat.get_label_name()
        chat.click_back()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        chat.click_back_by_android()
        time.sleep(1)
        mess = MessagePage()
        mess.open_message_page()
        mess.wait_for_page_load()
        mess.click_text(label_name)
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0003():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep.set_network_status(6)

    @tags('ALL', 'CMCC', 'DEBUG_1', 'label_grouping')
    def test_msg_weifenglian_fenzu_0004(self):
        """对发送失败的文件进行重发"""
        # 1、在当前聊天会话页面，断开网络，点击更多富媒体的文件按钮
        chat = LabelGroupingChatPage()
        chat.set_network_status(0)
        chat.wait_for_page_load()
        if not chat.is_open_more():
            chat.click_more()
        # 2、点击本地文件
        more_page = ChatMorePage()
        more_page.click_file()
        csf = ChatSelectFilePage()
        csf.wait_for_page_load()
        csf.click_local_file()
        # 3、选择任意文件，点击发送按钮
        local_file = ChatSelectLocalFilePage()
        # 进入预置文件目录，选择文件发送
        local_file.click_preset_file_dir()
        file = local_file.select_file(".xls")
        if file:
            local_file.click_send()
        else:
            local_file.click_back()
            local_file.click_back()
            csf.click_back()
        chat.wait_for_page_load()
        # 5.验证是否有发送失败的标示
        cwp = ChatWindowPage()
        cwp.wait_for_msg_send_status_become_to('发送失败', 10)
        # 6.对发送失败的文件进行重发

    @staticmethod
    def tearDown_test_msg_weifenglian_fenzu_0004():
        try:
            mep = MePage()
            mep.set_network_status(6)
        except:
            mep.set_network_status(6)
