import os
import math

# convert folder size.
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def getFolderSize():
    # assign size
    size = 0
    # assign folder path
    Folderpath = 'Backups/'
    
    # get size
    for path, dirs, files in os.walk(Folderpath):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
    
    return (size, len(files)) #folder size in KB and folder len files.
    
# display size
folderspec=getFolderSize()
print(folderspec[0],folderspec[1])