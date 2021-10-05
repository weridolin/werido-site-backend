'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-04 09:36:26
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-04 23:09:24
'''

import dataclasses

@dataclasses.dataclass
class DrugBrief(object):
    model:str = "words"

    @classmethod
    def from_model(cls,model):
        return cls(model=model)


    @property
    def cache_key(self):
        return f"drug:{self.model}.is_show"

@dataclasses.dataclass
class CommentBrief(object):
    model:str = "site"

    @classmethod
    def from_model(cls,model):
        return cls(model=model)

    @property
    def cache_key(self):
        return f"{self.model}:comments.is_valid"