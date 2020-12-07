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

    class IIRFilter:
        pass
