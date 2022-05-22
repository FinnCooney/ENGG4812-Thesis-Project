import winreg

# HKEY_CLASSES_ROOT\Wow6432Node\CLSID\{CF4F55F4-8F87-4D47-80BB-5808164BB3F8}

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

def extExists(ext) -> bool:
    with winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT) as hkey:
        try:
            sub_key = winreg.OpenKey(hkey, ext)
        except OSError:
            return False
        else:
            winreg.CloseKey(sub_key)
            return True

                
#with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey:
#    create_key(hkey, "SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.pptx", "SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.pppp")

#with winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT) as hkey:
#    create_key(hkey, ".pptx", ".pppp")

#with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey:
#    remove_key(hkey, "SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.ppp")
    

#with winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT) as hkey:
#    remove_key(hkey, ".ppp")
