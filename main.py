import flask
import data_proc as db_tool
import math
import os
from datetime import timedelta
app = flask.Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(seconds=1)


@app.route("/hook", methods=['POST'])
def hook():
    # 调用本地脚本进行更新
    os.system("git pull")
    return 'ok'


@app.route("/data/<data_name>")
def data(data_name):
    file_name = "data/"+data_name+".csv"
    if os.path.exists(file_name):
        return flask.render_template('data.html',
                                     data=flask.Markup(db_tool.markdown_trans(db_tool.to_table(file_name, ","))))
    else:
        return flask.render_template('404.html')


@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    return flask.send_from_directory("data", filename+".csv", as_attachment=True)


@app.route("/article/<article_id>")
def article(article_id):
    if article_id in db_tool.articles:
        entity = db_tool.articles[article_id]
        return flask.render_template("article.html", title=entity['title'],
                                     date=entity['date'], html=flask.Markup(entity['html']),
                                     detail_tags=flask.Markup(db_tool.get_detail_tags_html(article_id)))
    else:
        return flask.render_template('404.html')


def paging_html(objs, show_head, href):
    page_size = 7
    max_paging = 3
    paging = flask.request.args.get('paging')
    if paging is None or str(paging).isdigit():
        size = math.ceil(len(objs) / page_size)
        if paging is None:
            cur_page = 1
        elif int(paging) <= size:
            cur_page = int(paging)
        else:
            cur_page = 0
        if cur_page == 0:
            return flask.render_template('404.html')
        else:
            list_data = flask.Markup(''.join(objs[((cur_page - 1) * page_size):(cur_page * page_size)]))
            return flask.render_template("home.html",
                                         list_data=list_data,
                                         list_title=show_head,
                                         paging=flask.Markup(db_tool.get_paging(size, cur_page, max_paging, href)))
    else:
        return flask.render_template('404.html')


@app.route("/")
def hello():
    content = list()
    for item in db_tool.home_index:
        content.append(db_tool.get_item_html(item['article_id'], item['title'], item['date']))
    return paging_html(content, 'Recent Update', '')


@app.route("/about")
def about():
    return flask.render_template("about.html")


@app.route("/tags")
def tags():
    out = list()
    for key in db_tool.tags_index:
        out.append(db_tool.get_tags_html(key))
    return flask.render_template("tags.html", tags=flask.Markup(''.join(out)))


@app.route("/categories")
def categories():
    out = list()
    for key in db_tool.category_index:
        out.append(db_tool.get_category_html(key))
    return flask.render_template("categories.html", cate=flask.Markup(''.join(out)))


@app.route('/categories_list/<cate_key>/<sub_cate>')
def categories_list(cate_key, sub_cate):
    content = list()
    for item in db_tool.category_index[cate_key][sub_cate]:
        content.append(db_tool.get_item_html(item['article_id'], item['title'], item['date']))
    return paging_html(content, "分类："+cate_key+" > "+sub_cate,
                       '/categories_list/'+cate_key+"/"+sub_cate)


@app.route('/tags_list/<tag_key>/<sub_tag>')
def tags_list(tag_key, sub_tag):
    content = list()
    for item in db_tool.tags_index[tag_key][sub_tag]:
        content.append(db_tool.get_item_html(item['article_id'], item['title'], item['date']))
    return paging_html(content, "标签："+tag_key + " > " + sub_tag,
                       '/tags_list/'+tag_key+'/'+sub_tag)


@app.route("/images/<image_id>")
def index(image_id):
    image = open("images/{}.svg".format(image_id))
    resp = flask.Response(image, mimetype="image/svg+xml")
    return resp


if __name__ == "__main__":
    app.run('0.0.0.0', 80)
