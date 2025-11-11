class Student:
    # 类变量 - 在class内，def外
    school_name = "清华大学"  # 所有学生共享的学校名称
    student_count = 0        # 记录创建的学生总数
    
    def __init__(self, name, age):
        # 实例变量 - 每个对象独有的
        self.name = name
        self.age = age
        # 每次创建学生时，类变量+1
        Student.student_count += 1
    
    def get_info(self):
        return f"姓名:{self.name}, 年龄:{self.age}, 学校:{Student.school_name}"
    
    @classmethod
    def get_student_count(cls):
        return f"当前学生总数: {cls.student_count}"
    
    @classmethod
    def change_school(cls, new_school):
        cls.school_name = new_school

# ========== 使用示例 ==========

print("=== 1. 创建学生对象 ===")
# 创建第一个学生
stu1 = Student("张三", 18)
print(stu1.get_info())
print(Student.get_student_count())

print("\n=== 2. 创建更多学生 ===")
# 创建更多学生
stu2 = Student("李四", 19)
stu3 = Student("王五", 20)

print(f"stu2: {stu2.get_info()}")
print(f"stu3: {stu3.get_info()}")
print(Student.get_student_count())  # 现在有3个学生

print("\n=== 3. 访问类变量 ===")
# 通过类名访问类变量
print(f"学校名称: {Student.school_name}")
print(f"学生总数: {Student.student_count}")

# 通过对象访问类变量
print(f"stu1的学校: {stu1.school_name}")
print(f"stu2的学校: {stu2.school_name}")

print("\n=== 4. 修改类变量 ===")
# 修改学校名称（会影响所有对象）
Student.change_school("北京大学")
print("修改学校后:")
print(stu1.get_info())  # 学校变成北京大学
print(stu2.get_info())  # 学校变成北京大学
print(stu3.get_info())  # 学校变成北京大学

print("\n=== 5. 直接修改类变量 ===")
# 直接通过类名修改
Student.school_name = "上海交通大学"
print("再次修改学校后:")
print(f"stu1: {stu1.school_name}")
print(f"stu2: {stu2.school_name}")

print("\n=== 6. 注意：通过对象修改类变量的陷阱 ===")
# 如果通过对象修改类变量，实际上会创建实例变量
print("修改前:")
print(f"Student.school_name: {Student.school_name}")
print(f"stu1.school_name: {stu1.school_name}")

stu1.school_name = "我的个人学校"  # 这实际上创建了stu1的实例变量

print("修改后:")
print(f"Student.school_name: {Student.school_name}")  # 类变量没变
print(f"stu1.school_name: {stu1.school_name}")        # 实例变量
print(f"stu2.school_name: {stu2.school_name}")        # 还是原来的类变量

print("\n=== 7. 查看实例字典 ===")
# 查看对象的属性字典
print(f"stu1的属性: {stu1.__dict__}")  # 包含school_name实例变量
print(f"stu2的属性: {stu2.__dict__}")  # 不包含school_name

print("\n=== 8. 继续创建新学生 ===")
# 新创建的学生仍然使用类变量的值
stu4 = Student("赵六", 21)
print(f"stu4: {stu4.get_info()}")  # 学校是上海交通大学
print(Student.get_student_count())  # 现在有4个学生