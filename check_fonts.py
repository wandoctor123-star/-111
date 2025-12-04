import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import os

def check_fonts():
    output = []
    output.append(f"System: {platform.system()}")
    output.append("Checking for Chinese fonts...")
    
    # Common Chinese font names
    chinese_fonts = ['Microsoft YaHei', 'SimHei', 'SimSun', 'NSimSun', 'FangSong', 'KaiTi', 'Arial Unicode MS']
    
    found_fonts = []
    for font_name in chinese_fonts:
        try:
            # Try to find the font
            font_path = fm.findfont(font_name)
            # findfont returns a default if not found, so we need to check if it actually matches
            # But on Windows it might just return the path.
            # Let's check if the path contains the font name or looks like a font file
            output.append(f"Search for {font_name} returned: {font_path}")
            if 'Vera' in font_path or 'DejaVu' in font_path: # Matplotlib defaults
                 output.append(f"  -> Likely not found (defaulted to {font_path})")
            else:
                 found_fonts.append((font_name, font_path))
        except Exception as e:
            output.append(f"Could not find {font_name}: {e}")
            
    output.append("\nFound Chinese fonts:")
    for name, path in found_fonts:
        output.append(f"- {name}: {path}")

    with open('found_fonts.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print("Font check complete. Results written to found_fonts.txt")

if __name__ == "__main__":
    check_fonts()
