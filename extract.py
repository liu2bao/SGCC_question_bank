import os
import re
import xlwt
import utils_sqlite

path_data = 'data'
data_list = os.listdir('data')
db_name = r'E:\05_Job\materials\question_bank.db'
table_name = 'question_band'

def get_all_questions(file):
    with open(file,'rb') as f:
        D = [k.decode() for k in f.readlines()]
    segs = segment_parts(D)
    que_seg = {k:get_items(v) for k,v in segs.items()}
    return que_seg



def segment_parts(lines):
    pat = '第.*?部分'
    F = [re.match(pat,line) is not None for line in lines]
    no_f = [i for i in range(len(F)) if F[i]]
    segs = {}
    for i in range(len(no_f)):
        segdesc = lines[no_f[i]]
        desc = re.sub(pat,'',segdesc).strip()
        no_start = no_f[i]+1
        if i==len(no_f)-1:
            lines_seg_t = lines[no_start:]
        else:
            no_end = no_f[i+1]
            lines_seg_t = lines[no_start:no_end]
        segs[desc] = lines_seg_t
    return segs


def get_items(lines):
    questions = []
    question = {'option':{}}
    str_con_t = ''
    option = None
    for line in lines:
        sobj = re.match('(\d{1,3})\. ',line)
        if sobj:
            question = {'option':{}}
            no = int(sobj.groups()[0])
            question['no'] = no
            str_con_t = line[sobj.span()[1]:].strip()
        elif any([str.startswith(line,t+'. ') for t in ['A','B','C','D']]):
            if 'stem' not in question.keys():
                question['stem'] = str_con_t
            if option:
                question['option'][option] = str_con_t
            option = line[0]
            str_con_t = line[3:].strip()
        elif line.startswith('标准答案：'):
            question['option'][option] = str_con_t
            answer = line.replace('标准答案：','').strip()
            question['answer'] = answer
            questions.append(question)
        else:
            str_con_t = str_con_t+line.strip()

    return questions

if __name__=='__main__':
    all = {k.replace('.txt',''): get_all_questions(os.path.join(path_data, k)) for k in data_list}
    S = sum([sum([len(dd) for dd in d.values()]) for d in all.values()])
    '''
    I = []
    for a in all.keys():
        type_t = a+'题'
        for cl,d in all[a].items():
            for dd in d:
                i_t = [type_t,dd['no'],dd['stem'],cl,dd['answer'],*dd['option'].values()]
                I.append(i_t)
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('My Worksheet')
    for k in range(len(I)):
        for j in range(len(I[k])):
            worksheet.write(k, j, label=I[k][j])
    workbook.save('Excel_test.xls')
    '''

    if not os.path.isfile(db_name):
        D = []
        for type_t,DD in all.items():
            for class_t,DDD in DD.items():
                for ddd in DDD:
                    d_t = ddd.copy()
                    d_t.update({'type':type_t,'class':class_t,'right_times':0,'wrong_times':0})
                    D.append(d_t)
        utils_sqlite.insert_from_list_to_db(db_name,table_name,list_data=D,primary_key='no')



