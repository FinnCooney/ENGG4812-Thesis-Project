import os # Used to updated file endings
from time import sleep
import winreg # Used to update file extention mappings in registry
import string
import secrets

dirs = {'C:\\Users\\Finn\\OneDrive\\Uni\\Year4\\Sem2\\ENGG4812\\ENGG4812-Thesis-Project\\test-files'}
protected_exts = {'.pptx', '.docx', '.pdf'}
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
    print(exts_rand)
    for d in dirs:
        # Check directory exists
        if os.path.isdir(d):
            # Rotate file extentions in dir that are in extention list
            # Step through any child dirs
            dir = os.listdir(d)
            for f in dir:
                print(f)
                if os.path.isfile(f):
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
                        os.rename(f, f'{root}{new_ext}')

                        # Clean up old extention
                        if ext not in protected_exts:
                            with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey:
                                remove_key(hkey, f'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\{ext}')
                            with winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT) as hkey:
                                remove_key(hkey, ext)
                    # Allow for multiple files with the same extention
                    elif ext in exts_rand.values():
                        pos = exts_rand.index(ext)
                        new_ext = exts_rand[pos]
                        os.rename(f, f'{root}{new_ext}')

        """ Don't think I need this
        else:
            dirs.remove(d)
        """