import os
import time
import tornado.ioloop
import tornado.web

from settings import static_path


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        return self.render('index.html')


class UploadFileHandler(tornado.web.RequestHandler):

    def post(self):
        from settings import upload_path

        name = self.get_argument('name', '')
        student_number = self.get_argument('student_number', '')
        phone_number = self.get_argument('phone_number', '')


        if not(name and student_number and phone_number):
            self.finish(dict(result='Please input all fields!'))
            return
        if not student_number.isdigit():
            self.finish(dict(result='Please input correct student number!'))
            return
        
        now_time = time.strftime('%Y-%m-%dT%H-%M-%S',time.localtime(time.time()))
        dir_prefix = '_'.join([now_time, str(student_number)])
        file_metas = self.request.files['file']

        for meta in file_metas:
            filename = meta['filename']
            if not filename.endswith('.pdf'):
                self.finish(dict(result='Not a pdf file!'))
                return
            try:
                os.makedirs(os.path.join(upload_path, dir_prefix))
            except:
                pass
            # save file
            filepath = os.path.join(upload_path, dir_prefix, filename)
            with open(filepath,'wb') as up:
                up.write(meta['body'])
            # save other info
            filepath = os.path.join(upload_path, dir_prefix, 'info.txt')
            with open(filepath, 'w') as info:
                info.write('\n'.join([name, student_number, phone_number]))
            self.finish(dict(result='success'))


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/upload", UploadFileHandler)],
    static_path=static_path)

if __name__ == "__main__":
    application.listen(80, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()