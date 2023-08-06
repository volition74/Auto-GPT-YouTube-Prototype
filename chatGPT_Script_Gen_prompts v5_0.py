youtube_title_topic_Summary = """\
Summarise this topic into {min_summary_characters} characters or less.
###
{topic}
###"""

youtube_title_generator_prompt = """\
Based on the information I have about this channel: {ch_desc}. This channel makes videos mainly in these genres, {ch_vid_genres}. I want you to act as a viral YouTube title creator with a {ch_tone} tone and {ch_style} style. 
Think of titles that are catchy and attention-grabbing, and will encourage people to click and watch the video. The titles should be short, concise, and direct. They should also be creative and clever. Try to come up with titles that are unexpected and surprising. Do not use titles that are generic, or titles that have been used many times before. The mood or tone of the video is {mood_tone} and the video is about {topic}."""

youtube_thumbmail_generator_prompt = """I want you to act as a viral YouTube thumbnail creator. Think of thumbnails that are catchy and attention-grabbing, and will encourage people to click and watch the video. I will provide you with 10 Titles, the videos are suggested to have a mood or tone of {mood_tone}. You will suggest thumbnails for each describe what is in the thumbnail very well and be as detailed as you can, so desginers can understand and create. Here are the titles {user_titles}."""

youtube_script_generator_prompt = """Act as a professional YouTube video script writer and create an engaging script for a {minutes} minute video.
Think outside the box and come up with a creative, witty, and captivating script that people would be interested in watching and sharing. Utilize techniques to generate more engagement in the narration script. Create a timeline and stick to it for up to {minutes} minutes of spoken narration.

THE Topic IS: [{topic}]
The mood and or Tone is: [{mood_tone}]"""

tweet_from_youtube_prompt = """Act as if you're a social media expert. Give me a 10 tweet thread based on the follwing youtube transcript: {youtube_transcript}. The thread should be optimised for virality and contain hashtags and emoticons. Each tweet should not exceed 280 characters in length."""

youtube_channel_Synopsis = """\
Based on the information I have about this channel: {ch_desc}. This channel makes videos mainly in these genres, {ch_vid_genres}. I want you to act as a viral YouTube title creator with a {ch_tone} tone and {ch_style} style."""