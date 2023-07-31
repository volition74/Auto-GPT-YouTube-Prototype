import chat_gpt_api as gpt
import chatGPT_Script_Gen_prompts as pr
import tkinter as tk
from tkinter import filedialog
import os
import platform
import subprocess
import csv
from datetime import datetime

###############################  FUNCTIONS #####################################

# Open the folder where the text file is located
def open_folder(directory):
    if platform.system() == "Windows":
        os.startfile(directory)
    elif platform.system() == "Darwin":
        subprocess.Popen(['open', directory])
    else:
        subprocess.Popen(['xdg-open', directory])

def clean_filename(filename):
    invalid_chars = '<>:"/\|?*\n'
    for c in invalid_chars:
        filename = filename.replace(c, '_')
    return filename

def process_topic_and_minutes(user_topic, user_minutes, directory):
    # Parameters
    min_chars = "25"

    # Print topic heading
    print("Processing topic: " + user_topic + "\n")

    # Generate Topic Summary - use as Filename
    topic_summary_prompt = pr.youtube_title_topic_Summary.format(min_summary_characters=min_chars,topic=user_topic)
    topic_summary = gpt.basic_generation(topic_summary_prompt)
    print(topic_summary)

    # Clean topic_summary and user_minutes for use in filename
    clean_user_topic = clean_filename(topic_summary)
    clean_user_minutes = clean_filename(user_minutes)

    # Get current date and time
    now = datetime.now()
    timestamp = now.strftime('%y%m%d%H%M')

    # Create log file using user's preferred directory, user_topic, and current timestamp
    filename = os.path.join(directory, f'{clean_user_topic}_{clean_user_minutes}mins_{timestamp}_ScriptIdeas.txt')
    with open(filename, 'w', encoding='utf-8') as log_file:

        def print_and_log(message):
            print(message)
            log_file.write(message + '\n')

        # Generate 10 Catchy Title Ideas
        titles_prompt = pr.youtube_title_generator_prompt.format(topic=user_topic)
        titles = gpt.basic_generation(titles_prompt)
        print_and_log("----------------")
        print_and_log("Titles Ideas: " + user_topic + " - " + clean_user_minutes + "(minutes)" )
        print_and_log("----------------")
        print_and_log(titles)
        print_and_log("\n\n")

        # Generate Catchy Thumbnail Ideas
        thumbnail_prompt = pr.youtube_thumbmail_generator_prompt.format(user_titles=titles)
        thumbnails = gpt.basic_generation(thumbnail_prompt)
        print_and_log("----------------")
        print_and_log("Thumbnail Ideas:" + user_topic + " - " + clean_user_minutes + "(minutes)" )
        print_and_log("----------------")
        print_and_log(thumbnails)
        print_and_log("\n\n")

        # script
        script_prompt = pr.youtube_script_generator_prompt.format(minutes=user_minutes,topic=user_topic)
        script = gpt.basic_generation(script_prompt)
        print_and_log("----------------")
        print_and_log("Suggested Script:" + user_topic + " - " + clean_user_minutes + "(minutes)" )
        print_and_log("----------------")
        print_and_log(script)
        print_and_log("\n\n")

        # Into a twitter thread
        tweet_prompt = pr.tweet_from_youtube_prompt.format(youtube_transcript=script)
        tweet = gpt.basic_generation(tweet_prompt)
        print_and_log("----------------")
        print_and_log("Twitter Thread:" + user_topic + " - " + clean_user_minutes + "(minutes)" )
        print_and_log("----------------")
        print_and_log(tweet)
        print("\n\n\n")

####################################################################################

# Get user's preferred directory to save the log file
root = tk.Tk()
root.withdraw()
directory = filedialog.askdirectory()
root.destroy()

# Default video length
default_video_length = "10"

# Enter a Topic
user_topic = input("Enter your Video Topic?").strip()

if user_topic == '':
    root = tk.Tk()
    root.withdraw()
    csvfile = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    root.destroy()

    with open(csvfile, newline='') as f:
        reader = csv.reader(f)
        next(reader) # Skip header row
        for row in reader:
            user_topic, user_minutes = row
            user_topic = user_topic.strip()
            user_minutes = user_minutes.strip() if user_minutes.strip() else default_video_length

            process_topic_and_minutes(user_topic, user_minutes, directory)
else:
    user_minutes = input("Video Length?(minutes)").strip()
    user_minutes = user_minutes if user_minutes else default_video_length
    process_topic_and_minutes(user_topic, user_minutes, directory)

# Call the function at the end of the script
open_folder(directory)