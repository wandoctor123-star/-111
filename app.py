import streamlit as st
import pandas as pd
import time
import io
from data_processor import load_data, validate_columns, preprocess_data, calculate_stats
from chart_generator import generate_line_chart_1, generate_line_chart_2, generate_bar_chart, generate_pie_chart
from utils import combine_charts

# Set page config
st.set_page_config(page_title="AI 自动图表生成系统", layout="wide", initial_sidebar_state="expanded")

def main():
    # Sidebar Configuration
    st.sidebar.header("📊 图表设置")
    
    # 标题设置
    st.sidebar.subheader("📝 标题设置")
    default_title_all = "12 月运营日报图表"
    default_title_1 = "日报推送折线图"
    default_title_2 = "佩戴趋势折线图"
    default_title_3 = "日报推送柱状图"
    default_title_4 = "推送占比饼图"
    
    title_all = st.sidebar.text_input("总标题", default_title_all)
    title_1 = st.sidebar.text_input("图表 1 标题", default_title_1)
    title_2 = st.sidebar.text_input("图表 2 标题", default_title_2)
    title_3 = st.sidebar.text_input("图表 3 标题", default_title_3)
    title_4 = st.sidebar.text_input("图表 4 标题", default_title_4)
    
    # 颜色设置
    st.sidebar.subheader("🎨 颜色设置")
    st.sidebar.markdown("*自定义图表颜色，打造专属风格*")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        color_push = st.color_picker("日报推送", "#2E7D32", help="推送数据的颜色")
        color_wear = st.color_picker("手表佩戴", "#1976D2", help="佩戴数据的颜色")
    with col2:
        color_not_push = st.color_picker("日报未推送", "#F57C00", help="未推送数据的颜色")
        color_not_wear = st.color_picker("手表未佩戴", "#C62828", help="未佩戴数据的颜色")
    
    # 组装颜色字典
    colors = {
        'push': color_push,
        'not_push': color_not_push,
        'wear': color_wear,
        'not_wear': color_not_wear
    }
    
    # 预设配色方案
    st.sidebar.markdown("---")
    st.sidebar.markdown("**快速配色方案**")
    color_scheme = st.sidebar.selectbox(
        "选择预设方案",
        ["自定义", "商务专业", "清新活力", "沉稳大气", "科技蓝调"],
        help="选择预设配色方案或自定义"
    )
    
    # 应用预设配色
    if color_scheme == "商务专业":
        colors = {'push': '#2E7D32', 'not_push': '#F57C00', 'wear': '#1976D2', 'not_wear': '#C62828'}
    elif color_scheme == "清新活力":
        colors = {'push': '#00C853', 'not_push': '#FFB300', 'wear': '#00B0FF', 'not_wear': '#FF6D00'}
    elif color_scheme == "沉稳大气":
        colors = {'push': '#1B5E20', 'not_push': '#E65100', 'wear': '#0D47A1', 'not_wear': '#B71C1C'}
    elif color_scheme == "科技蓝调":
        colors = {'push': '#0091EA', 'not_push': '#00E5FF', 'wear': '#304FFE', 'not_wear': '#651FFF'}
    
    # Main Content
    st.title("📈 AI 自动图表生成系统")
    st.markdown("### 上传 Excel 表格，自动生成专业级图表并输出整合截图")
    st.markdown("---")
    
    uploaded_file = st.file_uploader("📁 请上传 Excel 文件", type=['xlsx', 'xls'], 
                                      help="支持 .xlsx 和 .xls 格式")
    
    if uploaded_file is not None:
        # Progress Bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Parsing
            status_text.text("🔍 [##--------] 20% 正在解析数据...")
            progress_bar.progress(20)
            time.sleep(0.5)
            
            df = load_data(uploaded_file)
            df = validate_columns(df)
            df = preprocess_data(df)
            
            # Step 2: Generating Charts
            status_text.text("🎨 [######----] 60% 正在生成图表...")
            progress_bar.progress(60)
            
            fig1 = generate_line_chart_1(df, title_1, colors)
            fig2 = generate_line_chart_2(df, title_2, colors)
            fig3 = generate_bar_chart(df, title_3, colors)
            fig4 = generate_pie_chart(df, title_4, colors)
            
            # Step 3: Combining
            status_text.text("🖼️ [#########-] 90% 正在整合图表...")
            progress_bar.progress(90)
            combined_img = combine_charts(fig1, fig2, fig3, fig4)
            
            status_text.text("✅ [##########] 100% 图表生成完成！")
            progress_bar.progress(100)
            time.sleep(0.5)
            status_text.empty()
            progress_bar.empty()
            
            # Display Stats
            stats = calculate_stats(df)
            st.success(f"📊 数据分析：最近一周推送率稳定在 **{stats['push_rate']:.1f}%** 左右，佩戴率为 **{stats['wear_rate']:.1f}%**。")
            
            # Display Charts
            st.markdown("---")
            st.subheader("📊 生成结果")
            
            # 使用两列布局展示图表
            col1, col2 = st.columns(2)
            with col1:
                st.pyplot(fig1)
                st.pyplot(fig3)
            with col2:
                st.pyplot(fig2)
                st.pyplot(fig4)
            
            st.markdown("---")
            st.subheader("🖼️ 整合截图（用于汇报）")
            st.image(combined_img, caption=title_all, use_column_width=True)
            
            # Download Button
            buf = io.BytesIO()
            combined_img.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            col_download1, col_download2, col_download3 = st.columns([1, 1, 2])
            with col_download1:
                st.download_button(
                    label="⬇️ 下载整合截图 (PNG)",
                    data=byte_im,
                    file_name="chart_summary.png",
                    mime="image/png",
                    use_container_width=True
                )
            
        except ValueError as e:
            st.error(f"❌ 数据格式错误：{str(e)}")
        except Exception as e:
            st.error(f"❌ 发生未知错误：{e}")
    else:
        # 显示使用说明
        st.info("👆 请上传包含以下列的 Excel 文件：**日期**、**日报推送**、**日报未推送**、**手表佩戴**（或腕表佩戴）、**手表未佩戴**（或腕表未佩戴）")
        
        # 显示示例
        with st.expander("📋 查看数据格式示例"):
            example_data = {
                '日期': ['2025.11.25', '2025.11.26', '2025.11.27'],
                '腕表未佩戴': [266, 287, 271],
                '腕表佩戴': [389, 370, 388],
                '日报未推送': [252, 280, 288],
                '日报推送': [403, 377, 371]
            }
            st.dataframe(pd.DataFrame(example_data), use_container_width=True)

if __name__ == "__main__":
    main()
