import os
from PIL import Image

def get_image_resolutions(directory):
    widths = []
    heights = []
    resolutions = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')):
                filepath = os.path.join(root, file)
                try:
                    with Image.open(filepath) as img:
                        width, height = img.size
                        widths.append(width)
                        heights.append(height)
                        resolutions.append(width * height)
                except Exception as e:
                    print(f"Error opening {filepath}: {e}")
    return widths, heights, resolutions

def main():
    directory = "plastic_coco/images"
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return
    
    widths, heights, resolutions = get_image_resolutions(directory)
    if not widths:
        print("No images found.")
        return
    
    min_width = min(widths)
    max_width = max(widths)
    avg_width = sum(widths) / len(widths)
    
    min_height = min(heights)
    max_height = max(heights)
    avg_height = sum(heights) / len(heights)
    
    avg_resolution = sum(resolutions) / len(resolutions)
    below_avg = sum(1 for r in resolutions if r < avg_resolution)
    above_avg = sum(1 for r in resolutions if r > avg_resolution)
    
    print(f"Minimum image resolution: {min_width} x {min_height}")
    print(f"Average image resolution: {avg_width:.2f} x {avg_height:.2f}")
    print(f"Largest image resolution: {max_width} x {max_height}")
    print(f"Images below average resolution ({avg_resolution:.0f} pixels): {below_avg}")
    print(f"Images above average resolution ({avg_resolution:.0f} pixels): {above_avg}")

if __name__ == "__main__":
    main()