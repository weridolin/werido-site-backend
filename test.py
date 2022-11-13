
tt = [
    {
        "id": 6,
        "p_id": None
    },
    {
        "id": 1,
        "p_id": 6
    },
    {
        "id": 2,
        "p_id": 1
    },
    {
        "id": 3,
        "p_id": 1
    },
    {
        "id": 4,
        "p_id": 1
    },
    {
        "id": 5,
        "p_id": 6
    }
]


def format_menu(source, parent, cache=[]):
    """
        把菜单生成的对应的树状结构
    """
    tree = []
    for item in source:
        if item["id"] in cache:
            continue
        if item["p_id"] == parent:
            cache.append(item["id"])
            item["child"] = format_menu(source, item["id"], cache)
            tree.append(item)
    return tree


print(format_menu(tt,parent=None))