from aiogram.filters import Filter
import os


class OwnerCheck(Filter):
    async def __call__(self, message):
        return message.business_connection_id == os.getenv('BUSINESS-CONNECTION-ID')


class OwnerMessageCheck(Filter):
    async def __call__(self, message):
        return message.from_user.id == int(os.getenv('OWNER-ID'))
