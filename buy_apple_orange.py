class AddLayer:
    def __init__(self):
        pass

    def forward(self, x, y):
        out = x + y
        return out

    def backward(self, dout):
        dx = dout * 1
        dy = dout * 1
        return dx, dy

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
orange=150
orange_num=3
tax=1.1

#layer
mul_apple_layer=MulLayer()
mul_orange_layer=MulLayer()
add_apple_orange_layer=AddLayer()
mul_tax_layer=MulLayer()

#forward
apple_price=mul_apple_layer.forward(apple,apple_num)
orange_price=mul_orange_layer.forward(orange,orange_num)
total_price=add_apple_orange_layer.forward(apple_price,orange_price)
final_price=mul_tax_layer.forward(total_price,tax)

#backward
dfinal_price=1
dtotal_price,dtax=mul_tax_layer.backward(dfinal_price)
dapple_price,dorange_price=add_apple_orange_layer.backward(dtotal_price)
dapple, dapple_num=mul_apple_layer.backward(dapple_price)
dorange, dorange_num=mul_orange_layer.backward(dorange_price)

print(final_price)
print(dapple, dapple_num, dorange, dorange_num, dtax)