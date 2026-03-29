class MulLayer:
    def __init__(self):
        self.x=None
        self.y=None

    def forward(self,x,y):
        self.x=x
        self.y=y
        out=x*y
        return out

    def backward(self,dout):
        dx=dout*self.y
        dy=dout*self.x
        return dx,dy

apple=100
apple_num=2
tax=1.1

#layer
mul_apple_layer=MulLayer()
mul_tax_layer=MulLayer()

#forward
apple_price=mul_apple_layer.forward(apple,apple_num)
total_price=mul_tax_layer.forward(apple_price,tax)
#计算图中，圆圈代表一个层级

print(total_price)

#backward
dtotal_price=1
dapple_price,dtax=mul_tax_layer.backward(dtotal_price)
#传入dout=1，表示total_price对apple_price的导数为1
dapple, dapple_num=mul_apple_layer.backward(dapple_price)
print(dapple, dapple_num, dtax)