import os

def dir_and_file_tree(path,temp_list):
    path_tree = os.listdir(path)     #获取当前目录下的文件和目录
    for item in path_tree:
        subtree= path+'\\'+item
        if os.path.isdir(subtree):      #判断是否为目录
            x1=[]
            item_dict={'name':item,'isParent':True,'children':x1}
            temp_list.append(item_dict)
            dir_and_file_tree(subtree,x1)   #递归深度优先遍历
        else:
            temp_list.append({'name':item})
    return temp_list


if __name__ == '__main__':
    basepath = './comments'
    qq=dir_and_file_tree(basepath,[])
    print(qq)
