import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager as fm
import platform
import os

# Set font for Chinese support
system_name = platform.system()

# 清除字体缓存（解决字体不生效问题）
try:
    fm._rebuild()
except:
    pass

if system_name == "Windows":
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
elif system_name == "Darwin":
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Heiti SC']
else:
    # Linux - 添加多个字体选项作为降级方案
    plt.rcParams['font.sans-serif'] = [
        'Noto Sans CJK SC',      # Google Noto 字体
        'Noto Sans CJK JP',
        'WenQuanYi Micro Hei',   # 文泉驿微米黑
        'WenQuanYi Zen Hei',     # 文泉驿正黑
        'Droid Sans Fallback',   # Android 字体
        'DejaVu Sans',           # 降级到英文字体
        'sans-serif'
    ]

plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# 统一的图表尺寸 - 确保所有图表比例一致
FIGURE_SIZE = (10, 7)
DPI = 120  # 高分辨率，确保字体清晰

# 统一的字体大小设置
TITLE_FONTSIZE = 18
LABEL_FONTSIZE = 13
TICK_FONTSIZE = 11
LEGEND_FONTSIZE = 12

# 默认颜色方案 - 专业商务风格
DEFAULT_COLORS = {
    'push': '#2E7D32',      # 深绿色 - 专业稳重
    'not_push': '#F57C00',  # 橙色 - 醒目但不刺眼
    'wear': '#1976D2',      # 蓝色 - 商务专业
    'not_wear': '#C62828'   # 深红色 - 对比鲜明
}

def generate_line_chart_1(df, title, colors=None):
    """
    Chart 1: Daily Report Push Line Chart
    Lines: Push (Green), Not Push (Orange)
    Markers: Yes
    Date Rotation: 45 degrees
    """
    if colors is None:
        colors = DEFAULT_COLORS
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZE, dpi=DPI)
    
    # 设置背景色为浅灰，更专业
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('white')
    
    # 绘制折线图，增加线宽和标记大小
    ax.plot(df['日期'], df['日报推送'], 
            marker='o', markersize=8, color=colors['push'], 
            label='日报推送', linewidth=3, alpha=0.9)
    ax.plot(df['日期'], df['日报未推送'], 
            marker='s', markersize=8, color=colors['not_push'], 
            label='日报未推送', linewidth=3, alpha=0.9)
    
    # 添加网格线，提升可读性
    ax.grid(True, linestyle='--', alpha=0.3, linewidth=1)
    ax.set_axisbelow(True)  # 网格线在图形下方
    
    # 设置标题和标签
    ax.set_title(title, fontsize=TITLE_FONTSIZE, fontweight='bold', pad=20)
    ax.set_xlabel('日期', fontsize=LABEL_FONTSIZE, fontweight='bold')
    ax.set_ylabel('数量', fontsize=LABEL_FONTSIZE, fontweight='bold')
    
    # 设置刻度字体大小
    ax.tick_params(axis='both', which='major', labelsize=TICK_FONTSIZE)
    plt.xticks(rotation=45, ha='right')
    
    # 图例设置
    ax.legend(fontsize=LEGEND_FONTSIZE, frameon=True, shadow=True, 
              fancybox=True, loc='best')
    
    plt.tight_layout()
    return fig

def generate_line_chart_2(df, title, colors=None):
    """
    Chart 2: Watch Wear Line Chart
    Lines: Wear (Blue), Not Wear (Red)
    Markers: Yes
    Date Rotation: 45 degrees
    """
    if colors is None:
        colors = DEFAULT_COLORS
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZE, dpi=DPI)
    
    # 设置背景色
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('white')
    
    # 绘制折线图
    ax.plot(df['日期'], df['手表佩戴'], 
            marker='o', markersize=8, color=colors['wear'], 
            label='手表佩戴', linewidth=3, alpha=0.9)
    ax.plot(df['日期'], df['手表未佩戴'], 
            marker='s', markersize=8, color=colors['not_wear'], 
            label='手表未佩戴', linewidth=3, alpha=0.9)
    
    # 添加网格线
    ax.grid(True, linestyle='--', alpha=0.3, linewidth=1)
    ax.set_axisbelow(True)
    
    # 设置标题和标签
    ax.set_title(title, fontsize=TITLE_FONTSIZE, fontweight='bold', pad=20)
    ax.set_xlabel('日期', fontsize=LABEL_FONTSIZE, fontweight='bold')
    ax.set_ylabel('数量', fontsize=LABEL_FONTSIZE, fontweight='bold')
    
    # 设置刻度字体大小
    ax.tick_params(axis='both', which='major', labelsize=TICK_FONTSIZE)
    plt.xticks(rotation=45, ha='right')
    
    # 图例设置
    ax.legend(fontsize=LEGEND_FONTSIZE, frameon=True, shadow=True, 
              fancybox=True, loc='best')
    
    plt.tight_layout()
    return fig

