import time

import requests
import zhihu
import wudao
import huggingface
from wudaoai.api_request import executeEngine, getToken


class FakeTextGenerator:

    def __init__(self):
        self.infilePath = None
        self.outfilePath = None
        self.__prompt = None
        self.config = None
        self.defaultConfig_ch = {
            "topP": 0.9,  # 核采样（必填）取值范围0～1
            "topK": 3,  # 采样（必填）取值范围0～10
            "temperature": 0.7,  # 概率分布调节（必填)取值范围0.5～1
            "presencePenalty": 2,  # 重复词去除（必填)取值范围0～3
            "frequencyPenalty": 2,  # 重复惩罚参数（必填)取值范围0～3
            "generatedLength": 512,  # 文本生成最大长度（必填)取值范围1～512
            "endTokens": ["<n>"],
            "prompt": "",
        }
        self.defaultConfig_en = {
            "parameters": {
                "max_new_tokens": 250,
                "num_return_sequences": 1,
                "temperature": 0.7,
                "repetition_penalty": 5.0,
                "return_full_text": False,
                "top_p": 0.95
            },
            "inputs": "",
            "options": {
                "wait_for_model": True
            }
        }
        self.defaultConfig_translation = {
            "inputs": "",
            "options": {
                "wait_for_model": True
            }
        }
        self.token_ch = getToken(wudao.api_key, wudao.public_key)
        self.token_en = huggingface.headers

    def setInfilePath(self, path):
        self.infilePath = path

    def setOutfilePath(self, path):
        self.outfilePath = path

    def readSentence(self, sentence):
        self.__prompt = sentence

    def query_ch(self, in_flag=False, out_flag=False):
        if in_flag:
            f = open(self.infilePath, "r", encoding="UTF-8")
            self.__prompt = "".join(s for s in f.readlines())
            f.close()
        elif self.__prompt is None:
            print("input a Chinese sentence or set a input file path")
            return None
        data = self.defaultConfig_ch.copy()
        data["prompt"] = self.__prompt
        response = executeEngine(wudao.ability_cc, wudao.engine_cc, self.token_ch, data)
        if not response["success"]:
            print(response["msg"])
            return None
        text = self.__prompt + "\n" + response["data"]["outputText"]
        if out_flag:
            f = open(self.outfilePath, "w", encoding="UTF-8")
            f.write(text)
            f.close()
        else:
            print(text)
        return text

    def query_en(self, in_flag=False, out_flag=False):
        if in_flag:
            f = open(self.infilePath, "r", encoding="UTF-8")
            self.__prompt = "".join(s for s in f.readlines())
            f.close()
        elif self.__prompt is None:
            print("input a English sentence or set a input file path")
            return None
        data = self.defaultConfig_en.copy()
        data["inputs"] = self.__prompt
        response = requests.post(huggingface.gptj, headers=self.token_en, json=data).json()
        text = self.__prompt + "\n" + response[0]["generated_text"]
        if out_flag:
            f = open(self.outfilePath, "w", encoding="UTF-8")
            f.write(text)
            f.close()
        else:
            print(text)
        return text

    def __translate(self):
        data = self.defaultConfig_translation.copy()
        data["inputs"] = self.__prompt
        response = requests.post(huggingface.zh2en, headers=self.token_en, json=data).json()
        text = response[0]["translation_text"]
        return text

    def generateOnZhihu(self):
        hotList = zhihu.zhihuHot()
        # print(hotList)
        cnt = 1
        for item in hotList:
            # print(item)
            description = item.split('\n')[0]
            print(description + '\n')
            self.readSentence(description)
            self.setOutfilePath("zhihu_ch_" + str(cnt) + ".txt")
            if self.query_ch(in_flag=False, out_flag=True) is None:
                continue
            self.readSentence(self.__translate())
            self.setOutfilePath("zhihu_en_" + str(cnt) + ".txt")
            self.query_en(in_flag=False, out_flag=True)
            cnt += 1


start = time.time()
a = FakeTextGenerator()
a.generateOnZhihu()
end = time.time()
print(end - start)
# 1419.0205891132355
