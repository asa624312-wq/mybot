from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
import asyncio

print("="*40)
print("Saved Messages Cycler")
print("="*40)

api_id = int(input("API ID: "))
api_hash = input("API HASH: ")
phone = input("رقمك بدون +: ")

client = TelegramClient("saved_cycler", api_id, api_hash)

async def main():
    await client.start(phone=phone)
    me = await client.get_me()
    my_id = me.id

    print("\n✓ تم تسجيل الدخول\n")

    target_group = int(input("ID المجموعة الهدف (-100...): "))
    message_count = int(input("عدد الرسائل المراد أخذها: "))
    cycle_delay = int(input("وقت الاستراحة بين كل دورة (بالثواني): "))

    enabled = False

    print("\n✓ الأداة جاهزة")
    print("1 = تشغيل")
    print("2 = إيقاف\n")

    @client.on(events.NewMessage(chats=target_group))
    async def controller(event):
        nonlocal enabled

        if event.sender_id != my_id:
            return

        text = event.raw_text.strip()

        if text == "1":
            enabled = True
            await event.delete()
            print("🟢 تم التشغيل")

        elif text == "2":
            enabled = False
            await event.delete()
            print("🔴 تم الإيقاف")

    async def cycler():
        nonlocal enabled

        while True:
            if enabled:
                try:
                    messages = await client.get_messages(
                        "me",
                        limit=message_count
                    )

                    messages = list(reversed(messages))

                    await client.forward_messages(
                        target_group,
                        messages
                    )

                    await asyncio.sleep(cycle_delay)

                except FloodWaitError as e:
                    print(f"⛔ فلود... انتظار {e.seconds} ثانية")
                    await asyncio.sleep(e.seconds)

                except Exception:
                    await asyncio.sleep(5)

            else:
                await asyncio.sleep(1)

    asyncio.create_task(cycler())
    await client.run_until_disconnected()


while True:
    try:
        client.loop.run_until_complete(main())
    except Exception:
        print("⚠️ انقطع الاتصال... انتظار عودة الانترنت")
        asyncio.sleep(5)
