import json
from user.models import User

from django.shortcuts import render
import websockets
import asyncio

FILES = {}
async def unknown(websocket):
    await websocket.send('connecting...')
    async for message in websocket:
        data = json.loads(message)
        print(data)
        if data['operation'] == 'connect': # 连接
            websocket.send(json.dumps({'result': 0, 'message': '已连接到同步编辑服务'}))
            fileID = data['fileID']
            userID = data['userID']
            if fileID not in FILES:
                FILES[fileID] = {}
            dic = FILES[fileID]
            broad = {'result': 0, 'message': '用户'+userID+"已加入编辑"}
            await asyncio.wait([ws.send(json.dumps(broad)) for ws in dic.values()])
            FILES[data['fileID']][data['userID']] = websocket
        elif data['operation'] == 'change':
            pass
        elif data['operation'] == 'disconnect': # 断开连接
            # websocket.send(json.dumps({'result': 0, 'message': '已连接到同步编辑服务'}))
            fileID = data['fileID']
            userID = data['userID']
            dic = FILES[fileID]
            broad = {'result': 0, 'message': '用户' + userID + "已离开"}
            FILES[fileID].pop(userID)
            await asyncio.wait([ws.send(json.dumps(broad)) for ws in dic.values()])

start_server = websockets.serve(unknown, '127.0.0.1', 8001)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
