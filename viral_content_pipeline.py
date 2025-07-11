#!/usr/bin/env python3
"""
Streamlined pipeline for creating viral AI comparison videos
Designed for quick production with pre-built projects
"""

import os
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import shutil

class ViralContentPipeline:
    def __init__(self, project_name="euler_equation"):
        self.project_name = project_name
        self.width = 1080  # TikTok/Reels format
        self.height = 1920
        self.fps = 30
        
        # Setup directories
        self.setup_directories()
        
        # Model branding
        self.models = {
            'claude': {
                'color': '#6B46C1',
                'tagline': 'Dark mode enthusiast 🌙',
                'style': 'Sophisticated'
            },
            'gpt4': {
                'color': '#10A37F',
                'tagline': 'Minimalist master ✨',
                'style': 'Clean'
            },
            'gemini': {
                'color': '#4285F4',
                'tagline': 'Color lover 🎨',
                'style': 'Playful'
            },
            'llama': {
                'color': '#FF6B6B',
                'tagline': 'Open source hero 🦙',
                'style': 'Practical'
            }
        }
    
    def setup_directories(self):
        """Create necessary directories"""
        dirs = ['inputs', 'temp', 'output', 'screenshots']
        for d in dirs:
            os.makedirs(d, exist_ok=True)
    
    def capture_screenshot(self, html_file, output_path):
        """Capture screenshot of HTML file using Playwright"""
        cmd = [
            "npx", "playwright", "screenshot",
            f"file://{os.path.abspath(html_file)}",
            output_path,
            "--viewport-size=1200,800",
            "--wait-for-timeout=3000"
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✓ Screenshot captured: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Screenshot failed: {e}")
            # Create placeholder
            self.create_placeholder_screenshot(output_path)
    
    def create_placeholder_screenshot(self, output_path):
        """Create a placeholder if screenshot fails"""
        img = Image.new('RGB', (1200, 800), '#1a1a1a')
        draw = ImageDraw.Draw(img)
        draw.text((600, 400), "Visualization", fill='#666', anchor='mm')
        img.save(output_path)
    
    def create_storyline_1_personality(self, model_data):
        """Vision 1: The Personality Test approach"""
        frames = []
        durations = []
        
        # 1. Hook (2s)
        hook = self.create_text_frame([
            "I asked 4 AIs to visualize",
            "the SAME math equation...",
            "",
            "Their personalities? 🤯"
        ], style='dramatic')
        frames.append(hook)
        durations.append(2)
        
        # 2. Quick personality reveals (2s each)
        for model, data in model_data.items():
            frame = self.create_personality_reveal(model, data)
            frames.append(frame)
            durations.append(2)
        
        # 3. Split screen comparison (4s)
        split = self.create_split_screen(model_data, title="Same equation. Different vibes.")
        frames.append(split)
        durations.append(4)
        
        # 4. CTA (3s)
        cta = self.create_text_frame([
            "Which AI matches",
            "YOUR coding style?",
            "",
            "Comment below! 👇",
            "#AIPersonality #CodingStyle"
        ], style='cta')
        frames.append(cta)
        durations.append(3)
        
        return frames, durations
    
    def create_storyline_2_plot_twist(self, model_data):
        """Vision 2: The Plot Twist approach"""
        frames = []
        durations = []
        
        # 1. Setup - Show identical equation (3s)
        equation_frame = self.create_equation_frame(
            "Every AI gave me this:",
            "e^(iπ) + 1 = 0"
        )
        frames.append(equation_frame)
        durations.append(3)
        
        # 2. Twist setup (2s)
        twist = self.create_text_frame([
            "But when I asked them",
            "to VISUALIZE it..."
        ], style='suspense')
        frames.append(twist)
        durations.append(2)
        
        # 3. Dramatic reveals with reactions (2s each)
        reactions = [
            "Claude went FULL cyberpunk",
            "GPT-4 kept it scholarly", 
            "Gemini made it a party",
            "Llama kept it real"
        ]
        
        for i, (model, data) in enumerate(model_data.items()):
            frame = self.create_dramatic_reveal(model, data, reactions[i])
            frames.append(frame)
            durations.append(2)
        
        # 4. Mind blown moment (3s)
        mind_blown = self.create_text_frame([
            "Same math.",
            "Same prompt.",
            "TOTALLY different results.",
            "",
            "Why? 🤯"
        ], style='dramatic')
        frames.append(mind_blown)
        durations.append(3)
        
        return frames, durations
    
    def create_storyline_3_competition(self, model_data):
        """Vision 3: The Competition approach"""
        frames = []
        durations = []
        
        # 1. Hook (2s)
        hook = self.create_text_frame([
            "Math teachers HATE",
            "this one trick...",
            "",
            "AI Visualization Battle! ⚔️"
        ], style='dramatic')
        frames.append(hook)
        durations.append(2)
        
        # 2. Scoring rounds (2.5s each)
        scores = {
            'claude': {'style': 9, 'clarity': 8, 'creativity': 10},
            'gpt4': {'style': 7, 'clarity': 10, 'creativity': 6},
            'gemini': {'style': 8, 'clarity': 7, 'creativity': 9},
            'llama': {'style': 6, 'clarity': 9, 'creativity': 7}
        }
        
        for model, data in model_data.items():
            frame = self.create_scoring_frame(model, data, scores.get(model, {}))
            frames.append(frame)
            durations.append(2.5)
        
        # 3. Winner announcement (3s)
        winner = self.create_winner_frame()
        frames.append(winner)
        durations.append(3)
        
        # 4. CTA (2s)
        cta = self.create_text_frame([
            "Try it yourself!",
            "Link in bio 🔗",
            "",
            "#AIBattle #MathViz"
        ], style='cta')
        frames.append(cta)
        durations.append(2)
        
        return frames, durations
    
    def create_text_frame(self, lines, style='default'):
        """Create a text frame with different styles"""
        img = Image.new('RGB', (self.width, self.height), '#0a0a0a')
        draw = ImageDraw.Draw(img)
        
        # Style configurations
        styles = {
            'dramatic': {'size': 70, 'color': '#FFFFFF', 'y_start': 600},
            'suspense': {'size': 80, 'color': '#FFD700', 'y_start': 700},
            'cta': {'size': 60, 'color': '#00FF88', 'y_start': 650},
            'default': {'size': 60, 'color': '#FFFFFF', 'y_start': 600}
        }
        
        config = styles.get(style, styles['default'])
        
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", config['size'])
        except:
            font = ImageFont.load_default()
        
        y = config['y_start']
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            x = (self.width - (bbox[2] - bbox[0])) // 2
            
            # Add shadow
            draw.text((x+3, y+3), line, fill='#000000', font=font)
            draw.text((x, y), line, fill=config['color'], font=font)
            
            y += config['size'] + 30
        
        # Save
        path = f"temp/text_{datetime.now().timestamp()}.png"
        img.save(path)
        return path
    
    def create_personality_reveal(self, model, data):
        """Create personality-focused reveal frame"""
        img = Image.new('RGB', (self.width, self.height), '#0a0a0a')
        draw = ImageDraw.Draw(img)
        
        model_info = self.models[model]
        
        # Model name with color
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 90)
            desc_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 50)
        except:
            title_font = ImageFont.load_default()
            desc_font = title_font
        
        # Title
        title = model.upper()
        bbox = draw.textbbox((0, 0), title, font=title_font)
        x = (self.width - (bbox[2] - bbox[0])) // 2
        
        # Colored background
        draw.rounded_rectangle([x-40, 150, x+bbox[2]-bbox[0]+40, 280],
                              radius=20, fill=model_info['color'])
        draw.text((x, 170), title, fill='#FFFFFF', font=title_font)
        
        # Screenshot
        if 'screenshot' in data and os.path.exists(data['screenshot']):
            ss = Image.open(data['screenshot'])
            ss.thumbnail((900, 600), Image.Resampling.LANCZOS)
            x_offset = (self.width - ss.width) // 2
            img.paste(ss, (x_offset, 350))
        
        # Personality traits
        traits = [
            model_info['tagline'],
            f"Style: {model_info['style']}",
            f"Vibe: {data.get('vibe', 'Unique')}"
        ]
        
        y = 1100
        for trait in traits:
            bbox = draw.textbbox((0, 0), trait, font=desc_font)
            x = (self.width - (bbox[2] - bbox[0])) // 2
            draw.text((x, y), trait, fill='#CCCCCC', font=desc_font)
            y += 80
        
        path = f"temp/reveal_{model}_{datetime.now().timestamp()}.png"
        img.save(path)
        return path
    
    def create_split_screen(self, model_data, title=""):
        """Create split screen comparison"""
        img = Image.new('RGB', (self.width, self.height), '#0a0a0a')
        draw = ImageDraw.Draw(img)
        
        # Title
        if title:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
            except:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), title, font=font)
            x = (self.width - (bbox[2] - bbox[0])) // 2
            draw.text((x, 80), title, fill='#FFFFFF', font=font)
        
        # 2x2 grid
        positions = [(0, 0), (1, 0), (0, 1), (1, 1)]
        cell_w = self.width // 2
        cell_h = (self.height - 200) // 2
        
        for i, (model, data) in enumerate(model_data.items()):
            if i >= 4:
                break
                
            col, row = positions[i]
            x = col * cell_w
            y = 200 + row * cell_h
            
            # Model label
            model_color = self.models[model]['color']
            draw.rectangle([x+10, y+10, x+cell_w-10, y+60],
                          fill=model_color)
            draw.text((x+20, y+20), model.upper(), fill='#FFFFFF')
            
            # Mini preview
            preview_box = [x+20, y+70, x+cell_w-20, y+cell_h-20]
            draw.rectangle(preview_box, outline=model_color, width=3)
        
        path = f"temp/split_{datetime.now().timestamp()}.png"
        img.save(path)
        return path
    
    def create_video(self, frames, durations, output_name):
        """Create final video from frames"""
        # Create concat file
        concat_file = "temp/concat.txt"
        with open(concat_file, 'w') as f:
            for frame, duration in zip(frames, durations):
                f.write(f"file '{os.path.abspath(frame)}'\n")
                f.write(f"duration {duration}\n")
            # Last frame
            f.write(f"file '{os.path.abspath(frames[-1])}'\n")
        
        # Output path
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
        print(f"\n✅ Video created: {output_path}")
        
        # Cleanup
        for frame in frames:
            if os.path.exists(frame):
                os.remove(frame)
        
        return output_path
    
    def quick_produce(self, model_htmls, storyline=1):
        """Main method to quickly produce a video"""
        
        print(f"\n🎬 Starting viral content production...")
        print(f"📖 Using storyline {storyline}")
        
        # Step 1: Capture screenshots
        model_data = {}
        for model, html_path in model_htmls.items():
            print(f"\n📸 Processing {model}...")
            
            screenshot_path = f"screenshots/{model}_{self.project_name}.png"
            self.capture_screenshot(html_path, screenshot_path)
            
            model_data[model] = {
                'html': html_path,
                'screenshot': screenshot_path,
                'vibe': self.analyze_vibe(html_path)
            }
        
        # Step 2: Create frames based on storyline
        if storyline == 1:
            frames, durations = self.create_storyline_1_personality(model_data)
            output_name = f"{self.project_name}_personality"
        elif storyline == 2:
            frames, durations = self.create_storyline_2_plot_twist(model_data)
            output_name = f"{self.project_name}_plot_twist"
        else:
            frames, durations = self.create_storyline_3_competition(model_data)
            output_name = f"{self.project_name}_competition"
        
        # Step 3: Create video
        video_path = self.create_video(frames, durations, output_name)
        
        return video_path
    
    def analyze_vibe(self, html_path):
        """Quick analysis of HTML to determine vibe"""
        try:
            with open(html_path, 'r') as f:
                content = f.read().lower()
            
            if 'dark' in content or '#000' in content:
                return "Dark & Mysterious"
            elif 'gradient' in content:
                return "Modern & Vibrant"
            elif 'minimal' in content:
                return "Clean & Simple"
            else:
                return "Unique"
        except:
            return "Creative"
    
    def create_equation_frame(self, text, equation):
        """Create frame showing the equation"""
        img = Image.new('RGB', (self.width, self.height), '#0a0a0a')
        draw = ImageDraw.Draw(img)
        
        try:
            text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
            eq_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 100)
        except:
            text_font = ImageFont.load_default()
            eq_font = text_font
        
        # Text
        bbox = draw.textbbox((0, 0), text, font=text_font)
        x = (self.width - (bbox[2] - bbox[0])) // 2
        draw.text((x, 600), text, fill='#FFFFFF', font=text_font)
        
        # Equation with glow
        bbox = draw.textbbox((0, 0), equation, font=eq_font)
        x = (self.width - (bbox[2] - bbox[0])) // 2
        
        # Glow effect
        for offset in range(5, 0, -1):
            alpha = int(255 * (1 - offset/5) * 0.3)
            draw.text((x, 800), equation, 
                     fill=(100, 200, 255, alpha), font=eq_font)
        
        draw.text((x, 800), equation, fill='#FFFFFF', font=eq_font)
        
        path = f"temp/equation_{datetime.now().timestamp()}.png"
        img.save(path)
        return path
    
    def create_dramatic_reveal(self, model, data, reaction):
        """Create dramatic reveal with reaction text"""
        img = Image.new('RGB', (self.width, self.height), '#0a0a0a')
        draw = ImageDraw.Draw(img)
        
        model_color = self.models[model]['color']
        
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 50)
            big_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 70)
        except:
            font = ImageFont.load_default()
            big_font = font
        
        # Model name
        draw.text((50, 100), model.upper(), fill=model_color, font=big_font)
        
        # Screenshot (if available)
        if 'screenshot' in data and os.path.exists(data['screenshot']):
            ss = Image.open(data['screenshot'])
            ss.thumbnail((900, 600), Image.Resampling.LANCZOS)
            x_offset = (self.width - ss.width) // 2
            
            # Add dramatic border
            bordered = Image.new('RGB', (ss.width + 10, ss.height + 10), model_color)
            bordered.paste(ss, (5, 5))
            img.paste(bordered, (x_offset - 5, 300))
        
        # Reaction text
        bbox = draw.textbbox((0, 0), reaction, font=font)
        x = (self.width - (bbox[2] - bbox[0])) // 2
        draw.text((x, 1100), reaction, fill='#FFD700', font=font)
        
        path = f"temp/dramatic_{model}_{datetime.now().timestamp()}.png"
        img.save(path)
        return path
    
    def create_scoring_frame(self, model, data, scores):
        """Create scoring frame for competition"""
        img = Image.new('RGB', (self.width, self.height), '#0a0a0a')
        draw = ImageDraw.Draw(img)
        
        model_info = self.models[model]
        
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
            score_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        except:
            title_font = ImageFont.load_default()
            score_font = title_font
        
        # Model name
        draw.text((100, 100), model.upper(), fill=model_info['color'], font=title_font)
        
        # Screenshot preview
        preview_y = 250
        preview_h = 500
        draw.rectangle([100, preview_y, 980, preview_y + preview_h],
                      outline=model_info['color'], width=5)
        draw.text((540, preview_y + 250), "[PREVIEW]", fill='#666', anchor='mm')
        
        # Scores
        y = preview_y + preview_h + 100
        total = 0
        
        for category, score in scores.items():
            # Score bar
            bar_width = int((score / 10) * 700)
            draw.rectangle([200, y, 200 + bar_width, y + 40],
                          fill=model_info['color'])
            
            # Label and score
            draw.text((100, y + 5), category.capitalize() + ":", 
                     fill='#FFFFFF', font=score_font)
            draw.text((920, y + 5), f"{score}/10", 
                     fill='#FFFFFF', font=score_font)
            
            total += score
            y += 80
        
        # Total score
        draw.text((100, y + 50), f"TOTAL: {total}/30", 
                 fill='#FFD700', font=title_font)
        
        path = f"temp/scoring_{model}_{datetime.now().timestamp()}.png"
        img.save(path)
        return path
    
    def create_winner_frame(self):
        """Create winner announcement frame"""
        img = Image.new('RGB', (self.width, self.height), '#0a0a0a')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 100)
            small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        except:
            font = ImageFont.load_default()
            small_font = font
        
        # Drum roll effect with gradient background
        for i in range(self.height):
            intensity = int(20 + 30 * abs(i - self.height/2) / (self.height/2))
            draw.rectangle([0, i, self.width, i+1], 
                          fill=(intensity, intensity, intensity))
        
        # Winner text
        texts = [
            ("And the winner is...", small_font, 600),
            ("🥁 🥁 🥁", font, 800),
            ("YOU DECIDE!", font, 1000),
            ("Vote in comments!", small_font, 1200)
        ]
        
        for text, text_font, y in texts:
            bbox = draw.textbbox((0, 0), text, font=text_font)
            x = (self.width - (bbox[2] - bbox[0])) // 2
            
            # Gold text for winner announcement
            if "YOU DECIDE" in text:
                draw.text((x+3, y+3), text, fill='#000', font=text_font)
                draw.text((x, y), text, fill='#FFD700', font=text_font)
            else:
                draw.text((x, y), text, fill='#FFFFFF', font=text_font)
        
        path = f"temp/winner_{datetime.now().timestamp()}.png"
        img.save(path)
        return path


