class stack(object):
    def __init__(self):
        self.pointer = -1
        self.body = []
        
    def push(self,data):
        self.body.append(data)
        self.pointer+= 1

    def pop(self,data):
        self.body.pop(pointer)
        self.pointer-=1

    def topitem(self):
        return self.body[self.pointer]
    
    def isEmpty(self):
        return self.body == []
        
    def __len__(self):
        return len(self.body)

    def __str__(self):
        return (str(self.body))[1:-1].replace(" ","")

    def getcurrentpointer(self):
        return self.pointer
    

stack1 = stack()
print(stack1)
stack1.push('bob')
print(stack1.getcurrentpointer())
stack1.push('steve')
print(stack1.getcurrentpointer())
stack1.push('fizz')
print(stack1)
print(stack1.getcurrentpointer())
print(stack1.topitem())
print(len(stack1))

    

