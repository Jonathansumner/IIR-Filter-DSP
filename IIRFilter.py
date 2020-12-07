import numpy as np


class IIR2Filter:
    def __init__(self, coeff):
        self.coeff = coeff
        self.FIRcoeff = self.coeff[0:3]
        self.IIRcoeff = self.coeff[3:6]
        self.accumulator_in = 0
        self.accumulator_out = 0
        self.buffer1 = 0
        self.buffer2 = 0
        self.input = 0
        self.output = 0

    def filter(self, input):
        self.input = input
        self.output = 0

        self.accumulator_in = self.input + self.buffer1 * -self.IIRcoeff[1] + self.buffer2 * -self.IIRcoeff[2]

        self.buffer2 = self.buffer1
        self.buffer1 = self.accumulator_in
        self.input = self.accumulator_out
        self.output = self.accumulator_out
        return self.output

    class IIRFilter:
        def __init__(self, coeff):
            self.coeff = coeff
            self.accumulator_input = np.zero(len(self.coeff))
            self.accumulator_output = np.zero(len(self.coeff))
            self.buffer1 = np.zeros(len(self.coeff))
            self.buffer2 = np.zeros(len(self.coeff))
            self.input = 0
            self.output = 0
            self.IIRList = []

            for i in range(len(self.coeff)):
                self.IIRList.append(IIR2Filter(self.coeff[i]))

        def filter(self, input):
            self.input = input
            self.output = 0
            for i in range(0, len(self.coeff)):
                self.output = self.IIRList[i].filter(self.output)
            return self.output
