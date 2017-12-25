# -*- coding: utf-8 -*-
import os, sys, shutil, re

def trip_space(s):

    while len(s) > 0 and s[-1] == '\x00':

        s = s[:-1]

##    while len(s) > 0 and s[:2]  == b'\x00\x00':

##        s = s[2:]

    return s

def _print(*args):
    try:
        for arg in args:
            print arg,
        print '\n'
    except UnicodeEncodeError as msg:
        print 'Error to print', args,  msg

# ID3V2, ID3V3
class MP3:
    def __init__(self, filepath):
        self.filepath = filepath
        f = open(filepath, 'rb')
        self.data = f.read()
        f.close()

        self.tags = {} # tags

        try:
            self.read_header()
            self.read_id_frame()
        except:
            pass

    def read_header(self):
        data = self.data

        self.Header = data[:3] #ID3
        self.Ver = ord(data[3:4])
        self.Revision = ord(data[4:5])
        self.Flag = ord(data[5:6])
        Size = data[6:10]
        self.total_size = (ord(Size[0])&0x7F)*0x200000+ (ord(Size[1] or 0)&0x7F)*0x400 + (ord(Size[2] or 0)&0x7F)*0x80 +(ord(Size[3] or 0)&0x7F)

        #print "Header=%s, Ver=%s, Revision=%s, Flag=%s, Size=%s\n" %(self.Header, self.Ver, self.Revision, self.Flag, self.total_size)

    def read_id_frame(self):
        data = self.data

        #if self.Ver == 2:
        cur_index = 10
        max_index = self.total_size
        while cur_index < self.total_size:
            FrameID = data[cur_index:cur_index+4]
            FrameSize = data[cur_index+4:cur_index+8]
            FSize = ord(FrameSize[0])*0x100000000 + ord(FrameSize[1])*0x10000+ ord(FrameSize[2])*0x100 + ord(FrameSize[3])
            FrameFlags = data[cur_index+8:cur_index+10]

            # Refers to http://blog.sina.com.cn/s/blog_80ab598b0102vbao.html
            # decoding tag info.
            if FrameID != 'APIC':

                info = data[cur_index+10:cur_index+10+FSize]
                try:
                    st = info.rfind(b'\xff\xfe')
                    if st != -1: # \x01\xff\xfe.....\xff\xfe
                        #print FrameID, r'\x01\xff\xfe', FSize
                        self.tags[FrameID] = trip_space(info[st+2:].decode('utf16'))
                    elif info.startswith(b'\x03'):
                        self.tags[FrameID] = trip_space(info[1:].decode())
                    else: #\x00
                        #print FrameID, 'decode gbk'
                        self.tags[FrameID] = info[1:-1].replace(b'\x00',b'\x20').decode('gbk')
                except UnicodeDecodeError as msg:
                    #print('Decode Error @%s, Content is %s\nMsg:%s'%(kind,info, msg))
                    pass

            cur_index += 10 + FSize

    def is_valid(self):
        return self.Header == 'ID3'

    def title(self):
        return self.tags.get('TIT2') or os.path.basename(self.filepath).split('.')[0]

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: %s [cache folder] [output_folder]' %sys.argv[0]
        sys.exit(0)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    files = os.listdir(input_dir)

    for file in files:
        src_path = os.path.join(input_dir, file)
        if os.path.isdir(src_path): continue # don't process directory

        mp3 = MP3(src_path)
        if mp3.is_valid():
            title = mp3.title()
            title_repl = re.sub('[\\\/\:\*\?"<>|]', '_', title)
            dest_path = os.path.join(output_dir, title_repl+'.mp3')
            _print(src_path, '>>', dest_path)
            shutil.copy(src_path, dest_path)
