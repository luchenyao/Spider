import json

filename = './law_result.json'

with open(filename, 'rb') as f:
    data = json.load(f)
    law_voc = {}
    for each_voc in data:
        voc_name = each_voc['title']
        content_list = each_voc['content']
        definition = content_list[0]
        key1 = voc_name+" "+definition['fir_class_title']
        value1 = ''.join(definition['description']).strip()
        value1.replace('\n','')
        law_voc[key1] = value1
        for i in range(1, len(content_list)):
            if len(content_list[i]['description'])!=0:
                if (isinstance(content_list[i]['description'][-1], dict) and
                    isinstance(content_list[i]['description'][0], dict)):
                    for each_sec in content_list[i]['description']:
                        key = voc_name+" " + \
                            content_list[i]['fir_class_title'] + \
                            " "+each_sec['sec_class_title']
                        key=key.replace("\n","")
                        value = ''.join(each_sec['para']).strip()
                        value=value.replace("\n","")
                        law_voc[key] = value

                if (isinstance(content_list[i]['description'][-1], str)
                    and isinstance(content_list[i]['description'][0], str)):
                    key = voc_name+" "+content_list[i]['fir_class_title']
                    value = ''.join(content_list[i]['description'])
                    key=key.replace("\n", "")
                    value=value.replace("\n", "")
                    law_voc[key] = value

                if (isinstance(content_list[i]['description'][-1], dict)
                    and isinstance(content_list[i]['description'][0], str)):
                    str_list=""
                    for each in content_list[i]['description']:
                        if isinstance(each,str):
                            str_list=str_list+each.strip()
                        else:
                            key=voc_name+" "+content_list[i]['fir_class_title']+" "+each['sec_class_title']
                            value=''.join(each['para']).strip()
                            law_voc[key]=value
                        key=voc_name+" "+content_list[i]['fir_class_title']+" "+"定义"
                        value=str_list
                        key = key.replace("\n", "")
                        value = value.replace("\n", "")
                        law_voc[key]=value


out_file='./law_output.txt'

with open(out_file,'w',encoding='utf-8') as f:
    for key in law_voc:
        key=key.replace('\xa0','')
        law_voc[key]=law_voc[key].replace('\xa0','')
        f.write(key+'\t'+law_voc[key]+'\n')

