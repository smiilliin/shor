# -*- coding: utf-8 -*-
# smiilliin

import math
import random
import numpy as np
from fractions import Fraction
from qiskit import Aer, QuantumCircuit, execute
from qiskit.circuit.library import QFT
import matplotlib.pyplot as plt


n = 3 # qbit 개수

def findPeriod(a, N):
  freq = getFrequency(a, N)
  # 분모의 최댓값을 N으로 설정한 채로 기약분수에 근사
  frac = Fraction(freq).limit_denominator(N)
  # 분모를 리턴(주파수의 역수 = 주기)
  # 주기가 정수로 나온다고 가정하는 것이다(정수가 아니면 뒤에 계산시 걸러진다)
  return frac.denominator


def calcPowMod(a, x, N):
  y = 1
  while (x > 0):
    if ((x & 1) == 1):
      y = (y * a) % N
    x = x >> 1
    a = (a * a) % N
  return y


def getFrequency(a, N):
  global qc, n
  qc = QuantumCircuit(n, n)

  for q in range(n):
    qc.h(q)  # 각 큐빗을 중첩시킨다(hadamard 게이트)

  for q in range(n):
    # 큐빗에 위상을 부여한다(pharse shift 게이트)
    qc.p(calcPowMod(a, q, N) * 2 * np.pi / n, q)

  qft = QFT(num_qubits=n, inverse=False)
  qc.append(qft, qargs=range(n))  # 각 큐비트에 QFT를 계산한다
  qc.measure(range(n), range(n))  # 관측도 추가한다

  backend = Aer.get_backend('qasm_simulator')

  result = execute(qc, backend, shots=1024, memory=True).result()
  readings = result.get_memory()
  freq = int(readings[0], 2) / (2 ** n)  # 데이터가 2의 n제곱 개 있으므로 정규화 시킨다

  return freq


def main():
  N = 11 * 17 # 인수분해 할 숫자
  p, q = calculate(N)
  print(N, "=", p, '*', q)
  qc.draw(output="mpl", filename="circuits.png")


def calculate(N):
  trial = 0

  while (True):
    trial += 1
    print('trial', trial)
    a = random.randint(2, N - 1)

    # gcd = math.gcd(N, a)
    # if (gcd != 1):
    #   gcd1 = gcd
    #   gcd2 = N // gcd
    # 비교 측정을 위해 랜덤하게 얻는 과정은 뺀다

    r = findPeriod(a, N)
    print('a:', a, 'r:', r)

    if (r % 2 != 0):
      print(end="\n")
      continue

    gcd1 = math.gcd(N, a ** (r // 2) + 1)
    gcd2 = math.gcd(N, a ** (r // 2) - 1)

    print('gcd1:', gcd1, 'gcd2:', gcd2)
    if (gcd1 == 1 or gcd2 == 1):
      print(end="\n")
      continue

    break

  return gcd1, gcd2


if (__name__ == "__main__"):
  main()
