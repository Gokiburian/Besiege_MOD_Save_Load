import xml.etree.ElementTree as ET
import pickle
import tkinter as tk
import tkinter.filedialog
import os
import sys



def main():
    window = tk.Tk()
    window.withdraw() #tkinterウィンドウの非表示



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



    try:
        tree = ET.parse(PATH)       #Modding.xmlの読み込み
    except:
        print('\n  There is an error in Modding.xml.')
        print('   Try restarting Besiege.')
        input('  (You can close this window)')
        return 1


    
    root = tree.getroot()
    disabledMods = set()
    maintenanceLastMods = set()
    
    for SA in root.iter('StringArray'):
        if SA.attrib['key'] == 'disabled-mods':         #使用していないModの情報取得
            disabledMods = set([S.text for S in SA.iter('String')])

        elif SA.attrib['key'] == 'maintenance-lastMods':        #使用可能なModの情報取得
            maintenanceLastMods = set([S.text.split('~')[0] for S in SA.iter('String')])

    print('\n disabled-mods')
    print(disabledMods)

    print('\n maintenance-lastMods')
    print(maintenanceLastMods)

    abledMods = maintenanceLastMods - disabledMods     #使用しているModを計算
    print('\n abledMods')
    print(abledMods,'\n')



    fTyp = [('modset', '*.bms')]        #保存場所、ファイル名をダイアログで決定
    iDir = os.path.abspath(os.path.dirname(__file__))
    filename = tkinter.filedialog.asksaveasfilename(filetypes=fTyp, initialdir=iDir, defaultextension='bms')

    if filename != '':      #保存
        with open(filename, 'wb') as f:
            pickle.dump(abledMods,f)
        print('    Successfully')
    else:
        print('Cancel')
        input('  (You can close this window)')
        return 0

    return 0





try:
    main()
except:
    import traceback
    traceback.print_exc()
    print("\n\n  An unexpected error occurred.\n Please contact the administrator.")
    print("  E-mail moto.allergyholder@gmail.com")
    input('  (You can close this window)')
