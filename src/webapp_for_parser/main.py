from aiohttp.web import _run_app
from aiohttp.web_app import Application
from src.webapp_for_parser.routes import \
    (check_data_handler, demo_handler,
     send_form_handler, delete_channel,
     get_channels, channel_handler,
     direction_from_handler, direction_to_handler,
     direction_to_change_the_settings_in_channel,
     get_configs_from_channel, change_the_settings_of_the_channel)
from src.tools_for_tg_bot.bot_for_replies import BotForReplies
from aiogram import Bot
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from src.tools_for_tg_bot.Configs.Config_base_url import BaseURL
import asyncio


TOKEN = '6356385807:AAHWycJ5m7jykCVRcDCWUa3BvFL_oRlou5k'


async def on_startup(bot: Bot, base_url: str):
    await bot.set_webhook(f"{base_url}/webhook")


class WebApp:
    def __init__(self, token: str):
        self.replier_bot = BotForReplies(token)
        self.bot = self.replier_bot.bot
        self.dispatcher = self.replier_bot.dispatcher
        self.app = Application()
        self.main()

    def main(self):
        self.dispatcher["base_url"] = BaseURL.URL
        self.dispatcher.startup.register(on_startup)

        self.app["bot"] = self.bot

        self.app.router.add_get("/main", demo_handler)
        self.app.router.add_get("/channel", channel_handler)
        self.app.router.add_get('/channel/from', direction_from_handler)
        self.app.router.add_get('/channel/to', direction_to_handler)
        self.app.router.add_get('/channel/change_the_settings_in_channel', direction_to_change_the_settings_in_channel)

        self.app.router.add_post("/main/checkData", check_data_handler)
        self.app.router.add_post("/main/sendForm", send_form_handler)
        self.app.router.add_post("/channel/delete_channel", delete_channel)
        self.app.router.add_post("/channel/get_channels", get_channels)
        self.app.router.add_post("/channel/get_configs_of_channel", get_configs_from_channel)
        self.app.router.add_post("/channel/ChangeRequest", change_the_settings_of_the_channel)
        SimpleRequestHandler(
            dispatcher=self.dispatcher,
            bot=self.bot,
        ).register(self.app, path="/webhook")
        setup_application(self.app, self.dispatcher, bot=self.bot)

    async def run_app(self):
        await self.replier_bot.start_pooling()
        await _run_app(self.app, host="127.0.0.1", port=8081)


if __name__ == '__main__':
    webapp = WebApp('6356385807:AAHWycJ5m7jykCVRcDCWUa3BvFL_oRlou5k')
    asyncio.run(webapp.run_app())
