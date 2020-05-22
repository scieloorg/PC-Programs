
def display_labeled_list(label, l):
    return '\n' + label + ': ' + str(len(l)) + '\n' + '\n'.join(display_sorted_list(l))


def display_sorted_list(l):
    return sorted(['   ' + item for item in l])


def display_pairs_list(pairs_list):
    return [c + ' => ' + n for c, n in pairs_list]


def display_key_value_list(pairs_list):
    return [k + ' => ' + v for k, v in pairs_list.items()]
