#!/usr/bin/env python3
"""
Automated video creation for AI model comparisons
Optimized for TikTok/Reels/Shorts format (9:16 aspect ratio)
"""

import os
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy.editor import *
import numpy as np
from datetime import datetime

class VideoAutomator:
    def __init__(self):
        self.video_width = 1080  # 9:16 aspect ratio
        self.video_height = 1920
        self.fps = 30
        
        # Define consistent styling
        self.colors = {
            'claude': '#6B46C1',  # Purple
            'gpt4': '#10A37F',    # Green  
            'gemini': '#4285F4',  # Blue
            'background': '#0F0F0F',
            'text': '#FFFFFF'
        }
        
    def create_intro_slide(self, prompt_title: str, duration: int = 2):
        """Create engaging intro slide"""
        
        # Create base image
        img = Image.new('RGB', (self.video_width, self.video_height), self.colors['background'])
        draw = ImageDraw.Draw(img)
        
        # Add gradient background
        for i in range(self.video_height):
            color_value = int(15 + (25 * (i / self.video_height)))
            draw.rectangle([0, i, self.video_width, i+1], fill=(color_value, color_value, color_value))
        
        # Load fonts (you'll need to have these)
        try:
            title_font = ImageFont.truetype("Arial-Bold.ttf", 80)
            subtitle_font = ImageFont.truetype("Arial.ttf", 50)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # Add text with shadow effect
        title_text = "AI BUILD BATTLE"
        subtitle_text = f"Challenge: {prompt_title}"
        prompt_text = "Same prompt. Different vibes."
        
        # Center text
        bbox = draw.textbbox((0, 0), title_text, font=title_font)
        x = (self.video_width - (bbox[2] - bbox[0])) // 2
        
        # Title with glow effect
        for offset in range(3, 0, -1):
            draw.text((x-offset, 600-offset), title_text, 
                     fill=(100, 100, 100, 128), font=title_font)
        draw.text((x, 600), title_text, fill=self.colors['text'], font=title_font)
        
        # Subtitle
        bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
        x = (self.video_width - (bbox[2] - bbox[0])) // 2
        draw.text((x, 750), subtitle_text, fill=self.colors['text'], font=subtitle_font)
        
        # Prompt text
        bbox = draw.textbbox((0, 0), prompt_text, font=subtitle_font)
        x = (self.video_width - (bbox[2] - bbox[0])) // 2
        draw.text((x, 850), prompt_text, fill=(200, 200, 200), font=subtitle_font)
        
        # Add emoji elements
        draw.text((100, 1000), "🤖", font=ImageFont.truetype("Arial.ttf", 100))
        draw.text((880, 1000), "💻", font=ImageFont.truetype("Arial.ttf", 100))
        draw.text((490, 1000), "⚔️", font=ImageFont.truetype("Arial.ttf", 100))
        
        # Save and create video clip
        intro_path = "temp_intro.png"
        img.save(intro_path)
        
        return ImageClip(intro_path).set_duration(duration)
    
    def create_model_reveal(self, model_name: str, screenshot_path: str, duration: int = 3):
        """Create individual model reveal with animation"""
        
        # Load and resize screenshot
        screenshot = Image.open(screenshot_path)
        
        # Calculate dimensions to fit in frame with padding
        target_width = int(self.video_width * 0.85)
        target_height = int(self.video_height * 0.5)
        
        # Resize maintaining aspect ratio
        screenshot.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Create frame
        frame = Image.new('RGB', (self.video_width, self.video_height), self.colors['background'])
        
        # Paste screenshot centered
        x_offset = (self.video_width - screenshot.width) // 2
        y_offset = (self.video_height - screenshot.height) // 2
        
        # Add shadow/glow effect
        shadow = Image.new('RGBA', screenshot.size, (0, 0, 0, 0))
        shadow.paste((0, 0, 0, 180), (0, 0, screenshot.width, screenshot.height))
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))
        
        frame.paste(shadow, (x_offset + 10, y_offset + 10), shadow)
        frame.paste(screenshot, (x_offset, y_offset))
        
        # Add model label
        draw = ImageDraw.Draw(frame)
        label_font = ImageFont.truetype("Arial-Bold.ttf", 70)
        
        # Model name with brand color
        model_display = model_name.upper()
        bbox = draw.textbbox((0, 0), model_display, font=label_font)
        x = (self.video_width - (bbox[2] - bbox[0])) // 2
        
        # Draw label background
        padding = 20
        draw.rounded_rectangle(
            [x - padding, 200 - padding, 
             x + (bbox[2] - bbox[0]) + padding, 200 + (bbox[3] - bbox[1]) + padding],
            radius=20,
            fill=self.colors.get(model_name, '#333333')
        )
        
        draw.text((x, 200), model_display, fill=self.colors['text'], font=label_font)
        
        # Add reaction text
        reactions = {
            'claude': "Dark mode vibes 🌙",
            'gpt4': "Clean & minimal ✨",
            'gemini': "Colorful energy 🎨"
        }
        
        reaction_font = ImageFont.truetype("Arial.ttf", 50)
        reaction = reactions.get(model_name, "Unique style 🎯")
        bbox = draw.textbbox((0, 0), reaction, font=reaction_font)
        x = (self.video_width - (bbox[2] - bbox[0])) // 2
        draw.text((x, self.video_height - 300), reaction, 
                 fill=(200, 200, 200), font=reaction_font)
        
        # Save and create clip
        reveal_path = f"temp_reveal_{model_name}.png"
        frame.save(reveal_path)
        
        # Create clip with zoom animation
        clip = ImageClip(reveal_path).set_duration(duration)
        
        # Add zoom in effect
        clip = clip.resize(lambda t: 1 + 0.05 * t)
        
        return clip
    
    def create_comparison_grid(self, screenshots: Dict[str, str], duration: int = 5):
        """Create side-by-side comparison"""
        
        # Create base frame
        frame = Image.new('RGB', (self.video_width, self.video_height), self.colors['background'])
        draw = ImageDraw.Draw(frame)
        
        # Add title
        title_font = ImageFont.truetype("Arial-Bold.ttf", 60)
        title = "SPOT THE DIFFERENCES"
        bbox = draw.textbbox((0, 0), title, font=title_font)
        x = (self.video_width - (bbox[2] - bbox[0])) // 2
        draw.text((x, 100), title, fill=self.colors['text'], font=title_font)
        
        # Calculate grid layout
        num_models = len(screenshots)
        if num_models <= 2:
            cols = 1
            rows = 2
        elif num_models <= 4:
            cols = 2
            rows = 2
        else:
            cols = 2
            rows = 3
        
        cell_width = self.video_width // cols
        cell_height = (self.video_height - 300) // rows  # Leave space for title and footer
        
        # Place screenshots in grid
        for idx, (model_name, screenshot_path) in enumerate(screenshots.items()):
            row = idx // cols
            col = idx % cols
            
            # Load and resize screenshot
            img = Image.open(screenshot_path)
            img.thumbnail((int(cell_width * 0.9), int(cell_height * 0.8)), 
                         Image.Resampling.LANCZOS)
            
            # Calculate position
            x = col * cell_width + (cell_width - img.width) // 2
            y = 250 + row * cell_height + (cell_height - img.height) // 2
            
            # Add border with model color
            border_img = Image.new('RGB', 
                                  (img.width + 10, img.height + 10), 
                                  self.colors.get(model_name, '#333333'))
            border_img.paste(img, (5, 5))
            
            frame.paste(border_img, (x, y))
            
            # Add model label
            label_font = ImageFont.truetype("Arial.ttf", 40)
            draw.text((x + 10, y - 40), model_name.upper(), 
                     fill=self.colors.get(model_name, '#FFFFFF'), 
                     font=label_font)
        
        # Add call to action
        cta_font = ImageFont.truetype("Arial-Bold.ttf", 50)
        cta = "Which is YOUR favorite? 👇"
        bbox = draw.textbbox((0, 0), cta, font=cta_font)
        x = (self.video_width - (bbox[2] - bbox[0])) // 2
        draw.text((x, self.video_height - 150), cta, 
                 fill=self.colors['text'], font=cta_font)
        
        # Save and create clip
        grid_path = "temp_grid.png"
        frame.save(grid_path)
        
        return ImageClip(grid_path).set_duration(duration)
    
    def add_background_music(self, video_clip):
        """Add trending TikTok-style background music"""
        
        # You would need to have a library of copyright-free music
        # or use TikTok's music library when uploading
        
        # For now, we'll add a simple beat using moviepy
        # In production, use actual trending audio
        
        return video_clip
    
    def create_comparison_video(self, screenshots: Dict[str, str], 
                              prompt_title: str, output_path: str):
        """Assemble the complete video"""
        
        clips = []
        
        # 1. Intro (2 seconds)
        intro_clip = self.create_intro_slide(prompt_title, duration=2)
        clips.append(intro_clip)
        
        # 2. Individual reveals (2.5 seconds each)
        for model_name, screenshot_path in screenshots.items():
            reveal_clip = self.create_model_reveal(model_name, screenshot_path, duration=2.5)
            
            # Add transition
            if clips:
                reveal_clip = reveal_clip.crossfadein(0.3)
            clips.append(reveal_clip)
        
        # 3. Comparison grid (5 seconds)
        grid_clip = self.create_comparison_grid(screenshots, duration=5)
        grid_clip = grid_clip.crossfadein(0.3)
        clips.append(grid_clip)
        
        # 4. Outro (2 seconds)
        outro_clip = self.create_outro_slide(duration=2)
        outro_clip = outro_clip.crossfadein(0.3)
        clips.append(outro_clip)
        
        # Concatenate all clips
        final_video = concatenate_videoclips(clips)
        
        # Add background music
        final_video = self.add_background_music(final_video)
        
        # Export with optimal settings for social media
        final_video.write_videofile(
            output_path,
            codec='libx264',
            fps=self.fps,
            preset='fast',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        # Clean up temp files
        for temp_file in os.listdir('.'):
            if temp_file.startswith('temp_'):
                os.remove(temp_file)
        
        return output_path
    
    def create_outro_slide(self, duration: int = 2):
        """Create engaging outro with call to action"""
        
        img = Image.new('RGB', (self.video_width, self.video_height), self.colors['background'])
        draw = ImageDraw.Draw(img)
        
        # Add gradient
        for i in range(self.video_height):
            color_value = int(15 + (25 * (i / self.video_height)))
            draw.rectangle([0, i, self.video_width, i+1], 
                          fill=(color_value, color_value, color_value))
        
        # Add text
        font_large = ImageFont.truetype("Arial-Bold.ttf", 70)
        font_medium = ImageFont.truetype("Arial.ttf", 50)
        
        texts = [
            ("FOLLOW FOR MORE", font_large, self.colors['text'], 700),
            ("AI BATTLES", font_large, self.colors['text'], 800),
            ("Drop your favorite in comments!", font_medium, (200, 200, 200), 1000),
            ("Which AI is your spirit animal?", font_medium, (200, 200, 200), 1100)
        ]
        
        for text, font, color, y_pos in texts:
            bbox = draw.textbbox((0, 0), text, font=font)
            x = (self.video_width - (bbox[2] - bbox[0])) // 2
            draw.text((x, y_pos), text, fill=color, font=font)
        
        # Add emojis
        emoji_font = ImageFont.truetype("Arial.ttf", 80)
        emojis = "🤖 💭 🎨 💻 ⚡"
        bbox = draw.textbbox((0, 0), emojis, font=emoji_font)
        x = (self.video_width - (bbox[2] - bbox[0])) // 2
        draw.text((x, 1300), emojis, font=emoji_font)
        
        outro_path = "temp_outro.png"
        img.save(outro_path)
        
        return ImageClip(outro_path).set_duration(duration)


# Usage example
if __name__ == "__main__":
    automator = VideoAutomator()
    
    # Example screenshots dictionary
    screenshots = {
        "claude": "screenshots/claude_calculator.png",
        "gpt4": "screenshots/gpt4_calculator.png",
        "gemini": "screenshots/gemini_calculator.png"
    }
    
    output_path = automator.create_comparison_video(
        screenshots=screenshots,
        prompt_title="Calculator App",
        output_path="output/calculator_comparison.mp4"
    )
    
    print(f"Video created: {output_path}")