def generate_bar_chart(df, title, colors=None):
    """
    Chart 3: Daily Report Push Bar Chart
    Type: Grouped Bar (to show comparison clearly)
    Colors: Push (Green), Not Push (Orange)
    """
    if colors is None:
        colors = DEFAULT_COLORS
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZE, dpi=DPI)
    
    # 设置背景色
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('white')
    
    x = range(len(df['日期']))
    width = 0.35
    
    # 绘制柱状图，添加边框使其更清晰
    bars1 = ax.bar([i - width/2 for i in x], df['日报推送'], width, 
                    label='日报推送', color=colors['push'], 
                    edgecolor='white', linewidth=1.5, alpha=0.9)
    bars2 = ax.bar([i + width/2 for i in x], df['日报未推送'], width, 
                    label='日报未推送', color=colors['not_push'], 
                    edgecolor='white', linewidth=1.5, alpha=0.9)
    
    # 添加网格线（仅Y轴）
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, linewidth=1)
    ax.set_axisbelow(True)
    
    # 设置标题和标签
    ax.set_title(title, fontsize=TITLE_FONTSIZE, fontweight='bold', pad=20)
    ax.set_xlabel('日期', fontsize=LABEL_FONTSIZE, fontweight='bold')
    ax.set_ylabel('数量', fontsize=LABEL_FONTSIZE, fontweight='bold')
    
    # 设置X轴刻度
    ax.set_xticks(x)
    ax.set_xticklabels(df['日期'], rotation=45, ha='right')
    ax.tick_params(axis='both', which='major', labelsize=TICK_FONTSIZE)
    
    # 图例设置
    ax.legend(fontsize=LEGEND_FONTSIZE, frameon=True, shadow=True, 
              fancybox=True, loc='best')
    
    plt.tight_layout()
    return fig

def generate_pie_chart(df, title, colors=None):
    """
    Chart 4: Daily Report Push Pie Chart
    Shows total Push vs Not Push
    Colors: Green, Orange
    Explode: Yes
    Labels: % + Number (Total)
    """
    if colors is None:
        colors = DEFAULT_COLORS
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZE, dpi=DPI)
    fig.patch.set_facecolor('white')
    
    total_push = df['日报推送'].sum()
    total_not_push = df['日报未推送'].sum()
    
    sizes = [total_push, total_not_push]
    labels = ['日报推送', '日报未推送']
    pie_colors = [colors['push'], colors['not_push']]
    explode = (0.05, 0.05)  # 轻微分离
    
    def func(pct, allvals):
        absolute = int(round(pct/100.*sum(allvals)))
        return "{:.1f}%\n({:d})".format(pct, absolute)
    
    # 绘制饼图 - 使用正常半径
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, 
                                        colors=pie_colors, 
                                        autopct=lambda pct: func(pct, sizes),
                                        shadow=True, startangle=90,
                                        textprops={'fontsize': TICK_FONTSIZE, 'fontweight': 'bold'})
    
    # 设置百分比文字为白色，更清晰
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(LABEL_FONTSIZE)
        autotext.set_fontweight('bold')
    
    # 设置标签文字
    for text in texts:
        text.set_fontsize(LABEL_FONTSIZE)
        text.set_fontweight('bold')
    
    # 设置标题
    ax.set_title(title, fontsize=TITLE_FONTSIZE, fontweight='bold', pad=20)
    
    # 调整子图位置，添加边距使其与其他图表显示大小一致
    # 其他图表有坐标轴占用空间，饼图需要手动添加相同的边距
    plt.subplots_adjust(left=0.15, right=0.85, top=0.92, bottom=0.08)
    
    return fig


