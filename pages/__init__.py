__all__ = [
    'SearchPage',

    'ContactDetailsPage',
    'NewContactPage',
    'GuidePage',
    'PermissionListPage',
    'AgreementDetailPage',
    'AgreementPage',
    'OneKeyLoginPage',
    'SmsLoginPage',
    'MePage',
    'MeSetCallPage',
    'MeSetContactsManagerPage',
    'MeSetDialPage',
    'MeSetDialWayPage',
    'MeSetFontSizePage',
    'MeSetFuHaoPage',
    'MeSetImprovePlanPage',
    'MeSetMultiLanguagePage',
    'SetMessageNoticePage',
    'SettingPage',
    'MeSetUpPage',
    'MeSmsSetPage',
    'MessagePage',
    'GroupChatSetPage',
    'GroupChatSetManagerPage',
    'GroupChatSetModifyMyCardPage',
    'GroupChatSetSeeMembersPage',
    'GroupChatSetSeeQRCodePage',
    'GroupNamePage',
]

from .Search import SearchPage
from .contacts import ContactDetailsPage
from .contacts import NewContactPage
from .groupset import GroupChatSetManagerPage
from .groupset import GroupChatSetModifyMyCardPage
from .groupset import GroupChatSetPage
from .groupset import GroupChatSetSeeMembersPage
from .groupset import GroupChatSetSeeQRCodePage
from .groupset import GroupNamePage
from .guide import GuidePage
from .guide import PermissionListPage
from .login import AgreementDetailPage
from .login import AgreementPage
from .login import OneKeyLoginPage
from .login import SmsLoginPage
from .me import MePage
from .me import MeSetCallPage
from .me import MeSetContactsManagerPage
from .me import MeSetDialPage
from .me import MeSetDialWayPage
from .me import MeSetFontSizePage
from .me import MeSetFuHaoPage
from .me import MeSetImprovePlanPage
from .me import MeSetMultiLanguagePage
from .me import MeSetUpPage
from .me import MeSmsSetPage
from .me import SetMessageNoticePage
from .me import SettingPage
from .message import MessagePage