# Example usage
if __name__ == "__main__":
    # Initialize pipeline
    pipeline = ViralContentPipeline("euler_visualization")
    
    # Example: You would provide your actual HTML files here
    model_htmls = {
        'claude': 'inputs/claude_euler.html',
        'gpt4': 'inputs/gpt4_euler.html',
        'gemini': 'inputs/gemini_euler.html',
        'llama': 'inputs/llama_euler.html'
    }
    
    # Create placeholder HTMLs for testing
    for model, path in model_htmls.items():
        if not os.path.exists(path):
            # Create simple test HTML
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        background: {'#000' if model == 'claude' else '#fff'};
                        color: {'#fff' if model == 'claude' else '#000'};
                        font-family: Arial;
                        padding: 50px;
                    }}
                    h1 {{ color: {pipeline.models[model]['color']}; }}
                </style>
            </head>
            <body>
                <h1>{model.upper()} Euler Visualization</h1>
                <p>e^(iπ) + 1 = 0</p>
                <canvas style="border: 2px solid {pipeline.models[model]['color']}; 
                              width: 400px; height: 400px;"></canvas>
            </body>
            </html>
            """
            
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(html_content)
            print(f"Created test HTML: {path}")
    
    # Produce videos for all 3 storylines
    print("\n🎬 Creating viral videos for all 3 storylines...\n")
    
    for storyline in [1, 2, 3]:
        print(f"\n{'='*50}")
        print(f"Creating Storyline {storyline}")
        print(f"{'='*50}")
        
        video_path = pipeline.quick_produce(model_htmls, storyline=storyline)
        print(f"✅ Storyline {storyline} complete: {video_path}")
    
    print("\n🎉 All videos created successfully!")
    print("\nNext steps:")
    print("1. Replace the test HTMLs with your actual AI outputs")
    print("2. Run: python viral_content_pipeline.py")
    print("3. Find your videos in the 'output' folder")
    print("4. Upload to TikTok/Reels/Shorts!")
