import unittest

from pages.workbench.organization.OrganizationStructure import OrganizationStructurePage
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


class OrganizationTest(TestCase):
    """工作台->组织架构"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile('Android-移动')

    def default_setUp(self):
        """进入组织架构页面"""
        Preconditions.select_mobile('Android-移动')
        mess = MessagePage()
        if mess.is_on_this_page():
            Preconditions.enter_organization_page()
            return
        osp = OrganizationStructurePage()
        if osp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
            return
        else:
            current_mobile().launch_app()
            Preconditions.enter_organization_page()

    def default_tearDown(self):
        pass

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0001(self):
        """工作台管理员权限可看到组织架构入口"""
        #1、进入工作台页面 2、点击组织架构
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        time.sleep(1)
        current_mobile().back()
        mess = MessagePage()
        mess.open_message_page()

    @staticmethod
    def setUp_test_ZZJG_0002():
        Preconditions.select_mobile('Android-移动')
        current_mobile().hide_keyboard_if_display()
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        preconditions.launch_app()
        # current_mobile().reset_app()
        # current_mobile().connect_mobile()
        Preconditions.make_already_in_message_page()

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0002(self):
        """从通讯录中进入组织架构"""
        #1、进入通讯录-和通讯录
        # 2、找到自己是管理员权限的企业通讯录
        # 3、点击右上角【...】
        # 4、点击【团队管理】
        mess = MessagePage()
        mess.wait_for_page_load()
        mess.open_contacts_page()
        contacts = ContactsPage()
        time.sleep(3)
        if ContactsPage().is_text_present('需要使用通讯录权限'):
            ContactsPage().click_allow()
        contacts.wait_for_page_load()
        contacts.click_one_firm2()
        time.sleep(2)
        # contacts.click_one_he_contacts()
        # time.sleep(1)
        contacts.click_he_more()
        time.sleep(2)
        contacts.click_text("团队管理")
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        time.sleep(3)
        current_mobile().back()
        time.sleep(1)
        current_mobile().back()
        time.sleep(1)
        mess.open_message_page()

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0003(self):
        """手动添加联系人"""
        # 1、点击“组织架构”应用
        # 2、点击“添加联系人”
        # 3、点击“手动输入添加”
        # 4、输入姓名：测试号
        # 5、输入主手机：15220089861
        # 6、点击“完成”
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        if not osp.swipe_and_find_element("yyx"):
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("手动输入添加")
            time.sleep(1)
            osp.input_contacts_name("yyx")
            osp.input_contacts_number("18920736596")
            time.sleep(2)
            osp.click_text("完成")
            if not osp.is_toast_exist("成功"):
                raise AssertionError("手动添加失败")
            osp.wait_for_page_load()
        else:
            print("已存在联系人yyx")

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0004(self):
        """手动添加联系人"""
        #1、点击“组织架构”应用
        # 2、点击“添加联系人”
        # 3、点击“手动输入添加”
        # 4、不输入姓名或主手机号码
        # 5、点击“完成”
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        osp.click_text("添加联系人")
        time.sleep(1)
        osp.click_text("手动输入添加")
        time.sleep(1)
        osp.click_text("完成")
        if not osp.is_toast_exist("请输入姓名"):
            raise AssertionError("没有出现toast提示")
        time.sleep(1)
        current_mobile().back()

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0005(self):
        """从手机通讯录添加联系人"""
        # 1、点击“组织架构”应用
        # 2、点击“添加联系人”
        # 3、点击“从手机通讯录添加”
        # 4、选择通讯录中的成员，点击【确定】
        osp = OrganizationStructurePage()
        time.sleep(2)
        osp.wait_for_page_load()
        slc = SelectLocalContactsPage()
        if osp.is_text_present("飞信电话"):
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("从手机通讯录添加")
            time.sleep(2)
            slc.click_one_contact("飞信电话")
            slc.click_sure()
            if not slc.is_toast_exist("1个联系人联系人在库中已存在"):
                print("飞信电话已经加入")
            time.sleep(2)
            if not osp.is_text_present("邀请成员加入团队"):
                raise AssertionError("没有返回上一级")
        else:
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("从手机通讯录添加")
            time.sleep(2)
            slc.click_one_contact("飞信电话")
            slc.click_sure()
            if not slc.is_toast_exist("操作成功"):
                raise AssertionError("操作不成功")
            time.sleep(2)
            if not osp.is_text_present("邀请成员加入团队"):
                raise AssertionError("没有返回上一级")

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0006(self):
        """从手机通讯录添加搜索的联系人"""
        # 1、点击“组织架构”应用
        # 2、点击“添加联系人”
        # 3、点击“从手机通讯录添加”
        # 4、在搜索框输入关键字
        # 5、点击联系人
        # 6、点击【确定】
        osp = OrganizationStructurePage()
        time.sleep(2)
        osp.wait_for_page_load()
        slc = SelectLocalContactsPage()
        if osp.is_text_present("飞信电话"):
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("从手机通讯录添加")
            time.sleep(2)
            sc = SelectContactsPage()
            # 搜索联系人
            sc.input_search_contact_message("飞信")
            # 选择“和飞信电话”联系人进行转发
            sc.click_one_contact("飞信电话")
            # slc.click_one_contact("和飞信电话")
            slc.click_sure()
            if not slc.is_toast_exist("1个联系人已存在"):
                raise AssertionError("操作不成功")
            time.sleep(2)
            if not osp.is_text_present("添加成员加入团队"):
                raise AssertionError("没有返回上一级")
        else:
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("从手机通讯录添加")
            time.sleep(2)
            sc = SelectContactsPage()
            # 搜索联系人
            sc.input_search_contact_message("飞信")
            # 选择“和飞信电话”联系人进行转发
            sc.click_one_contact("飞信电话")
            # slc.click_one_contact("和飞信电话")
            slc.click_sure()
            if not slc.is_toast_exist("操作成功"):
                raise AssertionError("操作不成功")
            time.sleep(2)
            if not osp.is_text_present("邀请成员加入团队"):
                raise AssertionError("没有返回上一级")

    # @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    @unittest.skip("平台已改动，与用例不符")
    def test_ZZJG_0007(self):
        """点击邀请小伙伴正常跳转到邀请成员页面"""
        # 1、点击“组织架构”应用
        # 2、点击“添加联系人”
        # 3、点击“邀请小伙伴”
        # 4、操作页面的各个按钮
        # 5、点返回
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        osp.click_text("添加联系人")
        time.sleep(1)
        osp.click_text("扫描二维码邀请")
        osp.wait_for_invite_page_load()
        osp.click_invite_mode_switch()
        time.sleep(2)
        if not osp.is_text_present("加入企业后仅可见自己"):
            raise AssertionError("访客模式开关不可用")
        time.sleep(2)
        osp.click_invite_save()
        if not osp.is_toast_exist("保存图片成功"):
            raise AssertionError("保存二维码按钮不可用")
        time.sleep(1)
        osp.click_invite_share()
        time.sleep(1)
        if not osp.is_exist_element_by_locatorname("点击右上角即可分享"):
            raise AssertionError("分享按钮不可用")
        current_mobile().back()
        current_mobile().back()
        osp.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0008(self):
        """点击取消，弹窗隐藏"""
        # 1、点击“组织架构”应用
        # 2、点击“添加联系人”
        # 3、点击“取消”
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        osp.click_text("添加联系人")
        time.sleep(1)
        # osp.click_text("取消")
        current_mobile().back()
        time.sleep(2)
        if osp.is_text_present("扫描二维码邀请"):
            raise AssertionError("弹窗隐藏失败")

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0009(self):
        """成功添加一个子部门"""
        # 1、点击“组织架构”应用
        # 2、点击“添加子部门”
        # 3、输入部门名称：“测试部”
        # 4、点击完成
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        osp.click_text("添加子部门")
        osp.wait_for_sub_department_page_load()
        osp.input_sub_department_name("哈哈")
        osp.click_text("完成")
        if osp.is_toast_exist("部门已存在，请勿重复添加"):
            current_mobile().back()
            osp.wait_for_page_load()
        else:
            osp.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0010(self):
        """从部门进入扫码审核"""
        # 1、点击“更多”
        # 2、点击“扫码审核”
        # 3、查看页面
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        osp.click_text("更多")
        time.sleep(1)
        osp.click_text("扫码审核")
        time.sleep(3)
        if not osp.is_text_present("扫码加入企业"):
            raise AssertionError("无法正常跳转到待审核页面")
        current_mobile().back()
        osp.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0011(self):
        """成功批量删除部门中成员信息"""
        # 1、点击“更多”
        # 2、点击“批量删除成员”
        # 3、勾选需要删除的成员
        # 4、点击“确定”
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        osp.click_text("更多")
        time.sleep(1)
        osp.click_text("批量删除成员")
        osp.wait_for_delete_contacts_page_load()
        time.sleep(3)
        els=osp.get_contacts_in_organization()
        if els:
            for el in els:
                el.click()
        else:
            raise AssertionError("当前组织没有成员，请添加")
        time.sleep(1)
        osp.click_text("确定")
        if not osp.is_toast_exist("成功"):
            raise AssertionError("没有删除成功")
        current_mobile().back()
        osp.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0014(self):
        """查看已审核列表"""
        # 1、点击“组织架构”应用
        # 2、点击“更多”
        # 3、点击“扫码审核”，切换到已审核列表
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        osp.click_text("更多")
        time.sleep(1)
        osp.click_text("扫码审核")
        time.sleep(2)
        if not osp.is_text_present("扫码加入企业"):
            raise AssertionError("无法正常跳转到审核页面")
        osp.click_text("已审核")
        time.sleep(2)
        current_mobile().back()
        osp.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0017(self):
        """当前页面无成员"""
        # 1、点击“更多”
        # 2、点击“批量删除成员”
        osp = OrganizationStructurePage()
        osp.wait_for_page_load()
        osp.click_text("更多")
        time.sleep(1)
        osp.click_text("批量删除成员")
        osp.wait_for_delete_contacts_page_load()
        els = osp.get_contacts_in_organization()
        if els:
            print("当前组织有成员")
        current_mobile().back()
        osp.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0018(self):
        """搜索已经存在的成员姓名"""
        # 1、点击“组织架构”应用
        # 2、搜索已存在成员姓名
        osp = OrganizationStructurePage()
        time.sleep(2)
        osp.wait_for_page_load()
        slc = SelectLocalContactsPage()
        if osp.is_text_present("飞信电话"):
            pass
        else:
            osp.click_text("添加联系人")
            time.sleep(1)
            osp.click_text("从手机通讯录添加")
            time.sleep(2)
            sc = SelectContactsPage()
            # 搜索联系人
            sc.input_search_contact_message("飞信")
            # 选择“和飞信电话”联系人进行转发
            sc.click_one_contact("飞信电话")
            # slc.click_one_contact("和飞信电话")
            slc.click_sure()
            if not slc.is_toast_exist("操作成功"):
                raise AssertionError("操作不成功")
            time.sleep(2)
            if not osp.is_on_this_page():
                raise AssertionError("没有返回上一级")
        osp.click_text("搜索")
        osp.input_search_box("飞信")
        time.sleep(2)
        if not osp.is_text_present("飞信电话"):
            raise AssertionError("搜索失败")

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0019(self):
        """搜索已经存在的成员电话（最少输入电话号码前6位）"""
        # 1、点击“组织架构”应用
        # 2、搜索已存在成员电话号码（最少输入电话号码前6位）
        osp = OrganizationStructurePage()
        time.sleep(2)
        osp.wait_for_page_load()
        number = current_mobile().get_cards(CardType.CHINA_MOBILE)[0]
        osp.click_text("搜索")
        osp.input_search_box(number[0:6])
        time.sleep(3)
        if not osp.is_text_present(number):
            raise AssertionError("搜索失败")

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0020(self):
        """搜索不经存在的成员姓名"""
        # 1、点击“组织架构”应用
        # 2、搜索不存在成员姓名
        osp = OrganizationStructurePage()
        time.sleep(2)
        osp.wait_for_page_load()
        osp.click_text("搜索")
        osp.input_search_box("不存在")
        time.sleep(3)
        if not osp.is_text_present("未搜索到相关结果"):
            raise AssertionError("搜索失败")

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0021(self):
        """搜索不存在的成员电话（最少输入电话号码前6位）"""
        # 1、点击“组织架构”应用
        # 2、搜索不存在成员电话号码（最少输入电话号码前6位）
        osp = OrganizationStructurePage()
        time.sleep(2)
        osp.wait_for_page_load()
        osp.click_text("搜索")
        osp.input_search_box("111111")
        time.sleep(3)
        if not osp.is_text_present("未搜索到相关结果"):
            raise AssertionError("搜索失败")

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0022(self):
        """点击顶部返回键，返回到上一级页面"""
        # 1、点击“组织架构”应用
        # 2、点击顶部返回键【 < 】
        osp = OrganizationStructurePage()
        time.sleep(2)
        osp.wait_for_page_load()
        osp.click_back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()

    @tags('ALL', "CMCC", 'workbench', 'ZZJG')
    def test_ZZJG_0023(self):
        """断网提示"""
        # 1、打开客户端
        # 2、进入工作台组织架构”图标
        # 4、断开网络
        # 5、点击其他元素
        osp = OrganizationStructurePage()
        time.sleep(2)
        osp.wait_for_page_load()
        current_mobile().back()
        workbench = WorkbenchPage()
        workbench.wait_for_page_load()
        workbench.set_network_status(0)
        time.sleep(8)
        workbench.click_organization()
        time.sleep(2)
        if not osp.is_text_present("网络出错，轻触屏幕重新加载"):
            raise AssertionError("没有出现‘网络出错，轻触屏幕重新加载’")
        osp.click_text("网络出错，轻触屏幕重新加载")
        if not osp.is_toast_exist("网络不可用，请检查网络设置"):
            raise AssertionError("没有出现‘网络不可用，请检查网络设置’toast提示")
        time.sleep(2)
        current_mobile().back()
        workbench.set_network_status(6)
        time.sleep(8)
        workbench.click_organization()
        time.sleep(2)
        osp.wait_for_page_load()
        workbench.set_network_status(0)
        time.sleep(8)
        osp.click_text("添加联系人")
        time.sleep(1)
        osp.click_text("手动输入添加")
        if not osp.is_toast_exist("无网络，请稍候重试"):
            raise AssertionError("没有‘无网络，请稍候重试’toast提示")

    def tearDown_test_ZZJG_0023(self):
        # 重连网络
        gcp = GroupChatPage()
        gcp.set_network_status(6)
