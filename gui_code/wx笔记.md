# wxpython 的笔记

## 图像id

#### 关键字

`ImageList` `Image` `index` `AssignImageList` `WithImages`

#### 例子

```python
import wx

image = wx.Image(path)
```
#### ImageList

- 初始化时需要指定图像的大小，一般来说二维的大小都是（宽， 高）。`mask`用于`transparent drawing`。

`ImageList(width, height, mask=True, initialCount=1)`

- 以列表的形式储存图像，储存形式没有指定。可以包含`bitmap`和`icon`两种格式。`icon`只能在`MSW`和`MAC OS`上能用。

- `ListCtrl`和`TreeCtrl`有关。

使用`Add(bitmap, mask=True)`会返回添加图像在`ImageList`中的索引。原图像并不会被被这里的操作所影响。
如果`bitmap`比规定的尺寸要大的话，会被切割成符合规定的。`icon`则不会。

##### WithImage

#### `Mixin`是什么意思？

面向对象语言里的一个编程概念，用于给其他类提供额外的功能而不增加其负担。向其他类注入代码。

以父类的方式只提供功能，不创建隔离，特殊化。

- 给多个不同类别的类添加相同的功能。
- 代码重用
- 以组合的方式创建类

<a target="blank" href="https://en.wikipedia.org/wiki/Mixin">维基百科</a>

##### 常见问题

Python类的多重继承，使得`mixin`的创建成为可能。Python的继承方式是<i style="color:red">从右到左</i>，左面的方法会覆盖右边的。不注意就会出错。

从右到左意味着最右边的类是基类，左边的类是用来给他提供扩展的。

```python
class Mixin1(object):
	def some_functions():
		print u"Mixin1 exist to extend main class"

class Mixin2(object):
	def some_functions():
		print u"Mixin2 exist to extend main class"

class BaseClass(object):
	def main_functions():
		print u"Main function"

class MoreFunction(Mixin2, Mixin1, BaseClass): # 专业的BaseClass在最右边
	def addition_function():
		print "addtion function"
```
<a target="blank" href="https://www.ianlewis.org/en/mixins-and-python">来自：www.ianlewis.org</a>

## wx.Toolbook

## 图像处理中的`mask`是什么意思？