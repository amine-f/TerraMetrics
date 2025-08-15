from PIL import Image, ImageDraw
import os

def create_favicon():
    # Create a 16x16 pixel image (smaller size for favicon)
    img = Image.new('RGBA', (16, 16), (46, 125, 50, 255))  # #2e7d32 in RGB
    draw = ImageDraw.Draw(img)
    
    # Draw a simple leaf shape in white
    points = [(8, 2), (14, 8), (8, 14), (2, 8)]
    draw.polygon(points, fill='white')
    
    # Save the image
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'images')
    os.makedirs(assets_dir, exist_ok=True)
    
    # Save as ICO file
    img.save(os.path.join(assets_dir, 'favicon.png'), format='PNG')

if __name__ == '__main__':
    create_favicon()
