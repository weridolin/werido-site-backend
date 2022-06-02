import re
from time import sleep
def get_undefined_variable_from_code(code,_global,_locals):
    ### 获取一段PYTHON代码中未定义的变量名称
    try:
        eval(code,_global,_locals)
    except NameError as exc:
        # 获取未定义的变量名
        undefined_var_name = re.search(pattern="\'(.*)\'",string=exc.__str__()).group().replace("'","").strip()
        print(undefined_var_name)
    except Exception as exc:
        print("该python表达式不合法")

def get_all_undefined_variable_from_code(code):
    _global = globals().copy()
    _local  = locals().copy()
    res = []
    class TemValue(object):

        def __getattribute__(self, __name: str):
            return self

        def __call__(self, *args,**kwds):
            return self

        def __add__(self,other):
            return self
        
        __sub__ = __add__ 
        __mul__ = __add__ 
        __truediv__ = __add__

    while True:
        try:
            eval(code,_global,_local)
            return res # 没有未定义的变量
        except NameError as exc:       
            undefined_var_name = re.search(pattern="\'(.*)\'",string=exc.__str__()).group().replace("'","").strip()
            res.append(undefined_var_name)
            _local.update({
                undefined_var_name:TemValue()
            })
        # except AttributeError as exc:
        #     print(exc.args)
        #     raise
        except Exception as exc:
            return res # 语法错误，直接返回



# r = get_all_undefined_variable_from_code('func([2,3.4,d,func2(s,3,d+f"{a}")])')
r = get_all_undefined_variable_from_code('func(b+2+adads,t*s,i/d)')
print(r)

# class ADD:
#     def __add__(self,other):
#         return self
    
#     def __mul__(self,other):
#         return self

# print(ADD()+1,ADD()*2)



