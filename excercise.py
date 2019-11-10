from extract import db_name, table_name
from extract import key_answer, key_no, key_option, key_stem, key_type, key_class, key_right_times, key_wrong_times
import utils_sqlite

question_bank = utils_sqlite.read_db(db_name, table_name, return_dict_form=True)


def show_item(item):
    flag_right = False
    stem = str(item[key_no]) + '.' + item[key_stem]
    print(stem)
    for op_no, op in item[key_option].items():
        print(op_no + '. ' + op)
    user_op = input()
    ops = [user_op, item[key_answer]]
    for i in range(len(ops)):
        op_t = [k.upper() for k in user_op]
        op_t.sort()
        op_t = ''.join(user_op)
        ops[i] = op_t
    if ops[0] == ops[1]:
        flag_right = True
    return flag_right


def exam(str_where=''):
    qb_t = utils_sqlite.read_db(db_name, table_name, return_dict_form=True, str_where=str_where)
    for item in qb_t:
        flag_right = show_item(item)
        if flag_right:
            key_update = key_right_times
            data_update = [item[key_right_times] + 1]
        else:
            key_update = key_wrong_times
            data_update = [item[key_wrong_times] + 1]
        key_ref = key_no
        value_ref = [item[key_no]]
        utils_sqlite.update_list_to_db_multiref(db_name, table_name, key_update, data_update, key_ref, value_ref)


if __name__ == '__main__':
    show_item(question_bank[0])
