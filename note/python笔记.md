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

## json python object map

|json|python|
|---|---|
|null|None|
|false|False|
|true|True|
|string|unicode|
|array|list|
|object|dict|
|number(int)|int long|
|number(real)|float|


## 网络编程 服务器跪了的情况

status code 

### requests 
    
    res.
    ok status_code raise_for_status elapsed encoding apparent_encoding close connection is_redirect history links json raw content reason text cookies headers

获取请求的内容

    res.request.
    body url headers method path_url  

### 想法

- 不设置超时。

使用 多线程 或者 协程同一个请求发起多次，直到得到正常反馈就停止其他请求。服务器错误就继续。
