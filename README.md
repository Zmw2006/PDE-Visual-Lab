# PDE Visual Lab｜偏微分方程可视化实验室

用交互图像理解偏微分方程。调整时间和参数，观察解的传播、扩散，以及特征线何时相交。界面与说明均为中文。

## 最简单的打开方式（推荐）

1. 在仓库页面点击绿色 **Code → Download ZIP**，下载并解压。
2. 双击文件夹里的 **`index.html`**。

网页会在浏览器中打开；**不用安装 Python、配置环境，也不用联网**。在手机上，也可把 `index.html` 保存到本地后用支持本地 HTML 的浏览器打开。页面提供播放/暂停、时间与参数调节、Burgers 方程初始点反查。

> GitHub 上点击 `index.html` 通常只会看到文件代码；请先下载，再在电脑上双击本地文件。

## 当前内容

| 模块 | 方程与初值 | 能看到什么 |
| --- | --- | --- |
| 线性输运 | $u_t+c u_x=0$；高斯初值 | 特征线 $x=\xi+ct$，波形随速度平移 |
| 无黏 Burgers | $u_t+u u_x=0$；$u_0(x)=-\sin x$ | 特征线图、初始点反查、$t=1$ 首次失去经典解 |
| 热方程 | $u_t=\kappa u_{xx}$；两个正弦模态 | 高频模态以更快的速率衰减 |
| 波动方程 | $u_{tt}=c^2u_{xx}$；高斯初位移、零初速度 | 达朗贝尔公式与波峰向两边传播 |

## 可选：运行原来的 Python 版本

如果你想使用 Streamlit 与 Plotly 版本，才需要 Python 3.10 或更新版本。在仓库根目录执行：

```bash
python -m venv .venv
```

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

macOS / Linux：

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

浏览器会打开应用（通常是 `http://localhost:8501`）。侧边栏选择方程，滑块控制时间与参数；可以用鼠标悬停在图线上读取坐标。

## 从 Burgers 页理解“求出 $u(x,t)$”

对初始点 $\xi$，沿特征线：

$$x=\xi-t\sin\xi,\qquad u=-\sin\xi.$$

假设选中 $(x,t)=(0.5,0.4)$，应用会先解方程 $x=\xi-t\sin\xi$ 求得 $\xi$，再代入 $u(x,t)=-\sin\xi$。这样从参数形式得到指定坐标的函数值。对 $0\le t<1$，

$$\frac{\partial x}{\partial\xi}=1-t\cos\xi>0,$$

所以每个 $x\in[-\pi,\pi]$ 对应唯一的 $\xi$。到 $t=1$，$\xi=0$ 处导数首次为零，解的空间导数发生爆破。再往后参数曲线可能折返，不能把它当成单值的经典解。**当前项目不计算激波后的熵弱解**。

## 验证与代码结构

```bash
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

## 模型范围

这是理解基础 PDE 的教学项目。热方程使用 $2\pi$ 周期边界条件；输运方程和波动方程在整条实线上取高斯初值。Burgers 特征图显示 $[-\pi,\pi]$ 范围的初始点；在 $t\ge1$ 时只显示特征曲线，不提供激波弱解。当前曲线来自解析公式，不是通用 PDE 数值求解器。

## 可继续扩展

1. 用守恒型有限体积方法计算 Burgers 方程的熵弱解，并与特征线相交图对照。
2. 在热方程页面加入任意初值的傅里叶级数近似，并显示截断误差。
3. 为波动方程加入非零初速度，逐步解释达朗贝尔积分项。

项目采用 MIT 许可，见 [LICENSE](LICENSE)。
