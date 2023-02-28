=====
miaou
=====

``pyzentao-specs`` 包含了 `pyzentao <https://github.com/philip1134/pyzentao>`__ 的
禅道API规格文件，``pyzentao`` 在 ``r0.3.0`` 版本之后不再更新规格文件，转而由本项目持续更新。


用法
----

下载
~~~~

.. code:: text

    git clone https://github.com/philip1134/pyzentao-specs.git

复制
~~~~

根据你的禅道版本，将对应的规格文件夹复制到你的业务项目目录下，例如你家在用禅道17.6版：

.. code:: text

    cp -r pyzentao-specs/v17.6 /path/to/my/project

使用Windows的童鞋请自便。

使用
~~~~

使用自定义目录初始化 pyzentao 对象

.. code:: python

    import pyzentao

    zentao = pyzentao.Zentao({
        "url": "http://my.zentao.site/zentao",
        "username": "admin",
        "password": "123456",
        "spec": {
            "path": "/path/to/my/project/v17.6", # 自定义规格文件的地址
            "merge": False,
        }
    })

如果需要支持新的禅道版本，可以提 issue 或发消息给我。也可以自己动手，想啥都有，只需使用 yaml 文件定义规格，格式如

.. code:: yaml

    user_task:
        method: GET
        path: user-task
        params:
            - userID
            - type
            - recTotal
            - recPerPage
            - pageID
    ...
