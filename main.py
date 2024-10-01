from os import path
import tkinter as t
from tkinter import messagebox as msgb
import random, json
import pyperclip as pc

W_EMAIL_ADDRESS = "USERNAME"

w_curr_dir  = path.dirname(__file__)
w_logo_file = f"{w_curr_dir}/images/logo.png"
w_pass_file_txt  = f"{w_curr_dir}/data/data.txt"
w_pass_file_json = f"{w_curr_dir}/data/data.json"

def generate_password() -> str:
    W_PASS_NR_LETTERS = random.randint(8, 10)
    W_PASS_NR_NUMBERS = random.randint(2, 4)
    W_PASS_NR_SYMBOLS = random.randint(2, 4)
    
    w_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    w_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    w_symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    
    w_pass_letters = [random.choice(w_letters) for _ in range(W_PASS_NR_LETTERS)]
    w_pass_numbers = [random.choice(w_numbers) for _ in range(W_PASS_NR_NUMBERS) ]    
    w_pass_symbols = [random.choice(w_symbols) for _ in range(W_PASS_NR_SYMBOLS) ]        
    
    w_new_password_list = w_pass_letters + w_pass_numbers + w_pass_symbols
    # print(w_new_password_list)    
    random.shuffle(w_new_password_list)
    # print(w_new_password_list)        
    
    w_new_password = "".join(w_new_password_list) #This join items in the list without the need for the the for loop below
    # w_new_password = ""
    # for char in w_new_password_list:
    #     w_new_password += char

    # print(w_new_password)                     
    
    return w_new_password
    

def main() -> None:
    
    w_my_window = t.Tk()
    w_my_window.title("Password Manager")    
    w_my_window.configure(padx=50, pady=50)    
    
    
    # def popupmsg(msg):
    #     popup = t.Tk()
    #     popup.wm_title("!")
    #     label = t.Label(popup, text=msg)
    #     label.pack(side="top", fill="x", pady=10)
    #     B1 = t.Button(popup, text="Okay", command = popup.destroy)
    #     B1.pack()
    #     popup.mainloop()
        
    # ---------------------------- PASSWORD GENERATOR ------------------------------- #
    def populate_password_field(p_password: str) -> None:
        # print(p_password)
        w_pass_entry.delete(0,t.END)
        w_pass_entry.insert(0, p_password)
        pc.copy(p_password)        
        
    def set_password() -> None:
        # raise NotImplementedError("'generate_password' is not impleted yet!!")    
        w_new_password = generate_password()
        populate_password_field(w_new_password)
        

    def get_passwords_data() -> json:
        try:
            with open(file=w_pass_file_json, mode="r") as f:                             
                w_data = json.load(f)                
        except Exception as e:
            # print(f"Fail to load data, should be new entry {e}")                
            return None                
        return w_data    

    def search_password_data() -> None:
        w_site_info: str = w_site_entry.get().title()

        if len(w_site_info) == 0 :
            msgb.showinfo(title="Oops!", message="Please make sure you haven't left any of the fields empty!!")        
            return
                
        w_data: json = get_passwords_data()
        # print(w_data)
        if w_data == None:
            msgb.showinfo(title="Oops!", message="Nothing found.. Sorry!!")        
        else:
            if w_site_info in w_data:
                w_username    = w_data[w_site_info]["username"]        
                w_password = w_data[w_site_info]["password"]        
                msgb.showinfo(title=w_site_info, message=f"Email/Username: {w_username}\nPassword: {w_password}")
                # populate_password_field(w_password)
            else:
                msgb.showinfo(title="Oops!", message="No search results found.. Sorry!!")
                
        
        
    # ---------------------------- SAVE PASSWORD ------------------------------- #    
    def save_password() -> None:
        w_site_info: str = w_site_entry.get().title()
        w_username: str  = w_username_entry.get()
        w_pass_info: str = w_pass_entry.get()

        if len(w_site_info) == 0 or len(w_username) == 0:
            msgb.showinfo(title="Oops!", message="Please make sure you haven't left any of the fields empty!!")        
            return
            
        w_choice = msgb.askokcancel(title=w_site_info, message=f"These are the details you entered: \nEmail: {w_username} "
                                                    f"\nPassword: {w_pass_info}\nIs it okay to save? ")
        # print(w_choice)
        if w_choice: 
            w_new_data: json = {
                w_site_info: {                    
                    "password":w_pass_info,
                    "username":w_username                  
                }
            }
        
            try:
                w_data: json = get_passwords_data()                    
                if w_data == None:
                    w_data = w_new_data
                else:
                    w_data.update(w_new_data)                    
            except Exception as e:
                # print(f"Fail to load data, should be new entry {e}")                
                w_data = w_new_data
                
            
            try:                                                  
                with open(file=w_pass_file_json, mode="w") as f:                                     
                    json.dump(w_data, f, indent=4, sort_keys=True)                    
            except Exception as e:
                print(f"Fail to dump new data {e}")                
                json.dump(w_new_data, f, indent=4, sort_keys=True)
                        
                
                
            # with open(file=w_pass_file_txt, mode="a") as f: 
            #     if path.getsize(w_pass_file_txt) > 0:
            #         f.write("\n")                            
            #     f.write(f"{w_site_info} | {w_username} | {w_pass_info}")
            w_site_entry.delete(0, t.END)
            w_pass_entry.delete(0, t.END)
        # else:
        #     msgb.showinfo(title="!", message="Nothing saved.")    
        # popupmsg("Done saving") 
        
            
    # ---------------------------- UI SETUP ------------------------------- #

    w_canvas = t.Canvas(w_my_window, width=200, height=200)
    w_logo_img = t.PhotoImage(file=w_logo_file)
    w_canvas.create_image(100, 100, image=w_logo_img)
    w_canvas.grid(row=0, column=1)    
    
    w_site_label     = t.Label(text="Website:")
    w_site_label.grid(row=1, column=0)            
    w_site_entry     = t.Entry(width=35)
    w_site_entry.focus()    
    w_site_entry.grid(row=1, column=1, sticky="W")    
    
    w_search_button = t.Button(text="Search", fg="blue", width=12, command=search_password_data)
    w_search_button.grid(row=1, column=2, sticky="E")
    
    w_username_label = t.Label(text="Email/Username:")
    w_username_label.grid(row=2, column=0)        
    w_username_entry = t.Entry(width=55)
    # w_username_entry.insert(0, W_EMAIL_ADDRESS)        
    w_username_entry.grid(row=2, column=1, columnspan=2, sticky="W")
    
    w_pass_label     = t.Label(text="Password:")
    w_pass_label.grid(row=3, column=0)       
    w_pass_entry       = t.Entry(width=30)        
    w_pass_entry.grid(row=3, column=1, sticky="W")    
            
    w_gen_button     = t.Button(text="Generate Password", command=set_password)
    w_gen_button.grid(row=3, column=2, sticky="E")
    
    w_add_button     = t.Button(text="Add", width=52, command=save_password)    
    w_add_button.grid(row=4, column=1, columnspan=2, sticky="E")    
    
    
    
    w_my_window.mainloop() #keep window open

if __name__ == "__main__":    
    main()
    
