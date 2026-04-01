import numpy as np  # 关键：导入numpy库，并起别名np

class Relu:
    def __init__(self):
        self.mask=None

    def forward(self,x):
        self.mask=(x<=0)
        out=x.copy()
        #如果直接写 out = x，本质是「引用赋值」—— 不是创建新的变量，而是让 out 和 x 指向同一个内存地址。
        #简单说：out 就是 x 的 “别名”，后续你对 out 做任何修改（比如修改 out 的值、调整元素），都会直接改变原始的 x（因为它们是同一个东西）。
        out[self.mask]=0
        #我输入的 x 是一个 numpy 数组，这一步是把小等0的地方的值改成0，其他地方保持不变。
        return out
        #返回一个数组

    def backward(self,dout):
        dout[self.mask]=0
        dx=dout
        return dx
    
class Sigmoid:
    def __init__(self):
        self.out=None

    def forward(self,x):
        out=1/(1+np.exp(-x))
        self.out=out
        return out

    def backward(self,dout):
        dx=dout*(1.0-self.out)*self.out
        return dx

class Affine:
    def __init__(self,W,b):
        self.W=W
        self.b=b
        self.x=None
        self.original_x_shape=None
        self.dW=None
        self.db=None

    def forward(self,x):
        # #为了进行矩阵运算，输入 x 的形状可能是二维以外的情况（比如一维），所以先把它变成二维。
        # self.original_x_shape=x.shape
        # x=x.reshape(x.shape[0],-1)
        self.x=x

        out=np.dot(self.x,self.W)+self.b
        return out

    def backward(self,dout):
        dx=np.dot(dout,self.W.T)
        self.dW=np.dot(self.x.T,dout)
        self.db=np.sum(dout,axis=0)

        # dx=dx.reshape(*self.original_x_shape)
        return dx
    
class SoftmaxWithLoss:
    def __init__(self):
        self.loss=None
        self.y=None
        self.t=None

    def forward(self,x,t):
        self.t=t
        self.y=self.softmax(x)
        #softmax函数的输出 self.y 是一个概率分布，表示每个类别的预测概率。交叉熵误差函数会
        # 比较这个预测概率分布 self.y 和真实标签 t 之间的差异，计算出一个数值来表示这个差异程度，
        # 这个数值就是损失（loss）。因此，self.loss 就是通过交叉熵误差函数计算出来的损失值，
        # 它反映了模型在当前输入 x 上的预测与真实标签 t 之间的差距。
        self.loss=self.cross_entropy_error(self.y,self.t)
        #cross_entropy_error 函数的作用是计算交叉熵误差（cross-entropy error），
        # 它是一个常用的损失函数，特别适用于分类问题。这个函数会比较模型的预测概率分布 self.y 和真实标签 t 之间的差异，
        # 并返回一个数值来表示这个差异程度，这个数值就是损失（loss）。因此，self.loss 就是
        # 通过 cross_entropy_error 函数计算出来的损失值，它反映了模型在当前输入 x 上的预测与真实标签 t 之间的差距。
        return self.loss

    def backward(self,dout=1):
        batch_size=self.t.shape[0]
        if self.t.size==self.y.size:
            dx=(self.y-self.t)/batch_size
        else:
            dx=self.y.copy()
            dx[np.arange(batch_size),self.t]=dx[np.arange(batch_size),self.t]-1
            dx=dx/batch_size
        return dx

    def softmax(self,x):
        if x.ndim==2:
            x=x.T
            x=x-np.max(x,axis=0)
            y=np.exp(x)/np.sum(np.exp(x),axis=0)
            return y.T

    def cross_entropy_error(self,y,t):
        if y.ndim==1:
            t=t.reshape(1,t.size)
            y=y.reshape(1,y.size)
        if t.size==y.size:
            t=t.argmax(axis=1)

        batch_size=y.shape[0]
        return -np.sum(np.log(y[np.arange(batch_size),t]+1e-7))/batch_size