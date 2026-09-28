# PDE Visual Lab｜偏微分方程可视化实验室

用交互图像理解偏微分方程。调整时间和参数，观察解的传播、扩散，以及特征线何时相交。界面与说明均为中文。

这是一个面向初学者的教学项目：从具体初值出发，一边拖动参数看图，一边对照解析公式理解图像。项目包含一个**双击即可打开的离线版**，也保留适合学习 Python 绘图的 Streamlit 版。

## 最简单的打开方式（推荐）

1. 在仓库页面点击绿色 **Code → Download ZIP**，下载并解压。
2. 双击文件夹里的 **`index.html`**。

网页会在浏览器中打开；**不用安装 Python、配置环境，也不用联网**。在手机上，也可把 `index.html` 保存到本地后用支持本地 HTML 的浏览器打开。页面提供播放/暂停、时间与参数调节、Burgers 方程初始点反查。

打开后，先在左侧选“输运方程”，拖动时间滑块；灰色虚线是 $t=0$ 的初始波形，蓝色实线是当前时刻的波形。点击“播放演化”自动播放，点击“重置”恢复本模块的初始设置。学完平移后，再选“Burgers 方程”观察特征线的变化。

> GitHub 上点击 `index.html` 通常只会看到文件代码；请先下载，再在电脑上双击本地文件。

## 当前内容

| 模块 | 方程与初值 | 能看到什么 |
| --- | --- | --- |
| 线性输运 | $u_t+c u_x=0$；高斯初值 | 特征线 $x=\xi+ct$，波形随速度平移 |
| 无黏 Burgers | $u_t+u u_x=0$；$u_0(x)=-\sin x$ | 特征线图、初始点反查、$t=1$ 首次失去经典解 |
| 热方程 | $u_t=\kappa u_{xx}$；两个正弦模态 | 高频模态以更快的速率衰减 |
| 波动方程 | $u_{tt}=c^2u_{xx}$；高斯初位移、零初速度 | 达朗贝尔公式与波峰向两边传播 |

### 推荐的学习顺序

1. **输运方程**：改变速度 $c$ 的正负，看波峰向右或向左移动，理解“沿特征线值不变”。
2. **Burgers 方程**：先看右侧的 $(x,t)$ 特征线，再在 $t<1$ 时选一个位置 $x$，看程序如何反查初始点 $\xi$。
3. **热方程**：增加时间或扩散系数 $\kappa$，对比两个不同频率的正弦模态如何衰减。
4. **波动方程**：从 $t=0$ 慢慢增大时间，看一个波包分为向左、向右传播的两束。

页面使用的是**指定初值的解析公式**，没有把任意 PDE 或任意初值交给通用数值求解器。

## 四个图像背后的数学

### 1. 线性输运：为什么只是平移？

设 $f(x)=e^{-(x/0.7)^2}$，考虑

$$
u_t+c u_x=0,\qquad u(x,0)=f(x).
$$

沿曲线 $x=x(t)$，链式法则给出

$$
\frac{\mathrm d}{\mathrm dt}u(x(t),t)=u_t+x'(t)u_x.
$$

让 $x'(t)=c$，右边便等于方程的左边，即 $0$。于是从 $x(0)=\xi$ 出发的特征线为 $x=\xi+ct$，沿它 $u$ 的值始终是 $f(\xi)$。给定 $(x,t)$ 时反推 $\xi=x-ct$，得到

$$
\boxed{u(x,t)=f(x-ct)=e^{-((x-ct)/0.7)^2}.}
$$

**操作验证：**令 $c=1,t=1$，波峰从 $x=0$ 移到 $x=1$；改成 $c=-1$，波峰则移到 $x=-1$。两次峰值都保持为 $1$。

### 2. Burgers 方程：为什么特征线会相交？

我们选择无黏 Burgers 方程与初值

$$
u_t+u u_x=0,\qquad u(x,0)=u_0(x)=-\sin x,\quad -\pi\leq x\leq\pi.
$$

