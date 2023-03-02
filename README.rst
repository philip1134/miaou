=====
miaou
=====

.. image:: https://img.shields.io/pypi/v/miaou.svg?color=orange
   :target: https://pypi.python.org/pypi/miaou
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/miaou.svg
   :target: https://pypi.org/project/miaou/
   :alt: Supported Python versions


``miaou`` 是 `pyzentao <https://github.com/philip1134/pyzentao>`__ 规格文件的自助生成工具。

宋朝的严羽在《沧浪诗话·诗辨》中说："大抵禅道惟在妙悟，诗道亦在妙悟"，于是取名 "妙悟 (miaou)"。


安装
----

.. code:: text

    $ pip install -U miaou

使用
----

使用 ``miaou`` 方法生成规格文件

.. code:: python

    import miaou

    miaou.generate(
        site_url="http://my.zentao.site",
        username="admin",
        password="123456",
        scanner="selenium",
        combined_print=True,
        output_path="."
    )

参数说明

- site_url
    你家禅道的域名，比如 "http://zentao.flyingcat.com"

- username
    登录用户名，用于禅道授权

- password
    登录密码，用于禅道授权

- scanner
    扫描器类型，目前自带扫描器支持 "selenium" 和 "api"，也可以自定义扫描器，详见下文

- combined_print
    合并打印规格，默认是 True ，会将规格打印到一个 yaml 文件，否则按 module 打印到不同文件

- output_path
    输出的目录，默认是当前目录

- config
    传给 scanner 的配置参数，应为 dict 类型

扫描器
-------

扫描禅道页面以获得规格，目前支持 ``selenium`` 和 ``api``，也可以自定义扫描器。

selenium
~~~~~~~~~

使用 ``selenium 4.8.0`` 版本以上，默认使用 chromedriver，可根据你的 Chrome 版本，在
`chromedriver <http://chromedriver.storage.googleapis.com/index.html>`__ 下载，并
添加到 path 中。如果要使用 firefox 可在参数中指定，例如

.. code:: python

    import miaou

    miaou.generate(
        ...
        scanner="selenium",
        config={"driver": "firefox"},
    )

api
~~~~

使用禅道对应的 API 生成规格。调用时指定扫描器类型即可

.. code:: python

    import miaou

    miaou.generate(
        ...
        scanner="api",
        ...
    )

注意，使用此扫描器生成的规格与禅道文档有一些不同，比如禅道文档中描述的查询 testsuite 的 API 为

.. code:: text

    GET  /zentao/testsuite.json

使用 ``selenium`` 扫描器生成的规格即为

.. code:: yaml

    testsuite:
        method: GET
        path: testsuite

而禅道 API 查询到的格式类似于

.. code:: text

    GET  /zentao/testsuite-index.json

所以使用 ``api`` 扫描器生成的规格为

.. code:: yaml

    testsuite_index:
        method: GET
        path: testsuite-index

这两种 API 得到的数据是相同的，所以在转换成 ``pyzentao`` 方法时请以你使用的规格文件为准。

自定义扫描器
~~~~~~~~~~~~~

也可以自定义扫描器，从 miaou.Scanner 继承

.. code:: python

    import miaou

    class MyScanner(miaou.Scanner):
        """doc string"""

        def __init__(self, config):
            ...


然后需要实现如下方法：

- open(self, site_url, username, password)
    一般是获得禅道授权

- close(self)
    清扫工作，没有就不写

- get_module_groups(self, dev_url)
    获得 API 模块页面链接，也就是 ``后台 - 二次开发 - API`` 页面左边栏 ``模块列表`` 下的那些链接。返回模块链接数组 [url...]

- get_apis(self, api_url)
    在指定的模块页面，即 api_url 中获取 API 规格，返回包含dict的数组类似 [{name, method, path, params}]

使用自定义扫描器

.. code:: python

    import miaou

    miaou.generate(
        ...
        scanner=MyScanner(config),
        ...
    )

另，此工具的功能仅在 ``Linux/Python3.10`` 环境下测试，使用其他环境的宝子请自娱自乐 ╮(╯▽╰)╭
