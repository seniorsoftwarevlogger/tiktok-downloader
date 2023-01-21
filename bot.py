from TikTokApi import TikTokApi

import asyncio
import nest_asyncio

import requests

from telegram import Bot

import re
import os


def from_admin(update):
    return update.message and update.message.from_user.username == os.environ.get('ADMIN')


def resolve(url):
    r = requests.head(url)
    return r.headers['Location']


async def main():
    # Fetch updates
    token = os.environ.get('TOKEN')

    async with Bot(token) as bot:
        updates = await bot.get_updates()

        if updates:
            # if more than 1 updates awailable, take 1
            try:
                update = next(m for m in updates if from_admin(m))
            except StopIteration:
                exit

            if not re.match("https://vm.tiktok.com/.*/", update.message.text):
                exit

            # Resolve full tiktok URL
            print(update.message.text)
            full_url = resolve(update.message.text)

            print(full_url)
            # fetch video and post
            video_id = full_url.split('/')[-1].split('?')[0]

            with TikTokApi(custom_verify_fp=os.environ.get('VERIFY')) as api:
                video = api.video(id=video_id)
                video_data = video.bytes()

                print(len(video_data))

                if len(video_data) > 1000:  # video can't be less than 1Kb
                    caption = video.info()[
                        'desc'] + "\n\n" + update.message.text + "\n\n@git_rebase"

                    await bot.send_video(os.environ.get('CHANNEL_ID'), video_data, caption=caption)

                    # confirm the update so that we don't fetch twice
                    await bot.get_updates(offset=update.update_id + 1)
                else:
                    # Got access denied
                    print(video_data)


if __name__ == '__main__':
    try:
        nest_asyncio.apply()
        asyncio.run(main())
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        pass
