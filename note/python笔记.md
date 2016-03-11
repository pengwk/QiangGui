# Python

## metaclass dynamic generate class

example:
```python
def a_function():
    pass

class MetaClass():
    __metaclass__ = a_function

    pass
```

## 路径名包含特殊字符 \x13

无解

    output_dir = "C:\Users\wk\OneDrive\W\QiangGui\img\23"
    
    IOError: [Errno 22] invalid mode ('wb') or filename: u'C:\\Users\\wk\\OneDrive\\W\\QiangGui\\img\x13\\\u9648\u8fdb.jpg'

字符\x10和\x13，或者说ASCII 10和13，\n \r

#### 结果

错误信息不注意，是保存的时候除出了问题，而不是打开的时候 \23 
\023  19  DC3  \x13  ^S    (Device control 3) (XOFF)  (Default UNIX STOP char.)

加上r就好了。 出错的前一行很重要！