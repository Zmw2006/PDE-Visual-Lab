"""可视化使用的方程模型；不依赖界面，便于单独验证。"""

import numpy as np


def gaussian(x, width=0.7):
    """初值 f(x)=exp(-(x/width)^2)。"""
    x = np.asarray(x)
    return np.exp(-((x / width) ** 2))


def advection(x, t, speed, width=0.7):
    """u_t+c u_x=0, u(x,0)=f(x)。"""
    return gaussian(np.asarray(x) - speed * t, width)


def burgers_initial(xi):
    """Burgers 方程的初值 u_0(x)=-sin(x)。"""
    return -np.sin(np.asarray(xi))


def burgers_position(xi, t):
    """特征线 x=xi+t*u_0(xi)。"""
    return np.asarray(xi) + t * burgers_initial(xi)


def burgers_foot(x, t, iterations=65):
    """在 0<=t<1、-pi<=x<=pi 时反求唯一的初始点 xi。"""
    if not 0 <= t < 1:
        raise ValueError("只有 0 ≤ t < 1 时才能反求全局经典解")
    if not -np.pi <= x <= np.pi:
        raise ValueError("x 必须属于 [-π, π]")
    low, high = -np.pi, np.pi
    for _ in range(iterations):
        mid = (low + high) / 2
        if burgers_position(mid, t) < x:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def heat(x, t, diffusivity):
    """周期初值 sin(x)+0.5 sin(2x) 的热方程解析解。"""
    x = np.asarray(x)
    return np.exp(-diffusivity * t) * np.sin(x) + 0.5 * np.exp(
        -4 * diffusivity * t
    ) * np.sin(2 * x)


def wave(x, t, speed, width=0.7):
    """零初速度和高斯初位移对应的达朗贝尔解。"""
    x = np.asarray(x)
    return 0.5 * (gaussian(x - speed * t, width) + gaussian(x + speed * t, width))
