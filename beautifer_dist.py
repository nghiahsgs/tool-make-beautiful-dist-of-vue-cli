import io
import os
import re
import sys

def write_file(file_name,ndung):
    f = io.open(file_name, 'w', encoding='utf-8')
    f.write(ndung)
    f.close()
    

def read_file(file_name):
    f = io.open(file_name, 'r', encoding='utf-8')
    ndung=f.read()
    f.close()
    return ndung

def regex_one_value(pattern, input_str):
    regex1=re.compile(pattern)
    kq=regex1.search(input_str)
    if kq:
        kq=kq.group(1)
    else:
        kq=''
    return kq

def regex_many_value(pattern, input_str):
    regex1=re.compile(pattern)
    kq=regex1.findall(input_str)
    return kq

if __name__ =="__main__":
    # route_name = 'order_ads'
    route_name = sys.argv[1]
    folder_dist = 'dist'
    file_name_html = 'index.html'

    file_name_html = os.path.join(folder_dist,file_name_html)
    data = read_file(file_name_html)

    #Step0 Remove file map
    L_remove_file = os.listdir(os.path.join(folder_dist,'js'))
    L_remove_file = [e for e in L_remove_file if 'map' in e]
    for e in L_remove_file:
        e =os.path.join(folder_dist,'js',e)
        os.remove(e)

    #Step1 GET all href
    pattern = 'href="(.*?)"'
    L_href = regex_many_value(pattern, data)
    L_href = [e[1:] for e in L_href]
    L_href = list(dict.fromkeys(L_href))


    #Step2 replace local link
    dem_css = 0
    dem_js = 0
    L_href_new = []

    for file_name in L_href:
        if 'css' in file_name:
            dem_css+=1
            new_file = f'css/{route_name}-{dem_css}.css'
            try:
                os.rename(os.path.join(folder_dist,file_name),os.path.join(folder_dist,new_file))
            except Exception as e:
                print("%s"%e)
            L_href_new.append(new_file)

        elif 'js' in file_name:
            dem_js+=1
            new_file = f'js/{route_name}-{dem_js}.js'
            try:
                os.rename(os.path.join(folder_dist,file_name),os.path.join(folder_dist,new_file))
            except Exception as e:
                print("%s"%e)
            L_href_new.append(new_file)

        else:
            L_href_new.append(file_name)

        

    #Step3 replace old link to new link in file index.html
    for index,href in enumerate(L_href):
        href_new = L_href_new[index]
        data = data.replace('/%s'%href,href_new)
        write_file(file_name_html,data)