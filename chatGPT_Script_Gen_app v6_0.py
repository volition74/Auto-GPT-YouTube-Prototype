import chat_gpt_api as gpt
import chatGPT_Script_Gen_prompts as pr
import chatGPT_Script_Gen_Channel_Info as ch
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
            
def get_channel_choice():
    channel_dict = {
        1: "RC Faster",
        2: "Broadcast Bytes",
        3: "Ben Howard"
    }
    while True:
        try:
            user_input = int(input("Enter your channel choice (1-RC Faster, 2-Broadcast Bytes, 3-Ben Howard): ").strip())
            return channel_dict[user_input]
        except (KeyError, ValueError):
            print("Invalid choice. Please enter a number 1, 2, or 3.")

def process_topic_minutes_mood(csv_line_number, user_topic, user_minutes, user_mood, channel, channel_description, channel_tone, channel_style, channel_video_genres, directory):
    # Parameters
    min_chars = "21"
    selected_model = gpt.set_model_by_choice(1)

    # Print topic heading
    print(f"Processing CSV line number: {csv_line_number}, Topic: {user_topic}, Mood: {user_mood}\n")

    # Generate Topic Summary - use as Filename
    topic_summary_prompt = pr.youtube_title_topic_Summary.format(min_summary_characters=min_chars,topic=user_topic)
    topic_summary = gpt.basic_generation(topic_summary_prompt, selected_model)
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
        print_and_log(f"------------------------ {channel} ------------------------------\n")
        print_and_log(f"Topic No#: {csv_line_number}, Topic: {user_topic}, Minutes: {user_minutes}, Mood: {user_mood}\n\n")

        # Generate 10 Catchy Title Ideas
        channel_summary = pr.youtube_channel_Synopsis.format(ch_desc=channel_description, ch_tone=channel_tone, ch_style=channel_style, ch_vid_genres=channel_video_genres )
        titles_prompt = pr.youtube_title_generator_prompt.format(mood_tone=user_mood, topic=user_topic, ch_desc=channel_description, ch_tone=channel_tone, ch_style=channel_style, ch_vid_genres=channel_video_genres )
        titles = gpt.basic_generation(titles_prompt, selected_model)
        print_and_log("----------------")
        print_and_log("Titles Ideas: " + user_topic + " - Mood: " + user_mood + ", " + clean_user_minutes + "(minutes)")
        print_and_log("----------------")
        print_and_log(titles)
        print_and_log("\n\n")

        # Generate Catchy Thumbnail Ideas
        thumbnail_prompt = pr.youtube_thumbmail_generator_prompt.format(mood_tone=user_mood, user_titles=titles)
        print_and_log("-------------------General PROMPT---------------------")
        print_and_log(channel_summary + "\n" + "\n")
        print_and_log(thumbnail_prompt + "\n")
        print_and_log("-------------------++++++++---------------------\n")
        thumbnails = gpt.basic_generation(channel_summary + "\n" + thumbnail_prompt, selected_model)
        print_and_log("----------------")
        print_and_log("Thumbnail Ideas: " + user_topic + " - Mood: " + user_mood + ", " + clean_user_minutes + "(minutes)")
        print_and_log("----------------")
        print_and_log(thumbnails)
        print_and_log("\n\n")

        # script
        script_prompt = pr.youtube_script_generator_prompt.format(minutes=user_minutes, topic=user_topic, mood_tone=user_mood)
        script = gpt.basic_generation(channel_summary + "\n" + script_prompt, selected_model)
        print_and_log("----------------")
        print_and_log("Suggested Script: " + user_topic + " - Mood: " + user_mood + ", " + clean_user_minutes + "(minutes)")
        print_and_log("----------------")
        print_and_log(script)
        print_and_log("\n\n")

        # Into a twitter thread
        tweet_prompt = pr.tweet_from_youtube_prompt.format(youtube_transcript=script)
        tweet = gpt.basic_generation(channel_summary + "\n" + tweet_prompt, selected_model)
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
            channel_name, user_topic, user_minutes, user_mood = row
            user_topic = user_topic.strip()
            user_minutes = user_minutes.strip()
            user_mood = user_mood.strip() if user_mood.strip() else 'Entertaining'  # use 'Entertaining' if mood is blank
            channel = channel_name
            channel_description = ch.channel_info[channel]['description']
            channel_tone = ch.channel_info[channel]['tone']
            channel_style = ch.channel_info[channel]['style']
            channel_video_genres = ch.channel_info[channel]['video genres']

            process_topic_minutes_mood(csv_line_number, user_topic, user_minutes, user_mood, channel, channel_description, channel_tone, channel_style, channel_video_genres, directory)
            csv_line_number += 1  # increment line number
else:
    user_minutes = input("Video Length?(minutes)").strip()
    user_mood = input("Mood/Tone of the Video?").strip()
    user_mood = user_mood if user_mood else 'Entertaining'  # use 'Entertaining' if mood is blank
    channel = get_channel_choice()
    channel_description = ch.channel_info[channel]['description']
    channel_tone = ch.channel_info[channel]['tone']
    channel_style = ch.channel_info[channel]['style']
    channel_video_genres = ch.channel_info[channel]['video genres']
    process_topic_minutes_mood(user_topic, user_minutes, user_mood, channel, channel_description, channel_tone, channel_style, channel_video_genres, directory)

# Call the function at the end of the script
open_folder(directory)