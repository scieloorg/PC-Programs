import os
import sys

class IDFile2ISIS:
    def __init__(self, cisis_path):
        self.cisis_path = cisis_path.replace('\\', '/')
        
        if os.path.exists(cisis_path):
            self.cisis_path = cisis_path
        else:
            print('Invalid cisis path: ' + cisis_path)
    
    def write_script(self, script_filename, cmd):
        f = open(script_filename, 'w')
        if '.bat' in script_filename:
            f.write(self.c2batch(cmd))
        else:
            f.write(cmd)
        f.close()
    def c2batch(self, cmd):
        cmd = cmd.replace('.sh', '.bat' )
        cmd = cmd.replace('./', 'call ' )
        cmd = cmd.replace('/', '\\')
        return cmd
    def create_script_content(self, db_path, db_name, report):
        files = os.listdir(db_path)
        cmd = 'cd '  + db_path + "\n" 
        for f in files:
            print(f)
            if '.id' in f:
                cmd += self.get_command(db_path + '/' + f, db_path + '/' + db_name, report)
        return cmd
    
    def get_command(self, id_filename, db_filename, report):
        return './id2mst.sh ' + self.cisis_path + ' ' + id_filename + ' ' + db_filename + "\n"
    
    def run_commands(self, commands, is_batch = False):
        if is_batch:
            commands = self.c2batch(commands)
        command_list = commands.split("\n")
        for cmd in command_list:
            os.system(cmd)
        
         
        
        
       
        
    