从初始点 $x(0)=\xi$ 出发，取特征线速度 $x'(t)=u(x(t),t)$。沿此曲线有

$$
\frac{\mathrm d}{\mathrm dt}u(x(t),t)=u_t+x'(t)u_x=u_t+u u_x=0.
$$

因此这条特征线上的 $u$ 一直等于初始值 $u_0(\xi)=-\sin\xi$，它的速度也一直是 $-\sin\xi$。积分得到

$$
\boxed{x=\xi-t\sin\xi,\qquad u=-\sin\xi.}
$$

不同初始点的速度不同，所以特征线会互相靠近。右侧图画的正是不同 $\xi$ 对应的直线；其中橙色横线是当前时间，红色横线标出 $t=1$。

### 3. 热方程：为什么高频起伏消失得快？

在 $2\pi$ 周期区间，初值为两个正弦模态之和：

$$
u_t=\kappa u_{xx},\qquad u(x,0)=\sin x+\tfrac12\sin(2x),\quad\kappa>0.
$$

因为 $\sin(nx)$ 的二阶导数是 $-n^2\sin(nx)$，频率为 $n$ 的模态系数按 $e^{-\kappa n^2t}$ 衰减。取 $n=1$ 和 $n=2$，得到

$$
\boxed{u(x,t)=e^{-\kappa t}\sin x+\tfrac12e^{-4\kappa t}\sin(2x).}
$$

第二个模态的频率是两倍，衰减指数中的系数是四倍。固定 $\kappa$ 并增大 $t$，就能看到较细密的起伏先变弱；调大 $\kappa$ 会加快整个过程。

### 4. 波动方程：为什么一束变两束？

在整条实线上取高斯初位移 $f(x)=e^{-(x/0.7)^2}$ 和零初速度：

$$
u_{tt}=c^2u_{xx},\qquad u(x,0)=f(x),\qquad u_t(x,0)=0,\quad c>0.
$$

达朗贝尔公式此时化为

$$
\boxed{u(x,t)=\tfrac12f(x-ct)+\tfrac12f(x+ct).}
$$

第一项向右、第二项向左。$t=0$ 时两束半幅波包重合，合起来正好是初值；随时间增加，波峰中心逐渐移向 $x=ct$ 和 $x=-ct$。

## 从 Burgers 模块理解“求出 $u(x,t)$”

这一节重点回答“特征线方程算出来了，为什么还没看到 $u(x,t)$？”对初始点 $\xi$，沿特征线：

$$
x=\xi-t\sin\xi,\qquad u=-\sin\xi.
$$

这是一个以 $\xi$ 为参数的表示。要得到固定位置的函数值，必须先由 $x$ 和 $t$ **反求初始点 $\xi$**。例如选中 $(x,t)=(0.5,0.4)$，先解

$$
0.5=\xi-0.4\sin\xi\quad\Longrightarrow\quad\xi\approx0.781832,
$$

再代入第二个等式：

$$
\boxed{u(0.5,0.4)=-\sin(0.781832)\approx-0.704581.}
$$

这就是“从特征线求出 $u(x,t)$”的完整步骤。网页上的“指定位置 $x$”滑块做的也是这件事：在 $t<1$ 时用二分法求 $\xi$，然后计算 $-\sin\xi$。

为什么只在 $t<1$ 时反查？因为

$$
\frac{\partial x}{\partial\xi}=1-t\cos\xi>0,
$$

当 $0\le t<1$ 时，$1-t\cos\xi\ge1-t>0$。于是映射 $\xi\mapsto x$ 严格递增，每个 $x\in[-\pi,\pi]$ 对应唯一的 $\xi$。进一步由链式法则，

$$
u_x(x,t)=\frac{-\cos\xi}{1-t\cos\xi}.
$$

