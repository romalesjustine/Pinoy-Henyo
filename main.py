import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from game_master import GameMaster

class PinoyHenyoGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("Pinoy Henyo with Genetic Algorithm")

        self.game_master: GameMaster = None
        self.costs = []
        self.last_displayed_guess = None

        self.setup_ui()

    def setup_ui(self):
        paned = tk.PanedWindow(self.master,
                               orient=tk.HORIZONTAL,
                               sashrelief=tk.RAISED)
        paned.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(paned)
        paned.add(left_frame, minsize=400)

        right_frame = tk.Frame(paned)
        paned.add(right_frame, minsize=400)

        input_frame = tk.Frame(left_frame)
        input_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(input_frame,
                 text="Enter word to guess:").pack(side=tk.LEFT)
        self.word_entry = tk.Entry(input_frame)
        self.word_entry.pack(side=tk.LEFT,
                             padx=5,
                             expand=True,
                             fill=tk.X)

        self.start_button = tk.Button(input_frame,
                                      text="Start Game",
                                      command=self.on_start_button)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.confirm_button = tk.Button(left_frame,
                                        text="Confirm Guess is Correct",
                                        state=tk.DISABLED,
                                        command=self.on_confirm_button)
        self.confirm_button.pack(pady=10, padx=10, fill=tk.X)

        table_frame = tk.Frame(left_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("generation", "guess", "cost")
        self.tree = ttk.Treeview(table_frame,
                                 columns=columns,
                                 show="headings",
                                 selectmode="browse")
        self.tree.heading("generation", text="Generation")
        self.tree.heading("guess", text="Guessed Word")
        self.tree.heading("cost", text="Cost")
        self.tree.column("generation", width=80, anchor=tk.CENTER)
        self.tree.column("guess", width=120, anchor=tk.CENTER)
        self.tree.column("cost", width=80, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame,
                                  orient=tk.VERTICAL,
                                  command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.fig.tight_layout(pad=3)
        self.ax.set_title("Convergence Plot (Cost vs. Generations)")
        self.ax.set_xlabel("Generations", labelpad=10)
        self.ax.set_ylabel("Cost", labelpad=10)
        self.line, = self.ax.plot([], [], 'b-')
        self.ax.grid()

        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH,
                                         expand=True,
                                         padx=10,
                                         pady=10)

        status_frame = tk.Frame(left_frame)
        status_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        self.gen_label = tk.Label(status_frame, text="Generation: 0")
        self.gen_label.pack(anchor='w')

        self.best_guess_label = tk.Label(status_frame,
                                         text="Best Guess: N/A")
        self.best_guess_label.pack(anchor='w')

        self.cost_label = tk.Label(status_frame,
                                   text="Best Cost: N/A")
        self.cost_label.pack(anchor='w')

    def on_start_button(self):
        word = self.word_entry.get().strip().lower()
        if not word.isalpha():
            messagebox.showerror("Invalid Input",
                                 "Please enter a valid alphabetic word.")
            return

        self.game_master = GameMaster(
            population_size=20,
            mutation_rate=0.1,
            max_generations=1000
        )

        gen0, best0, cost0, _ = self.game_master.start(word)

        self.tree.delete(*self.tree.get_children())
        self.tree.insert("", tk.END, values=(gen0, best0, cost0))
        self.last_displayed_guess = best0

        self.gen_label.config(text=f"Generation: {gen0}")
        self.best_guess_label.config(text=f"Best Guess: {best0}")
        self.cost_label.config(text=f"Best Cost: {cost0:.2f}")

        self.costs = [cost0]
        self.update_plot()

        self.confirm_button.config(state=tk.NORMAL if cost0 == 0 else tk.DISABLED)

        self.master.after(100, self.ga_step)

    def ga_step(self):
        if self.game_master is None:
            return

        gen, alltime_best, alltime_cost, _ = self.game_master.step()

        population = self.game_master.engine.population
        pairs = [(ind, self.game_master.engine.compute_cost(ind))
                 for ind in population]
        pairs.sort(key=lambda x: (x[1], x[0]))
        gen_best, gen_best_cost = pairs[0]

        if gen_best == self.last_displayed_guess:
            for cand, cost in pairs:
                if cost == gen_best_cost and cand != self.last_displayed_guess:
                    gen_best, gen_best_cost = cand, cost
                    break

        self.tree.insert("", tk.END,
                         values=(gen, gen_best, gen_best_cost))
        self.last_displayed_guess = gen_best

        self.gen_label.config(text=f"Generation: {gen}")
        self.best_guess_label.config(
            text=f"Best Guess: {alltime_best}")
        self.cost_label.config(text=f"Best Cost: {alltime_cost:.2f}")

        self.costs.append(alltime_cost)
        self.update_plot()

        if alltime_cost == 0:
            self.confirm_button.config(state=tk.NORMAL)
            messagebox.showinfo("Success!",
                                f"Exact word guessed: {alltime_best}")
            return

        if gen >= self.game_master.max_generations:
            self.confirm_button.config(state=tk.NORMAL)
            messagebox.showinfo("Stopped",
                                f"Max generations reached. Best guess: {alltime_best}")
            return

        self.master.after(100, self.ga_step)

    def update_plot(self):
        self.line.set_data(range(len(self.costs)), self.costs)
        self.ax.set_xlim(0, max(10, len(self.costs)))
        self.ax.set_ylim(0, max(self.costs) + 1 if self.costs else 1)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.tight_layout(pad=3)
        self.canvas.draw()

    def on_confirm_button(self):
        if self.game_master:
            best_guess, _ = self.game_master.get_best()
            messagebox.showinfo("Game Over",
                                f"The guessed word '{best_guess}' was confirmed correct!")
        self.game_master = None
        self.confirm_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")
    app = PinoyHenyoGUI(root)
    root.mainloop()
