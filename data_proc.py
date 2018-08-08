import markdown
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_DELETE, IN_CREATE, IN_MODIFY
import json
import os
import glob
import math
import threading


articles = dict()
home_index = list()
category_index = dict()
tags_index = dict()
extensions = ['markdown.extensions.extra',
              'markdown.extensions.abbr',
              'markdown.extensions.attr_list',
              'markdown.extensions.def_list',
              'markdown.extensions.fenced_code',
              'markdown.extensions.footnotes',
              'markdown.extensions.tables',
              'markdown.extensions.smart_strong',
              'markdown.extensions.admonition',
              'markdown.extensions.codehilite',
              'markdown.extensions.headerid',
              'markdown.extensions.meta',
              'markdown.extensions.nl2br',
              'markdown.extensions.sane_lists',
              'markdown.extensions.smarty',
              'markdown.extensions.toc',
              'markdown.extensions.wikilinks']


def check_head(v_dict):
    if 'tags' not in v_dict:
        return False
    if 'date' not in v_dict:
        return False
    if 'title' not in v_dict:
        return False
    if 'categories' not in v_dict:
        return False
    return True


def markdown_trans(content):
    return markdown.markdown(content, output_format='html5', extensions=extensions)


def trim_md(md_file):
    input_file = open(md_file, mode="r", encoding="utf-8")
    text = input_file.readlines()
    start = False
    log = False
    check_dict = dict()
    content = list()
    try:
        for row in text:
            row_content = row.strip(' ').strip('﻿').strip('\n')
            if start:
                kv = row.split('=')
                if len(kv) == 2:
                    check_dict[kv[0].strip(' ')] = json.loads(kv[1].strip(' ').strip('\n'))
            if log:
                if len(row_content) > 0:
                    content.append(row_content)
            if not start and row_content == "+++":
                start = True
            elif start and row_content == "+++":
                start = False
                log = True
        if len(check_dict) > 0 and check_head(check_dict):
            content = '\n'.join(content)
            content = markdown_trans(content)
        else:
            content = ''
    except Exception as e:
        print(str(e))
    return check_dict, content


def remove_cate_tag(article_id):
    for cate_key in articles[article_id]['cate']:
        # print(cate_key.encode('utf-8'))
        # 判断category_index中是否存在
        if cate_key in category_index:
            # print("exist1")
            for sub_key in articles[article_id]['cate'][cate_key]:
                # print(sub_key.encode('utf-8'))
                if sub_key in category_index[cate_key]:
                    # print("exist2")
                    cur_loc = -1
                    for loc in range(0, len(category_index[cate_key][sub_key])):
                        if category_index[cate_key][sub_key][loc]['article_id'] == article_id:
                            cur_loc = loc
                            break
                    # print(str(cur_loc))
                    if cur_loc > -1:
                        del category_index[cate_key][sub_key][loc]
                        # print("deleted.")
                        if len(category_index[cate_key][sub_key]) == 0:
                            del category_index[cate_key][sub_key]
            if len(category_index[cate_key]) == 0:
                del category_index[cate_key]
    for tag_key in articles[article_id]['tag']:
        if tag_key in tags_index:
            for sub_key in articles[article_id]['tag'][tag_key]:
                if sub_key in tags_index[tag_key]:
                    cur_loc = -1
                    for loc in range(0, len(tags_index[tag_key][sub_key])):
                        if tags_index[tag_key][sub_key][loc]['article_id'] == article_id:
                            cur_loc = loc
                            break
                    if cur_loc > -1:
                        del tags_index[tag_key][sub_key][loc]
                        if len(tags_index[tag_key][sub_key]) == 0:
                            del tags_index[tag_key][sub_key]
            if len(tags_index[tag_key]) == 0:
                del tags_index[tag_key]


def remove_one_file(file):
    article_id = file.split('/')[-1].strip('.md')
    for loc in range(0, len(home_index)):
        if home_index[loc]['article_id'] == article_id:
            break
    del home_index[loc]
    remove_cate_tag(article_id)
    del articles[article_id]


def modify_one_file(file):
    out_dict, html = trim_md(file)
    if len(out_dict) > 0:
        article_id = file.split('/')[-1].strip('.md')
        has_exist = article_id in articles
        meta_dict = {'title': out_dict['title'], 'date': out_dict['date'], 'article_id': article_id}
        if has_exist:
            for loc in range(0, len(home_index)):
                if home_index[loc]['article_id'] == article_id:
                    home_index[loc] = meta_dict
            remove_cate_tag(article_id)
        else:
            home_index.insert(0, meta_dict)
        add_cate_tag(out_dict, article_id)
        articles[article_id] = {'title': out_dict['title'],
                                'date': out_dict['date'],
                                'html': html,
                                'cate': out_dict['categories'],
                                'tag': out_dict['tags']}


def add_cate_tag(out_dict, article_id):
    meta_dict = {'title': out_dict['title'], 'date': out_dict['date'], 'article_id': article_id}
    for cate_key in out_dict['categories']:
        for sub_key in out_dict['categories'][cate_key]:
            if cate_key not in category_index:
                category_index[cate_key] = dict()
            if sub_key not in category_index[cate_key]:
                category_index[cate_key][sub_key] = list()
            category_index[cate_key][sub_key].append(meta_dict)
    for tags_key in out_dict['tags']:
        for sub_key in out_dict['tags'][tags_key]:
            if tags_key not in tags_index:
                tags_index[tags_key] = dict()
            if sub_key not in tags_index[tags_key]:
                tags_index[tags_key][sub_key] = list()
            tags_index[tags_key][sub_key].append(meta_dict)


