# 语音转写
调用讯飞API对语音文件进行识别，并将结果转化成word文件输出。

## Features
- Web界面  
- 数据库记录文件哈希值和返回值，避免重复识别相同文件
- 定时轮询识别进度

## Usage
- 克隆代码到本地  
`git clone https://github.com/JoJoJoJoJoJoJo/MeetingHelper.git`

- 安装python3及相关依赖  
`pip3 install -r requirements.txt`

- 前往[讯飞开放平台](https://www.xfyun.cn/)注册账号，购买语音转写并创建应用，获得APP_ID和SECRET_KEY

- 创建main.py：  
```python
from app import create_app, db

import os
import webbrowser
import threading


if __name__ == '__main__':
    os.environ['XF_APP_ID'] = 'YOUR APP ID'
    os.environ['XF_SECRET_KEY'] = 'YOUR SECRET KEY'
    app = create_app()
    if not os.path.exists(str(db.get_engine(app).url)[10:]):
        db.create_all(app=app)
    threading.Timer(2, lambda: webbrowser.open('http://localhost:5000')).start()
    app.run()

```
 
- 运行`python main.py`
 
## Known Issues
- Flask cli未生效，数据库创建及更新比较麻烦
 
 