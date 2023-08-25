def remove_spaces(value: str) -> str:
    value = str(value)
    splitted_value = list(value)

    pass_begin = False
    pass_end = False

    for _ in splitted_value:
        if not pass_begin:
            if splitted_value[0] == " ":
                del splitted_value[0]
            else:
                pass_begin = True

        if not pass_end:
            if splitted_value[-1] == " ":
                del splitted_value[-1]
            else:
                pass_end = True

        if pass_end and pass_begin:
            break

    return ''.join(splitted_value)
