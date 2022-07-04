import numpy as np
from scipy.special import erf
import math
from pynverse import inversefunc

##-----##-----##-----##-----##-----##-----##

def s(elements):
    return np.std(np.array(elements))


class MathHelper:

    def __init__(self):
        self.__data_x = list()
        self.__data_y = list()


    @property
    def data_x(self):
        return self.__data_x

    @data_x.setter
    def data_x(self, data):
        self.__data_x = np.array(data)

    @property
    def data_y(self):
        return self.__data_y

    @data_y.setter
    def data_y(self, data):
        self.__data_y = np.array(data)


    def k(self):
        sum = 0
        avg_x = np.average(self.data_x)
        avg_y = np.average(self.data_y)
        for i in range(0, len(self.__data_x)):
            sum += (self.__data_x[i] - avg_x) * (self.__data_y[i] - avg_y)
        return sum / len(self.__data_x)


    def r(self):
        return self.k() / (s(self.__data_x) * s(self.__data_y))


    def z(self):
        fraction = (1 + self.r()) / (1 - self.r())
        return 0.5 * (math.log(fraction))


class MathHelperLarge(MathHelper):

    def romanov(self):
        return 3 * ((1 - self.r()**2) / math.sqrt(len(self.data_x)))

    def print_calculation(self):
        print("Статистичний кореляційний момент: ", round(self.k(), 5))
        print("Середнє квадратичне відхилення по х: ", round(s(self.data_x), 5))
        print("Середнє квадратичне відхилення по у: ", round(s(self.data_y), 5))
        print("Статистичний коефіцієнт кореляції: ", round(self.r(), 5))
        print("Критерій Романовського: ", round(self.romanov(), 5))

        r_abs = round(abs(self.r()), 6)
        romanov_abs = round(abs(self.romanov()), 6)

        if r_abs >= romanov_abs:
            print(r_abs, "≥", romanov_abs, " - між величинами існує кореляційний зв'язок")
        else:
            print(r_abs, "<", romanov_abs, " - між величинами не існує кореляційного зв'язку")


class MathHelperSmall(MathHelper):

    def laplace(self, alpha):
        erf(1)
        phi = lambda x: erf(x / 2 ** 0.5) / 2
        inv_lap = inversefunc(phi)
        return inv_lap((1 - alpha) / 2)


    def fisher_interval_assessment(self, alpha):
        lower = (self.z() - (self.laplace(alpha) / (math.sqrt(len(self.data_x) - 3))))
        upper = (self.z() + (self.laplace(alpha) / (math.sqrt(len(self.data_x) - 3))))
        return lower, upper


    def range_length(self, alpha):
        rx1, rx2 = self.rxs(alpha)
        return rx2 - rx1


    def rxs(self, alpha):
        rx1 = (math.exp(2 * (self.z() - (self.laplace(alpha) / (math.sqrt(len(self.data_x) - 3))))) - 1) \
              / (math.exp(2 * (self.z() - (self.laplace(alpha) / (math.sqrt(len(self.data_x) - 3))))) + 1)
        rx2 = (math.exp(2 * (self.z() + (self.laplace(alpha) / (math.sqrt(len(self.data_x) - 3))))) - 1) \
              / (math.exp(2 * (self.z() + (self.laplace(alpha) / (math.sqrt(len(self.data_x) - 3))))) + 1)
        return rx1, rx2


    def print_calculation(self, alpha):
        print("Alpha = ", alpha)
        print("Статистичний кореляційний момент: ", round(self.k(), 5))
        print("Середнє квадратичне відхилення по х: ", round(s(self.data_x), 5))
        print("Середнє квадратичне відхилення по у: ", round(s(self.data_y), 5))
        print("Статистичний коефіцієнт кореляції: ", round(self.r(), 5))
        print("Значення аргументу функції Лапласа t: ", round(float(self.laplace(alpha)), 5))
        print("Емпіричне значення функції Фішера: ", round(self.z(), 5))

        lower, upper = self.fisher_interval_assessment(alpha)
        print("Інтервальна оцінка для теоретичної функції Фішера: ", round(lower, 5), " <= z <=", round(upper, 5))

        rx1, rx2 = self.rxs(alpha)
        print("Інтервальна оцінка коефіцієнта кореляції: ",  round(rx1, 5), " <= rxy <= ", round(rx2, 5))

        range_length = self.range_length(alpha)
        print("Довжина інтервалу: ", round(range_length, 5))

        if range_length > abs(self.r()):
            print("l > |rxy*| - зв'язку між елементами вибірки не існує\n")
        else:
            print("l < |rxy*| - зв'язок міє елементами вибірки існує\n")