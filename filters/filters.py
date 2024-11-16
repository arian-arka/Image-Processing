import math, numpy

import numpy as np


class Filters:
    @staticmethod
    def _loop(dim, callback):
        matrix = [[0 for j in range(dim[1])] for i in range(dim[0])]
        for u in range(dim[0]):
            for v in range(dim[1]):
                matrix[u][v] = callback(u, v)
        return matrix

    @staticmethod
    def idealLPF(dim, d0):
        def callback(u, v):
            d = math.sqrt((u - dim[0] / 2) ** 2 + (v - dim[1] / 2) ** 2)
            return 0 if d0 > d else 1

        return Filters._loop(dim, callback)

    @staticmethod
    def idealHPF(dim, d0):
        def callback(u, v):
            d = math.sqrt((u - dim[0] / 2) ** 2 + (v - dim[1] / 2) ** 2)
            return 1 if d0 > d else 0

        return Filters._loop(dim, callback)

    @staticmethod
    def idealBPF(dim, d0, bw):
        def callback(u, v):
            d = math.sqrt((u - dim[0] / 2) ** 2 + (v - dim[1] / 2) ** 2)
            return 0 if d <= (d0 - bw / 2) or d >= (d0 + bw / 2) else 1

        return Filters._loop(dim, callback)

    @staticmethod
    def idealBSF(dim, d0, bw):
        def callback(u, v):
            d = math.sqrt((u - dim[0] / 2) ** 2 + (v - dim[1] / 2) ** 2)
            return 1 if d <= (d0 - bw / 2) or d >= (d0 + bw / 2) else 0

        return Filters._loop(dim, callback)

    @staticmethod
    def gaussianLPF(dim, d0):
        def callback(u, v):
            d = math.sqrt((u - dim[0] / 2) ** 2 + (v - dim[1] / 2) ** 2)
            return math.e ** (- (d ** 2 / (2 * d0 ** 2)))

        return Filters._loop(dim, callback)

    @staticmethod
    def gaussianHPF(dim, d0):
        def callback(u, v):
            d = math.sqrt((u - dim[0] / 2) ** 2 + (v - dim[1] / 2) ** 2)
            return 1 - math.e ** (- (d ** 2 / (2 * d0 ** 2)))

        return Filters._loop(dim, callback)

    @staticmethod
    def gaussianBPF(dim, d0, bw):  # search
        def callback(u, v):
            d = math.sqrt((u - dim[0] / 2) ** 2 + (v - dim[1] / 2) ** 2)
            if bw * d == 0:
                return math.exp(- ((d ** 2 - d0 ** 2) / (2 * 0.000001)) ** 2)
            return math.exp(- ((d ** 2 - d0 ** 2) / (2 * bw * d)) ** 2)

        return Filters._loop(dim, callback)

    @staticmethod
    def gaussianBSF(dim, d0, bw):
        def callback(u, v):
            d = math.sqrt((u - dim[0] / 2) ** 2 + (v - dim[1] / 2) ** 2)
            if bw * d == 0:
                return 1 - math.exp(- ((d ** 2 - d0 ** 2) / (2 * 0.000001)) ** 2)
            return 1 - math.exp(- ((d ** 2 - d0 ** 2) / (2 * bw * d)) ** 2)

        return Filters._loop(dim, callback)

    @staticmethod
    def butterworthLPF(dim, d0, _2n):
        def callback(u, v):
            d = math.sqrt((u - dim[0] / 2) ** 2 + (v - dim[1] / 2) ** 2)
            return 1 / (1 + (d / d0) ** (2 * _2n))

        return Filters._loop(dim, callback)

    @staticmethod
    def butterworthHPF(dim, d0, _2n):
        def callback(u, v):
            d = math.sqrt((u - dim[0] / 2) ** 2 + (v - dim[1] / 2) ** 2)
            if d == 0:
                return 1 / (1 + (d0 / 0.000001) ** (2 * _2n))
            return 1 / (1 + (d0 / d) ** (2 * _2n))

        return Filters._loop(dim, callback)

    @staticmethod
    def butterworthBPF(dim, d0, bw, _2n):  ##### search
        def callback(u, v):
            d = math.sqrt((u - dim[0] / 2) ** 2 + (v - dim[1] / 2) ** 2)
            if d == 0:
                return 1 / (1 + ((d ** 2 - d0 ** 2) / (0.000001)) ** (2 * _2n))
            return 1 / (1 + ((d ** 2 - d0 ** 2) / (d * bw)) ** (2 * _2n))

        return Filters._loop(dim, callback)

    @staticmethod
    def butterworthBSF(dim, d0, bw, _2n):
        def callback(u, v):
            d = math.sqrt((u - dim[0] / 2) ** 2 + (v - dim[1] / 2) ** 2)
            if d ** 2 - d0 ** 2 == 0:
                return 1 / (1 + ((d * bw) / (0.000001)) ** (2 * _2n))
            return 1 / (1 + ((d * bw) / (d ** 2 - d0 ** 2)) ** (2 * _2n))

        return Filters._loop(dim, callback)

    @staticmethod
    def notchIdeal(dim, d0, u0, v0):
        def callback(u, v):
            d1 = math.sqrt((u - dim[0] / 2 - u0) ** 2 + (v - dim[1] / 2 - v0) ** 2)
            d2 = math.sqrt((u - dim[0] / 2 + u0) ** 2 + (v - dim[1] / 2 + v0) ** 2)
            return 0 if d1 <= d0 or d2 <= d0 else 1

        return Filters._loop(dim, callback)

    @staticmethod
    def notchGaussian(dim, d0, u0, v0):
        def callback(u, v):
            d1 = math.sqrt((u - dim[0] / 2 - u0) ** 2 + (v - dim[1] / 2 - v0) ** 2)
            d2 = math.sqrt((u - dim[0] / 2 + u0) ** 2 + (v - dim[1] / 2 + v0) ** 2)
            return 1 - math.exp(-((d1 * d2) / (2 * d0 ** 2)))

        return Filters._loop(dim, callback)

    @staticmethod
    def notchButterworh(dim, d0, u0, v0, _2n):
        def callback(u, v):
            d1 = math.sqrt((u - dim[0] / 2 - u0) ** 2 + (v - dim[1] / 2 - v0) ** 2)
            d2 = math.sqrt((u - dim[0] / 2 + u0) ** 2 + (v - dim[1] / 2 + v0) ** 2)
            if d1 * d2 == 0:
                return 1 / (1 + (d0 ** 2 / (0.000001)))
            return 1 / (1 + (d0 ** 2 / (d1 * d2)) ** _2n)

        return Filters._loop(dim, callback)


def transformPI(mat):
    return [[-1 ** (i + j) * mat[i][j] for j in range(len(mat[0]))] for i in range(len(mat))]
