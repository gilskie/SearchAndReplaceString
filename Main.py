import SearchAndTagString
import configparser
import sys
import tkinter
import tkinter.ttk
from tkinter import filedialog
from tkinter import messagebox
import ntpath
import os
import re


def main():
    try:
        config = configparser.ConfigParser()
        configuration_file = sys.path[0] + '\configurationFile.ini'
        # print(f"Configuration location: {configuration_file}")

        config.read(configuration_file)

        default_setting = config["Default"]
        input_location = default_setting["input_location"]
        output_location = default_setting["output_location"]
        table_file = default_setting["table_file"]
        table_file_drop_down = default_setting["table_file_drop_down"]
        # breakpoint()

        # populate_table_to_class(table_file)
        generate_view(table_file, table_file_drop_down, input_location, output_location)

    except Exception as e:
        print(f"Error occurred: {e}")


# generate view for the tool
def generate_view(table_file, table_file_drop_down, input_location, output_location):
    window = tkinter.Tk()
    window.title("Welcome to final project!")
    window.geometry("450x200")

    # for first field which is browsing file that is to be processed!
    lbl_select_file = tkinter.Label(window, text = "Select a file:")
    lbl_select_file.grid(column = 0, row = 0, sticky=tkinter.W)

    label_file_display = tkinter.Label(window, width=35)
    label_file_display.grid(column=1, row=0, sticky=tkinter.W)

    def browse_file():
        file_name_location = filedialog.askopenfilename(initialdir=input_location,
                                                        title="Select file",
                                                        filetypes=(("Text files", "*.txt"),
                                                                   ("all files", "*.*")))
        # entry_file.configure(text=file_name_location)
        msg_box_search_and_replace = messagebox.askokcancel("User selection:", "Use the search and replace(Note: "
                                                                               "cancel will use the drop down module)?")

        if msg_box_search_and_replace and len(file_name_location) > 0:
            # proceed with condition(search and replace) below if user decides to press okay button from above
            # else it will inform user to select tag from drop down and text o be applied with.
            # print(f"Proceed with search and replace! {table_file}")
            # file_name_location => will hold the complete location of the filename!
            # table_file => will hold the complete location of the table search and replace file which will be

            # used to the file_name_location.
            file_input = open(file_name_location, "rt")
            # print(f"output location: {output_location}\{ntpath.basename(file_name_location)}")

            if os.path.isfile(output_location + "\\" + ntpath.basename(file_name_location)):
                # print(f"File already exists!")
                # delete file if it already exists on the output.
                os.unlink(output_location + "\\" + ntpath.basename(file_name_location))

            file_output = open(output_location + "\\" + ntpath.basename(file_name_location), "wt")
            complete_table_list = populate_table_to_class(table_file)

            # read per line!
            for line in file_input:
                flag_has_match = False
                # iterate on the list if there are flag text of which tag is to be applied with!
                for list_item in complete_table_list:
                    if line.__contains__(list_item.search_text):
                        # print(f"Found line:{line}, {list_items.search_text}")
                        # start inserting tag from text with opening and closing tag!
                        file_output.write(perform_auto_tag(line,
                                                           list_item.search_text,
                                                           list_item.tag_string_opening))
                        flag_has_match = True
                # means that there is no match found on the line of which insertion of tag is to be applied with!
                if flag_has_match is False:
                    file_output.write(line)
                    print("Not found!")

            file_input.close()
            file_output.close()
            messagebox.showinfo(title="Information:", message="Done generating the output for search and replace.")
        else:
            label_file_display.configure(text=file_name_location)
            combo.focus()

    btn_browse = tkinter.Button(window,
                                text="Browse file",
                                fg="blue",
                                command=browse_file)
    btn_browse.grid(column = 2, row = 0, sticky=tkinter.W)

    # for second field which is selecting the tags that is to be processed!
    lbl_tag = tkinter.Label(window, text="Select a tag:")
    lbl_tag.grid(column=0, row=1, sticky=tkinter.W)

    combo = tkinter.ttk.Combobox(window, state="readonly")
    combo["values"] = populate_drop_down(table_file_drop_down)

    combo.current(1)
    combo.grid(column = 1, row = 1, sticky=tkinter.W)

    # for third field which is entering a text that is to be searched then tagged with based on the drop down value!
    lbl_enter_text = tkinter.Label(window, text="Enter a text")
    lbl_enter_text.grid(column=0, row=2, sticky=tkinter.W)

    entry_text = tkinter.Entry(window, width = 35, state="normal")
    entry_text.grid(column=1, row=2, sticky=tkinter.W)

    check_box_space_required_variable = tkinter.BooleanVar()
    check_box_space_required = tkinter.Checkbutton(window, text="Require Space?",
                                                   variable=check_box_space_required_variable)
    check_box_space_required.grid(column=2, row=2, sticky=tkinter.W)

    # for fourth field output path and button for new output location!
    lbl_output_path = tkinter.Label(window, text= "Output path")
    lbl_output_path.grid(column=0, row=3, sticky=tkinter.W)

    label_output_path_display = tkinter.Label(window, text=output_location, width=35)
    label_output_path_display.grid(column=1, row=3, sticky=tkinter.W)

    def locate_output_path():
        new_output_file_location = filedialog.askdirectory(initialdir= output_location,
                                                           title="Select new output location:")
        label_output_path_display.configure(text=new_output_file_location)

    button_locate_output_path = tkinter.Button(window,
                                               text="Browse output path",
                                               fg="blue",
                                               command=locate_output_path)
    button_locate_output_path.grid(column=2, row=3, sticky=tkinter.W)

    # fifth field which contains all of the buttons process and validate.
    def process_file():
        # combo.get() => combo text value!
        # file_name_location => complete location of the filename that is to be processed with!
        combo_value = str(combo.get()).replace("\n", "")
        file_location = label_file_display['text']
        text_entry_value = entry_text.get()
        insert_space_before_and_after = ""

        if len(label_output_path_display["text"]) > 0:
            new_output_location = label_output_path_display["text"]

        if len(file_location) > 0 and len(text_entry_value) > 0:
            # print(f"Combo value: {combo_value}, {file_location},
            # {text_entry_value},
            # {output_location + '|' + ntpath.basename(file_location)}")
            file_input = open(file_location, "rt")

            if os.path.isfile(output_location + "\\" + ntpath.basename(file_location)) and len(output_location) > 0:
                os.unlink(output_location + "\\" + ntpath.basename(file_location))
            else:
                os.unlink(new_output_location + "\\" + ntpath.basename(file_location))

            if len(new_output_location) > 0:
                file_output = open(new_output_location + "\\" + ntpath.basename(file_location), "wt")
            else:
                file_output = open(output_location + "\\" + ntpath.basename(file_location), "wt")

            if check_box_space_required_variable.get() is True:
                insert_space_before_and_after = " "

            for line in file_input:
                flag = False
                if line.__contains__(text_entry_value):
                    file_output.write(perform_auto_tag(line, insert_space_before_and_after + text_entry_value + insert_space_before_and_after, combo_value))
                    flag = True
                if flag is False:
                    file_output.write(line)
                    # print("Not found!")

            file_input.close()
            file_output.close()
            messagebox.showinfo(title="Information:", message="Done generating the output for drop down replace.")
        else:
            messagebox.showinfo(title="Information", message="Please check if input file is selected "
                                                             "or text is provided!")

    btn_process = tkinter.Button(window,
                                 text = "Process",
                                 fg="green",
                                 command=process_file)
    btn_process.grid(column=0, row=4, sticky=tkinter.W)

    # Requirement from Renz!
    def validate_file():
        print(f"Validating file!")

    btn_validate = tkinter.Button(window,
                                  text="Validate",
                                  fg="orange",
                                  command=validate_file)
    btn_validate.grid(column=1, row=4, sticky=tkinter.W)

    # note: must be last always!
    window.mainloop()


