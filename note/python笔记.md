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

### iter_content(chunk_size=1)

默认的chunk_size只有1 byte； 1MB = 1024 * 1024 * 1 Byte

### 想法

- 不设置超时。

使用 多线程 或者 协程同一个请求发起多次，直到得到正常反馈就停止其他请求。服务器错误就继续。

## 大文件内存、断电保护

    file.flush() # 清除内部缓冲区 internal buffer
    os.fsync()   # 清除 operating system buffer 把文件写到磁盘上

## 下载


### 文件大小

    bytes = res.headers["Content-Length"] 

### 网速

byte/time

    KB = 1024Byte 
    KB/s

Mbps MB 

bits per second 

KiB KB

bit binary digit


### 下载进度



### 断点下载 多线程、进程 下载同一文件 



### 文件合并

### 单位换算

byte bit kb mb gb 


## multiprocessing 

### 关键字

1. picklability
2. Entry Point
3. Proxies
4. Pid
5. Zombie
6. Thread Safe
7. Weakref
8. callback
9. bound or unbound methods

### 共享变量数据结构

Value(type, initial_value)

    from multiprocessing import Value

    s = Value("i", 0)
    print s.value

|typecode|python|
|----|-----|
|i|int|
|u|unicode|
|d|double|
|f|float|

Array(typecode, )

### 终止进程

    process.terminate()


### 打包支持

    multiprocessing.freeze_support()

### CPU个数

    multiprocessing.cpu_count()

## ?

    sys.stdout.write()
    sys.stdout.flush()

## urlparse

### url的组成部分

    from urlparse import urlparse
    parsed = urlparse('http://user:pass@NetLoc:80/  path;parameters?query=argument#fragment')
    print 'scheme  :', parsed.scheme
    print 'netloc  :', parsed.netloc
    print 'path    :', parsed.path
    print 'params  :', parsed.params
    print 'query   :', parsed.query
    print 'fragment:', parsed.fragment
    print 'username:', parsed.username
    print 'password:', parsed.password
    print 'hostname:', parsed.hostname, '(netloc in lower case)'
    print 'port    :', parsed.port
    
    $ python urlparse_urlparseattrs.py

    scheme  : http
    netloc  : user:pass@NetLoc:80
    path    : /path
    params  : parameters
    query   : query=argument
    fragment: fragment
    username: user
    password: pass
    hostname: netloc (netloc in lower case)
    port    : 80


### 博客、资料

1. <a href="https://pymotw.com/2/urlparse/">urlparse参数解释</a>


## 
