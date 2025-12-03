import io
from PIL import Image, ImageDraw, ImageFont

def combine_charts(fig1, fig2, fig3, fig4, title="图表汇总"):
    """
    Combines 4 matplotlib figures into a single 2x2 image with high quality.
    Layout:
    [Fig1] [Fig2]
    [Fig3] [Fig4]
    """
    # Convert figures to PIL Images with high DPI for clarity
    images = []
    for fig in [fig1, fig2, fig3, fig4]:
        buf = io.BytesIO()
        # 使用高DPI保存，确保清晰度
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=150, facecolor='white')
        buf.seek(0)
        img = Image.open(buf)
        images.append(img)
    
    # 确保所有图片尺寸一致（取最大尺寸）
    max_width = max(img.size[0] for img in images)
    max_height = max(img.size[1] for img in images)
    
    # 将所有图片调整为相同尺寸
    resized_images = []
    for img in images:
        # 创建白色背景
        new_img = Image.new('RGB', (max_width, max_height), 'white')
        # 居中粘贴原图
        offset_x = (max_width - img.size[0]) // 2
        offset_y = (max_height - img.size[1]) // 2
        new_img.paste(img, (offset_x, offset_y))
        resized_images.append(new_img)
    
    # 设置间距和边距
    padding = 30  # 图表之间的间距
    margin = 40   # 外边距
    
    # 计算总尺寸
    total_width = max_width * 2 + padding + margin * 2
    total_height = max_height * 2 + padding + margin * 2
    
    # 创建白色背景的组合图像
    combined_image = Image.new('RGB', (total_width, total_height), 'white')
    
    # 粘贴图表
    # 左上
    combined_image.paste(resized_images[0], (margin, margin))
    # 右上
    combined_image.paste(resized_images[1], (max_width + padding + margin, margin))
    # 左下
    combined_image.paste(resized_images[2], (margin, max_height + padding + margin))
    # 右下
    combined_image.paste(resized_images[3], (max_width + padding + margin, max_height + padding + margin))
    
    # 添加分隔线，使布局更清晰
    draw = ImageDraw.Draw(combined_image)
    line_color = '#E0E0E0'
    line_width = 2
    
    # 垂直分隔线
    vertical_x = max_width + margin + padding // 2
    draw.line([(vertical_x, margin), (vertical_x, total_height - margin)], 
              fill=line_color, width=line_width)
    
    # 水平分隔线
    horizontal_y = max_height + margin + padding // 2
    draw.line([(margin, horizontal_y), (total_width - margin, horizontal_y)], 
              fill=line_color, width=line_width)
    
    return combined_image
