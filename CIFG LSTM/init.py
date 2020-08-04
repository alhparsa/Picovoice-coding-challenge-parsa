import numpy as np


def sigmoid(in_array):
    res = 1 / (1 + np.exp(-in_array))
    return res


class Cell:
    def __init__(self):
        return

    def calculateForgetGate(self):
        """
        For CIFG, the output gate is defined as transpose of f = 1 - transpose of inputGate.
        """
        self.forgetGate = np.transpose(
            np.ones(self.inputGate.shape[::-1]) - self.inputGate.transpose())

    def calculateInputGate(self):
        updateValues = sigmoid(
            np.matmul(self.inputWeight, self.prevAndInput) + self.inputBias)
        candValues = np.tanh(
            np.matmul(self.cellWeight, self.prevAndInput) + self.cellBias)
        self.inputGate = np.matmul(updateValues, candValues)

    def calcualteCellState(self):
        self.cellState = self.prevCell * self.forgetGate + self.inputGate

    def calculateOutputGate(self):
        self.outputGate = sigmoid(
            np.matmul(self.prevAndInput) + self.outputBias)
        self.output = matmul(self.outputGate, np.tanh(self.cellState))
