class Matrix:
    def __init__(self):
        print("请分别输入行数和列数")
        self.rows = int(input())
        self.cols = int(input())
        self.Matrix = []

        print("请输入矩阵数据（逐行输入，用空格分隔）:")

        for i in range(self.rows):
            row = list(map(float, input(f"第{i+1}行: ").split()))
            self.Matrix.append(row)

    def create_empty(self):
        #创建空矩阵
        matrix.Matrix = [[0] * self.cols for _ in range(self.rows)]
        return matrix
    
    def __getitem__(self,index):
        # 取矩阵的元素
        if isinstance(index,tuple):
            i,j = index
            return self.Matrix[i][j]
            
    def __str__(self):
        # 将矩阵格式化为易读的字符串
        return '\n'.join(' '.join(map(str, row)) for row in self.Matrix)
    
    def Print(self):
        return self.Matrix
    
    def add(self,matrix2):
        # 矩阵加法
        result = Matrix.create_empty()
        for i in range(self.rows):
            for j in range(self.cols):
                result.Matrix[i][j] = self.Matrix[i][j] + matrix2[i, j]
        return result
matrix = Matrix()
matrix_2 = Matrix()
print(matrix,"\n")
matrix = matrix.add(matrix_2)
print(matrix)

