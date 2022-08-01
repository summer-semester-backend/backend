# 代码风格

为了防止世界被破坏, 为了维护世界的和平!

## 接口

### api

- 格式为`/api/module/someInterface`
- 模块名和接口名超过一个单词则用**小驼峰**

### request格式

- json格式, 字段名使用**小驼峰**

### 返回内容格式

- json格式, 字段名使用**小驼峰**
- `result` 0表示有问题, 1表示没问题
- `message` 简单描述操作结果
- `content` 为可选, 提供更多信息
- 例子:
    ```json
    {
      "result": 1,
      "message": "提示信息",
      "content": {
        "xxx": ".......",
        "someInform": "....."
      }
    }
    ```

## 后端命名

- 使用下划线分割
- 类名首字母大写, 其余首字母小写
- 变量名: `var_name`
- 函数名: `function_name`
- 类名: `Class_Name`
- 类实例名: `instance_name`
- 类成员名: `member_name`