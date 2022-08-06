# 同步广播

成功打开原型图文件之后, 需要向后端`8001`端口发送数据, 以在websocket服务中进行注册.

数据内容为:
```json
{
  "operation": "register",
  "fileID": "文件的ID",
  "userID": "本用户的ID"
}
```

服务端