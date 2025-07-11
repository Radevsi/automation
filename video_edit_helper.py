#!/usr/bin/env python3
"""
Helper script for making minimal edits to generated videos
"""

import os
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

class VideoEditHelper:
    def __init__(self, project_name):
        self.project_name = project_name
        self.width = 1080
        self.height = 1920
        self.fps = 30
        
        # Create edit workspace
        os.makedirs("edits", exist_ok=True)
        os.makedirs("edits/frames", exist_ok=True)
        
    def extract_frames_from_video(self, video_path):
        """Extract all frames from existing video"""
        print(f"📸 Extracting frames from {video_path}...")
        
        # Clear existing frames
        frame_dir = "edits/frames"
        for f in os.listdir(frame_dir):
            if f.endswith('.png'):
                os.remove(os.path.join(frame_dir, f))
        
        # Extract frames
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', 'fps=1',  # Extract 1 frame per second
            'edits/frames/frame_%03d.png'
        ]
        
        subprocess.run(cmd, check=True)
        
        # Get frame list
        frames = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])
        print(f"✅ Extracted {len(frames)} frames")
        
        return [os.path.join(frame_dir, f) for f in frames]
    
    def preview_frames(self, frames):
        """Show preview of all frames with numbers"""
        print("\n📋 Frame Preview:")
        print("-" * 50)
        
        for i, frame_path in enumerate(frames):
            # Get frame info
            img = Image.open(frame_path)
            
            # Try to detect what type of frame it is
            frame_type = self.detect_frame_type(img)
            
            print(f"Frame {i}: {frame_type}")
            print(f"  Path: {frame_path}")
            print(f"  Size: {img.size}")
            print()
    
    def detect_frame_type(self, img):
        """Try to detect what type of frame this is"""
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Sample some pixels to guess content
        center_color = img.getpixel((img.width // 2, img.height // 2))
        
        # Very basic detection
        if sum(center_color) < 100:  # Mostly dark
            return "Dark frame (likely text or intro)"
        elif sum(center_color) > 600:  # Mostly light
            return "Light frame"
        else:
            return "Content frame"
    
    def edit_text_frame(self, frame_number, new_text_lines, output_path=None):
        """Replace text in a specific frame"""
        frames = self.get_current_frames()
        
        if frame_number >= len(frames):
            print(f"❌ Frame {frame_number} doesn't exist!")
            return None
        
        # Create new text frame
        img = Image.new('RGB', (self.width, self.height), '#0a0a0a')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 70)
        except:
            font = ImageFont.load_default()
        
        # Draw new text
        y = 600
        for line in new_text_lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            x = (self.width - (bbox[2] - bbox[0])) // 2
            
            # Shadow
            draw.text((x+3, y+3), line, fill='#000000', font=font)
            draw.text((x, y), line, fill='#FFFFFF', font=font)
            
            y += 90
        
        # Save
        if not output_path:
            output_path = frames[frame_number]
        
        img.save(output_path)
        print(f"✅ Updated frame {frame_number}")
        
        return output_path
    
    def remove_frame(self, frame_number):
        """Remove a frame from the sequence"""
        frames = self.get_current_frames()
        
        if frame_number >= len(frames):
            print(f"❌ Frame {frame_number} doesn't exist!")
            return
        
        # Delete the frame
        os.remove(frames[frame_number])
        print(f"✅ Removed frame {frame_number}")
        
        # Renumber remaining frames
        self.renumber_frames()
    
    def duplicate_frame(self, frame_number, insert_after=None):
        """Duplicate a frame"""
        frames = self.get_current_frames()
        
        if frame_number >= len(frames):
            print(f"❌ Frame {frame_number} doesn't exist!")
            return
        
        # Copy frame
        source = frames[frame_number]
        if insert_after is None:
            insert_after = frame_number
        
        # Create new filename
        new_path = f"edits/frames/frame_dup_{datetime.now().timestamp()}.png"
        img = Image.open(source)
        img.save(new_path)
        
        print(f"✅ Duplicated frame {frame_number}")
        
        # Renumber frames
        self.renumber_frames()
    
    def replace_frame_content(self, frame_number, new_image_path):
        """Replace a frame with a new image"""
        frames = self.get_current_frames()
        
        if frame_number >= len(frames):
            print(f"❌ Frame {frame_number} doesn't exist!")
            return
        
        # Load and resize new image
        new_img = Image.open(new_image_path)
        new_img = new_img.resize((self.width, self.height), Image.Resampling.LANCZOS)
        
        # Save over existing frame
        new_img.save(frames[frame_number])
        print(f"✅ Replaced frame {frame_number}")
    
    def add_overlay_to_frame(self, frame_number, overlay_text, position='bottom'):
        """Add text overlay to existing frame"""
        frames = self.get_current_frames()
        
        if frame_number >= len(frames):
            print(f"❌ Frame {frame_number} doesn't exist!")
            return
        
        # Load frame
        img = Image.open(frames[frame_number])
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 50)
        except:
            font = ImageFont.load_default()
        
        # Calculate position
        bbox = draw.textbbox((0, 0), overlay_text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        
        if position == 'bottom':
            y = self.height - 200
        elif position == 'top':
            y = 100
        else:  # center
            y = self.height // 2
        
        # Draw background box
        padding = 20
        draw.rounded_rectangle(
            [x - padding, y - padding, 
             x + text_width + padding, y + 60 + padding],
            radius=10,
            fill=(0, 0, 0, 180)
        )
        
        # Draw text
        draw.text((x, y), overlay_text, fill='#FFFFFF', font=font)
        
        # Save
        img.save(frames[frame_number])
        print(f"✅ Added overlay to frame {frame_number}")
    
    def change_frame_duration(self, frame_durations):
        """Change how long each frame appears
        
        Args:
            frame_durations: dict of {frame_number: duration_in_seconds}
        """
        self.frame_durations = frame_durations
        print(f"✅ Updated frame durations")
    
    def get_current_frames(self):
        """Get current frame list"""
        frame_dir = "edits/frames"
        frames = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])
        return [os.path.join(frame_dir, f) for f in frames]
    
    def renumber_frames(self):
        """Renumber frames to be sequential"""
        frames = self.get_current_frames()
        
        # Sort by modification time to maintain order
        frames.sort(key=lambda x: os.path.getmtime(x))
        
        # Rename to temporary names first
        temp_names = []
        for i, old_path in enumerate(frames):
            temp_path = f"edits/frames/temp_{i:03d}.png"
            os.rename(old_path, temp_path)
            temp_names.append(temp_path)
        
        # Rename to final names
        for i, temp_path in enumerate(temp_names):
            final_path = f"edits/frames/frame_{i:03d}.png"
            os.rename(temp_path, final_path)
        
        print(f"✅ Renumbered {len(frames)} frames")
    
    def rebuild_video(self, output_name=None, custom_durations=None):
        """Rebuild video from edited frames"""
        frames = self.get_current_frames()
        
        if not frames:
            print("❌ No frames found!")
            return
        
        print(f"\n🎬 Rebuilding video from {len(frames)} frames...")
        
        # Default duration or custom
        if custom_durations:
            durations = custom_durations
        else:
            # Default 2 seconds per frame
            durations = {i: 2.0 for i in range(len(frames))}
        
        # Create concat file
        concat_file = "edits/concat.txt"
        with open(concat_file, 'w') as f:
            for i, frame_path in enumerate(frames):
                duration = durations.get(i, 2.0)
                f.write(f"file '{os.path.abspath(frame_path)}'\n")
                f.write(f"duration {duration}\n")
            # Last frame
            f.write(f"file '{os.path.abspath(frames[-1])}'\n")
        
        # Output path
        if not output_name:
            output_name = f"{self.project_name}_edited"
        
        output_path = f"output/{output_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        
        # FFmpeg command
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-vf', f'fps={self.fps},format=yuv420p',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            output_path
        ]
        
        subprocess.run(cmd, check=True)
        print(f"✅ Video rebuilt: {output_path}")
        
        return output_path
    
    def create_edit_config(self):
        """Save current edit configuration"""
        frames = self.get_current_frames()
        
        config = {
            'project': self.project_name,
            'frames': [os.path.basename(f) for f in frames],
            'durations': getattr(self, 'frame_durations', {}),
            'timestamp': datetime.now().isoformat()
        }
        
        config_path = f"edits/edit_config_{self.project_name}.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Saved edit configuration: {config_path}")
        
        return config_path


