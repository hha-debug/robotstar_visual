class Matrix:
    def __init__(self, rows, cols, data=None):
        """初始化矩阵"""
        if rows <= 0 or cols <= 0:
            raise ValueError("行数和列数必须为正整数")
        
        self.rows = rows
        self.cols = cols
        self.data = data if data else [[0] * cols for _ in range(rows)]
        
        if data and (len(data) != rows or any(len(row) != cols for row in data)):
            raise ValueError("数据维度与指定的行列数不匹配")

    def __add__(self, other):
        """矩阵加法"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("矩阵维度不匹配")
        return Matrix(self.rows, self.cols, [
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def __sub__(self, other):
        """矩阵减法"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("矩阵维度不匹配")
        return Matrix(self.rows, self.cols, [
            [self.data[i][j] - other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def __mul__(self, other):
        """矩阵乘法"""
        if self.cols != other.rows:
            raise ValueError("矩阵维度不匹配")
        return Matrix(self.rows, other.cols, [
            [sum(self.data[i][k] * other.data[k][j] for k in range(self.cols)) for j in range(other.cols)]
            for i in range(self.rows)
        ])

    def transpose(self):
        """矩阵转置"""
        return Matrix(self.cols, self.rows, [
            [self.data[i][j] for i in range(self.rows)] for j in range(self.cols)
        ])

    def __str__(self):
        """矩阵打印"""
        return "\n".join([f"[ {' '.join(map(str, row))} ]" for row in self.data])

    def __repr__(self):
        return f"Matrix({self.rows}, {self.cols})"

    def __eq__(self, other):
        """矩阵是否相等"""
        return self.rows == other.rows and self.cols == other.cols and all(
            abs(self.data[i][j] - other.data[i][j]) < 1e-10 for i in range(self.rows) for j in range(self.cols)
        )


class SquareMatrix(Matrix):
    def __init__(self, size, data=None):
        """初始化方阵"""
        if data and (len(data) != size or any(len(row) != size for row in data)):
            raise ValueError("数据不是方阵")
        super().__init__(size, size, data)

    def trace(self):
        """矩阵迹"""
        return sum(self.data[i][i] for i in range(self.rows))

    def is_symmetric(self):
        """判断是否对称矩阵"""
        return all(self.data[i][j] == self.data[j][i] for i in range(self.rows) for j in range(i + 1, self.cols))

    def __repr__(self):
        return f"SquareMatrix({self.rows})"


# 测试代码
if __name__ == "__main__":
    m1 = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
    m2 = Matrix(2, 3, [[6, 5, 4], [3, 2, 1]])
    print(m1 + m2)  # 矩阵加法
    print(m1 - m2)  # 矩阵减法

    m3 = Matrix(3, 2, [[1, 2], [3, 4], [5, 6]])
    print(m1 * m3)  # 矩阵乘法

    print(m1.transpose())  # 矩阵转置

    sm1 = SquareMatrix(3, [[1, 2, 3], [2, 4, 5], [3, 5, 6]])
    print(sm1.trace())  # 方阵迹
    print(sm1.is_symmetric())  # 判断是否对称矩阵
