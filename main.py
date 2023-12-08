from flask import Flask, render_template, url_for,send_from_directory, request,redirect
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)



app.config['UPLOAD_FOLDER'] = "file_storage/"
app.config['MAX_CONTENT_PATH'] = 1000000


bloglist = {}
reversed_bloglist = {}
bloglist = {}
blst = os.listdir("blogs")
for i in range(len(blst)):
    name = blst[len(blst)-1-i][5:]
    reversed_name = blst[i][5:]
    bloglist[name[:-4]] = blst[len(blst)-1-i]
    reversed_bloglist[reversed_name[:-4]] = blst[i]
def reloadFiles():
    bloglist = {}
    blst = os.listdir("blogs")
    for i in range(len(blst)):
        name = blst[len(blst)-1-i][5:]
        reversed_name = blst[i][5:]
        bloglist[name[:-4]] = blst[len(blst)-1-i]
        reversed_bloglist[reversed_name[:-4]] = blst[i]
    return (bloglist,blst)
reloadFiles()
lngth = len(bloglist)


@app.route("/")
@app.route("/index")
def homepage():
    reloadFiles()
    return render_template("index.html", lst=bloglist)


@app.route("/blogs")
def blogs():
    bloglist, blst = reloadFiles()
    return render_template("blogs.html",lst=bloglist,btndst="/blogs/rev")



@app.route("/blogs/<name>/")
def viewblog(name):
    bloglist, blst = reloadFiles()
    with open("blogs/" + bloglist[name]) as F:
        cnt = F.readlines()
        header=cnt.pop(0)
        date=cnt.pop(0)
    return render_template("blogTmp.html",date=date,header=header,content=cnt,g=len(cnt))


@app.route("/", methods=['GET', 'POST'])
def search():
    getSearch = request.form['SearchBar']
    
    return redirect("/")



@app.route("/upload", methods=['GET', 'POST'])
def upload():
    list = os.listdir(app.root_path+'/file_storage')
    return render_template("uploader.html", list=list)



@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
        f = request.files['file']
        f.save(app.root_path+"/file_storage/"+secure_filename(f.filename))
        return redirect("/upload")

@app.route("/test/<name>")
def test(name):
    
    
    return render_template("test.html", test=name)

@app.route("/file/<filename>")
def download(filename):
    # Specify the path to your file storage folder
    folder_path = 'file_storage'
    
    # Use send_from_directory to send the file to the user
    return send_from_directory(folder_path, filename, as_attachment=True)
if __name__ == "__main__":
    app.run()