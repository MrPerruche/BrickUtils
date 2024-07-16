print('dev tools')
print('small toolset to help working on brickutils')
print('1: convert hsva to u8 hsva')
print('2: convert u8 hsva to hsva')
print('3: reset config.json')


tool = input()


if tool == '1':

    h = float(input('h°='))
    s = float(input('s%='))
    v = float(input('v%='))
    a = float(input('a%='))

    print(f'{int(h/360*255)=}, {int(s/100*255)=}, {int(v/100*255)=}, {int(a/100*255)=}')

elif tool == '2':

    h = float(input('hu8='))
    s = float(input('su8='))
    v = float(input('vu8='))
    a = float(input('au8='))

    print(f'{h/255*360=}, {s/255*100=}, {v/255*100=}, {a/255*100=}')

elif tool == '3':

    from os.path import join, dirname, realpath
    cwd = dirname(realpath(__file__))
    source = join(cwd, 'resources', 'default_config')  # has no extension
    new_path = join(cwd, 'config.json')

    with open(source, 'rb') as f:
        file = f.read()

    with open(new_path, 'wb') as f:
        f.write(file)

input('press anything to quit.')