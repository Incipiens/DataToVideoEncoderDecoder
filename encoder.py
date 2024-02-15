# encoder.py

import cv2
import numpy as np
import time
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip

start_time = time.time()

def file_to_binary(file_path):
    """Converts file content to a binary string."""
    with open(file_path, 'rb') as file:
        content = file.read()
    return ''.join(format(byte, '08b') for byte in content)

# Change pixel_size here
def binary_to_frames(binary_data, frame_size=(1920, 1080), pixel_size=5):
    """Converts binary data to a list of frames."""
    width, height = frame_size
    pixels_per_width = width // pixel_size
    pixels_per_height = height // pixel_size
    
    # Calculate total pixels per frame and how many frames are needed
    total_pixels_per_frame = pixels_per_width * pixels_per_height
    total_frames_needed = len(binary_data) // total_pixels_per_frame + (1 if len(binary_data) % total_pixels_per_frame else 0)
    
    frames = []
    for frame_index in range(total_frames_needed):
        frame = np.ones((height, width, 3), np.uint8) * 255 # Start with a white frame
        start_index = frame_index * total_pixels_per_frame
        end_index = start_index + total_pixels_per_frame
        frame_data = binary_data[start_index:end_index]
        
        for index, bit in enumerate(frame_data):
            x = (index % pixels_per_width) * pixel_size
            y = (index // pixels_per_width) * pixel_size
            color = 0 if bit == '1' else 255 # Black for '1', white for '0'
            frame[y:y+pixel_size, x:x+pixel_size] = color
        
        frames.append(frame)
    return frames

# Can increase FPS but risks triggering irreversible compression on YouTube
def save_frames_to_video(frames, output_file='output.mp4', fps=15):
    """Saves frames to a video file."""
    height, width = frames[0].shape[:2]
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    
    for frame in frames:
        out.write(frame)
    out.release()

def add_audio_to_video(video_path, audio_path, output_path):
    #  Load the video clip
    video_clip = VideoFileClip(video_path)
    
    # Load the audio file
    audio_clip = AudioFileClip(audio_path)
    
    # Calculate the duration of the audio and video
    video_duration = video_clip.duration
    audio_duration = audio_clip.duration
    
    # Loop the audio if necessary
    if video_duration > audio_duration:
        # Calculate the number of loops required
        loop_count = int(video_duration // audio_duration) + 1
        # Create a composite audio clip with the audio looped
        audio_loops = [audio_clip] * loop_count
        looped_audio_clip = CompositeAudioClip(audio_loops)
        # Set the audio of the video clip as the looped audio, trimming to video duration
        final_audio_clip = looped_audio_clip.set_duration(video_clip.duration)
    else:
        # If the video is shorter than one loop of the audio, just trim the audio
        final_audio_clip = audio_clip.set_duration(video_clip.duration)
    
    # Set the audio of the video clip
    final_clip = video_clip.set_audio(final_audio_clip)
    
    # Write the result to a file
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Example usage
if __name__ == "__main__":
    file_path = 'filenamehere'
    audio_path = 'sneakysnitch.mp3'
    binary_data = file_to_binary(file_path)
    frames = binary_to_frames(binary_data)
    save_frames_to_video(frames, 'data_video.mp4')

    # Uncomment the below if you want music in your video lol
    #add_audio_to_video('data_video.mp4', audio_path, 'data_video_audio.mp4')

end_time = time.time()
print(f"Encoding completed in {end_time - start_time:.2f} seconds.")