from video_edit_helper import VideoEditHelper

editor = VideoEditHelper("euler_visualization")

# Extract frames from your generated video
editor.extract_frames_from_video('output/euler_visualization_plot_twist_20250711_155858.mp4')

# See what you have
editor.preview_frames(editor.get_current_frames())

original_number_of_frames = len(editor.get_current_frames())

# Make your edits
editor.edit_text_frame(0, ['Every AI gave me this: ', 'as the best math formula'])  # Change text
editor.remove_frame(6)  # Remove a frame
# editor.add_overlay_to_frame(2, 'MIND BLOWN 🤯')  # Add overlay
# editor.duplicate_frame(1)  # Duplicate for emphasis

# Change timing
# editor.change_frame_duration({
#     0: 3,    # Hook stays longer
#     1: 2,    # Normal
#     2: 4,    # Dramatic pause
#     3: 1.5   # Quick transition
# })

print(f"Original number of frames: {original_number_of_frames}")
print(f"Edited number of frames: {len(editor.get_current_frames())}")

# Rebuild video
editor.rebuild_video('euler_edited')