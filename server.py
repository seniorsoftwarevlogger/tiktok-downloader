from http.server import BaseHTTPRequestHandler, HTTPServer
from TikTokApi import TikTokApi

import argparse
import re
import os


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if None != re.search('/' + os.environ.get('CODE') + '/*', self.path):
            videoId = self.path.split('/')[-1]

            self.send_response(200)
            self.send_header('Content-Type', 'video/mp4')
            self.end_headers()

            with TikTokApi(custom_verify_fp=os.environ.get('VERIFY')) as api:
                video = api.video(id=videoId)
                video_data = video.bytes()
                self.wfile.write(video_data)
        else:
            self.send_response(400)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(str.encode(("Nope")))

        return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTTP Server')
    parser.add_argument(
        'port', type=int, help='Listening port for HTTP Server')
    parser.add_argument('ip', help='HTTP Server IP')
    args = parser.parse_args()

    with HTTPServer((args.ip, args.port), HTTPRequestHandler) as server:
        print("Serving at port", args.port)
        server.serve_forever()
