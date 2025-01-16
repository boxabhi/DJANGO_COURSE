from gtts import gTTS  
import os  


# def generateAudio(text):
    
#     tts = gTTS(text=text, lang='en', slow=False)  
#     tts.save("output.mp3")  

# generateAudio()

# from moviepy import VideoFileClip,AudioFileClip, ImageClip, TextClip, CompositeVideoClip


# def generate_dynamic_captions(text, total_duration, num_segments=4):
#     # Split the text into segments
#     words = text.split()
#     segment_size = len(words) // num_segments
#     segments = [' '.join(words[i * segment_size:(i + 1) * segment_size]) for i in range(num_segments)]
    
#     # Adjust for any leftover words
#     if len(words) % num_segments != 0:
#         segments[-1] += ' ' + ' '.join(words[num_segments * segment_size:])
    
#     # Calculate segment durations
#     segment_duration = total_duration / num_segments
#     subs = [((i * segment_duration, (i + 1) * segment_duration), segment) for i, segment in enumerate(segments)]
    
#     # Time formatting function
#     def format_time(seconds):
#         hrs = int(seconds // 3600)
#         mins = int((seconds % 3600) // 60)
#         secs = int(seconds % 60)
#         millis = int((seconds - int(seconds)) * 1000)
#         return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"
    
#     # Generate SRT content
#     srt_content = ""
#     for idx, ((start, end), segment) in enumerate(subs, 1):
#         srt_content += f"{idx}\n"
#         srt_content += f"{format_time(start)} --> {format_time(end)}\n"
#         srt_content += f"{segment}\n\n"
    
#     return srt_content

# from moviepy.video.tools.subtitles import SubtitlesClip
# hindi_text = "क्या आप जानते हैं कि रोमन साम्राज्य का एक विशाल और परिष्कृत व्यापार नेटवर्क था? उनकी सड़कें और जलसेतु इंजीनियरिंग के चमत्कार थे जिन्होंने भूमध्य सागर में व्यापार और परिवहन को सुगम बनाया।"  

# def mp3PNGMerge():
#     generator = lambda txt: TextClip(txt, font='Arial', fontsize=24, color='white')
#     subs = generate_dynamic_captions(hindi_text, 15)

#     audio_clip = AudioFileClip("output.mp3")
#     image_clip = ImageClip("image.jpeg")
#     video_clip = image_clip.with_audio(audio_clip)
#     video_clip.duration = audio_clip.duration
#     video_clip.fps = 30
#     video_clip.write_videofile('_CLIP.mp4')


#     subtitles = SubtitlesClip('m.srt', generator)

#     video = VideoFileClip("_CLIP.mp4")
#     result = CompositeVideoClip([video, subtitles.set_pos(('center','bottom'))])

#     result.write_videofile("__output.mp4")


# # mp3PNGMerge()


# # print(generate_dynamic_captions(hindi_text, 15))


import cv2
from gtts import gTTS
import os
import cv2
import numpy as np
from gtts import gTTS
import os
def generateAudio(text):
    tts = gTTS(text=text, lang='hi', slow=False)
    tts.save("output.mp3")
    return "output.mp3"
def apply_zoom_smooth(img, zoom_factor=1.2, duration=3, fps=30):
    target_width, target_height = 1080, 1920
    zoomed_frames = []
    total_frames = duration * fps
    h, w = img.shape[:2]

    for i in range(total_frames):
        scale = 1 + (zoom_factor - 1) * (i / total_frames)
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

        # Crop or pad to 1080x1920
        if new_h >= target_height and new_w >= target_width:
            # Crop center
            x_start = (new_w - target_width) // 2
            y_start = (new_h - target_height) // 2
            cropped = resized[y_start:y_start + target_height, x_start:x_start + target_width]
        else:
            # Pad if smaller
            cropped = resize_and_pad(resized, (target_width, target_height))

        zoomed_frames.append(cropped)
    
    return zoomed_frames

# Resize and pad to fit YouTube Shorts (1080x1920)
def resize_and_pad(img, target_size=(1080, 1920)):
    target_width, target_height = target_size
    img_h, img_w = img.shape[:2]
    
    scale = min(target_width / img_w, target_height / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    pad_x = (target_width - new_w) // 2
    pad_y = (target_height - new_h) // 2
    
    padded_img = cv2.copyMakeBorder(resized, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    return padded_img

# Create video from images with smooth zoom and captions
def create_video(image_paths, text, output_video="output_video.avi"):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    frame_size = (1080, 1920)
    out = cv2.VideoWriter(output_video, fourcc, 30, frame_size)

    # Generate audio
    audio_path = generateAudio(text)

    # Process each image
    for img_path in image_paths:
        img = cv2.imread(img_path)
        frames = apply_zoom_smooth(img)

        # Add text captions
        for frame in frames:
            frame = add_caption(frame, text)
            out.write(frame)

    out.release()

    # Merge video and audio using ffmpeg
    os.system(f'ffmpeg -i {output_video} -i output.mp3 -c:v libx264 -c:a aac -strict experimental final_output.mp4')

# Add caption to the video frame
def add_caption(frame, text):
    height, width, _ = frame.shape
    font_scale = 2
    thickness = 3

    # Text Size
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
    text_x = (width - text_size[0]) // 2
    text_y = height - 100

    # Background rectangle for text
    cv2.rectangle(frame, (text_x - 20, text_y - 60), (text_x + text_size[0] + 20, text_y + 20), (0, 0, 0), -1)
    
    # Render text
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
    
    return frame

# List of images
images = ["image.jpeg", "image1.jpeg", "image3.jpeg", "image5.jpeg"]
caption_text = "अपने शरीर को आवश्यक विटामिन और खनिजों से पोषण देने के लिए फल, सब्जियां और साबुत अनाज जैसे पूरे, अपरिष्कृत खाद्य पदार्थों को प्राथमिकता दें। इससे ऊर्जा का स्तर और समग्र कल्याण में सुधार हो सकता है।"

# Create the video
create_video(images, caption_text)