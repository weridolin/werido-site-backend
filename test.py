import uiautomation as uia
import win32gui

res, cache = list(), list()


def get_all_hwnd(hwnd, _):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        if win32gui.GetWindowText(hwnd)!="":
            print(hex(hwnd), win32gui.GetClassName(hwnd),hwnd,win32gui.GetWindowText(hwnd))
        # c = uia.ControlFromHandle(hwnd)
        # if c.ClassName != "" and c.ClassName not in cache:
        #     res.append({
        #         "name": c.ClassName,
        #         "value": c.ClassName,
        #         "key": len(res)
        #     })
        #     cache.append(c.ClassName)


win32gui.EnumWindows(get_all_hwnd, 0)
print(res)

# import psutil
# import win32gui

# def get_process_by_handle(handle):
#     try:
#         process_id = win32gui(handle)[1]
#         process = psutil.Process(process_id)
#         return process
#     except psutil.NoSuchProcess:
#         return None

# # 假设你有一个窗口句柄 hwnd
# hwnd = 2035794  # 替换成你的实际窗口句柄

# process = get_process_by_handle(hwnd)
# if process:
#     print("进程名称:", process.name())
#     print("进程 ID:", process.pid)
# else:
#     print("找不到对应的进程信息")


import uiautomation as uia

for c in uia.GetRootControl().GetChildren():
    print(c.Name)