在 $\xi=0$ 处，这个导数是 $-1/(1-t)$，当 $t\uparrow1$ 时趋向 $-\infty$。**$t=1$ 是首次梯度爆破的时刻**；之后特征线相交，参数曲线可能折返，不能把它当作单值的全局经典解。项目会继续画出特征线帮助理解，但**不计算激波后的熵弱解**，也不会把折返曲线说成真正的弱解。

## 可选：运行原来的 Python 版本

**只想看可视化时，不需要这一步。** 如果你想学习或修改 Streamlit 与 Plotly 代码，才需要 Python 3.10 或更新版本。在仓库根目录执行：

```bash
python -m venv .venv
```

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

macOS / Linux：

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

浏览器会打开应用（通常是 `http://localhost:8501`）。侧边栏选择方程，滑块控制时间与参数；可以用鼠标悬停在图线上读取坐标。

停止服务时，在运行命令的终端按 `Ctrl+C`。若 Windows PowerShell 不允许激活虚拟环境，可以直接运行 `.venv\Scripts\python -m pip install -r requirements.txt`，再运行 `.venv\Scripts\python -m streamlit run app.py`。

## 验证与代码结构

普通使用者不需要运行测试。修改代码时，可以使用以下命令，其中 `node` 只是离线版的开发检查工具，**双击 `index.html` 不需要安装 Node.js**：

```bash
node tests/check_html.mjs
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m compileall -q app.py pde_visual_lab
```

- `index.html`：无需安装或联网的单文件版，推荐从这里开始。
- `app.py`：可选的 Streamlit 页面与 Plotly 图像。
- `pde_visual_lab/models.py`：四种模型的解析式及 Burgers 初始点反求。
- `tests/test_models.py`：初值、传播公式与 Burgers 特征映射的数值验证。
- `tests/check_html.mjs`：使用 Node.js 内置功能检查离线页面四个模块的渲染与交互。
- `.github/workflows/test.yml`：每次推送与拉取请求自动验证 Python 与离线版。

离线版把页面、样式、解析公式和交互逻辑全部放在 `index.html`；它没有外部脚本依赖。Python 版把计算放在 `pde_visual_lab/models.py`，页面放在 `app.py`。两个入口都展示本 README 的四类指定模型，适合从“直接使用”逐步过渡到“阅读和修改源码”。

## 常见问题

**Q：在 GitHub 点开 `index.html`，为什么只看到代码？**  
A：GitHub 的文件页展示源代码。选择 **Code → Download ZIP**，解压后双击本地的 `index.html`。

**Q：没有网络或没有 Python，还能运行吗？**  
A：能。离线版使用一个自包含 HTML 文件；下载好以后，打开和使用都不需要网络、Python 或 Node.js。

**Q：为什么 Burgers 方程在 $t\ge1$ 时不显示指定位置的 $u(x,t)$？**  
A：原先“反求唯一 $\xi$”的方法不再给出全局经典解。要研究激波之后的解，还需要弱解与熵条件；当前项目没有实现它们。

**Q：能输入任意方程和初值吗？**  
A：目前不能。四个模块采用固定的教学例子，目的是让图像和推导对应清楚；它还不是通用的 PDE 求解器。

**Q：离线版和 Python 版选哪个？**  
A：想直接观察现象，选 `index.html`；想继续学习 Python、Streamlit 和 Plotly 的实现，选 `app.py`。

## 模型范围

这是理解基础 PDE 的教学项目。热方程使用 $2\pi$ 周期边界条件；输运方程和波动方程在整条实线上取高斯初值。Burgers 特征图显示 $[-\pi,\pi]$ 范围的初始点；在 $t\ge1$ 时只显示特征曲线，不提供激波弱解。当前曲线来自解析公式，不是通用 PDE 数值求解器。

## 可继续扩展

1. 用守恒型有限体积方法计算 Burgers 方程的熵弱解，并与特征线相交图对照。
2. 在热方程页面加入任意初值的傅里叶级数近似，并显示截断误差。
3. 为波动方程加入非零初速度，逐步解释达朗贝尔积分项。

项目采用 MIT 许可，见 [LICENSE](LICENSE)。
