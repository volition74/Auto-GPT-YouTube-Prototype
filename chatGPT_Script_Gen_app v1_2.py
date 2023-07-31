import chat_gpt_api as gpt
import chatGPT_Script_Gen_prompts as pr
import tkinter as tk
from tkinter import filedialog
import os
import platform
import subprocess

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
    invalid_chars = '<>:"/\|?*'
    for c in invalid_chars:
        filename = filename.replace(c, '_')
    return filename

####################################################################################

# Get user's preferred directory to save the log file
root = tk.Tk()
root.withdraw()
directory = filedialog.askdirectory()
root.destroy()

#step 1: Enter a Topic
user_topic = input("Enter your Video Topic?").strip()
user_minutes = input("Video Length?(minutes)").strip()

#step 2: Generate Topic Summary - use as Filename
topic_summary_prompt = pr.youtube_title_topic_Summary.format(topic=user_topic)
topic_summary = gpt.basic_generation(topic_summary_prompt)
print(topic_summary)

# Clean topic_summary and user_minutes for use in filename
clean_user_topic = clean_filename(topic_summary)
clean_user_minutes = clean_filename(user_minutes)

# Create log file using user's preferred directory and user_topic
filename = os.path.join(directory, f'{clean_user_topic}_{clean_user_minutes}mins_ScriptIdeas.txt')
log_file = open(filename, 'w', encoding='utf-8')

def print_and_log(message):
    print(message)
    log_file.write(message + '\n')

#step 2: Generate 10 Catchy Title Ideas
titles_prompt = pr.youtube_title_generator_prompt.format(topic=user_topic)
titles = gpt.basic_generation(titles_prompt)
print_and_log("----------------")
print_and_log("Titles Ideas: ")
print_and_log("----------------")
print_and_log(titles)
print_and_log("\n\n")

#step 3: Generate Catchy Thumbnail Ideas
thumbnail_prompt = pr.youtube_thumbmail_generator_prompt.format(user_titles=titles)
thumbnails = gpt.basic_generation(thumbnail_prompt)
print_and_log("----------------")
print_and_log("Thumbnail Ideas: ")
print_and_log("----------------")
print_and_log(thumbnails)
print_and_log("\n\n")

#step 4: script
script_prompt = pr.youtube_script_generator_prompt.format(minutes=user_minutes,topic=user_topic)
script = gpt.basic_generation(script_prompt)
print_and_log("----------------")
print_and_log("Suggested Script: ")
print_and_log("----------------")
print_and_log(script)
print_and_log("\n\n")

#step 5: Into a twitter thread
tweet_prompt = pr.tweet_from_youtube_prompt.format(youtube_transcript=script)
tweet = gpt.basic_generation(tweet_prompt)
print_and_log("----------------")
print_and_log("Twitter Thread: ")
print_and_log("----------------")
print_and_log(tweet)

log_file.close()

# Call the function at the end of the script
open_folder(directory)