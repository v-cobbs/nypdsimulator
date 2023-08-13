

from tkinter import Tk, Label, Button, StringVar, IntVar, Entry, messagebox, Toplevel
from PIL import Image, ImageTk

class CustomDialog(Toplevel):
    def __init__(self, parent, message, image_path):
        Toplevel.__init__(self, parent)
        self.title("Final Report")
        Label(self, text=message).pack()
        raw_image = Image.open(image_path)
        img_width, img_height = 200, 200  # Specify desired width and height here
        resized_image = raw_image.resize((img_width, img_height))
        image = ImageTk.PhotoImage(resized_image)
    
        img_label = Label(self, image=image)
        img_label.image = image  # Keep a reference to prevent GC from discarding the image.
        img_label.pack()
        Button(self, text="OK", command=self.destroy).pack()

class BudgetApp:
    images = {}

    def __init__(self, master):
        self.master = master
        self.master.title("Budget Simulator")

        img_width_budget, img_height_budget = 100, 100
        img_width, img_height = 100, 100

        self.images['NYPD spending on facial recognition technology (Idemia Solutions contracts)'] = ImageTk.PhotoImage(Image.open('facial_recognitionpng.png').resize((img_width_budget, img_height_budget)))
        self.images['Estimated total NYPD spending on surveillance'] = ImageTk.PhotoImage(Image.open('nypd_surveillance.png').resize((img_width_budget, img_height_budget)))
        self.images['Asylum court fees'] = ImageTk.PhotoImage(Image.open('asylum_court.png').resize((img_width, img_height)))
        self.images['NYC public transportation costs for 1 year'] = ImageTk.PhotoImage(Image.open('subway.png').resize((img_width, img_height)))
        self.images['Bacon egg and cheese'] = ImageTk.PhotoImage(Image.open('baconeggandcheese.png').resize((img_width, img_height)))
        self.images['Avg 3 bedroom apartment rent in the Bronx'] = ImageTk.PhotoImage(Image.open('bronx.png').resize((img_width, img_height)))

        self.budgets = {
            'NYPD spending on facial recognition technology (Idemia Solutions contracts)': 16594258.0,
            'Estimated total NYPD spending on surveillance': 3000000000,
        }

        self.options = {
            'Asylum court fees': 4000,
            'NYC public transportation costs for 1 year': 1716,
            'Bacon egg and cheese' : 3.50,
            'Avg 3 bedroom apartment rent in the Bronx': 3000,
        }

        self.chosen_budget = StringVar()
        self.expenditures = {option: IntVar(value=0) for option in self.options}
        self.remaining_budget = StringVar(value="First, select a budget.\n Then, type in a number and click the corresponding image")
        self.entries = {}
        self.budget_buttons = {}
        self.spend_buttons = {}

        self.init_ui()

    def init_ui(self):
        Label(self.master, text="Select a budget:").grid(row=0, column=0)
        for i, budget in enumerate(self.budgets, start=1):
            img = self.images[budget]
            self.budget_buttons[budget] = Button(self.master, image=img, text=f"{budget}: {self.budgets[budget]}", compound='bottom', command=lambda b=budget: self.select_budget(b))
            self.budget_buttons[budget].image = img
            self.budget_buttons[budget].grid(row=i, column=0, sticky='w')

        Label(self.master, text="Spend budget on").grid(row=0, column=1)
        for i, option in enumerate(self.options, start=1):
            img = self.images[option]
            self.entries[option] = Entry(self.master)
            self.entries[option].grid(row=i, column=1, sticky='w')
            self.spend_buttons[option] = Button(self.master, image=img, text=f"{option}: {self.options[option]}", compound='bottom', command=lambda o=option: self.spend_money(o))
            self.spend_buttons[option].image = img
            self.spend_buttons[option].grid(row=i, column=2, sticky='w')

        Label(self.master, text="Helpful hints: There have been over 90,000 asylum seekers arriving in NYC this past year \n  There are 68,884 unhoused people" + 
            f"including 21,805 children in the NYC municipal shelter system \n"  +
            f"There are 1.2 million food insecure NYC residents \n  Depending on your budget, you may not be able to help everyone, but see how far you get").grid(row=0, column=0, columnspan =2, sticky='ew')
        Label(self.master, textvariable=self.remaining_budget).grid(row=1, column=3)
        Button(self.master, text="I'm done", command=self.done).grid(row=len(self.options)+1, column=2, sticky='w')
        
    def disable_budget_buttons(self):
            for button in self.budget_buttons.values():
                button['state'] = 'disabled'
                
    def select_budget(self, budget):
        self.chosen_budget.set(budget)
        self.remaining_budget.set(f"Remaining budget: {self.budgets[budget]}")
        self.disable_budget_buttons()

    def spend_money(self, option):
        try:
            times = int(self.entries[option].get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a number")
            return
        total_cost = times * self.options[option]
        if total_cost > self.budgets[self.chosen_budget.get()]:
            messagebox.showerror("Error", "Not enough budget remaining")
        else:
            self.budgets[self.chosen_budget.get()] -= total_cost
            self.remaining_budget.set(f"Remaining budget: {self.budgets[self.chosen_budget.get()]}")
            self.expenditures[option].set(self.expenditures[option].get() + times)
            self.entries[option].delete(0, 'end')

    def done(self):
        message = self.construct_report_message()
        image_path = 'facial_recognitionpng.png'  
        CustomDialog(self.master, message, image_path)

    def construct_report_message(self):
        total_spent = sum(self.options[option]*times.get() for option, times in self.expenditures.items())
        total_items = sum(times.get() for times in self.expenditures.values())
        asylum_seekers_helped = self.expenditures['Asylum court fees'].get() 
        transport_paid = self.expenditures['NYC public transportation costs for 1 year'].get()
        meals_provided = self.expenditures['Bacon egg and cheese'].get()
        rent_paid = self.expenditures['Avg 3 bedroom apartment rent in the Bronx'].get()
        
        message = (
            f"Great job, and thanks for trying out the NYPD Budget Simulator!\n"
            f"Your Budget was {self.chosen_budget.get()}\n"
            f"You spent a total of ${total_spent} "
            f"with ${self.budgets[self.chosen_budget.get()]} left over \n"
            f"In total, you used the budget money {total_items} times \n"
            f"You helped {asylum_seekers_helped} people seek asylum \n" +
            f"Paid for {transport_paid} New Yorkers to use public transportation for a full year \n" + 
            f"Covered monthly rent for {rent_paid} families \n" +
            f"And last but not least bought {meals_provided} bacon egg and cheeses (I hope you share!)"
        )
        return message

if __name__ == "__main__":
    root = Tk()
    budget_app = BudgetApp(root)
    root.mainloop()

