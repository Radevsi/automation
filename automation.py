#!/usr/bin/env python3
"""
Simple video creation using FFmpeg directly (no MoviePy required)
This is more reliable and faster than MoviePy
"""

import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import json
from datetime import datetime
import numpy as np

class SimpleVideoCreator:
    def __init__(self):
        self.width = 1080  # 9:16 for TikTok/Reels
        self.height = 1920
        self.fps = 30
        self.temp_dir = "temp_frames"
        
        # Create temp directory
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs("output", exist_ok=True)
        os.makedirs("screenshots", exist_ok=True)
        
        # Model colors for branding
        self.colors = {
            'claude': '#6B46C1',
            'gpt4': '#10A37F', 
            'gemini': '#4285F4',
            'llama': '#FF6B6B'
        }
        
    def create_text_image(self, text_lines, output_path, bg_color='#0F0F0F', 
                         text_color='#FFFFFF', font_size=60):
        """Create a simple text image"""
        img = Image.new('RGB', (self.width, self.height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Try to use a nice font, fall back to default if not available
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Calculate text positions
        y_position = self.height // 2 - (len(text_lines) * font_size)
        
        for line in text_lines:
            # Get text dimensions
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x_position = (self.width - text_width) // 2
            
            # Draw text with shadow for better visibility
            shadow_offset = 3
            draw.text((x_position + shadow_offset, y_position + shadow_offset), 
                     line, fill='#000000', font=font)
            draw.text((x_position, y_position), line, fill=text_color, font=font)
            
            y_position += font_size + 20
        
        img.save(output_path)
        return output_path
    
    def create_screenshot_frame(self, screenshot_path, model_name, output_path):
        """Create a frame showing a screenshot with model label"""
        # Create base frame
        frame = Image.new('RGB', (self.width, self.height), '#0F0F0F')
        draw = ImageDraw.Draw(frame)
        
        # Add model label at top
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
            small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        except:
            font = ImageFont.load_default()
            small_font = font
        
        # Model name
        model_color = self.colors.get(model_name, '#FFFFFF')
        text = model_name.upper()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x_position = (self.width - text_width) // 2
        
        # Draw colored background for label
        padding = 30
        draw.rounded_rectangle(
            [x_position - padding, 100, 
             x_position + text_width + padding, 200],
            radius=20,
            fill=model_color
        )
        draw.text((x_position, 120), text, fill='#FFFFFF', font=font)
        
        # Load and place screenshot if it exists
        if os.path.exists(screenshot_path):
            screenshot = Image.open(screenshot_path)
            
            # Resize to fit
            max_width = int(self.width * 0.9)
            max_height = int(self.height * 0.6)
            screenshot.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Center the screenshot
            x_offset = (self.width - screenshot.width) // 2
            y_offset = 300
            
            # Add a border
            border_size = 5
            bordered = Image.new('RGB', 
                               (screenshot.width + 2*border_size, 
                                screenshot.height + 2*border_size), 
                               model_color)
            bordered.paste(screenshot, (border_size, border_size))
            
            frame.paste(bordered, (x_offset - border_size, y_offset))
        else:
            # Placeholder if screenshot doesn't exist
            draw.text((self.width//2 - 200, self.height//2), 
                     "[Screenshot would go here]", 
                     fill='#666666', font=small_font)
        
        # Add descriptive text
        descriptions = {
            'claude': "Dark mode vibes 🌙",
            'gpt4': "Clean & minimal ✨",
            'gemini': "Colorful energy 🎨",
            'llama': "Open source power 🔥"
        }
        
        desc = descriptions.get(model_name, "Unique approach 🎯")
        bbox = draw.textbbox((0, 0), desc, font=small_font)
        text_width = bbox[2] - bbox[0]
        x_position = (self.width - text_width) // 2
        draw.text((x_position, self.height - 200), desc, fill='#CCCCCC', font=small_font)
        
        frame.save(output_path)
        return output_path
    
    def create_comparison_grid(self, screenshots, output_path):
        """Create a grid showing all screenshots side by side"""
        frame = Image.new('RGB', (self.width, self.height), '#0F0F0F')
        draw = ImageDraw.Draw(frame)
        
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
            small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
        except:
            font = ImageFont.load_default()
            small_font = font
        
        # Title
        title = "SPOT THE DIFFERENCES"
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text(((self.width - text_width) // 2, 80), title, fill='#FFFFFF', font=font)
        
        # Calculate grid layout
        num_screenshots = len(screenshots)
        if num_screenshots <= 2:
            cols, rows = 1, 2
        elif num_screenshots <= 4:
            cols, rows = 2, 2
        else:
            cols, rows = 2, 3
            
        cell_width = self.width // cols
        cell_height = (self.height - 300) // rows
        
        # Place screenshots
        for idx, (model_name, screenshot_path) in enumerate(screenshots.items()):
            row = idx // cols
            col = idx % cols
            
            # Cell position
            cell_x = col * cell_width
            cell_y = 250 + row * cell_height
            
            # Model label
            model_color = self.colors.get(model_name, '#FFFFFF')
            draw.text((cell_x + 20, cell_y), model_name.upper(), 
                     fill=model_color, font=small_font)
            
            # Mini screenshot placeholder
            preview_box = [
                cell_x + 20,
                cell_y + 50,
                cell_x + cell_width - 20,
                cell_y + cell_height - 20
            ]
            draw.rectangle(preview_box, outline=model_color, width=3)
            draw.text((cell_x + 30, cell_y + cell_height // 2), 
                     "[Preview]", fill='#666666', font=small_font)
        
        # Call to action
        cta = "Which style do YOU prefer? 👇"
        bbox = draw.textbbox((0, 0), cta, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text(((self.width - text_width) // 2, self.height - 150), 
                 cta, fill='#FFFFFF', font=font)
        
        frame.save(output_path)
        return output_path
    
    def create_video_from_images(self, image_paths, durations, output_path, 
                                transition_duration=0.5):
        """Use FFmpeg to create video from images"""
        
        # Create a concat file for FFmpeg
        concat_file = os.path.join(self.temp_dir, "concat.txt")
        with open(concat_file, 'w') as f:
            for img_path, duration in zip(image_paths, durations):
                f.write(f"file '{os.path.abspath(img_path)}'\n")
                f.write(f"duration {duration}\n")
            # Add last image again to ensure it displays
            f.write(f"file '{os.path.abspath(image_paths[-1])}'\n")
        
        # FFmpeg command to create video
        cmd = [
            'ffmpeg',
            '-y',  # Overwrite output
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-vf', f'fps={self.fps},format=yuv420p',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            output_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"Video created successfully: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error creating video: {e}")
            print(f"Error output: {e.stderr.decode()}")
            
            # Fallback: create simple slideshow
            print("Trying simpler approach...")
            self.create_simple_slideshow(image_paths, durations, output_path)
    
    def create_simple_slideshow(self, image_paths, durations, output_path):
        """Fallback method: Create a simple slideshow without transitions"""
        
        # Create individual video segments
        segment_files = []
        
        for i, (img_path, duration) in enumerate(zip(image_paths, durations)):
            segment_file = os.path.join(self.temp_dir, f"segment_{i}.mp4")
            
            cmd = [
                'ffmpeg',
                '-y',
                '-loop', '1',
                '-i', img_path,
                '-c:v', 'libx264',
                '-t', str(duration),
                '-pix_fmt', 'yuv420p',
                '-vf', f'scale={self.width}:{self.height}',
                segment_file
            ]
            
            subprocess.run(cmd, check=True)
            segment_files.append(segment_file)
        
        # Concatenate segments
        concat_file = os.path.join(self.temp_dir, "segments.txt")
        with open(concat_file, 'w') as f:
            for segment in segment_files:
                f.write(f"file '{os.path.abspath(segment)}'\n")
        
        cmd = [
            'ffmpeg',
            '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-c', 'copy',
            output_path
        ]
        
        subprocess.run(cmd, check=True)
        
        # Clean up segments
        for segment in segment_files:
            os.remove(segment)
    
    def create_comparison_video(self, prompt_title, screenshots):
        """Main method to create the full comparison video"""
        
        frames = []
        durations = []
        
        # 1. Intro slide (2 seconds)
        intro_path = os.path.join(self.temp_dir, "01_intro.png")
        self.create_text_image(
            ["AI BUILD BATTLE", "", f"Challenge: {prompt_title}", "", 
             "Same prompt.", "Different vibes.", "", "🤖 ⚔️ 💻"],
            intro_path
        )
        frames.append(intro_path)
        durations.append(2)
        
        # 2. Individual model reveals (2.5 seconds each)
        for i, (model_name, screenshot_path) in enumerate(screenshots.items()):
            frame_path = os.path.join(self.temp_dir, f"02_model_{i}_{model_name}.png")
            self.create_screenshot_frame(screenshot_path, model_name, frame_path)
            frames.append(frame_path)
            durations.append(2.5)
        
        # 3. Comparison grid (4 seconds)
        grid_path = os.path.join(self.temp_dir, "03_grid.png")
        self.create_comparison_grid(screenshots, grid_path)
        frames.append(grid_path)
        durations.append(4)
        
        # 4. Outro (2 seconds)
        outro_path = os.path.join(self.temp_dir, "04_outro.png")
        self.create_text_image(
            ["FOLLOW FOR MORE", "AI BATTLES", "", 
             "Drop your favorite", "in the comments!", "", 
             "🤖 💭 🎨 💻 ⚡"],
            outro_path
        )
        frames.append(outro_path)
        durations.append(2)
        
        # Create video
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"output/ai_battle_{prompt_title.replace(' ', '_')}_{timestamp}.mp4"
        
        self.create_video_from_images(frames, durations, output_path)
        
        # Clean up temp frames
        for frame in frames:
            if os.path.exists(frame):
                os.remove(frame)
        
        return output_path

# Test the video creator
if __name__ == "__main__":
    creator = SimpleVideoCreator()
    
    # Create dummy screenshots for testing
    test_screenshots = {}
    for model in ['claude', 'gpt4', 'gemini']:
        # Create a simple test image
        test_img_path = f"screenshots/test_{model}.png"
        img = Image.new('RGB', (800, 600), '#FFFFFF')
        draw = ImageDraw.Draw(img)
        draw.text((50, 50), f"{model.upper()} Output", fill='#000000')
        draw.rectangle([20, 20, 780, 580], outline='#000000', width=2)
        img.save(test_img_path)
        test_screenshots[model] = test_img_path
    
    # Create video
    output = creator.create_comparison_video("Calculator App", test_screenshots)
    print(f"Created video: {output}")
    
    # Quick test without screenshots
    print("\nTesting without screenshots...")
    empty_screenshots = {
        'claude': 'nonexistent1.png',
        'gpt4': 'nonexistent2.png',
        'gemini': 'nonexistent3.png'
    }
    output2 = creator.create_comparison_video("Todo App", empty_screenshots)
    print(f"Created video: {output2}")
