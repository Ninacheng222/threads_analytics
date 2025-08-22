from typing import Dict
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap

class ShareableContentGenerator:
    def __init__(self):
        self.ig_story_size = (1080, 1920)  # Instagram Stories dimensions
        self.colors = {
            'cosmic_purple': '#6B46C1',
            'mystic_blue': '#3B82F6', 
            'stellar_pink': '#EC4899',
            'golden_yellow': '#F59E0B',
            'deep_space': '#1F2937',
            'white': '#FFFFFF'
        }
        
    def generate_ig_story_image(self, portrait: Dict) -> str:
        """Generate Instagram Story image as base64 string"""
        try:
            # Create image with gradient background
            img = Image.new('RGB', self.ig_story_size, color='#1F2937')
            draw = ImageDraw.Draw(img)
            
            # Create gradient effect (simplified)
            for i in range(self.ig_story_size[1]):
                alpha = i / self.ig_story_size[1]
                color = self._blend_colors('#6B46C1', '#3B82F6', alpha)
                draw.line([(0, i), (self.ig_story_size[0], i)], fill=color)
            
            # Add mystical decorations
            self._add_mystical_decorations(draw)
            
            # Add content
            self._add_portrait_content(draw, portrait)
            
            # Convert to base64
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
            
        except Exception as e:
            return self._generate_fallback_image()
    
    def generate_threads_post_text(self, portrait: Dict) -> str:
        """Generate shareable text for Threads"""
        archetype = portrait.get('archetype', 'The Emerging Creator')
        content_dna = portrait.get('content_dna', {})
        posting_spirit = portrait.get('posting_spirit', 'Digital Wanderer')
        quote = portrait.get('shareable_quote', '✨ Your creative energy is unique ✨')
        
        # Get top content type
        top_content_type = max(content_dna.items(), key=lambda x: x[1]) if content_dna else ('personal', 50)
        
        post_text = f"""🔮 Just discovered my Creator DNA! ✨

{quote}

My digital aura reveals:
🎭 Archetype: {archetype}
📱 Content DNA: {top_content_type[1]}% {top_content_type[0].title()}
🌙 Posting Spirit: {posting_spirit}

What's YOUR creator personality? 

Find out your mystical creator portrait 👇
threadsfortune.app

#CreatorDNA #ThreadsPersonality #ContentCreator #CreatorQuiz"""

        return post_text
    
    def generate_share_urls(self, portrait: Dict) -> Dict[str, str]:
        """Generate sharing URLs for different platforms"""
        threads_text = self.generate_threads_post_text(portrait)
        
        return {
            'threads': f"https://threads.net/intent/post?text={self._url_encode(threads_text)}",
            'twitter': f"https://twitter.com/intent/tweet?text={self._url_encode(threads_text[:280])}",
            'copy_text': threads_text
        }
    
    def _blend_colors(self, color1: str, color2: str, alpha: float) -> str:
        """Blend two hex colors"""
        # Simple color blending for gradient effect
        c1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
        c2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
        
        blended = tuple(int(c1[i] * (1-alpha) + c2[i] * alpha) for i in range(3))
        return f"#{blended[0]:02x}{blended[1]:02x}{blended[2]:02x}"
    
    def _add_mystical_decorations(self, draw):
        """Add mystical decorative elements"""
        # Add some stars and cosmic elements
        import random
        
        for _ in range(50):
            x = random.randint(0, self.ig_story_size[0])
            y = random.randint(0, self.ig_story_size[1] // 3)
            size = random.randint(2, 6)
            
            # Draw a simple star (circle for now)
            draw.ellipse([x-size, y-size, x+size, y+size], fill='#FFFFFF', outline='#F59E0B')
    
    def _add_portrait_content(self, draw, portrait: Dict):
        """Add the creator portrait content to image"""
        try:
            # Try to use a default font, fallback to default if not available
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
        except:
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
        
        # Main title
        draw.text((540, 200), "🔮 Your Creator DNA", font=title_font, 
                 fill='#FFFFFF', anchor='mm')
        
        # Archetype
        archetype = portrait.get('archetype', 'The Emerging Creator')
        draw.text((540, 300), archetype, font=title_font, 
                 fill='#F59E0B', anchor='mm')
        
        # Content DNA
        content_dna = portrait.get('content_dna', {})
        y_pos = 450
        for content_type, percentage in content_dna.items():
            text = f"{content_type.title()}: {percentage}%"
            draw.text((540, y_pos), text, font=body_font, 
                     fill='#FFFFFF', anchor='mm')
            y_pos += 50
        
        # Quote
        quote = portrait.get('shareable_quote', '✨ Your creative energy is unique ✨')
        wrapped_quote = textwrap.fill(quote, width=30)
        draw.text((540, 700), wrapped_quote, font=body_font, 
                 fill='#EC4899', anchor='mm')
        
        # CTA
        draw.text((540, 1600), "Discover your Creator DNA", font=body_font, 
                 fill='#FFFFFF', anchor='mm')
        draw.text((540, 1650), "threadsfortune.app", font=body_font, 
                 fill='#F59E0B', anchor='mm')
    
    def _generate_fallback_image(self) -> str:
        """Generate a simple fallback image if main generation fails"""
        img = Image.new('RGB', self.ig_story_size, color='#6B46C1')
        draw = ImageDraw.Draw(img)
        
        draw.text((540, 960), "🔮 Creator DNA", font=ImageFont.load_default(), 
                 fill='#FFFFFF', anchor='mm')
        draw.text((540, 1020), "Discover your mystical", font=ImageFont.load_default(), 
                 fill='#FFFFFF', anchor='mm')
        draw.text((540, 1060), "creator personality", font=ImageFont.load_default(), 
                 fill='#FFFFFF', anchor='mm')
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    def _url_encode(self, text: str) -> str:
        """URL encode text for sharing URLs"""
        import urllib.parse
        return urllib.parse.quote(text)