def add_one_file(file):
    out_dict, html = trim_md(file)
    if len(out_dict) > 0:
        article_id = file.split('/')[-1].strip('.md')
        articles[article_id] = {'title': out_dict['title'],
                                'date': out_dict['date'],
                                'html': html,
                                'cate': out_dict['categories'],
                                'tag': out_dict['tags']}
        meta_dict = {'title': out_dict['title'], 'date': out_dict['date'], 'article_id': article_id}
        home_index.append(meta_dict)
        add_cate_tag(out_dict, article_id)


def init_db():
    files = glob.glob("post/*.md")
    files.sort(key=os.path.getmtime)
    files.reverse()
    for m in files:
        add_one_file(m)


def get_item_html(article_id, title, date):
    out = '<nav class="list-item">' + \
      '<a href="/article/'+article_id+'">'+title+'</a>' + \
      '<span class="list-item-date">'+date + \
      '</span>' + \
      '</nav>'
    return out


def get_tags_html(tags_key):
    out = '<blockquote><h2 class="category-title" style="font-size:2rem">'+tags_key+'</h2></blockquote>'
    for sub_key in tags_index[tags_key]:
        sub_out = '<ul class="category-item"><li>' + \
                  '<a href="/tags_list/'+tags_key+'/'+sub_key+'" style="font-size:1.5rem">'+sub_key+'</a>' + \
                  '<span class="category-item-count"><sup>('+str(len(tags_index[tags_key][sub_key]))+')</sup></span>' +\
                  '</li></ul>'
        out = out + sub_out
    return out


def get_category_html(cate_key):
    out = '<blockquote><h2 class="category-title" style="font-size:2rem">'+cate_key+'</h2></blockquote>'
    for sub_key in category_index[cate_key]:
        sub_out = '<ul class="category-item"><li>' + \
                  '<a href="/categories_list/'+cate_key+'/'+sub_key+ '" style="font-size:1.5rem">'+sub_key+'</a>' + \
                  '<span class="category-item-count"><sup>('+str(len(category_index[cate_key][sub_key])) + ')</sup></span>' +\
                  '</li></ul>'
        out = out + sub_out
    return out


def get_detail_tags_html(article_id):
    out = ''
    for cate_key in articles[article_id]['cate']:
        out = out + '<li><i class="fa fa-category">'+cate_key+' > </i>'
        for sub_key in articles[article_id]['cate'][cate_key]:
            out = out + '<a href="/categories_list/'+cate_key+'/'+sub_key+'">'+sub_key+'</a>'
        out = out + '</li>'
    for tag_key in articles[article_id]['tag']:
        out = out + '<li><i class="fa fa-tags">'+tag_key+' > </i>'
        for sub_key in articles[article_id]['tag'][tag_key]:
            out = out + '<a href="/tags_list/'+tag_key+'/'+sub_key+'">'+sub_key+'</a>'
        out = out + '</li>'
    return out


def get_paging(size, cur_page, max_page, href):
    if cur_page > 1:
        out = '<div class="page"><a href="'+href+'?paging='+str(cur_page - 1)+'">上一页</a>&nbsp;'
    else:
        out = '<div class="page"><a>上一页</a>&nbsp;'
    if cur_page > max_page:
        ratio = math.floor(cur_page/max_page-0.001)
        _from = ratio*max_page+1
        _to = size
        if _to > max_page + _from - 1:
            _to = max_page + _from - 1
    else:
        _from = 1
        _to = max_page
        if _to > size:
            _to = size
    for i in range(_from, _to+1):
        if cur_page == i:
            style = 'style="background-color:#ccc;color:white"'
        else:
            style = ''
        out = out + '<a ' + style + ' href="'+href+'?paging=' + str(i) + '">' + str(i) + '</a>&nbsp;'
    if cur_page < size:
        out = out + '<a href="'+href+'?paging='+str(cur_page + 1)+'">下一页</a></div>'
    else:
        out = out + '<a>下一页</a></div>'
    return out


class EventHandler(ProcessEvent):
    def process_IN_DELETE(self, event):
        file = os.path.join(event.path, event.name)
        if file.endswith('.md'):
            print("Delete file:%s." % file)
            remove_one_file(file)

    def process_IN_MODIFY(self, event):
        file = os.path.join(event.path, event.name)
        if file.endswith('.md'):
            print("Modify file:%s." % file)
            modify_one_file(file)


def fs_monitor(path='.'):
    wm = WatchManager()
    mask = IN_DELETE | IN_CREATE | IN_MODIFY
    notifier = Notifier(wm, EventHandler())
    wm.add_watch(path, mask, auto_add=True, rec=True)
    print("now starting monitor %s." % path)
    while True:
        try:
            notifier.process_events()
            if notifier.check_events():
                print("check event true.")
                notifier.read_events()
        except KeyboardInterrupt:
            print("keyboard Interrupt.")
            notifier.stop()
            break


def to_table(filename, sep):
    file_obj_r = open(filename, 'r')
    out = list()
    count = 0
    for line in file_obj_r:
        rec = line.split(sep)
        new_rec = [i.strip() for i in rec]
        new_rec = '|' + '|'.join(new_rec) + '|' + '\n'
        out.append(new_rec)
        if count == 0:
            head_rec = '|'
            head_rec = head_rec + '---|'*len(rec)
            head_rec += '\n'
            out.append(head_rec)
        count += 1
        if count >= 100:
            break
    file_obj_r.close()
    return ''.join(out)


init_db()
task = threading.Thread(target=fs_monitor, args=("post",))
task.start()
