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
        remark = self.get_argument('remark', '')


        if not(name and student_number and phone_number):
        	return self.render('result.html', result='negative', result_header='Upload Failed', result_content='Please input all fields!')
        if not student_number.isdigit():
        	return self.render('result.html', result='negative', result_header='Upload Failed', result_content='Please input correct student number!')
        
        now_time = time.strftime('%Y-%m-%dT%H-%M-%S',time.localtime(time.time()))
        dir_prefix = '_'.join([now_time, str(student_number)])
        try:
        	file_metas = self.request.files['file']
        except:
        	return self.render('result.html', result='negative', result_header='Upload Failed', result_content='Please select a file to print!')

        for meta in file_metas:
            filename = meta['filename']
            if not filename.endswith('.pdf'):
            	return self.render('result.html', result='negative', result_header='Upload Failed', result_content='Not a pdf file!')
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
                info.write('\n'.join([name, student_number, phone_number, '-------', remark]))
            return self.render('result.html', result='positive', result_header='Upload Success', result_content='Please connect us to get the file.')


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/upload", UploadFileHandler)],
    static_path=static_path)

if __name__ == "__main__":
    application.listen(80, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()