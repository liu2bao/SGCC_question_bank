from extract import db_name, table_name
from extract import key_answer, key_no, key_option, key_stem, key_type, \
    key_class, key_right_times, key_wrong_times,key_skip
import utils_sqlite
import os
import time
import numpy as np

question_bank = utils_sqlite.read_db(db_name, table_name, return_dict_form=True)


def show_item(item_ori,disorganize=False):
    item = item_ori.copy()
    if disorganize:
        options = item[key_option]
        Nops = len(options)
        if len(item[key_option])>2:
            option_keys = list(options.keys())
            option_values = list(options.values())
            flags_right_old = np.array([k in item[key_answer] for k in option_keys])
            idx_rand = np.random.permutation(Nops)
            item[key_option] = {option_keys[i]:option_values[idx_rand[i]] for i in range(Nops)}
            flags_right_new = flags_right_old[idx_rand]
            answers_new = [option_keys[i] for i in range(Nops) if flags_right_new[i]]
            answers_new.sort()
            answer_new = ''.join(answers_new).upper().strip()
            item[key_answer] = answer_new

    flag_right = False
    stem = '%s (%s)\n%d. %s'% (item[key_type],item[key_class],item[key_no],item[key_stem])
    print(stem)
    op_nos = list(item[key_option].keys())
    op_nos.sort()
    for op_no in op_nos:
        op = item[key_option][op_no]
        print(op_no + '. ' + op)
    user_op = input()
    ops = [user_op, item[key_answer]]
    for i in range(len(ops)):
        op_t = [k.upper() for k in ops[i]]
        op_t.sort()
        op_t = ''.join(op_t)
        ops[i] = op_t
    if ops[0] == ops[1]:
        flag_right = True
    return flag_right


def exam(str_where='',disorganize=False):
    right_num = 0
    wrong_num = 0
    qb_t = utils_sqlite.read_db(db_name, table_name, return_dict_form=True, str_where=str_where)
    qb_t_d = {d[key_no]:d for d in qb_t if not d[key_skip]}
    idx = {d[key_no]:(d[key_wrong_times]*2-d[key_right_times]+np.random.rand()
                     -np.log(d[key_wrong_times]+d[key_right_times]))
           for d in qb_t}
    idx_idx = np.argsort(list(idx.values()))[::-1]
    orders = np.array(list(idx.keys()))[idx_idx]
    total_num = len(qb_t_d)
    for o_t in orders:
        item = qb_t_d[o_t]
        if not item[key_skip]:
            os.system('cls')
            print('right: {rn} of {tn}\nwrong: {wn} of {tn}'.format(rn=right_num,wn=wrong_num,tn=total_num))
            print('\n\n-----------------------------------------------')
            flag_right = show_item(item,disorganize=disorganize)
            if flag_right:
                right_num += 1
                print('right')
                print('skip? (Y/N):')
                S = input()
                key_update = key_right_times
                right_times = item[key_right_times] + 1
                data_update = [right_times]
                if S=='Y':
                    key_update = [key_update,key_skip]
                    data_update = [[right_times,True]]
            else:
                wrong_num += 1
                str_info = '-----------------------------------------------\nWRONG (right:%s)' % item[key_answer]
                print(str_info)
                key_update = key_wrong_times
                data_update = [item[key_wrong_times] + 1]
            key_ref = key_no
            value_ref = [item[key_no]]
            utils_sqlite.update_list_to_db_multiref(db_name, table_name, key_update, data_update, key_ref, value_ref)
            if not flag_right:
                S = input()


if __name__ == '__main__':
    exam(disorganize=True)
    # exam(' where no=423')
