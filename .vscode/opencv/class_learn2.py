class Person():
    def __init__(self,name,age,gender):
       self.name=name
       self.age=age
       self.gender=gender
    def have_birthday(self):
        self.age += 1
    def introduce(self):
        print(f"我叫{self.name},{self.age}岁,{self.gender}")
        return  f"我叫{self.name}, {self.age}岁, {self.gender}"
p1 = Person("Alice", 25, "female")
print(p1.introduce())  # "我叫Alice, 25岁, 女性"
p1.have_birthday()
print(p1.age)  # 26
