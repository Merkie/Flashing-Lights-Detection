import cv2
import numpy as np
import json
import datetime
import time

# Function to process a video file and detect flashing lights
def process_video(file_path, threshold, downscale):
    # Function to check if the frame contains a flashing light based on brightness difference
    def check_frame(frame, prev_brightness, brightness_threshold):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        brightness_diff = abs(brightness - prev_brightness)
        if brightness_diff > brightness_threshold:
            return True, brightness
        else:
            return False, brightness

    # Function to process timestamps and combine consecutive flashing light events
    def process_timestamps(timestamps):
        combined_timestamps = []
        for ts in timestamps:
            if not combined_timestamps or datetime.datetime.strptime(ts['start'], '%H:%M:%S') - datetime.datetime.strptime(combined_timestamps[-1]['end'], '%H:%M:%S') > datetime.timedelta(seconds=1):
                combined_timestamps.append(ts)
            else:
                combined_timestamps[-1]['end'] = ts['end']
                combined_timestamps[-1]['flashing_frames_count'] += ts['flashing_frames_count']
                if combined_timestamps[-1]['flashing_frames_count'] <= 3:
                    combined_timestamps.pop()
        return combined_timestamps

    # Initialize video capture object
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        return {'error': 'Error opening the video file.'}

    flashing_lights = [] # List to store timestamps of flashing lights
    flashing_start_time = None
    flashing_end_time = None
    flashing_detected = False
    prev_brightness = None
    flashing_frames_count = 0
    resize_frames = True
    start_time = time.time()

    # Iterate through video frames
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame if needed
        if resize_frames:
            frame = cv2.resize(frame, (0, 0), fx=downscale, fy=downscale)

        # Initialize prev_brightness for the first frame
        if prev_brightness is None:
            prev_brightness = np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            continue

        # Check if the current frame has flashing light
        is_flashing, brightness = check_frame(frame, prev_brightness, threshold)
        if is_flashing:
            flashing_frames_count += 1
            if not flashing_detected:
                flashing_start_time = datetime.datetime.utcfromtimestamp(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000).strftime('%H:%M:%S')
                flashing_detected = True
            prev_brightness = brightness
        else:
            # If flashing light sequence has ended, add the timestamp to the list
            if flashing_detected:
                flashing_end_time = datetime.datetime.utcfromtimestamp(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000).strftime('%H:%M:%S')
                if(flashing_frames_count > 1):
                    flashing_lights.append({'start': flashing_start_time, 'end': flashing_end_time, 'flashing_frames_count': flashing_frames_count})
                flashing_detected = False
                flashing_frames_count = 0
            prev_brightness = brightness

    # Process the timestamps to combine consecutive flashing events
    processed_flashing_lights = process_timestamps(flashing_lights)
    processing_time = time.time() - start_time
    
    # Remove the flashing_frames_count key from the output
    for i in processed_flashing_lights:
        i.pop('flashing_frames_count')
    
    # Return the output
    output = {'flashingLightsDetected': len(processed_flashing_lights) > 0, 'timestamps': processed_flashing_lights, 'processingTimeInSeconds': round(processing_time, 2)}
    
    # Release the video capture object and destroy all windows
    cap.release()
    cv2.destroyAllWindows()
    
    # Return the output
    return output
