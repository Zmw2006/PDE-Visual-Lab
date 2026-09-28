"""运行方式：streamlit run app.py。"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from pde_visual_lab.models import (
    advection,
    burgers_foot,
    burgers_initial,
    burgers_position,
    gaussian,
    heat,
    wave,
)


st.set_page_config(page_title="PDE Visual Lab · 偏微分方程可视化", page_icon="∂", layout="wide")


def new_figure(title, xlabel="位置 x", ylabel="解 u(x,t)"):
    fig = go.Figure()
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template="plotly_white",
        height=480,
        legend=dict(orientation="h", y=1.12),
        margin=dict(l=20, r=20, t=90, b=20),
    )
    return fig


def line(fig, x, y, name, color, dash=None):
    fig.add_trace(
        go.Scatter(
            x=x, y=y, mode="lines", name=name,
            line=dict(color=color, width=3, dash=dash),
        )
    )


st.title("∂ PDE Visual Lab")
st.caption("动手改变参数，看偏微分方程的解与特征线怎样演化")

topic = st.sidebar.radio(
    "选择方程",
    ["线性输运方程", "Burgers 方程与特征线", "热方程", "波动方程"],
)
st.sidebar.markdown("**使用方法**：拖动时间和参数，比较初值与当前解；在 Burgers 页面选择位置，追踪它的初始点。")

if topic == "线性输运方程":
    st.header("线性输运：形状不变地移动")
    st.latex(r"u_t+c u_x=0,\qquad u(x,0)=e^{-(x/0.7)^2}")
    speed = st.slider("传播速度 c（负值向左）", -2.0, 2.0, 1.0, 0.1)
    t = st.slider("时间 t", 0.0, 3.0, 0.8, 0.05)
    x = np.linspace(-6, 6, 800)
    fig = new_figure("波形平移")
    line(fig, x, gaussian(x), "初值 t=0", "#94a3b8", "dash")
    line(fig, x, advection(x, t, speed), f"当前 t={t:g}", "#2563eb")
    fig.update_yaxes(range=[-0.05, 1.1])
    st.plotly_chart(fig, width="stretch")
    st.latex(r"x=\xi+ct,\qquad u(x,t)=u_0(\xi)=u_0(x-ct)")
    st.info("沿着每条直线 x=ξ+ct，解的数值保持不变。速度 c 决定移动方向和快慢。")

elif topic == "Burgers 方程与特征线":
    st.header("Burgers 方程：特征线何时相交？")
    st.latex(r"u_t+u\,u_x=0,\qquad u(x,0)=-\sin x\quad (-\pi\leq x\leq\pi)")
    t = st.slider("时间 t", 0.0, 1.6, 0.4, 0.02)
    xi = np.linspace(-np.pi, np.pi, 800)
    times = np.linspace(0, 1.6, 180)
    left, right = st.columns(2)
    with left:
        fig = new_figure("特征线图：横轴是 x，纵轴是 t", "位置 x", "时间 t")
        for foot in np.linspace(-np.pi, np.pi, 23):
            fig.add_trace(
                go.Scatter(
                    x=burgers_position(foot, times), y=times,
                    mode="lines", showlegend=False,
                    line=dict(color="#2563eb", width=1.6),
                    hovertemplate=f"初始点 ξ={foot:.2f}<br>x=%{{x:.2f}}<br>t=%{{y:.2f}}<extra></extra>",
                )
            )
        fig.add_hline(y=t, line_color="#f97316", line_dash="dash")
        fig.add_hline(y=1, line_color="#dc2626", line_dash="dot", annotation_text="首次失去经典解 t=1")
        fig.update_xaxes(range=[-4, 4])
        fig.update_yaxes(range=[0, 1.6])
        st.plotly_chart(fig, width="stretch")
    with right:
        fig = new_figure("固定时刻的参数曲线：每个 ξ 对应 (x,u)")
        line(fig, xi, burgers_initial(xi), "初值 t=0", "#94a3b8", "dash")
        line(fig, burgers_position(xi, t), burgers_initial(xi), f"参数曲线 t={t:g}", "#2563eb")
        fig.update_xaxes(range=[-np.pi, np.pi])
        fig.update_yaxes(range=[-1.15, 1.15])
        st.plotly_chart(fig, width="stretch")
    st.latex(r"x=\xi-t\sin\xi,\qquad u= -\sin\xi,\qquad \frac{\partial x}{\partial\xi}=1-t\cos\xi")
    if t < 1:
        xpick = st.slider("选一个位置 x，反查特征线的初始点", -3.0, 3.0, 0.0, 0.05)
        foot = burgers_foot(xpick, t)
        st.success(
            f"在 (x,t)=({xpick:.2f},{t:.2f})，特征线从 ξ={foot:.4f} 出发；"
            f"因此 u(x,t)=−sin(ξ)={float(burgers_initial(foot)):.4f}。"
        )
    else:
        st.warning(
            "t≥1 时，ξ=0 附近的特征映射不再处处可逆；右图只是参数曲线，"
            "不能作为单值的全局经典解。这里未计算激波后的弱解。"
        )
    st.caption("因为初始斜率 u₀'(ξ)=−cos ξ 的最小值为 −1，首次梯度爆破时刻为 t*=1。")

elif topic == "热方程":
    st.header("热方程：高频起伏消散得更快")
    st.latex(r"u_t=\kappa u_{xx},\qquad u(x,0)=\sin x+\tfrac12\sin(2x)")
    diffusivity = st.slider("扩散系数 κ", 0.05, 1.0, 0.3, 0.05)
    t = st.slider("时间 t", 0.0, 5.0, 1.0, 0.1)
    x = np.linspace(-np.pi, np.pi, 800)
    fig = new_figure("周期区间 [-π,π] 内的扩散")
    line(fig, x, heat(x, 0, diffusivity), "初值 t=0", "#94a3b8", "dash")
    line(fig, x, heat(x, t, diffusivity), f"当前 t={t:g}", "#dc2626")
    fig.update_yaxes(range=[-1.5, 1.5])
    st.plotly_chart(fig, width="stretch")
    st.latex(r"u(x,t)=e^{-\kappa t}\sin x+\tfrac12e^{-4\kappa t}\sin(2x)")
    st.info("二倍频项的指数衰减率是四倍：波峰与波谷逐渐变平。这里采用周期边界条件。")

else:
    st.header("波动方程：一个脉冲分成左右两半")
    st.latex(r"u_{tt}=c^2u_{xx},\qquad u(x,0)=e^{-(x/0.7)^2},\qquad u_t(x,0)=0")
    speed = st.slider("波速 c", 0.2, 2.0, 1.0, 0.1)
    t = st.slider("时间 t", 0.0, 3.0, 1.0, 0.05)
    x = np.linspace(-7, 7, 900)
    fig = new_figure("达朗贝尔公式：左右传播")
    line(fig, x, gaussian(x), "初位移 t=0", "#94a3b8", "dash")
    line(fig, x, wave(x, t, speed), f"当前 t={t:g}", "#7c3aed")
    fig.update_yaxes(range=[-0.05, 1.1])
    st.plotly_chart(fig, width="stretch")
    st.latex(r"u(x,t)=\tfrac12 f(x-ct)+\tfrac12 f(x+ct)")
    st.info("初速度为零，所以两个方向各分得一半振幅；两束波重叠时数值相加。")

st.divider()
st.caption("解析模型仅用于展示上述初值和边界设定；Burgers 方程在 t≥1 的弱解不在当前版本中。")
