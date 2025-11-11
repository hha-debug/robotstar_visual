class Matrix:
    def __init__(self, rows, cols, data=None):
        """
        初始化矩阵
        :param rows: 行数
        :param cols: 列数
        :param data: 可选，二维列表数据
        """
        if rows <= 0 or cols <= 0:
            raise ValueError("行数和列数必须为正整数")
        
        self.rows = rows
        self.cols = cols
        
        if data is None:
            # 创建零矩阵
            self.data = [[0 for _ in range(cols)] for _ in range(rows)]
        else:
            # 验证数据维度
            if len(data) != rows or any(len(row) != cols for row in data):
                raise ValueError("数据维度与指定的行列数不匹配")
            self.data = data
    
    def __add__(self, other):
        """矩阵加法"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("矩阵维度不匹配，无法相加")
        
        result = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = self.data[i][j] + other.data[i][j]
        return result
    
    def __sub__(self, other):
        """矩阵减法"""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("矩阵维度不匹配，无法相减")
        
        result = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = self.data[i][j] - other.data[i][j]
        return result
    
    def __mul__(self, other):
        """矩阵乘法"""
        if self.cols != other.rows:
            raise ValueError("矩阵维度不匹配，无法相乘")
        
        result = Matrix(self.rows, other.cols)
        for i in range(self.rows):
            for j in range(other.cols):
                for k in range(self.cols):
                    result.data[i][j] += self.data[i][k] * other.data[k][j]
        return result
    
    def transpose(self):
        """矩阵转置"""
        result = Matrix(self.cols, self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[j][i] = self.data[i][j]
        return result
    
    def __str__(self):
        """以矩阵形式打印"""
        output = []
        for i in range(self.rows):
            row_str = "[ " + " ".join(f"{elem:8.2f}" for elem in self.data[i]) + " ]"
            output.append(row_str)
        return "\n".join(output)
    
    def __repr__(self):
        return f"Matrix({self.rows}, {self.cols})"
    
    def __eq__(self, other):
        """判断两个矩阵是否相等"""
        if self.rows != other.rows or self.cols != other.cols:
            return False
        for i in range(self.rows):
            for j in range(self.cols):
                if abs(self.data[i][j] - other.data[i][j]) > 1e-10:
                    return False
        return True


class SquareMatrix(Matrix):
    def __init__(self, size, data=None):
        """
        初始化方阵
        :param size: 方阵大小
        :param data: 可选，二维列表数据
        """
        if data is not None:
            # 检查是否为方阵
            if len(data) != size or any(len(row) != size for row in data):
                raise ValueError("数据不是方阵")
        
        super().__init__(size, size, data)
        self.size = size
    
    def trace(self):
        """返回矩阵的迹（主对角线元素之和）"""
        trace_sum = 0
        for i in range(self.size):
            trace_sum += self.data[i][i]
        return trace_sum
    
    def is_symmetric(self):
        """判断矩阵是否为对称矩阵"""
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if self.data[i][j] != self.data[j][i]:
                    return False
        return True
    
    def __repr__(self):
        return f"SquareMatrix({self.size})"


# 测试代码
if __name__ == "__main__":
    print("=== 测试 Matrix 类 ===")
    
    # 创建普通矩阵
    m1 = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
    m2 = Matrix(2, 3, [[6, 5, 4], [3, 2, 1]])
    
    print("矩阵 m1:")
    print(m1)
    print("\n矩阵 m2:")
    print(m2)
    
    print("\n矩阵加法 m1 + m2:")
    print(m1 + m2)
    
    print("\n矩阵减法 m1 - m2:")
    print(m1 - m2)
    
    # 矩阵乘法测试
    m3 = Matrix(3, 2, [[1, 2], [3, 4], [5, 6]])
    print("\n矩阵 m3:")
    print(m3)
    
    print("\n矩阵乘法 m1 * m3:")
    print(m1 * m3)
    
    print("\n矩阵转置 m1:")
    print(m1.transpose())
    
    print("\n=== 测试 SquareMatrix 类 ===")
    
    # 创建方阵
    try:
        sm1 = SquareMatrix(3, [[1, 2, 3], [2, 4, 5], [3, 5, 6]])
        print("方阵 sm1:")
        print(sm1)
        
        print(f"\n矩阵的迹: {sm1.trace()}")
        print(f"是否为对称矩阵: {sm1.is_symmetric()}")
        
        # 非对称矩阵测试
        sm2 = SquareMatrix(2, [[1, 2], [3, 4]])
        print("\n方阵 sm2:")
        print(sm2)
        print(f"是否为对称矩阵: {sm2.is_symmetric()}")
        
    except ValueError as e:
        print(f"错误: {e}")
    
    # 测试错误情况
    print("\n=== 测试错误情况 ===")
    try:
        # 尝试创建非方阵的 SquareMatrix
        invalid_sm = SquareMatrix(2, [[1, 2, 3], [4, 5, 6]])
    except ValueError as e:
        print(f"预期错误: {e}")