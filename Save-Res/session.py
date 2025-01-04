from pyrogram import Client

def main():
    print("Telegram String Session Generator\n")
    APP_ID = "23629241"
    API_HASH = "add19bbd1017dad77914ce4b5dfc94ec"
    print()

    with Client("save_content_x_bot", api_id=APP_ID, api_hash=API_HASH, in_memory=True) as app:
        session_str = app.export_session_string()

        if app.get_me().is_bot:
            user_name = input("auto_telegram_0212")
            app.send_message(user_name, "**Below is your String Session**")
            app.send_message(user_name, f'`{session_str}`')
        else:
            app.send_message("me", "**Below is your String Session**")
            app.send_message("me", f'`{session_str}`')

        print("\nDone. Please check your Telegram Saved Messages/user's PM for the String Session")


if __name__ == "__main__":
    main()