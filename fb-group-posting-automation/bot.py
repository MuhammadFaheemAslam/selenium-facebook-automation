from selenium import webdriver
import os, random, logging, time
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from core.facebook_login import login_facebook
from core.facebook_utils import load_caption, read_credentials, read_groups_url, failed_log, update_failed_groups_file
from core.facebook_poster import post_in_facebook_group

# === Configure Logging with Daily Rotating Log Files ===

# Generate log file name with current date
today = datetime.now().strftime("%Y-%m-%d")
log_filename = f"logs/automation_{today}.log"

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# File handler - rotates logs daily, keeps 7 days of backup
file_handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=7, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"))

# Stream handler - console output
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"))

# Add handlers to the logger
logger.handlers = [file_handler, stream_handler]

# === Bot Logic ===
def run_bot():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    CAPTION_PATH = os.path.join(BASE_DIR, "data/post_content", "description.txt")
    MEDIA_PATH = os.path.join(BASE_DIR, "data/post_content/media")
    CRED_PATH = os.path.join(BASE_DIR, "data", "credentials.txt")
    GROUP_PATH = os.path.join(BASE_DIR, "data", "groups_url.txt")
    FAILED_PATH = os.path.join(BASE_DIR, 'logs', "failed_posted.txt")
    
    if os.path.exists(FAILED_PATH):
        os.remove(FAILED_PATH)
        logging.info("🧹 Cleaned up previous failed_posted.txt file")

    all_media = [
        os.path.join(MEDIA_PATH, filename)
        for filename in os.listdir(MEDIA_PATH)
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".mp4", ".mov", ".avi"))
    ]

    if not all_media:
        logging.warning("No media files found in media directory.")
        return

    caption = load_caption(CAPTION_PATH)
    all_accounts = read_credentials(CRED_PATH)
    media_files = random.sample(all_media, min(10, len(all_media)))
    group_urls = read_groups_url(GROUP_PATH)

    total_success = 0
    total_failure = 0

    for email, password in all_accounts:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=options)

        try:
            logged_msg = login_facebook(driver, email, password)
            if logged_msg:
                for group_url in group_urls:
                    post_result = post_in_facebook_group(driver, group_url, media_files, caption)

                    if not post_result:
                        failed_log(FAILED_PATH, group_url, email)
                    else:
                        total_success += 1

                failed_group_urls = read_groups_url(FAILED_PATH)

                for attempt in range(2):  # Only 2 retry attempts
                    if not failed_group_urls:
                        break  # All succeeded

                    logging.info(f"=== Retry Attempt {attempt + 1} ===")
                    still_failed = []

                    for failed_group in failed_group_urls:
                        logging.info(" ")
                        logging.info(f"Retrying group: {failed_group}")
                        retry_result = post_in_facebook_group(driver, failed_group, media_files, caption)

                        if not retry_result:
                            still_failed.append(failed_group)
                        else:
                            total_success += 1
                            logging.info(f"Posted successfully in retry attempt {attempt + 1}: {failed_group}")

                    failed_group_urls = still_failed
                    update_failed_groups_file(FAILED_PATH, failed_group_urls)

                total_failure += len(failed_group_urls)
            else:
                logging.info("Login Failed")

        finally:
            logging.info(f"Logging out and closing browser for {email}")
            driver.quit()

    # Final Summary
    logging.info("=" * 50)
    logging.info(f"🎯 Total Groups Successfully Posted: {total_success}")
    logging.info(f"❌ Total Groups Failed After Retries: {total_failure}")
    logging.info("=" * 50)


if __name__ == "__main__":
    logging.info("=" * 50)
    logging.info("🚀 Starting Facebook Group Posting Automation Script")
    logging.info(f"🕒 Run started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info("=" * 50)
    
    run_bot()
