
def display_sorted_list(label, l):
    return '\n' + label + ': ' + str(len(l)) + '\n' + '\n'.join(sorted(l))


def display_pairs_list(pairs_list):
    return ['   ' + c + ' => ' + n for c, n in pairs_list]


def display_key_value_list(pairs_list):
    return ['   ' + k + ' => ' + pairs_list[k] for k in sorted(pairs_list.keys())]
