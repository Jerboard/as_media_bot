from enum import Enum


class UserButton(str, Enum):
    MAIN = '📞 Отправить контакт'


group_user = {
    'wo_phone': 'Гости',
    'with_phone': 'С контактом',
}