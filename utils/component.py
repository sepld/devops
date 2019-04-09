def merge_list(*args):
    """
    用于将多个列表合并成一个， 返回新列表并去重
    :param args: list
    :return:  new list
    """
    new_list = []
    for a in args:
        assert isinstance(a, list), ["merge_list's args [%s] must be list"]
        for s in a:
            new_list.append(s)
    return list(set(new_list))
