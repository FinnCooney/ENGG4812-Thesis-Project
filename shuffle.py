import os # Used to updated file endings
from time import sleep
import winreg # Used to update file extention mappings in registry
import string
import secrets

dirs = {'C:\\Users\\FinnC.DESKTOP-J259HOQ\\Documents'}
protected_exts = {'.der', '.pfx', '.key', '.crt', '.csr', '.p12', '.pem', '.odt', '.ott', '.sxw', '.stw', '.uot', '.3ds', '.max', '.3dm', '.ods', '.ots', '.sxc', '.stc', '.dif', '.slk', '.wb2', '.odp', '.otp', '.sxd', '.std', '.uop', '.odg', '.otg', '.sxm', '.mml', '.lay', '.lay6', '.asc', '.sqlite3', '.sqlitedb', '.sql', '.accdb', '.mdb', '.dbf', '.odb', '.frm', '.myd', '.myi', '.ibd', '.mdf', '.ldf', '.sln', '.suo', '.cpp', '.pas', '.asm', '.cmd', '.bat', '.ps1', '.vbs', '.dip', '.dch', '.sch', '.brd', '.jsp', '.php', '.asp', '.java', '.jar', '.class', '.mp3', '.wav', '.swf', '.fla', '.wmv', '.mpg', '.vob', '.mpeg', '.asf', '.avi', '.mov', '.mp4', '.3gp', '.mkv', '.3g2', '.flv', '.wma', '.mid', '.m3u', '.m4u', '.djvu', '.svg', '.psd', '.nef', '.tiff', '.tif', '.cgm', '.raw', '.gif', '.png', '.bmp', '.jpg', '.jpeg', '.vcd', '.iso', '.backup', '.zip', '.rar', '.tgz', '.tar', '.bak', '.tbk', '.bz2', '.PAQ', '.ARC', '.aes', '.gpg', '.vmx', '.vmdk', '.vdi', '.sldm', '.sldx', '.sti', '.sxi', '.602', '.hwp', '.snt', '.onetoc2', '.dwg', '.pdf', '.wk1', '.wks', '.123', '.rtf', '.csv', '.txt', '.vsdx', '.vsd', '.edb', '.eml', '.msg', '.ost', '.pst', '.potm', '.potx', '.ppam', '.ppsx', '.ppsm', '.pps', '.pot', '.pptm', '.pptx', '.ppt', '.xltm', '.xltx', '.xlc', '.xlm', '.xlt', '.xlw', '.xlsb', '.xlsm', '.xlsx', '.xls', '.dotx', '.dotm', '.dot', '.docm', '.docb', '.docx', '.doc'}
exts_rand = {}

def extExists(ext) -> bool:
    with winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT) as hkey:
        try:
            sub_key = winreg.OpenKey(hkey, ext)
        except OSError:
            return False
        else:
            winreg.CloseKey(sub_key)
            return True

def extension_init():
    for e in protected_exts:
        exts_rand.update({e:e})
        
def extension_gen(e):
    prev = e
    keys = exts_rand.keys()
    while e in keys or e in protected_exts or extExists(e):
        print(keys)
        print(e)
        ext = e
        e = '.' + (''.join(secrets.choice(string.ascii_lowercase) for _ in range(len(e) - 1))) # Might randomise the length of the exts
    
    ext = exts_rand.pop(prev)
    exts_rand.update({e:ext})
    print(exts_rand)
    return e

def create_key(parent_key, old_key, new_key):
    print (f'{parent_key}, {old_key}, {new_key}')
    with winreg.CreateKey(parent_key, new_key) as new:
        with winreg.OpenKey(parent_key, old_key, 0, winreg.KEY_READ) as old:
            keys, values, time = winreg.QueryInfoKey(old)
            if keys != 0:
                for i in range(keys):
                    sub_key = winreg.EnumKey(old, i)
                    create_key(parent_key, f'{old_key}\{sub_key}', f'{new_key}\{sub_key}')
            for i in range(values):
                name, data, t = winreg.EnumValue(old, i)
                winreg.SetValueEx(new, name, 0, t, data)
                print(winreg.EnumValue(old, i))

def remove_key(parent_key, old_key):
    with winreg.OpenKey(parent_key, old_key, 0, winreg.KEY_ALL_ACCESS) as old:
        keys, values, time = winreg.QueryInfoKey(old)
        while keys != 0:
            sub_key = winreg.EnumKey(old,0)
            remove_key(parent_key, f'{old_key}\{sub_key}')
            keys, values, time = winreg.QueryInfoKey(old)
        winreg.DeleteKey(parent_key, old_key)

if __name__ == "__main__":
    extension_init()
    for d in dirs:
        # Check directory exists
        if os.path.isdir(d):
            # Rotate file extentions in dir that are in extention list
            # Step through any child dirs
            dir = os.listdir(d)
            print(dir)

            for f in dir:
                print(f)
                print(f'{d}\\{f}')
                if os.path.isfile(f'{d}\\{f}'):
                    split = os.path.splitext(f)
                    root = split[0]
                    ext = split[1]
                    print("Here")
                    # Check if the extention should be shuffled
                    print(ext)
                    if ext in exts_rand:
                        print(exts_rand)

                        # Generate new extention and copy the keys of the old one
                        new_ext = extension_gen(ext)
                        with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey:
                            create_key(hkey, f'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\{ext}', f'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\{new_ext}')
                        with winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT) as hkey:
                            create_key(hkey, ext, new_ext)
                        os.rename(f'{d}\\{f}', f'{d}\\{root}{new_ext}')

                        # Clean up old extention
                        if ext not in protected_exts:
                            with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey:
                                remove_key(hkey, f'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\{ext}')
                            with winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT) as hkey:
                                remove_key(hkey, ext)
                    # Allow for multiple files with the same extention 
                    elif ext in exts_rand.values():
                        pos = list(exts_rand.values()).index(ext)
                        new_ext = list(exts_rand.keys())[pos]
                        os.rename(f'{d}\\{f}', f'{d}\\{root}{new_ext}')


        """ Don't think I need this
        else:
            dirs.remove(d)
        """