from subprocess import check_output
from pathlib import Path
import subprocess
import argparse
import sys

class n0te():
    def __init__(self):
        self.editor = "vim"                                        #$$$$$$$$ CHANGE THIS $$$$$$$$
        # Dir to save n0tes
        self.dir = "%s/Documents/notes/" % str(Path.home())         #$$$$$$$$ CHANGE THIS $$$$$$$$ default value is $HOME/Documents/notes/
        self.main()


    def banner(self):
        print("""
        ███╗   ██╗ ██████╗ ████████╗███████╗
        ████╗  ██║██╔═████╗╚══██╔══╝██╔════╝
        ██╔██╗ ██║██║██╔██║   ██║   █████╗
        ██║╚██╗██║████╔╝██║   ██║   ██╔══╝
        ██║ ╚████║╚██████╔╝   ██║   ███████╗
        ╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚══════╝
        """)

    def list_notes(self,letter=None):
        """
        List notes into directory
        :return: print '.md' files
        """
        # dont list directories
        out = check_output(["find", self.dir, "-maxdepth", "1", "-type", "f", "-printf","%f\n"])
        out_str = out.decode("utf-8")
        list_files = sorted(out_str.split("\n"))            # sort ASC files
        for w in range(len(list_files)):                    # foreach files
            list_files[w]=list_files[w].replace(".md","")   # replace '.md'
        if list_files[0] == "": #delete empty
            list_files.remove(list_files[0])
        if letter == None: # print notes
            print("Note list:")
            [print("• "+w) for w in list_files]          
        else:
            print("Note list with '%s' keyword:" % letter)
            for w in list_files:
                if w.startswith(letter):
                    print("\t• "+w)
        

    def verify_note(self, note):
        """
        Verify input note
        :param note: note name
        :return:
        """
        out = check_output(["ls", self.dir])
        return str(out).find(note)

    def display_note(self, note):
        """
        mdv the note
        :param note: note name
        :return:
        """
        if str(note).find(".md") == -1:
            note = note+".md"
        if self.verify_note(note) != -1:
            #subprocess.run(["mdv", "/home/dylan/Documents/notes/"+note, "|", "lolcat"])
            import os
            #os.system("mdv "+self.dir+note+" | lolcat")
            os.system("mdless "+self.dir+note)
        else:
            print("404 n0te not found..")

    def edit_note(self, note):
        creer = False
        if str(note).find(".md") == -1:
            note = note+".md"

        if self.verify_note(note) == -1:
            print("404 n0te not found..")
            rep = input("Create n0te ? (y/n) ")
            if rep.upper() == "Y":
                creer = True
        if self.verify_note(note) != -1 or creer is True:
            print("Openning %s" %self.editor)
            #print("%s/Documents/note/%s" %(dir,note))

            subprocess.run([self.editor, "%s%s" %(self.dir,note)])

    def delete_note(self, note):
        if str(note).find(".md") == -1:
            note = note+".md"
        if self.verify_note(note) == -1:
            print("404 n0te not found !")
        if self.verify_note(note) != -1:
            rep = input("Delete this n0te: %s ? (y/n) "%note)
            if rep.upper() == "Y":
                subprocess.run(["rm", "/home/dylan/Documents/notes/" + note])
                print("File '%s' deleted" %(self.dir+note))
            else:
                print("Cancel")

    def main(self):
        import os
        if len(sys.argv) == 2 and sys.argv[1] == "todo":
            os.system("cat "+self.dir+"todo.md")
            exit(0)
        self.banner()
        if len(sys.argv) == 1:
            self.list_notes()
        if "-l" in sys.argv :    # list notes
            if len(sys.argv) == 2:
                self.list_notes()
            if len(sys.argv) == 3:
                self.list_notes(sys.argv[2])
        elif "-h" in sys.argv:  # help
            print("n0te")
            print("\t-l: List n0tes")
            print("\t-e name: Execute %s to edit {nom}"%self.editor)
            print("\tname: Display n0te 'name'")
        elif len(sys.argv) == 2:  # display
            self.display_note(sys.argv[1])
        elif len(sys.argv) == 3 and "-e" in sys.argv:  # display
            note = None
            for j in sys.argv:
                if j != "-e" and j != sys.argv[0]:
                    note=j
            self.edit_note(note)
        elif len(sys.argv) == 3 and "-d" in sys.argv:  # display
            note = None
            for j in sys.argv:
                if j != "-d" and j != sys.argv[0]:
                    note=j
            self.delete_note(note)


if __name__ == "__main__":
    n0te()
