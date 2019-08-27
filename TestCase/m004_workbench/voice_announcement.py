import unittest

from pages.workbench.manager_console.WorkbenchManagerPage import WorkBenchManagerPage
from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
from pages.workbench.voice_notice.VoiceNotice import VoiceNoticePage
from preconditions.BasePreconditions import WorkbenchPreconditions
from library.core.TestCase import TestCase
from library.core.utils.testcasefilter import tags
from library.core.utils.applicationcache import current_mobile
from pages import *
import time

from pages.workbench.create_team.CreateTeam import CreateTeamPage
from library.core.utils.applicationcache import current_mobile, current_driver, switch_to_mobile
from TestCase.m001_login.login import *


class Preconditions(WorkbenchPreconditions):
    """前置条件"""
    pass


class VoiceAnnouncementTest(TestCase):
    """工作台->语音通知"""

    @classmethod
    def setUpClass(cls):
        pass

    def default_setUp(self):
        """进入语音通知页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_voice_announcement_page()
            return
        workbench = WorkbenchPage()
        if workbench.is_on_this_page():
            workbench.open_message_page()
            Preconditions.enter_voice_announcement_page()
            return
        vnp = VoiceNoticePage()
        if vnp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_voice_announcement_page()

    def default_tearDown(self):
        pass

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0001(self):
        """网络正常情况下正常跳转到应用首页"""
        # 1、点击【语音通知】
        # 2、查看跳转页面
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0002(self):
        """网络异常情况下提示页面"""
        # 1、断开网络
        # 2、点击【语音通知】
        # 3、查看跳转页面
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        current_mobile().back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.set_network_status(0)
        time.sleep(8)
        workbench.click_voice_notice()
        time.sleep(2)
        if not vnp.is_text_present("网络出错，轻触屏幕重新加载"):
            raise AssertionError("没有出现‘网络出错，轻触屏幕重新加载’")
        vnp.click_text("网络出错，轻触屏幕重新加载")
        if not vnp.is_toast_exist("网络不可用，请检查网络设置"):
            raise AssertionError("没有出现‘网络不可用，请检查网络设置’toast提示")
        time.sleep(2)
        current_mobile().back()

    def tearDown_test_YYTZ_0002(self):
        # 重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)
        time.sleep(8)

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0003(self):
        """剩余条数显示正确"""
        # 1、查看本月剩余通知条数
        # 2、发送一条语音通知，选择1个成员
        # 3、查看本月剩余通知条数权益是否正常减去已发送的数量
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        time.sleep(3)
        if vnp.is_text_present("本月剩余通知 50 条"):
            #创建语音通知
            vnp.click_text("创建语音通知")
            time.sleep(2)
            vnp.input_notice_text("哈哈")
            time.sleep(2)
            vnp.click_add()
            sc = SelectContactsPage()
            sc.click_local_contacts()
            sc.click_one_contact("飞信电话")
            time.sleep(2)
            sc.click_sure_bottom()
            time.sleep(2)
            vnp.click_send()
            vnp = VoiceNoticePage()
            vnp.wait_for_page_loads()
            time.sleep(5)
            if not vnp.is_text_present("本月剩余通知 49 条"):
                raise AssertionError("剩余条数无法正常减1")
        else:
            print("已创建通知")

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0005(self):
        """正常展开收起权益"""
        # 1、点击本月剩余通知条数旁边的下三角
        # 2、点击展开页面的上三角
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_text("本月剩余通知")
        time.sleep(2)
        if not vnp.is_text_present("企业认证"):
            raise AssertionError("不可正常展开")
        vnp.click_element_("上三角")
        time.sleep(2)
        if vnp.is_text_present("企业认证"):
            raise AssertionError("不可正常收起")

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0006(self):
        """跳转企业认证"""
        # 1、点击本月剩余通知条数旁边的下三角
        # 2、点击“企业认证”
        # 3、点击“马上去认证”
        # 4、点击复制地址
        # 5、点击【x】
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_text("本月剩余通知")
        time.sleep(2)
        vnp.click_text("企业认证")
        time.sleep(3)
        if not vnp.is_text_present("马上去认证"):
            raise AssertionError("不可正常进入企业认证详情页")
        vnp.click_text("马上去认证")
        time.sleep(2)
        if not vnp.is_text_present("如何申请认证"):
            raise AssertionError("没有弹出‘如何申请认证’弹窗")
        vnp.click_text("复制地址")
        if not vnp.is_toast_exist("复制成功"):
            raise AssertionError("没有弹出复制成功toast提示")
        time.sleep(3)
        vnp.click_text("马上去认证")
        time.sleep(2)
        vnp.click_element_("如何申请认证X号")
        time.sleep(1)
        if vnp.is_text_present("如何申请认证"):
            raise AssertionError("不可关闭弹窗")
        current_mobile().back()
        vnp.wait_for_page_loads()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0007(self):
        """可正常跳转到充值页面"""
        # 1、点击本月剩余通知条数旁边的下三角
        # 2、点击“充值”
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_text("本月剩余通知")
        time.sleep(2)
        vnp.click_text("充值")
        time.sleep(5)
        if not vnp.is_text_present("和飞信套餐"):
            raise AssertionError("不可正常跳转到充值页面")
        current_mobile().back()
        vnp.wait_for_page_loads()
        time.sleep(3)

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0008(self):
        """添加搜索出的成员"""
        # 1、点击“+”
        # 2、搜索关键词
        # 3、点击搜索结果中的成员
        # 4、点击“确定”
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        time.sleep(2)
        vnp.click_text("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.input_search_keyword("飞信")
        time.sleep(3)
        vnp.click_text("飞信电话")
        time.sleep(2)
        sc.click_sure_bottom()
        time.sleep(2)
        if not vnp.is_text_present("飞信电话"):
            raise AssertionError("成员列表不能显示已勾选成员信息")
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0009(self):
        """多个部门成员累加"""
        # 1、点击“+”
        # 2、进入多个部门勾选成员
        # 3、点击“确定”
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        time.sleep(2)
        sc = SelectContactsPage()
        sc.click_text("选择企业通讯录联系人")
        time.sleep(5)
        if sc.swipe_and_find_element("bm1"):
            time.sleep(2)
            sc.click_element_("bm1")
            time.sleep(2)
            aa = sc.get_firm_contacts_name_list()
            sc.click_text(aa[0])
            current_mobile().back()
            sc.click_element_("bm2")
            time.sleep(2)
            sc.click_text(aa[1])
            if not sc.is_text_present("2/1000"):
                raise AssertionError("部门人数不可以叠加")
            sc.click_text("2/1000")
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().launch_app()
            mess=MessagePage()
            mess.wait_for_page_load()
            mess.open_workbench_page()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_message_page()
            Preconditions.create_sub_department("bm1")
            Preconditions.create_sub_department("bm2")
            workbench.open_workbench_page()
            time.sleep(2)
            if workbench.is_on_welcome_page():
                workbench.click_now_create_team()
            else:
                a = 0
                while a < 10:
                    workbench.wait_for_page_load()
                    workbench.click_voice_notice()
                    time.sleep(5)
                    if workbench.is_text_present("认证失败"):
                        current_mobile().back()
                        a += 1
                    else:
                        break
            vnp = VoiceNoticePage()
            vnp.wait_for_page_loads()
            vnp.click_element_("创建语音通知")
            time.sleep(2)
            vnp.click_add()
            time.sleep(2)
            sc = SelectContactsPage()
            sc.click_text("选择企业通讯录联系人")
            time.sleep(2)
            sc.click_text("bm1")
            time.sleep(2)
            aa = sc.get_firm_contacts_name_list()
            sc.click_text(aa[0])
            current_mobile().back()
            sc.click_text("bm2")
            time.sleep(2)
            sc.click_text(aa[1])
            if not sc.is_text_present("2/1000"):
                raise AssertionError("部门人数不可以叠加")
            sc.click_text("2/1000")
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0010(self):
        """移除成员"""
        # 1、点击“+”
        # 2、选择多个成员
        # 3、部门下已选择成员，再次点击图像取消勾选
        # 4、在顶部栏已选择成员信息点击成员图像移除成员
        # 5、点击“确定”
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        time.sleep(2)
        sc = SelectContactsPage()
        sc.click_text("选择企业通讯录联系人")
        time.sleep(2)
        if not sc.swipe_and_find_element("bm0"):
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_message_page()
            Preconditions.create_sub_department("bm0")
            workbench.open_workbench_page()
            time.sleep(2)
            if workbench.is_on_welcome_page():
                workbench.click_now_create_team()
            else:
                a = 0
                while a < 10:
                    workbench.wait_for_page_load()
                    workbench.click_voice_notice()
                    time.sleep(5)
                    if workbench.is_text_present("认证失败"):
                        current_mobile().back()
                        a += 1
                    else:
                        break
            vnp = VoiceNoticePage()
            vnp.wait_for_page_loads()
            vnp.click_element_("创建语音通知")
            time.sleep(2)
            vnp.click_add()
            time.sleep(2)
            sc = SelectContactsPage()
            sc.click_text("选择企业通讯录联系人")
            time.sleep(2)
            sc.click_one_contact("bm0")
            aa = sc.get_firm_contacts_name_list()
            sc.click_text(aa[0])
            time.sleep(2)
            sc.click_text(aa[0])
            time.sleep(2)
            if sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("再次点击图像不可成功取消")
            sc.click_text(aa[0])
            time.sleep(2)
            sc.click_element_("搜索框左边选中联系人")
            time.sleep(2)
            if sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("在顶部栏点击图像不可成功取消")
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            sc.click_one_contact("bm0")
            aa = sc.get_firm_contacts_name_list()
            sc.click_text(aa[0])
            time.sleep(2)
            sc.click_text(aa[0])
            time.sleep(2)
            if sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("再次点击图像不可成功取消")
            sc.click_text(aa[0])
            time.sleep(2)
            sc.click_element_("搜索框左边选中联系人")
            time.sleep(2)
            if sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("在顶部栏点击图像不可成功取消")
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0011(self):
        """移除成员再添加成员"""
        # 1、点击“+”
        # 2、选择多个成员
        # 3、部门下已选择成员，再次点击图像取消勾选
        # 4、在顶部栏已选择成员信息点击成员图像移除成员
        # 5、再添加其他成员
        # 6、点击“确定”
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        time.sleep(2)
        sc = SelectContactsPage()
        sc.click_text("选择企业通讯录联系人")
        time.sleep(2)
        if not sc.swipe_and_find_element("bm0"):
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_message_page()
            Preconditions.create_sub_department("bm0")
            workbench.open_workbench_page()
            time.sleep(2)
            if workbench.is_on_welcome_page():
                workbench.click_now_create_team()
            else:
                a = 0
                while a < 10:
                    workbench.wait_for_page_load()
                    workbench.click_voice_notice()
                    time.sleep(5)
                    if workbench.is_text_present("认证失败"):
                        current_mobile().back()
                        a += 1
                    else:
                        break
            vnp = VoiceNoticePage()
            vnp.wait_for_page_loads()
            vnp.click_element_("创建语音通知")
            time.sleep(2)
            vnp.click_add()
            time.sleep(2)
            sc = SelectContactsPage()
            sc.click_text("选择企业通讯录联系人")
            time.sleep(2)
            sc.click_one_contact("bm0")
            aa = sc.get_firm_contacts_name_list()
            sc.click_text(aa[0])
            time.sleep(2)
            sc.click_text(aa[0])
            time.sleep(2)
            if sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("再次点击图像不可成功取消")
            sc.click_text(aa[0])
            time.sleep(2)
            sc.click_element_("搜索框左边选中联系人")
            time.sleep(2)
            if sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("在顶部栏点击图像不可成功取消")
            sc.click_text(aa[1])
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选择")
            sc.click_text("确定")
            time.sleep(2)
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            sc.click_one_contact("bm0")
            aa = sc.get_firm_contacts_name_list()
            sc.click_text(aa[0])
            time.sleep(2)
            sc.click_text(aa[0])
            time.sleep(2)
            if sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("再次点击图像不可成功取消")
            sc.click_text(aa[0])
            time.sleep(2)
            sc.click_element_("搜索框左边选中联系人")
            time.sleep(2)
            if sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("在顶部栏点击图像不可成功取消")
            sc.click_text(aa[1])
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选择")
            sc.click_text("确定")
            time.sleep(2)
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()



    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0012(self):
        """无号码或自己等于100，成员等于20的时候成员不可勾选"""
        # 1、点击“+”
        # 2、选择无号码或自己等级 = 100
        # 时，成员等级等于20的用户
        # 3、点击“确定”
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        time.sleep(2)
        vnp.click_text("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        sc.click_one_contact(phone_number)
        if not vnp.is_toast_exist("该联系人不可选择"):
            raise AssertionError("没有提示“该联系人不可选”")
        current_mobile().back()
        current_mobile().back()
        current_mobile().back()
        vnp.wait_for_page_loads()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0014(self):
        """语音时长小于1s"""
        # 1、点击“创建语音通知”
        # 2、点击话筒icon录制语音
        # 3、按住话筒录制小于1s语音就松手
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        time.sleep(2)
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_element_("语音按钮")
        time.sleep(2)
        vnp.click_element_("语音话筒按钮")
        if vnp.is_text_present("始终允许"):
            vnp.click_text("始终允许")
            time.sleep(2)
            vnp.click_element_("语音话筒按钮")
        if not vnp.is_toast_exist("时间太短"):
            raise AssertionError("没有提示时间太短")
        current_mobile().back()
        current_mobile().back()
        vnp.wait_for_page_loads()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0015(self):
        """录制语音时长为59s"""
        # 1、点击“创建语音通知”
        # 2、点击话筒icon录制语音
        # 3、按住话筒录制59s语音就松手
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        time.sleep(2)
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_element_("语音按钮")
        time.sleep(2)
        vnp.press_element_("语音话筒按钮", 59000)
        time.sleep(2)
        if not vnp.is_text_present('59"'):
            raise AssertionError("没有显示时长")
        if not vnp.is_element_exit("已录制的语音"):
            raise AssertionError("不存在已录制的语音")
        if not vnp.is_element_exit("已录制语音删除按钮"):
            raise AssertionError("不存在已录制语音删除按钮")
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0016(self):
        """录制语音时长为60s"""
        # 1、点击“创建语音通知”
        # 2、点击话筒icon录制语音
        # 3、按住话筒录制为60s语音就松手
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        time.sleep(2)
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_element_("语音按钮")
        time.sleep(2)
        vnp.press_element_("语音话筒按钮", 60000)
        time.sleep(2)
        if not vnp.is_text_present('60"'):
            raise AssertionError("没有显示时长")
        if not vnp.is_element_exit("已录制的语音"):
            raise AssertionError("不存在已录制的语音")
        if not vnp.is_element_exit("已录制语音删除按钮"):
            raise AssertionError("不存在已录制语音删除按钮")
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0017(self):
        """录制语音时长大于60s"""
        # 1、点击“创建语音通知”
        # 2、点击话筒icon录制语音
        # 3、按住话筒录制大于60s语音就松手
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        time.sleep(2)
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_element_("语音按钮")
        time.sleep(2)
        vnp.press_element_("语音话筒按钮", 63000)
        time.sleep(2)
        if not vnp.is_text_present('60"'):
            raise AssertionError("没有显示时长")
        if not vnp.is_element_exit("已录制的语音"):
            raise AssertionError("不存在已录制的语音")
        if not vnp.is_element_exit("已录制语音删除按钮"):
            raise AssertionError("不存在已录制语音删除按钮")
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0020(self):
        """录制后点击录音后边的删除按钮"""
        # 1、点击“创建语音通知”
        # 2、点击话筒icon录制语音
        # 3、录制成功之后，点击录音后边的删除按钮
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        time.sleep(2)
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_element_("语音按钮")
        time.sleep(2)
        vnp.press_element_("语音话筒按钮", 3000)
        time.sleep(2)
        vnp.click_element_("已录制语音删除按钮")
        time.sleep(2)
        if not vnp.is_text_present("点击此处录入语音"):
            raise AssertionError("录制内容删除不成功")
        if not vnp.is_text_present("创建语音通知"):
            raise AssertionError("不在当前页面")
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0021(self):
        """录制后点击小键盘，切换到输入模式"""
        # 1、点击“创建语音通知”
        # 2、点击话筒icon录制语音
        # 3、录制成功之后，点击录音右下角的小键盘icon
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        time.sleep(2)
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_element_("语音按钮")
        time.sleep(2)
        vnp.press_element_("语音话筒按钮", 3000)
        time.sleep(2)
        vnp.click_element_("键盘")
        time.sleep(2)
        if not vnp.is_text_present("请输入通知内容"):
            raise AssertionError("切换到输入模式失败")
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0024(self):
        """成功创建一条语音通知，输入内容，设置定时，添加按键反馈"""
        # 1、点击“创建语音通知”
        # 2、输入通知内容
        # 3、添加接收人
        # 4、设置定时时间，设置反馈按键信息
        # 5、点击“发送”
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_element_("语音按钮")
        time.sleep(2)
        vnp.press_element_("语音话筒按钮", 2000)
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        sc.click_one_contact("飞信电话")
        time.sleep(2)
        sc.click_sure_bottom()
        time.sleep(2)
        vnp.click_send()
        vnp.wait_for_page_loads()

    # @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    # def test_YYTZ_0025(self):
    #     """删除发送成功的语音通知"""
    #     # 1、点击一条发送成功的语音通知
    #     # 2、点击“更多”-“删除”
    #     # 3、点击“确定”
    #     vnp = VoiceNoticePage()
    #     vnp.wait_for_page_loads()
    #     time.sleep(2)
    #     vnp.click_element_("创建通知语音")
    #     time.sleep(2)
    #     vnp.click_text("更多")
    #     time.sleep(1)
    #     vnp.click_text("删除")
    #     time.sleep(2)
    #     vnp.click_text("确定")
    #     vnp.wait_for_page_loads()
    #     time.sleep(2)
    #     if vnp.is_text_present('2"'):
    #         raise AssertionError("我创建的列表中被删除的通知信息没有被移除")

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0029(self):
        """用户不在任何部门下"""
        # 1.点击“+”添加联系人
        # 2.点击返回或者面包屑中的企业通讯录
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        time.sleep(2)
        vnp.click_text("企业通讯录")
        time.sleep(2)
        # if not vnp.is_text_present("当前组织"):
        #     raise AssertionError("没有跳转到企业层级")
        current_mobile().back()
        current_mobile().back()
        current_mobile().back()
        # current_mobile().back()
        vnp.wait_for_page_loads()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0033(self):
        """选择用户本人"""
        # 1、点击用户本人头像
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        sc.click_one_contact(phone_number)
        if not vnp.is_toast_exist("该联系人不可选择"):
            raise AssertionError("没有该联系人不可选择提示")
        current_mobile().back()
        current_mobile().back()
        time.sleep(2)
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0035(self):
        """搜索不存在的用户昵称"""
        # 1、搜索不存在的用户名称
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.input_search_keyword("哟哟哟")
        time.sleep(2)
        if sc.is_element_present_by_locator("联系人横框"):
            raise AssertionError("搜索结果有误")
        current_mobile().back()
        current_mobile().back()
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0036(self):
        """搜索“我的电脑”"""
        # 1、搜索“我的电脑”
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.input_search_keyword("我的电脑")
        time.sleep(2)
        if sc.is_element_present_by_locator("联系人横框"):
            raise AssertionError("搜索结果有误")
        current_mobile().back()
        current_mobile().back()
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0037(self):
        """11位号码精准搜索"""
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("18920796596"):
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp= ContactsPage()
            cp.create_contacts_if_not_exits("主子","18920796596")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_voice_notice()
            vnp.wait_for_page_loads()
            vnp.click_text("创建语音通知")
            time.sleep(2)
            vnp.click_add()
            sc.input_search_keyword("18920796596")
            time.sleep(2)
            if not sc.is_text_present("主子"):
                raise AssertionError("搜索结果有误")
            sc.click_text("主子")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("18920796596")
            time.sleep(2)
            if not sc.is_text_present("主子"):
                raise AssertionError("搜索结果有误")
            sc.click_text("主子")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0038(self):
        """6-10位数字可支持模糊搜索匹配结果"""
        # 1.在搜索框输入6 - 10位数字, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("18920796596"):
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("主子", "18920796596")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_voice_notice()
            vnp.wait_for_page_loads()
            vnp.click_text("创建语音通知")
            time.sleep(2)
            vnp.click_add()
            sc.input_search_keyword("189207965")
            time.sleep(2)
            if not sc.is_text_present("主子"):
                raise AssertionError("搜索结果有误")
            sc.click_text("主子")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("189207965")
            time.sleep(2)
            if not sc.is_text_present("主子"):
                raise AssertionError("搜索结果有误")
            sc.click_text("主子")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0039(self):
        """联系人姓名（全名）精准搜索"""
        # 1.在搜索框输入联系人姓名（全名）, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("18920796596"):
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("主子", "18920796596")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_voice_notice()
            vnp.wait_for_page_loads()
            vnp.click_text("创建语音通知")
            time.sleep(2)
            vnp.click_add()
            sc.input_search_keyword("主子")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("主子")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0040(self):
        """联系人姓名（非全名）模糊搜索"""
        # 1.在搜索框输入联系人联系人姓名（非全名）, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("18920796596"):
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("主子", "18920796596")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_voice_notice()
            vnp.wait_for_page_loads()
            vnp.click_text("创建语音通知")
            time.sleep(2)
            vnp.click_add()
            sc.input_search_keyword("主")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("主")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0041(self):
        """字母搜索，按照联系人的姓（包含字母）"""
        # 1.在搜索框输入1字母, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("18920796596"):
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("主子", "18920796596")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_voice_notice()
            vnp.wait_for_page_loads()
            vnp.click_text("创建语音通知")
            time.sleep(2)
            vnp.click_add()
            sc.input_search_keyword("z")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("z")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0042(self):
        """字母搜索，按照联系人的姓（包含字母）"""
        # 1.在搜索框输入1字母, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("18920796596"):
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("主子", "18920796596")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_voice_notice()
            vnp.wait_for_page_loads()
            vnp.click_text("创建语音通知")
            time.sleep(2)
            vnp.click_add()
            sc.input_search_keyword("z")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("z")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0043(self):
        """字母搜索可支持多个字母大小写同时匹配"""
        # 1.在搜索框输入多方大小写字母, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("18920796596"):
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("主子", "18920796596")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_voice_notice()
            vnp.wait_for_page_loads()
            vnp.click_text("创建语音通知")
            time.sleep(2)
            vnp.click_add()
            sc.input_search_keyword("Zhu")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("Zhu")
            time.sleep(2)
            if not sc.is_text_present("18920796596"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796596")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0044(self):
        """特殊字符可支持搜索匹配"""
        # 1.在搜索框输入特殊字符, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("属下 &"):
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("属下 &", "18920796566")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_voice_notice()
            vnp.wait_for_page_loads()
            vnp.click_text("创建语音通知")
            time.sleep(2)
            vnp.click_add()
            sc.input_search_keyword("&")
            time.sleep(2)
            if not sc.is_text_present("18920796566"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796566")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("&")
            time.sleep(2)
            if not sc.is_text_present("18920796566"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796566")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0045(self):
        """纯空格键不支持搜索匹配"""
        # 1.在搜索框输入空格，查看显示
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("属下 &"):
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("属下 &", "18920796566")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_voice_notice()
            vnp.wait_for_page_loads()
            vnp.click_text("创建语音通知")
            time.sleep(2)
            vnp.click_add()
            sc.input_search_keyword(" ")
            time.sleep(2)
            if sc.is_text_present("18920796566"):
                raise AssertionError("搜索结果有误")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword(" ")
            time.sleep(2)
            if sc.is_text_present("18920796566"):
                raise AssertionError("搜索结果有误")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0046(self):
        """空格键+文本 可支持匹配"""
        # 1.在搜索框输入空格键 + 文本, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("属下 &"):
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("属下 &", "18920796566")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_voice_notice()
            vnp.wait_for_page_loads()
            vnp.click_text("创建语音通知")
            time.sleep(2)
            vnp.click_add()
            sc.input_search_keyword(" 属下")
            time.sleep(2)
            if not sc.is_text_present("18920796566"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796566")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword(" 属下")
            time.sleep(2)
            if not sc.is_text_present("18920796566"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920796566")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0047(self):
        """搜索框输入，不限制字符，可一键删除，可按输入盘删除键删除"""
        # 1.在搜索框输入长文本
        # 2.在输入框滑动已输入的文字
        # 3.点击键盘删除
        # 4.点击X一键删除
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        time.sleep(2)
        sc = SelectContactsPage()
        mess = "哈" * 30
        sc.input_search_keyword(mess)
        time.sleep(2)
        sc.press_and_move_right()
        time.sleep(2)
        vnp.click_element_("查询文本删除X")
        if not sc.is_text_present("搜索或输入号码"):
            raise AssertionError("输入框没有自动清空")
        current_mobile().back()
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0048(self):
        """搜索本机号码"""
        # 1.在搜索框输入本机号码，查看匹配结果
        # 2.点击本机联系人
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        phone_number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        if not sc.swipe_and_find_element(phone_number):
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("本机", phone_number)
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_voice_notice()
            vnp.wait_for_page_loads()
            vnp.click_text("创建语音通知")
            time.sleep(2)
            vnp.click_add()
            sc.input_search_keyword(phone_number)
            time.sleep(2)
            if not sc.is_text_present("本机"):
                if not sc.is_text_present("aa"):
                    raise AssertionError("搜索结果有误")
                else:
                    sc.click_text("aa")
            else:
                sc.click_text("本机")
            if not sc.is_toast_exist("该联系人不可选择"):
                raise AssertionError("没有toast提示该联系人不可选择")
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword(phone_number)
            time.sleep(2)
            if not sc.is_text_present("本机"):
                if not sc.is_text_present("aa"):
                    raise AssertionError("搜索结果有误")
                else:
                    sc.click_text("aa")
            else:
                sc.click_text("本机")
            if not sc.is_toast_exist("该联系人不可选择"):
                raise AssertionError("没有toast提示该联系人不可选择")
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0050(self):
        """字母+汉字组合可精准搜索"""
        # 1.在搜索框输入：字母 + 汉字, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("a加1"):
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("a加1", "18920798888")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_voice_notice()
            vnp.wait_for_page_loads()
            vnp.click_text("创建语音通知")
            time.sleep(2)
            vnp.click_add()
            sc.input_search_keyword("a加")
            time.sleep(2)
            if not sc.is_text_present("18920798888"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920798888")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("a加")
            time.sleep(2)
            if not sc.is_text_present("18920798888"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920798888")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0051(self):
        """字母+汉字+数字 组合可精准搜索"""
        # 1.在搜索框输入：字母 + 汉字 + 数字, 查看匹配结果
        # 2.点击结果，查看是否可选择成功
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        if not sc.swipe_and_find_element("a加1"):
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_contacts_page()
            if workbench.is_text_present("始终允许"):
                workbench.click_text("始终允许")
            cp = ContactsPage()
            cp.create_contacts_if_not_exits("a加1", "18920798888")
            time.sleep(2)
            cp.open_workbench_page()
            workbench.wait_for_page_load()
            workbench.click_voice_notice()
            vnp.wait_for_page_loads()
            vnp.click_text("创建语音通知")
            time.sleep(2)
            vnp.click_add()
            sc.input_search_keyword("a加1")
            time.sleep(2)
            if not sc.is_text_present("18920798888"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920798888")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            sc.input_search_keyword("a加1")
            time.sleep(2)
            if not sc.is_text_present("18920798888"):
                raise AssertionError("搜索结果有误")
            sc.click_text("18920798888")
            time.sleep(2)
            if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
                raise AssertionError("不可成功选中")
            if not sc.is_text_present("搜索或输入号码"):
                raise AssertionError("输入框没有自动清空")
            if not sc.is_text_present("/1000"):
                raise AssertionError("右上角没有展示已选人数/上限人数")
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0052(self):
        """搜索非企业联系人提示无结果"""
        # 1、搜索不存在在企业通讯录中的用户电话号码，大陆号码11位或8位香港号码
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        time.sleep(2)
        sc = SelectContactsPage()
        sc.click_text("选择企业通讯录联系人")
        time.sleep(2)
        sc.input_search_keyword("12345678")
        time.sleep(3)
        if not sc.is_text_present("无搜索结果"):
            raise AssertionError("没有提示“无搜索结果”")
        current_mobile().back()
        current_mobile().back()
        current_mobile().back()
        current_mobile().back()
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0053(self):
        """任意点击搜索结果联系人"""
        # 1、任意点击头像，选择人员
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        time.sleep(2)
        sc = SelectContactsPage()
        sc.input_search_keyword("12560")
        time.sleep(3)
        if not sc.is_text_present("飞信电话"):
            raise AssertionError("搜索结果有误")
        sc.click_text("012560")
        time.sleep(2)
        if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
            raise AssertionError("不可成功选中")
        if not sc.is_text_present("/1000"):
            raise AssertionError("右上角没有展示已选人数/上限人数")
        current_mobile().back()
        time.sleep(2)
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0054(self):
        """取消选择人员"""
        # 1、再次点击头像，取消选择人员
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        time.sleep(2)
        sc = SelectContactsPage()
        sc.input_search_keyword("12560")
        time.sleep(3)
        if not sc.is_text_present("飞信电话"):
            raise AssertionError("搜索结果有误")
        sc.click_text("012560")
        time.sleep(2)
        if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
            raise AssertionError("不可成功选中")
        if not sc.is_text_present("/1000"):
            raise AssertionError("右上角没有展示已选人数/上限人数")
        sc.input_search_keyword("12560")
        time.sleep(3)
        if not sc.is_text_present("飞信电话"):
            raise AssertionError("搜索结果有误")
        sc.click_text("012560")
        time.sleep(2)
        if sc.is_element_present_by_locator("搜索框左边选中联系人"):
            raise AssertionError("左侧选中联系人没有撤消")
        if sc.is_text_present("/1000"):
            raise AssertionError("右侧已选人员数字没有-1")
        current_mobile().back()
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0055(self):
        """多选-任意选择多位联系人"""
        # 1、任意选择多位联系人
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        time.sleep(2)
        sc = SelectContactsPage()
        sc.click_local_contacts()
        time.sleep(2)
        scp=SelectLocalContactsPage()
        contactNnames = scp.get_contacts_name()
        a=list(contactNnames)
        if len(a) > 1:
            # 选择多个联系人
            scp.select_one_member_by_name(a[0])
            scp.select_one_member_by_name(a[1])
        else:
            raise AssertionError("通讯录联系人数量不足，请添加")
        time.sleep(2)
        if not sc.is_element_present_by_locator("搜索框左边选中联系人"):
            raise AssertionError("不可成功选中")
        if not sc.is_text_present("/1000"):
            raise AssertionError("右上角没有展示已选人数/上限人数")
        current_mobile().back()
        current_mobile().back()
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0056(self):
        """添加多部门联系人"""
        # 1、进入A部门勾选C用户后，返回一级页面在进入B部门勾选其它用户
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_add()
        time.sleep(2)
        sc = SelectContactsPage()
        sc.click_text("选择企业通讯录联系人")
        time.sleep(2)
        if sc.swipe_and_find_element("bm1"):
            time.sleep(2)
            sc.click_text("bm1")
            time.sleep(2)
            aa=sc.get_firm_contacts_name_list()
            sc.click_text(aa[0])
            current_mobile().back()
            sc.click_text("bm2")
            time.sleep(2)
            sc.click_text(aa[1])
            if not sc.is_text_present("2/1000"):
                raise AssertionError("部门人数不可以叠加")
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
        else:
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()
            workbench.open_message_page()
            Preconditions.create_sub_department("bm1")
            Preconditions.create_sub_department("bm2")
            time.sleep(5)
            workbench.open_workbench_page()
            time.sleep(2)
            if workbench.is_on_welcome_page():
                workbench.click_now_create_team()
            else:
                a = 0
                while a < 10:
                    workbench.wait_for_page_load()
                    workbench.click_voice_notice()
                    time.sleep(5)
                    if workbench.is_text_present("认证失败"):
                        current_mobile().back()
                        a += 1
                    else:
                        break
            vnp = VoiceNoticePage()
            vnp.wait_for_page_loads()
            vnp.click_element_("创建语音通知")
            time.sleep(2)
            vnp.click_add()
            time.sleep(2)
            sc = SelectContactsPage()
            sc.click_text("选择企业通讯录联系人")
            time.sleep(2)
            sc.click_one_contact("bm1")
            time.sleep(2)
            aa = sc.get_firm_contacts_name_list()
            sc.click_text(aa[0])
            current_mobile().back()
            sc.click_one_contact("bm2")
            time.sleep(2)
            sc.click_text(aa[1])
            if not sc.is_text_present("2/1000"):
                raise AssertionError("部门人数不可以叠加")
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            current_mobile().back()
            vnp.click_close_more()
            workbench = WorkbenchPage()
            workbench.wait_for_page_load()

    # @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    # def test_YYTZ_0059(self):
    #     """直接添加接收人后再次点击'+'"""
    #     # 1、点击“+”添加接收人
    #     # 2、任意选择2位以上联系人后点击确定
    #     # 3、再次点击”+“添加接收人
    #     # 4、任意选择联系人之后，点击确定
    #     vnp = VoiceNoticePage()
    #     vnp.wait_for_page_loads()
    #     vnp.click_element_("创建语音通知")
    #     time.sleep(2)
    #     vnp.click_add()
    #     time.sleep(2)
    #     sc = SelectContactsPage()
    #     sc.click_local_contacts()
    #     slc = SelectLocalContactsPage()
    #     names = slc.get_contacts_name_list()
    #     time.sleep(2)
    #     sc.click_one_contact(names[0])
    #     sc.click_one_contact(names[1])
    #     sc.click_one_contact(names[2])
    #     time.sleep(2)
    #     sc.click_sure_bottom()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0060(self):
        """无缓存数据-无网络时点击“+”添加接收人"""
        # 1、点击“+”添加联系人
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        vnp.set_network_status(0)
        time.sleep(8)
        vnp.click_add()
        time.sleep(2)
        sc = SelectContactsPage()
        sc.click_text("选择企业通讯录联系人")
        if not vnp.is_toast_exist("网络连接异常"):
            raise AssertionError("没有网络异常提示")
        vnp.set_network_status(6)
        time.sleep(8)
        current_mobile().back()
        current_mobile().back()
        current_mobile().back()
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    def tearDown_test_YYTZ_0060(self):
        vnp = VoiceNoticePage()
        vnp.set_network_status(6)
        time.sleep(8)

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0061(self):
        """有缓存数据-无网络时点击“+”添加接收人"""
        # 1、点击“+”添加联系人
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        vnp.set_network_status(0)
        time.sleep(8)
        vnp.click_add()
        time.sleep(2)
        sc = SelectContactsPage()
        sc.click_text("选择企业通讯录联系人")
        if not vnp.is_toast_exist("网络连接异常"):
            raise AssertionError("没有网络异常提示")
        # if not vnp.is_text_present("企业通讯录"):
        #     raise AssertionError("没有转到企业子一层级")
        vnp.set_network_status(6)
        time.sleep(8)
        current_mobile().back()
        current_mobile().back()
        current_mobile().back()
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    def tearDown_test_YYTZ_0061(self):
        vnp = VoiceNoticePage()
        vnp.set_network_status(6)
        time.sleep(8)

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0062(self):
        """断开网络，点击“发送”"""
        # 1、点击“创建语音通知”
        # 2、添加接收人
        # 3、其他信息正常填写
        # 4、断开网络
        # 5、点击“发送”
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        time.sleep(2)
        # 创建语音通知
        vnp.click_text("创建语音通知")
        time.sleep(2)
        vnp.input_notice_text("哈哈")
        time.sleep(2)
        vnp.click_add()
        sc = SelectContactsPage()
        sc.click_local_contacts()
        sc.click_one_contact("飞信电话")
        time.sleep(2)
        sc.click_sure_bottom()
        time.sleep(2)
        vnp.set_network_status(0)
        time.sleep(8)
        vnp.click_send()
        if not vnp.is_toast_exist("当前网络不可用，请检查连接"):
            raise AssertionError("没有网络异常提示")
        vnp.set_network_status(6)
        time.sleep(8)
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    def tearDown_test_YYTZ_0062(self):
        vnp = VoiceNoticePage()
        vnp.set_network_status(6)
        time.sleep(8)

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0063(self):
        """点击顶部返回键"""
        # 1、在任意页面点击顶部【 < 】
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        # vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'YYTZ')
    def test_YYTZ_0064(self):
        """点击顶部关闭按钮"""
        # 在其他有关闭按钮页面，点击顶部【x】
        vnp = VoiceNoticePage()
        vnp.wait_for_page_loads()
        vnp.click_element_("创建语音通知")
        time.sleep(2)
        vnp.click_close_more()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()