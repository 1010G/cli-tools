from subprocess import check_output
from pathlib import Path
import subprocess
import argparse
import sys

class n0te():
    def __init__(self):
        self.editor = "atom"                                        #$$$$$$$$ CHANGE THIS $$$$$$$$
        # Dir to save n0tes
        self.dir = "%s/Documents/notes/" % str(Path.home())         #$$$$$$$$ CHANGE THIS $$$$$$$$ default value is $HOME/Documents/notes/
        self.main()

    def list_notes(self):
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
        [print(w) for w in list_files]          # print notes

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
            os.system("mdv "+self.dir+note)
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
            print("Openning  d'%s" %self.editor)
            print("%s/Documents/note/%s" %(dir,note))

            subprocess.run(["atom", "%s%s" %(self.dir,note)])

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
        if len(sys.argv) == 1:
            self.list_notes()

        if "-l" in sys.argv and len(sys.argv) == 2:    # list notes
            self.list_notes()
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
