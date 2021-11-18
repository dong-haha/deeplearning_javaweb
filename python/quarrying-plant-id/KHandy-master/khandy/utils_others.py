import time
import socket
import logging
from collections import OrderedDict


def print_with_no(obj):
    if hasattr(obj, '__len__'):
        for k, item in enumerate(obj):
            print('[{}/{}] {}'.format(k+1, len(obj), item)) 
    elif hasattr(obj, '__iter__'):
        for k, item in enumerate(obj):
            print('[{}] {}'.format(k+1, item)) 
    else:
        print('[1] {}'.format(obj))
        
      
def get_file_line_count(filename):
    line_count = 0
    buffer_size = 1024 * 1024 * 8
    with open(filename, 'r') as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            line_count += data.count('\n')
    return line_count

    
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
    
 
class ContextTimer(object):
    """
    References:
        WithTimer in https://github.com/uber/ludwig/blob/master/ludwig/utils/time_utils.py
    """
    def __init__(self, name=None, use_log=False, quiet=False):
        self.use_log = use_log
        self.quiet = quiet
        if name is None:
            self.name = ''
        else:
            self.name = '{}, '.format(name.rstrip())
                
    def __enter__(self):
        self.start_time = time.time()
        if not self.quiet:
            self._print_or_log('{}{} starts'.format(self.name, self._now_time_str))
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.quiet:
            self._print_or_log('{}elapsed_time = {:.5}s'.format(self.name, self.get_eplased_time()))
            self._print_or_log('{}{} ends'.format(self.name, self._now_time_str))
            
    @property
    def _now_time_str(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
    def _print_or_log(self, output_str):
        if self.use_log:
            logging.info(output_str)
        else:
            print(output_str)
            
    def get_eplased_time(self):
        return time.time() - self.start_time
        
    def enter(self):
        """Manually trigger enter"""
        self.__enter__()
        