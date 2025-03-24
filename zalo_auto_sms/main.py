from auto_zalo_msg import AutoZaloMsg
from create_log import Logger
import pandas as pd
from time import sleep

logger = Logger()

will_send = input("Will you send message? (y/n): ")

logger.log_print(will_send)
logger.log_print("Script started")

try:
    logger.log_print("Load contact data")
    data_file = r"contact_info.csv"
    data = pd.read_csv(data_file, dtype=str)

    logger.log_print("Load message template")
    with open(r"message_template.txt", "r", encoding="utf-8") as file:
        message_template = file.read()

    logger.log_print("Open Browser")
    auto_msg = AutoZaloMsg()

    logger.log_print("Open Website")
    auto_msg.open_zalo()

    logger.log_print("Check loggin status")

    sleep(5)
    if not auto_msg.check_login():
        logger.log_print("Logging error, please try again")
    else:
        logger.log_print("Logged in")

        for index, driver_data in data.iterrows():
            driver_phone = driver_data['phone']
            driver_name = driver_data['name']
            attempt = auto_msg.attempt_search + 1
            message_lines = [
                line if line.strip() else ' '
                for line in
                message_template.format(driver_name=driver_data["name"], driver_phone=driver_data["phone"]).split("\n")
            ]

            logger.log_print(f'Contact #{attempt}:')
            logger.log_print(f'Processing {driver_phone} - {driver_name}')
            sleep(2)
            auto_msg.search_driver(driver_phone)

            sleep(2)
            if auto_msg.has_exist_driver():
                logger.log_print("Driver found")
                sleep(2)
                if auto_msg.is_new_account():
                    driver_account = auto_msg.driver_account
                    logger.log_print(f'Driver Zalo Account: {driver_account}')
                    sleep(2)
                    auto_msg.send_message(message_lines, will_send)
                    logger.log_print("Message sent successfully")
                else:
                    driver_account = auto_msg.driver_account
                    logger.log_print(f'Driver Zalo Account: {driver_account}')
                    logger.log_print("This account has already been sent a message")
            else:
                logger.log_print("Driver not found")

            sleep(2)

            logger.log_print("Update status")
            data.at[index, 'status'] = auto_msg.sent_status

        logger.log_print("Done")
        logger.log_print("Close Browser")
        auto_msg.quit()

        logger.log_print("Save contact data")
        data.to_csv(data_file, index=False)

        logger.log_print("Script finished successfully")
except Exception as e:
    logger.log_print(f"Error occurred: {e}")
