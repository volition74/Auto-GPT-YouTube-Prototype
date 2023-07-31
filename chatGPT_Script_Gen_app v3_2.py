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
        
def clean_ending_punctuation_and_inner_periods(text):
    # Remove trailing punctuation
    text = text.rstrip(' .,;:!?"')
    # Replace periods with dashes
    text = text.replace('.', '-')
    return text

def clean_filename(filename):
    invalid_chars = '<>:"/\|?*\n'
    for c in invalid_chars:
        filename = filename.replace(c, '_')
    return filename

def get_start_line():
    while True:
        start_line_input = input("Enter the line number in the CSV to start from (default is 1): ")
        if not start_line_input:  # If user hits enter without typing anything
            return 1
        elif start_line_input.isdigit() and int(start_line_input) >= 1:
            return int(start_line_input)
        else:
            print("Invalid input. Please enter a number greater than or equal to 1.")

def process_topic_minutes_mood(csv_line_number, user_topic, user_minutes, user_mood, directory):
    # Parameters
    min_chars = "21"

    # Print topic heading
    print(f"Processing CSV line number: {csv_line_number}, Topic: {user_topic}, Mood: {user_mood}\n")

    # Generate Topic Summary - use as Filename
    topic_summary_prompt = pr.youtube_title_topic_Summary.format(min_summary_characters=min_chars,topic=user_topic)
    topic_summary = gpt.basic_generation(topic_summary_prompt)
    print(topic_summary)

    # Clean topic_summary and user_minutes for use in filename
    clean_topic_punctuation_and_inner_periods = clean_ending_punctuation_and_inner_periods(topic_summary)
    clean_user_topic = clean_filename(clean_topic_punctuation_and_inner_periods)
    clean_user_minutes = clean_filename(user_minutes)

    # Get current date and time
    now = datetime.now()
    timestamp = now.strftime('%y%m%d%H%M')

    # Create log file using user's preferred directory, user_topic, and current timestamp
    filename = os.path.join(directory, f'{str(csv_line_number).zfill(3)}_{clean_user_topic}_{clean_user_minutes}mins_{timestamp}_ScriptIdeas.txt')
    with open(filename, 'w', encoding='utf-8') as log_file:
        
        def print_and_log(message):
            print(message)
            log_file.write(message + '\n')

        # Print CSV line number, topic, minutes and mood at the top of the log file
        print_and_log(f"CSV line number: {csv_line_number}, Topic: {user_topic}, Minutes: {user_minutes}, Mood: {user_mood}\n\n")
        
        def print_and_log(message):
            print(message)
            log_file.write(message + '\n')

        # Generate 10 Catchy Title Ideas
        titles_prompt = pr.youtube_title_generator_prompt.format(mood_tone=user_mood, topic=user_topic)
        titles = gpt.basic_generation(titles_prompt)
        print_and_log("----------------")
        print_and_log("Titles Ideas: " + user_topic + " - Mood: " + user_mood + ", " + clean_user_minutes + "(minutes)")
        print_and_log("----------------")
        print_and_log(titles)
        print_and_log("\n\n")

        # Generate Catchy Thumbnail Ideas
        thumbnail_prompt = pr.youtube_thumbmail_generator_prompt.format(mood_tone=user_mood, user_titles=titles)
        thumbnails = gpt.basic_generation(thumbnail_prompt)
        print_and_log("----------------")
        print_and_log("Thumbnail Ideas: " + user_topic + " - Mood: " + user_mood + ", " + clean_user_minutes + "(minutes)")
        print_and_log("----------------")
        print_and_log(thumbnails)
        print_and_log("\n\n")

        # script
        script_prompt = pr.youtube_script_generator_prompt.format(minutes=user_minutes, topic=user_topic, mood_tone=user_mood)
        script = gpt.basic_generation(script_prompt)
        print_and_log("----------------")
        print_and_log("Suggested Script: " + user_topic + " - Mood: " + user_mood + ", " + clean_user_minutes + "(minutes)")
        print_and_log("----------------")
        print_and_log(script)
        print_and_log("\n\n")

        # Into a twitter thread
        tweet_prompt = pr.tweet_from_youtube_prompt.format(youtube_transcript=script)
        tweet = gpt.basic_generation(tweet_prompt)
        print_and_log("----------------")
        print_and_log("Twitter Thread: " + user_topic + " - Mood: " + user_mood + ", " + clean_user_minutes + "(minutes)")
        print_and_log("----------------")
        print_and_log(tweet)
        print_and_log("\n\n")

####################################################################################

# Get user's preferred directory to save the log file
root = tk.Tk()
root.withdraw()
directory = filedialog.askdirectory()
root.destroy()

# Enter a Topic
user_topic = input("Enter your Video Topic?").strip()

if user_topic == '':
    root = tk.Tk()
    root.withdraw()
    csvfile = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    root.destroy()

    start_line = get_start_line()

    with open(csvfile, newline='') as f:
        reader = csv.reader(f)
        for _ in range(start_line):  # Skip the specified number of rows
            try:
                next(reader)
            except StopIteration:  # There are less rows in the file than the start_line
                print(f"The CSV file only has {start_line - 1} lines. Please check your data and start row and try again.")
                exit(1)

        csv_line_number = start_line
        for row in reader:
            user_topic, user_minutes, user_mood = row
            user_topic = user_topic.strip()
            user_minutes = user_minutes.strip()
            user_mood = user_mood.strip() if user_mood.strip() else 'Entertaining'  # use 'Entertaining' if mood is blank

            process_topic_minutes_mood(csv_line_number, user_topic, user_minutes, user_mood, directory)
            csv_line_number += 1  # increment line number
else:
    user_minutes = input("Video Length?(minutes)").strip()
    user_mood = input("Mood/Tone of the Video?").strip()
    user_mood = user_mood if user_mood else 'Entertaining'  # use 'Entertaining' if mood is blank
    process_topic_minutes_mood(user_topic, user_minutes, user_mood, directory)

# Call the function at the end of the script
open_folder(directory)