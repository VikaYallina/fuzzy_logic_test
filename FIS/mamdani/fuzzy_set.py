import math

import numpy as np
import copy
import matplotlib.pyplot as plt


class FuzzySet:
    _precision: int = 3

    def __init__(self, name, domain_min, domain_max, res):

        self._domain_min = domain_min
        self._domain_max = domain_max
        self._res = res

        self._domain = np.linspace(domain_min, domain_max, res)
        self._dom = np.zeros(self._domain.shape)
        self._name = name
        self._last_dom_value = 0

    def __getitem__(self, x_val):
        return self._dom[np.abs(self._domain - x_val).argmin()]

    def __setitem__(self, x_val, dom):
        self._dom[np.abs(self._domain - x_val).argmin()] = round(dom, self._precision)

    def __str__(self):
        return ' + '.join([str(a) + '/' + str(b) for a, b in zip(self._dom, self._domain)])

    def __get_last_dom_value(self):
        return self._last_dom_value

    def __set_last_dom_value(self, d):
        self._last_dom_value = d

    last_dom_value = property(__get_last_dom_value, __set_last_dom_value)

    @property
    def name(self):
        return self._name

    @property
    def empty(self):
        return np.all(self._dom == 0)

    @property
    def name(self):
        return self._name

    @classmethod
    def create_trapezoidal(cls, name, domain_min, domain_max, res, a, b, c, d):
        t1fs = cls(name, domain_min, domain_max, res)

        a = t1fs._adjust_domain_val(a)
        b = t1fs._adjust_domain_val(b)
        c = t1fs._adjust_domain_val(c)
        d = t1fs._adjust_domain_val(d)

        t1fs._dom = np.round(
            np.minimum(np.maximum(np.minimum((t1fs._domain - a) / (b - a), (d - t1fs._domain) / (d - c)), 0), 1),
            t1fs._precision)
        return t1fs

    @classmethod
    def create_triangular(cls, name, domain_min, domain_max, res, a, b, c):
        t1fs = cls(name, domain_min, domain_max, res)

        a = t1fs._adjust_domain_val(a)
        b = t1fs._adjust_domain_val(b)
        c = t1fs._adjust_domain_val(c)

        if b == a:
            t1fs._dom = np.round(np.maximum((c - t1fs._domain) / (c - b), 0), t1fs._precision)
        elif b == c:
            t1fs._dom = np.round(np.maximum((t1fs._domain - a) / (b - a), 0), t1fs._precision)
        else:
            t1fs._dom = np.round(np.maximum(np.minimum((t1fs._domain - a) / (b - a), (c - t1fs._domain) / (c - b)), 0),
                                 t1fs._precision)

        return t1fs

    @classmethod
    def create_gauss(cls, name, domain_min, domain_max, res, sigma, c):
        t1fs = cls(name, domain_min, domain_max, res)

        sigma = t1fs._adjust_domain_val(sigma)
        c = t1fs._adjust_domain_val(c)

        t1fs._dom = np.round(np.power(np.e, -(t1fs._domain - c) ** 2 / (2 * sigma ** 2)), t1fs._precision)
        return t1fs

    @classmethod
    def create_z(cls, name, domain_min, domain_max, res, a, b):
        t1fs = cls(name, domain_min, domain_max, res)

        a = t1fs._adjust_domain_val(a)
        b = t1fs._adjust_domain_val(b)

        t1fs._dom = np.round(np.array([t1fs.z_func(t, a, b) for t in t1fs._domain]), t1fs._precision)
        return t1fs

    @classmethod
    def create_pi(cls, name, domain_min, domain_max, res, a, b, c, d):
        t1fs = cls(name, domain_min, domain_max, res)

        a = t1fs._adjust_domain_val(a)
        b = t1fs._adjust_domain_val(b)
        c = t1fs._adjust_domain_val(c)
        d = t1fs._adjust_domain_val(d)

        t1fs._dom = np.round(np.array([t1fs.pi_func(t, a, b, c, d) for t in t1fs._domain]), t1fs._precision)
        return t1fs

    @classmethod
    def create_s(cls, name, domain_min, domain_max, res, a, b):
        t1fs = cls(name, domain_min, domain_max, res)

        a = t1fs._adjust_domain_val(a)
        b = t1fs._adjust_domain_val(b)

        t1fs._dom = np.round(np.array([t1fs.s_func(t, a, b) for t in t1fs._domain]), t1fs._precision)
        return t1fs

    def pi_func(self, x, a, b, c, d):
        mid_ab = (a + b) / 2.0
        mid_cd = (c + d) / 2.0
        if x <= a:
            return 0.0
        elif a <= x <= mid_ab:
            return 2 * np.power((x - a) / (b - a), 2)
        elif mid_ab <= x <= b:
            return 1 - 2 * np.power((x - b) / (b - a), 2)
        elif b <= x <= c:
            return 1.0
        elif c <= x <= mid_cd:
            return 1 - 2 * np.power((x - c) / (d - c), 2)
        elif mid_cd <= x <= d:
            return 2 * np.power((x - d) / (d - c), 2)
        else:
            return 0.0

    def z_func(self, x, a, b):
        mid = a + b / 2.0
        if x <= a:
            return 1.0
        elif a <= x <= mid:
            return 1 - 2 * np.power((x - a) / (b - a), 2)
        elif mid <= x <= b:
            return 2 * np.power((x - b) / (b - a), 2)
        else:
            return 0.0

    def s_func(self, x, a, b):
        mid = a + b / 2.0
        if x <= a:
            return 0.0
        elif a <= x <= mid:
            return 2 * np.power((x - a) / (b - a), 2)
        elif mid <= x <= b:
            return 1 - 2 * np.power((x - b) / (b - a), 2)
        else:
            return 1.0

    def _adjust_domain_val(self, x_val):
        return self._domain[np.abs(self._domain - x_val).argmin()]

    def clear_set(self):
        self._dom.fill(0)

    def min_scalar(self, val):

        result = FuzzySet(f'({self._name}) min ({val})', self._domain_min, self._domain_max, self._res)
        result._dom = np.minimum(self._dom, val)

        return result

    def max_scalar(self, val):

        result = FuzzySet(f'({self._name}) max ({val})', self._domain_min, self._domain_max, self._res)
        result._dom = np.maximum(self._dom, val)

        return result

    def union(self, f_set):

        result = FuzzySet(f'({self._name}) union ({f_set._name})', self._domain_min, self._domain_max, self._res)
        result._dom = np.maximum(self._dom, f_set._dom)

        return result

    def intersection(self, f_set):

        result = FuzzySet(f'({self._name}) intersection ({f_set._name})', self._domain_min, self._domain_max, self._res)
        result._dom = np.minimum(self._dom, f_set._dom)

        return result

    def complement(self):

        result = FuzzySet(f'not ({self._name})', self._domain_min, self._domain_max, self._res)
        result._dom = 1 - self._dom

        return result

    def cog_defuzzify(self):

        num = np.sum(np.multiply(self._dom, self._domain))
        den = np.sum(self._dom)

        return num / den

    def domain_elements(self):
        return self._domain

    def dom_elements(self):
        return self._dom

    def plot_set(self, ax, col=''):
        ax.plot(self._domain, self._dom, col)
        ax.set_ylim([-0.1, 1.1])
        ax.set_title(self._name)
        ax.grid(True, which='both', alpha=0.4)
        ax.set(xlabel='x', ylabel='$\mu(x)$')


if __name__ == "__main__":
    s = FuzzySet.create_trapezoidal('test', 1, 100, 100, 20, 30, 50, 80)

    print(s.empty)

    u = FuzzySet('u', 1, 100, 100)

    print(u.empty)

    t = FuzzySet.create_pi("p", 0, 400, 400, 265, 300, 486.3, 843.9)

    # g = FuzzySet.create_gauss('gauss', 0, 90, 90, 5.5, 30)

    # z = FuzzySet.create_z('z', 0,4,4,0,2)
    fig, axs = plt.subplots(1, 1)

    # s.union(t).complement().intersection(s).min_scalar(0.2).plot_set(axs)
    t.plot_set(axs)

    plt.show()
    print(s.cog_defuzzify())