# Example usage and common edits
if __name__ == "__main__":
    # Initialize editor
    editor = VideoEditHelper("euler_visualization")
    
    print("🎬 Video Edit Helper")
    print("=" * 50)
    
    # Example workflow:
    print("\n1️⃣ First, extract frames from your video:")
    print("   editor.extract_frames_from_video('output/your_video.mp4')")
    
    print("\n2️⃣ Preview what frames you have:")
    print("   editor.preview_frames(editor.get_current_frames())")
    
    print("\n3️⃣ Common edits:")
    
    print("\n   📝 Change text in frame 0:")
    print("   editor.edit_text_frame(0, ['New Title', 'New Subtitle'])")
    
    print("\n   ❌ Remove frame 3:")
    print("   editor.remove_frame(3)")
    
    print("\n   ➕ Add overlay to frame 2:")
    print("   editor.add_overlay_to_frame(2, 'MIND BLOWN 🤯', position='bottom')")
    
    print("\n   ⏱️ Change frame durations:")
    print("   editor.change_frame_duration({0: 3, 1: 2, 2: 4, 3: 2})")
    
    print("\n   📄 Duplicate frame 1:")
    print("   editor.duplicate_frame(1)")
    
    print("\n4️⃣ Rebuild the video:")
    print("   editor.rebuild_video('my_edited_version')")
    
    print("\n" + "=" * 50)
    print("Interactive mode - try these commands!")
    
    # Create a test video for demonstration
    test_frames = []
    for i in range(5):
        img = Image.new('RGB', (1080, 1920), '#0a0a0a')
        draw = ImageDraw.Draw(img)
        draw.text((540, 960), f"Frame {i}", fill='#FFFFFF', anchor='mm', 
                 font=ImageFont.load_default())
        path = f"edits/frames/frame_{i:03d}.png"
        img.save(path)
        test_frames.append(path)
    
    print(f"\n✅ Created {len(test_frames)} test frames in edits/frames/")
    print("You can now test the editing functions!")
