import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import os
import sys

# 设置 Matplotlib 后端（在导入 pyplot 之前）
matplotlib.use('Agg')

print(f"=== Font Initialization for {platform.system()} ===")

# 强制清除字体缓存
def clear_font_cache():
    try:
        cache_dir = matplotlib.get_cachedir()
        print(f"Cache directory: {cache_dir}")
        
        # 尝试删除所有字体缓存文件
        cache_files = [
            'fontlist-v330.json',
            'fontlist-v320.json', 
            'fontlist-v310.json'
        ]
        
        for cache_file in cache_files:
            cache_path = os.path.join(cache_dir, cache_file)
            if os.path.exists(cache_path):
                os.remove(cache_path)
                print(f"✓ Removed cache: {cache_file}")
    except Exception as e:
        print(f"Cache clear warning: {e}")

clear_font_cache()

# 重建字体管理器
try:
    fm._rebuild()
    print("✓ Font manager rebuilt")
except Exception as e:
    print(f"Font rebuild warning: {e}")

# 配置中文字体
def setup_fonts():
    system = platform.system()
    
    if system == "Linux":
        # Streamlit Cloud / Linux
        print("Configuring for Linux/Streamlit Cloud...")
        
        # 方法1：直接加载字体文件
        font_paths = [
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
            '/usr/share/fonts/truetype/wqy-microhei/wqy-microhei.ttc',
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/noto-cjk/NotoSansCJK-Regular.ttc',
        ]
        
        font_loaded = False
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    # 直接注册字体
                    fm.fontManager.addfont(font_path)
                    prop = fm.FontProperties(fname=font_path)
                    font_name = prop.get_name()
                    
                    # 设置为默认字体
                    plt.rcParams['font.family'] = 'sans-serif'
                    plt.rcParams['font.sans-serif'] = [font_name] + plt.rcParams.get('font.sans-serif', [])
                    
                    print(f"✓✓✓ SUCCESS: Loaded {font_name} from {font_path}")
                    font_loaded = True
                    break
                except Exception as e:
                    print(f"Failed to load {font_path}: {e}")
        
        if not font_loaded:
            print("⚠ No font file loaded, using font names")
            plt.rcParams['font.sans-serif'] = [
                'WenQuanYi Micro Hei',
                'WenQuanYi Zen Hei', 
                'Noto Sans CJK SC',
                'DejaVu Sans'
            ]
    
    elif system == "Windows":
        # Windows
        print("Configuring for Windows...")
        font_paths = [
            r'C:\Windows\Fonts\msyh.ttc',
            r'C:\Windows\Fonts\simhei.ttf',
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    fm.fontManager.addfont(font_path)
                    prop = fm.FontProperties(fname=font_path)
                    font_name = prop.get_name()
                    plt.rcParams['font.family'] = 'sans-serif'
                    plt.rcParams['font.sans-serif'] = [font_name] + plt.rcParams.get('font.sans-serif', [])
                    print(f"✓✓✓ SUCCESS: Loaded {font_name}")
                    break
                except Exception as e:
                    print(f"Failed: {e}")
    
    else:
        # macOS
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC']
    
    # 解决负号显示
    plt.rcParams['axes.unicode_minus'] = False
    
    # 打印最终配置
    print(f"Final font.sans-serif: {plt.rcParams['font.sans-serif'][:3]}")
    print("=== Font Initialization Complete ===\n")

setup_fonts()

# 统一的图表尺寸
FIGURE_SIZE = (10, 7)
DPI = 120

# 统一的字体大小设置
TITLE_FONTSIZE = 18
LABEL_FONTSIZE = 13
TICK_FONTSIZE = 11
LEGEND_FONTSIZE = 12

# 默认颜色方案
DEFAULT_COLORS = {
    'push': '#2E7D32',
    'not_push': '#F57C00',
    'wear': '#1976D2',
    'not_wear': '#C62828'
}

def generate_line_chart_1(df, title, colors=None):
    """Chart 1: Daily Report Push Line Chart"""
    if colors is None:
        colors = DEFAULT_COLORS
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZE, dpi=DPI)
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('white')
    
    ax.plot(df['日期'], df['日报推送'], 
            marker='o', markersize=8, color=colors['push'], 
            label='日报推送', linewidth=3, alpha=0.9)
    ax.plot(df['日期'], df['日报未推送'], 
            marker='s', markersize=8, color=colors['not_push'], 
            label='日报未推送', linewidth=3, alpha=0.9)
    
    ax.grid(True, linestyle='--', alpha=0.3, linewidth=1)
    ax.set_axisbelow(True)
    
    ax.set_title(title, fontsize=TITLE_FONTSIZE, fontweight='bold', pad=20)
    ax.set_xlabel('日期', fontsize=LABEL_FONTSIZE, fontweight='bold')
    ax.set_ylabel('数量', fontsize=LABEL_FONTSIZE, fontweight='bold')
    
    ax.tick_params(axis='both', which='major', labelsize=TICK_FONTSIZE)
    plt.xticks(rotation=45, ha='right')
    
    ax.legend(fontsize=LEGEND_FONTSIZE, frameon=True, shadow=True, 
              fancybox=True, loc='best')
    
    plt.tight_layout()
    return fig

