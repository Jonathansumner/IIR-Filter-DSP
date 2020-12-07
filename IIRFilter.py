import numpy as np


class IIR2Filter:
    # Initializes a 2nd order IIR Filter where the coefficients map to the FIR and IIR part of the filter
    # b0,b1, and b2 can be found in the first half of the coefficients
    # a0, a1, and a2 can be found in the second half of the coefficients
    # a0 is always 1, so it can be disregarded
    # other variables are also initialised, such as buffers to act as delay-lines
    # and input/output helper variables
    def __init__(self, coeff):
        self.coeff = coeff
        self.FIRcoeff = self.coeff[0:3]  # b0, b1, and b2
        self.IIRcoeff = self.coeff[3:6]  # a0, a1, and a2
        self.accumulator_in = 0
        self.accumulator_out = 0
        self.buffer1 = 0
        self.buffer2 = 0
        self.input = 0
        self.output = 0

    def filter(self, input):
        # initialize the input; output to be returned
        self.input = input
        self.output = 0

        # IIR part of the filter
        self.accumulator_in = self.input + self.buffer1 * -self.IIRcoeff[1] + self.buffer2 * -self.IIRcoeff[2]

        # FIR part of the filter
        self.accumulator_out = self.accumulator_in * self.FIRcoeff[0] + self.buffer1 * self.FIRcoeff[1] + self.buffer2 * \
                               self.FIRcoeff[2]

        # Shifting values through the delay-line
        self.buffer2 = self.buffer1
        self.buffer1 = self.accumulator_in
        self.input = self.accumulator_out
        self.output = self.accumulator_out
        return self.output


class IIRFilter:
    def __init__(self, coeff):
        self.coeff = coeff
        self.accumulator_input = np.zeros(len(self.coeff))
        self.accumulator_output = np.zeros(len(self.coeff))
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
        self.output = self.IIRList[0].filter(input)
        for i in range(1, len(self.coeff)):
            self.output = self.IIRList[i].filter(self.output)
        return self.output
