import xml.etree.ElementTree as ET
import pickle
import tkinter as tk
import tkinter.filedialog
import os
import sys
import subprocess



def main():
    window = tk.Tk()
    window.withdraw()       #tkinterウィンドウの非表示



    directory = sys.argv[0].rsplit('\\',1)[0]+'\\'      #本体のディレクトリの取得
    print('Directory:', directory)
    

    
    if not os.path.isfile(directory+'path.txt'):      #path.txtがない場合、新規作成するか確認
        print('\n  Not find path.txt.')
        print('  Place loadmod.exe and path.txt in the same directory.')
        if input('\n  Make a new path.txt and continue?(y/n)  >  ')=='y':
            with open(directory+'path.txt', 'w') as f:
                f.write('C:\Program Files (x86)\Steam\steamapps\common\Besiege\Besiege_Data\Mods\Config\Modding.xml')
            print('making {}path.txt\n'.format(directory))
        else:
            print('Cancel')
            input('  (You can close this window)')
            return 0
   
    with open(directory+'path.txt', 'r') as f:        #path.txtの読み込み
        PATH = f.read()
        print('PATH:',PATH)

    if not os.path.isfile(PATH):        #path.txtにModding.xmlがない場合、中止
        print('\n  There is an error in the path.')
        print('  Please check and correct path.txt!')
        input('  (You can close this window)')
        return 1

    

    if len(sys.argv) > 1:       #引数がある場合、その引数のファイルを使う
        print('Input:',sys.argv[1])
        filename = sys.argv[1]
    else:       #ない場合はダイアログを出す
        fTyp = [('modset', '*.bms')]
        iDir = os.path.abspath(os.path.dirname(__file__))
        filename = tkinter.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)

    if filename !='':       #ファイルの読み込み
        with open(filename, 'rb') as f:
            try:
                abledMods = pickle.load(f)
                abledMods = abledMods | set()
            except:
                print('  Can not open this file.')
                print('  Please use another file or resave.')
                input('  (You can close this window)')
                return 1
    else:
        print('Cancel')
        input('  (You can close this window)')
        return 0

    print('\n abledMods')
    print(abledMods)



    try:
        tree = ET.parse(PATH) #Modding.xmlの読み込み
    except:
        print('\n  There is an error in Modding.xml.')
        print('  Try replacing Modding.xml with the backup file or restarting Besiege.')

        if input('\n  Replacing Modding.xml with the backup and continue?(y/n)  >  ')=='y':
            if not os.path.isfile(directory+'backup\\Modding.xml'):     #不具合発生時バックアップでModding.xmlを置き換えるか確認
                print('  Not find backup\\Modding.xml.')
                print('  Replacing failed.')
                print('  Try restarting Besiege.')
                input('  (You can close this window)')
                return 1
            else:
                print('> copy "{}backup\\Modding.xml" "{}"'.format(directory,PATH))
                if subprocess.call('copy "{}backup\\Modding.xml" "{}"'.format(directory,PATH),shell=True) == 0:      #バックアップの使用
                    print('Replacing successful.')
                    try:
                        tree = ET.parse(PATH)
                        print('  The error is resolved.\n')
                    except:
                        print('  BUT the error is NOT resolved.')
                        print('  Try restarting Besiege.')
                        input('  (You can close this window)')
                        return 1
                        
                else:
                    print('  Replacing failed.')
                    print('  Try replacing Modding.xml with the backup file in manual or restarting Besiege.')
                    input('  (You can close this window)')
                    return 1
        else:
            print('Cancel')
            input('  (You can close this window)')
            return 0


    
    root = tree.getroot()
    maintenanceLastMods = set()
    
    for SA in root.iter('StringArray'):
        if SA.attrib['key'] == 'maintenance-lastMods':      #利用可能なModの情報を取得
            maintenanceLastMods = set([S.text.split('~')[0] for S in SA.iter('String')])
            skip_mod = False
        if SA.attrib['key'] == 'disabled-mods':      #現在の使用していないModの情報を削除
            root.remove(SA)

    disabledMods = maintenanceLastMods - abledMods      #使用していないModを計算

    if disabledMods != set():
        SA_D = ET.SubElement(root, 'StringArray',attrib={'key':'disabled-mods'})
        for disabledMod in disabledMods:
            ET.SubElement(SA_D, 'String').text = disabledMod      #新しい使用していないModの情報を追加

    print('\n','maintenance-lastMods')
    print(maintenanceLastMods)

    print('\n','disabled-mods')
    print(disabledMods,'\n')



    skip_backup = False
    if not os.path.isdir(directory+'backup'):     #バックアップディレクトリがなければ作成するか確認
        print('  Not find backup directory.')
        print('  Place loadmod.exe and backup directory in the same directory.')
        if input('\n  Make a new backup directory and continue?(y/n)  >  ')=='y':
            print('> mkdir "{}backup"'.format(directory))
            if subprocess.call('mkdir "{}backup"'.format(directory),shell=True) != 0:
                print('  Making failed.')
                if input('\n  Continue without backup?(y/n)  >  ')!='y':
                    print('Cancel')
                    input('  (You can close this window)')
                    return 0
                else:
                    print()
                    skip_backup = True
        else:
            print('Cancel')
            input('  (You can close this window)')
            return 0

    if not skip_backup:        
        print('> copy "{}" "{}backup\\Modding.xml"'.format(PATH,directory))
        if subprocess.call('copy "{}" "{}backup\\Modding.xml"'.format(PATH,directory),shell=True) == 0:      #バックアップの作成
            print('  Backup successful.')
        else:
            print('  Backup failed.')
            if input('\n  Continue without backup?(y/n)  >  ')!='y':
                print('Cancel')
                input('  (You can close this window)')
                return 0



    tree.write(PATH,'utf-8')        #Modding.xmlへの書き込み
    print('\n    Successfully')



    
    if not os.path.isfile('{}Besiege.url'.format(directory)):       #Besiege.urlがなければ作成
        print('\n  Not find Besiege.url.')
        
        #if input('\n  Make a new Besiege.url and start Besiege?(y/n)  >  ')=='y':
        if True:
            with open(directory+'Besiege.url', 'w') as f:
                f.write('[InternetShortcut]\nURL="steam://rungameid/346010"')
            print('making {}Besiege.url'.format(directory))
        else:
            print('Cancel')
            input('  (You can close this window)')
            return 0        

    print('\n> "{}Besiege.url"'.format(directory))
    if subprocess.run('"{}Besiege.url"'.format(directory),shell=True).returncode==0:     #Besiege起動
        print('  Starting Besiege')
    else:
        print('  Starting Besiege failed.')
        print('  Some error occurred when starting Besiege.')
        input('  (You can close this window)')

    return 0





try:
    main()
except:
    import traceback
    print()
    traceback.print_exc()
    print('\n\n  An unexpected error occurred.\n Please contact the administrator.')
    print('  E-mail moto.allergyholder@gmail.com')
    input('  (You can close this window)')

