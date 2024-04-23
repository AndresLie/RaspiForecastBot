import requests
import json
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJleHAiOjE3MjQ1NjQ3OTAsImF1ZCI6IndtbWtzLmNzaWUuZWR1LnR3IiwidmVyIjowLjEsInNjb3BlcyI6IjAiLCJzZXJ2aWNlX2lkIjoiMSIsInVzZXJfaWQiOiI0ODEiLCJpc3MiOiJKV1QiLCJpZCI6NjkzLCJpYXQiOjE3MDkwMTI3OTAsIm5iZiI6MTcwOTAxMjc5MCwic3ViIjoiIn0.mSdq3C-nbN82ew69EdskKdBkq3oDCe-8cg1bK6gkxWAjwADjMelUOzg85rZxd-INMa2kDy0gobhGiZ-AEy0XGcqT3Xlx1Ps_0FXu7Oaryj3g7bkPYRpTBayk9dVXnLchcfKBnLLJXpp0ZuuxVwOWJS25G5nFLtB3j532gqHPHdk'
def request(sent, token):
    res = requests.post("http://140.116.245.157:2001", data={"data":sent, "token":token})
    if res.status_code == 200:
        return json.loads(res.text)
    else:
        return None 

def removeDuplicate(ner):
    res={}
    for i in ner:
        if i[3] not in res.keys():
            res[i[3]]=i
        else:
            if(res[i[3]][2]!=i[2]):
                continue
    return res

def getTag(sentence):
    r = request(sentence, token)
    ner=r['ner'][0]
    res=removeDuplicate(ner)
    res=[item[2] for item in res.values()]
    return res


if __name__ == "__main__":
    sent = "明天適合去阿里山嗎?"
    print(getTag(sent))
    # r = request(sent, token)
    # ner=r['ner'][0]
    # res=removeDuplicate(ner)
    # res=[item[2] for item in res.values()]
    # print(res)
