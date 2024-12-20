from moviepy.editor import VideoFileClip

# Paths
input_video_path = '/home/iplslam/Husha/Data/onigajo/20230208/case02/cam3.mp4'
output_video_path = '/home/iplslam/Husha/Data/movie/1/onigajo_case02_2_cam3.mp4'  # 出力ファイルは入力と別パスに

# Time range for trimming (in seconds)
start_time = 180    # Start time in seconds
end_time = 300      # End time in seconds

# Load video
video = VideoFileClip(input_video_path)

# Trim video
trimmed_video = video.subclip(start_time, end_time)

# Save trimmed video
trimmed_video.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

print(f"Trimmed video saved to {output_video_path}")