def populate_drop_down(table_drop_down_location):
    if len(table_drop_down_location) > 0:
        f = open(table_drop_down_location, "r")
        lines = f.readlines()

        my_drop_down_string = []
        for line in lines:
            my_drop_down_string.append(line)
            # print(f"{line}")
        return my_drop_down_string
    else:
        return 0


def populate_table_to_class(table_file_location):
    # print(f"{len(table_file_location)} , {len(table_drop_down_location)}")
    if len(table_file_location) > 0:
        f = open(table_file_location,"r")
        lines = f.readlines()
        my_search_and_tag_string = []

        for line in lines:
            # print(f"Lines: {line}")
            line = line.replace("\n","")
            tag_string = line.split('|||')
            my_search_and_tag_string.append(SearchAndTagString.SearchAndTagString(tag_string[0],
                                                                                  tag_string[1],
                                                                                  tag_string[2]))
        # breakpoint()
        f.close()

        # for tag in my_search_and_tag_string:
        #     print(f"{tag.search_text}, {tag.tag_string}")
        return my_search_and_tag_string

    else:
        return 0


def perform_auto_tag(file_content, text_to_find, expected_tag):
    complete_tag = str(expected_tag) + str(text_to_find) + str(expected_tag.replace("<","</"))
    file_content = re.sub("([^>]+)" + text_to_find + "([^<]+)", r"\1" + complete_tag + r"\2", file_content)
    return file_content


main()
