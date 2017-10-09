class utils:
    @staticmethod
    def replacePreGetBody(body,replace):
        if(body.find(replace)>=0):
            body=body.strip();
            #print(body[len(body)-2])
            #print(len(body))
            if(body.rfind(';')>=0):
                body = body[body.index(replace) + len(replace):len(body) - 2];
            else:
                body = body[body.index(replace) + len(replace):len(body) - 1];
        return body;