
# {type:"logp",# }


class Line:
    def __init__(self,code,breakpoint,id) -> None:
        self.code=code
        self.breakpoint=breakpoint
        self.id=id

class LoopGen:

    stop_at_loop_condition:False
    already_loop_count:int=0
    items:list[Line] =["a=2","b=3","print(a)","print(b)"]
    # loop_conditions={"type":"range","start":0,"end":10,"step":1}

    def update_items(self,new_items):
        self.items = new_items
        ...

    def parse(self,data):
        ...

    def run(self):
        if self.stop_at_loop_condition:
            globals().update(locals())
            yield
        
        while not self.is_end_loop():
            self.already_loop_count+=1
            for i in self.items:
                if i.breakpoint:
                    yield
                else:
                    exec(i)
                    globals().update(locals())

    def is_end_loop(self):
        if self.already_loop_count >=4:
            return True
        return False


def _exec(code):
    if isinstance(code,"str"):
        exec(code)
    elif isinstance:
        ...

loop_gen = LoopGen()
gen = loop_gen.run()

# for i in range(10):
code:Line = gen.send(None)
while code.breakpoint:
    LoopGen.items[1]="b=4"
    gen.send(None)
    gen.send(None)
    gen.send(None)
    gen.send(None)
    print(globals())

# for code in codes:
#     exec(code)
# print(globals(),locals)

# import time
# t = [1,2,3,4]
# for i in t:
#     # t.append(5)
#     t.insert(0,5)
#     print(t)
#     print(i)
#     time.sleep(2)

