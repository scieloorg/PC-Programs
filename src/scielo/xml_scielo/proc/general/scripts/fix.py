import sys, os

for f in os.listdir(sys.argv[1]):
    
    if not f.startswith('fixed_'):    
    
        print(sys.argv[1] + '/' + f)
        fp = open(sys.argv[1] + '/' + f, 'r')
        a = fp.read()
        a = a[a.find('<article'):]
        fp.close()

        print(sys.argv[1] + '/fixed_' + f)
        fp = open(sys.argv[1] + '/fixed_' + f, 'w')
        fp.write(a)
        fp.close()
