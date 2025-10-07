import streamlit as st
import graphviz
import numpy as np

# 设置页面配置
st.set_page_config(
    page_title="创业决策辅助系统",
    page_icon="💼",
    layout="wide"
)

# 页面标题
st.title("💼 创业决策辅助系统")
st.write("基于多因素分析的创业决策树模型，帮助您做出更明智的创业选择")

# 侧边栏 - 输入参数
st.sidebar.header("请输入您的情况")

# 收集用户输入
funds = st.sidebar.slider("初始资金(万元)", 0, 200, 50)
risk_tolerance = st.sidebar.radio(
    "您的风险承受能力",
    ("高", "中", "低")
)
experience = st.sidebar.slider("相关行业经验(年)", 0, 10, 2)
market_demand = st.sidebar.radio(
    "您评估的市场需求",
    ("高", "中", "低")
)
business_idea = st.sidebar.text_input("您的创业想法简述", "例如：开一家特色咖啡店")

# 转换为数值以便计算
risk_score = {"高": 3, "中": 2, "低": 1}[risk_tolerance]
market_score = {"高": 3, "中": 2, "低": 1}[market_demand]

# 计算决策分数
score = (
    min(funds / 100, 1) * 0.3 +  # 资金权重30%
    (risk_score / 3) * 0.2 +     # 风险承受权重20%
    min(experience / 5, 1) * 0.2 +  # 经验权重20%
    (market_score / 3) * 0.3     # 市场权重30%
) * 100

# 决策逻辑
decision_path = []
recommendation = ""
explanation = ""

decision_path.append("开始创业评估")

if funds >= 50:
    decision_path.append(f"资金充足({funds}万元) → 评估风险承受能力")
    if risk_tolerance in ["高", "中"]:
        decision_path.append(f"风险承受能力{risk_tolerance} → 评估行业经验")
        if experience >= 2:
            decision_path.append(f"行业经验充足({experience}年) → 评估市场需求")
            if market_demand == "高":
                recommendation = "强烈建议创业"
                explanation = "您的资金充足，风险承受能力良好，有一定行业经验，且市场需求高，创业成功几率较大。"
            elif market_demand == "中":
                recommendation = "建议创业，但需做好市场调研"
                explanation = "您的基本条件良好，但市场需求中等，建议进一步细化市场定位和竞争策略。"
            else:
                recommendation = "建议暂缓创业，重新评估市场"
                explanation = "市场需求较低，即使其他条件良好，也面临较大市场风险。"
        else:
            recommendation = "建议先积累行业经验"
            explanation = f"您的资金和风险承受能力尚可，但行业经验不足({experience}年)，建议先在目标行业积累经验。"
    else:
        recommendation = "建议谨慎考虑创业"
        explanation = "您的风险承受能力较低，创业可能带来较大心理和经济压力，建议谨慎决策。"
else:
    recommendation = "建议先积累资金或寻求融资"
    explanation = f"您的初始资金不足({funds}万元)，难以应对创业初期的各种开支和风险，建议先积累资金。"

# 显示决策结果
st.subheader("📊 决策结果分析")

col1, col2 = st.columns(2)

with col1:
    st.metric("创业适宜度评分", f"{score:.1f}/100分")
    st.success(f"建议: {recommendation}")
    st.info(f"解释: {explanation}")
    
    st.subheader("🔍 决策路径")
    for i, step in enumerate(decision_path):
        st.write(f"{i+1}. {step}")

with col2:
    st.subheader("🌳 决策树可视化")
    # 创建决策树可视化
    dot = graphviz.Digraph()
    dot.attr(rankdir="LR")
    
    # 添加节点
    dot.node("start", "考虑创业?")
    dot.node("funds", f"资金≥50万?\n您的情况: {funds}万")
    
    if funds >= 50:
        dot.node("risk", f"风险承受能力?\n您的情况: {risk_tolerance}")
        dot.edge("start", "funds", "是")
        
        if risk_tolerance in ["高", "中"]:
            dot.node("exp", f"经验≥2年?\n您的情况: {experience}年")
            dot.edge("funds", "risk", "是")
            dot.edge("risk", "exp", "高/中")
            
            if experience >= 2:
                dot.node("market", f"市场需求?\n您的情况: {market_demand}")
                dot.edge("exp", "market", "是")
                dot.edge("market", "result", recommendation, style="bold", color="green")
            else:
                dot.edge("exp", "result", recommendation, style="bold", color="orange")
        else:
            dot.edge("funds", "risk", "是")
            dot.edge("risk", "result", recommendation, style="bold", color="orange")
    else:
        dot.edge("start", "funds", "是")
        dot.edge("funds", "result", recommendation, style="bold", color="orange")
    
    dot.node("result", recommendation, shape="box", style="filled", color="lightgreen")
    
    # 显示决策树
    st.graphviz_chart(dot)

# 决策建议详情
st.subheader("💡 详细决策建议")
if score >= 70:
    st.write("""
    1. 制定详细的商业计划，明确盈利模式
    2. 建立核心团队，弥补自身短板
    3. 做好资金规划，预留6-12个月的运营资金
    4. 考虑从小规模试点开始，验证商业模式
    """)
elif score >= 40:
    st.write("""
    1. 先通过兼职或副业形式测试创业想法
    2. 积极寻找合作伙伴，分担风险和资源压力
    3. 参加相关行业培训，提升专业能力
    4. 建立人脉网络，寻找潜在客户和投资人
    """)
else:
    st.write("""
    1. 优先考虑就业，积累资金和经验
    2. 深入研究目标行业，找出市场痛点
    3. 学习商业知识，为未来创业做准备
    4. 关注行业动态，等待合适的创业时机
    """)

# 底部信息
st.markdown("---")
st.write("提示：本决策工具仅供参考，实际创业决策需综合更多因素考虑。")