def generate_line_chart_2(df, title, colors=None):
    """Chart 2: Watch Wear Line Chart"""
    if colors is None:
        colors = DEFAULT_COLORS
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZE, dpi=DPI)
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('white')
    
    ax.plot(df['日期'], df['手表佩戴'], 
            marker='o', markersize=8, color=colors['wear'], 
            label='手表佩戴', linewidth=3, alpha=0.9)
    ax.plot(df['日期'], df['手表未佩戴'], 
            marker='s', markersize=8, color=colors['not_wear'], 
            label='手表未佩戴', linewidth=3, alpha=0.9)
    
    ax.grid(True, linestyle='--', alpha=0.3, linewidth=1)
    ax.set_axisbelow(True)
    
    ax.set_title(title, fontsize=TITLE_FONTSIZE, fontweight='bold', pad=20)
    ax.set_xlabel('日期', fontsize=LABEL_FONTSIZE, fontweight='bold')
    ax.set_ylabel('数量', fontsize=LABEL_FONTSIZE, fontweight='bold')
    
    ax.tick_params(axis='both', which='major', labelsize=TICK_FONTSIZE)
    plt.xticks(rotation=45, ha='right')
    
    ax.legend(fontsize=LEGEND_FONTSIZE, frameon=True, shadow=True, 
              fancybox=True, loc='best')
    
    plt.tight_layout()
    return fig

def generate_bar_chart(df, title, colors=None):
    """Chart 3: Daily Report Push Bar Chart"""
    if colors is None:
        colors = DEFAULT_COLORS
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZE, dpi=DPI)
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('white')
    
    x = range(len(df['日期']))
    width = 0.35
    
    bars1 = ax.bar([i - width/2 for i in x], df['日报推送'], width, 
                    label='日报推送', color=colors['push'], 
                    edgecolor='white', linewidth=1.5, alpha=0.9)
    bars2 = ax.bar([i + width/2 for i in x], df['日报未推送'], width, 
                    label='日报未推送', color=colors['not_push'], 
                    edgecolor='white', linewidth=1.5, alpha=0.9)
    
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, linewidth=1)
    ax.set_axisbelow(True)
    
    ax.set_title(title, fontsize=TITLE_FONTSIZE, fontweight='bold', pad=20)
    ax.set_xlabel('日期', fontsize=LABEL_FONTSIZE, fontweight='bold')
    ax.set_ylabel('数量', fontsize=LABEL_FONTSIZE, fontweight='bold')
    
    ax.set_xticks(x)
    ax.set_xticklabels(df['日期'], rotation=45, ha='right')
    ax.tick_params(axis='both', which='major', labelsize=TICK_FONTSIZE)
    
    ax.legend(fontsize=LEGEND_FONTSIZE, frameon=True, shadow=True, 
              fancybox=True, loc='best')
    
    plt.tight_layout()
    return fig

def generate_pie_chart(df, title, colors=None):
    """Chart 4: Daily Report Push Pie Chart"""
    if colors is None:
        colors = DEFAULT_COLORS
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZE, dpi=DPI)
    fig.patch.set_facecolor('white')
    
    total_push = df['日报推送'].sum()
    total_not_push = df['日报未推送'].sum()
    
    sizes = [total_push, total_not_push]
    labels = ['日报推送', '日报未推送']
    pie_colors = [colors['push'], colors['not_push']]
    explode = (0.05, 0.05)
    
    def func(pct, allvals):
        absolute = int(round(pct/100.*sum(allvals)))
        return "{:.1f}%\n({:d})".format(pct, absolute)
    
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, 
                                        colors=pie_colors, 
                                        autopct=lambda pct: func(pct, sizes),
                                        shadow=True, startangle=90,
                                        textprops={'fontsize': TICK_FONTSIZE, 'fontweight': 'bold'})
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(LABEL_FONTSIZE)
        autotext.set_fontweight('bold')
    
    for text in texts:
        text.set_fontsize(LABEL_FONTSIZE)
        text.set_fontweight('bold')
    
    ax.set_title(title, fontsize=TITLE_FONTSIZE, fontweight='bold', pad=20)
    
    plt.subplots_adjust(left=0.15, right=0.85, top=0.92, bottom=0.08)
    
    return fig
