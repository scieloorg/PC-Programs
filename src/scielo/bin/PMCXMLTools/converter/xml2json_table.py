
class XML2JSONTable:

    def __init__(self, filename):
        
        self.start = MyNode(None)
        
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        
        
        
        last_level = -1
        parent_node = MyNode(None)
        current_node = self.start
        self.start.xpath = '.'
        current_node.parent = parent_node
        
        
        for line in lines:
            level = self.get_level(line)
            
            c = line.strip() 

            values  = c.split(' ')
            
            attr = ''
            xpath = ''
            to = ''
            default = ''
            if len(values) >= 1:
                xpath = values[0]
            if len(values) >= 2:
                to = values[1]
            if len(values) >= 3:
                default = values[2]
                

            if xpath.startswith('@'):
                attr = xpath
                xpath = ''
            elif xpath == '.':
                xpath = ''
            elif '/@' in xpath:
                attr = xpath[xpath.find('/@')+1:]
                xpath = xpath[0:xpath.find('/@')]
            if len(xpath)>0 and not xpath.startswith('.//') :
                xpath = './' + xpath
            
            new_node = MyNode(parent_node)
            new_node.xpath = xpath
            new_node.to = to
            if default == 'XML':
                new_node.xml = True
            else:
                new_node.default = default
            
            new_node.attr = attr
            if last_level < level:
                # down
                parent_node = current_node
                new_node.parent = current_node
                parent_node.children.append(new_node)
                current_node = new_node
            else:
                if last_level > level:
                    # previous level
                    count = last_level - level 
                    for i in range(0,count):
                        current_node = current_node.parent
                        parent_node = parent_node.parent
                        
                    parent_node.children.append(new_node)
                    new_node.parent = parent_node
                    current_node = new_node
                else:
                    if last_level == level:
                        # same level
                        new_node.parent = parent_node
                        parent_node.children.append(new_node)
                        
                        current_node = new_node
                    else:
                        pass
            last_level = level
            
            
        #self.print_structure()
            
    def print_structure(self):
        self.print_node(self.start, 0)
        
    def print_node(self, node, level=0):
        if node != None:
            r = ' ' * level * 2 + node.xpath + ' ' + node.to + ' ' + node.default 
            print(r)
            level += 1
        
            for child in node.children:
                self.print_node(child, level)
        
    def get_level(self, line):
        line = line.rstrip()
        if '      ' in line:
            r = 3
        else:
            if '    ' in line:
                r = 2
            else:
                if '  ' in line:
                    r = 1
                else:
                    r = 0
        return r
         
class MyNode:
    def __init__(self, parent):
        self.xpath = ''
        self.to = ''
        self.default = ''
        self.children = []
        self.parent = parent
        self.attr = ''
        self.xml = False



        