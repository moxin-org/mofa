class ComplexNumber:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        return ComplexNumber(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return ComplexNumber(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        real = self.real * other.real - self.imag * other.imag
        imag = self.real * other.imag + self.imag * other.real
        return ComplexNumber(real, imag)

    def __truediv__(self, other):
        denom = other.real ** 2 + other.imag ** 2
        real = (self.real * other.real + self.imag * other.imag) / denom
        imag = (self.imag * other.real - self.real * other.imag) / denom
        return ComplexNumber(real, imag)

    def __str__(self):
        return f"{self.real} + {self.imag}i"

def main():
    print("复数计算器")
    real1 = float(input("输入第一个复数的实部: "))
    imag1 = float(input("输入第一个复数的虚部: "))
    real2 = float(input("输入第二个复数的实部: "))
    imag2 = float(input("输入第二个复数的虚部: "))

    c1 = ComplexNumber(real1, imag1)
    c2 = ComplexNumber(real2, imag2)

    print("选择操作: ")
    print("1. 加法")
    print("2. 减法")
    print("3. 乘法")
    print("4. 除法")
    choice = input("输入选择(1/2/3/4): ")

    if choice == '1':
        result = c1 + c2
    elif choice == '2':
        result = c1 - c2
    elif choice == '3':
        result = c1 * c2
    elif choice == '4':
        result = c1 / c2
    else:
        print("无效选择")
        return

    print(f"结果: {result}")

if __name__ == "__main__":
    main()