import subprocess
import os
import re

def extract_number(filename):
    """ Extracts a number from a filename. """
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

def create_silence(duration, output_file):
    """ Create a segment of silence. """
    subprocess.run(['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-t', str(duration), output_file])

# Directory paths for audio, video, and output
audio_dir = 'Audio_Vid_Merge/audio'
video_dir = 'Audio_Vid_Merge/video'
output_dir = 'Audio_Vid_Merge/audio+video'
timings_file = 'Audio_Vid_Merge/timings.txt'

# Supported audio and video extensions
audio_extensions = ['.mp3', '.wav', '.aifc', '.aac', '.ogg', '.flac']
video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv']

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load the timings from the timings.txt file and filter based on audio extensions
with open(timings_file, 'r') as file:
    timings = [line.strip().split(', ') for line in file.readlines() if os.path.splitext(line.strip().split(', ')[0])[1].lower() in audio_extensions]

# Sort the timings based on the audio file number
timings.sort(key=lambda x: extract_number(x[0]))

# Initialize variables
concat_list = []
last_end_time = 0

# Process each entry in the timings
for entry in timings:
    filename, start_time, end_time = entry
    start_time, end_time = float(start_time), float(end_time)
    audio_file_path = os.path.join(audio_dir, filename)
    audio_extension = os.path.splitext(filename)[1]

    # Add silence if there is a gap
    if start_time > last_end_time:
        silence_duration = start_time - last_end_time
        silence_file = f'silence_{last_end_time}_{start_time}{audio_extension}'
        create_silence(silence_duration, silence_file)
        concat_list.append(silence_file)

    # Trim the audio file to the specified duration and add to the list
    trimmed_audio = f'trimmed_{start_time}_{end_time}{audio_extension}'
    subprocess.run(['ffmpeg', '-i', audio_file_path, '-ss', str(start_time), '-t', str(end_time - start_time), '-c', 'copy', trimmed_audio])
    concat_list.append(trimmed_audio)

    last_end_time = end_time

# Create a file for concatenation
with open('concat_list.txt', 'w') as file:
    for audio in concat_list:
        file.write(f"file '{audio}'\n")

# Concatenate all the segments
concatenated_audio = 'concatenated_audio' + audio_extension  # Use the extension of the last audio file
subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'concat_list.txt', '-c', 'copy', concatenated_audio])

# Assuming there's only one video file in the video directory
video_files = [os.path.join(video_dir, file) for file in os.listdir(video_dir) if os.path.splitext(file)[1].lower() in video_extensions]
if not video_files:
    raise Exception("No video files found in the 'video' directory.")
video_file = video_files[0]  # Select the first video file

# Get the duration of the concatenated audio
audio_duration = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', concatenated_audio]).strip())

# Get the duration of the video
video_duration = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_file]).strip())

# Determine the final audio file to use
if video_duration > audio_duration:
    # Add silence to the end of the audio if the video is longer
    silence_duration = video_duration - audio_duration
    silence_output = f'final_silence{audio_extension}'
    create_silence(silence_duration, silence_output)
    final_audio = 'final_audio' + audio_extension
    subprocess.run(['ffmpeg', '-i', concatenated_audio, '-i', silence_output, '-filter_complex', '[0:0][1:0]concat=n=2:v=0:a=1', final_audio])
elif video_duration < audio_duration:
    # Trim the audio if it's longer than the video
    final_audio = 'final_audio' + audio_extension
    subprocess.run(['ffmpeg', '-i', concatenated_audio, '-ss', '0', '-t', str(video_duration), '-c', 'copy', final_audio])
else:
    final_audio = concatenated_audio

# Output file path in the audio+video folder
output_extension = os.path.splitext(video_file)[1]
output_file = os.path.join(output_dir, 'final_output' + output_extension)

# Merge audio with video, excluding original audio track
subprocess.run(['ffmpeg', '-i', video_file, '-i', final_audio, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', '-map', '0:v', '-map', '1:a', output_file])

# Clean up temporary files
os.remove('concat_list.txt')
for file in concat_list:
    os.remove(file)
if final_audio != concatenated_audio:
    os.remove(concatenated_audio)
if 'silence_output' in locals():
    os.remove(silence_output)