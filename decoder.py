# decoder.py

import cv2
import numpy as np
import time

start_time = time.time()

def video_to_frames(video_path):
    """Extracts frames from a video."""
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

def frames_to_binary(frames, pixel_size=10):
    """Converts frames to binary data."""
    binary_data = ""
    for frame in frames:
        height, width = frame.shape[:2]
        for y in range(0, height, pixel_size):
            for x in range(0, width, pixel_size):
                pixel = frame[y:y+pixel_size, x:x+pixel_size]
                if np.mean(pixel) < 128: # Assuming black pixel represents '1', checking average of pixels
                    binary_data += '1'
                else:
                    binary_data += '0'
    return binary_data

def binary_to_file(binary_data, output_file_path):
    """Converts binary data to a file."""
    byte_array = bytearray()
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        byte_array.append(int(byte, 2))
    with open(output_file_path, 'wb') as file:
        file.write(byte_array)

# Example usage
if __name__ == "__main__":
    video_path = 'data_video.mp4'
    frames = video_to_frames(video_path)
    binary_data = frames_to_binary(frames)
    binary_to_file(binary_data, 'output2.png')

end_time = time.time()
print(f"Decoding completed in {end_time - start_time:.2f} seconds.")