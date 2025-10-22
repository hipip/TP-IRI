import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from SearchEngine import search_images

class ImageSearchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Search Engine")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Create main frame
        self.main_frame = tk.Frame(root, bg='#f0f0f0')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Search section
        self.create_search_section()
        
        # Results section
        self.create_results_section()
        
    def create_search_section(self):
        """Create the search input and button section"""
        search_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        search_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = tk.Label(search_frame, text="Image Search Engine", 
                              font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#333')
        title_label.pack(pady=(0, 20))
        
        # Search input frame
        input_frame = tk.Frame(search_frame, bg='#f0f0f0')
        input_frame.pack(fill=tk.X)
        
        # Search input
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(input_frame, textvariable=self.search_var, 
                                   font=('Arial', 14), width=50, relief=tk.SOLID, bd=1)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry.bind('<Return>', lambda e: self.search_images())
        
        # Search button
        self.search_button = tk.Button(input_frame, text="Search", 
                                     command=self.search_images,
                                     font=('Arial', 14, 'bold'),
                                     bg='#4CAF50', fg='white',
                                     relief=tk.FLAT, padx=20, pady=5)
        self.search_button.pack(side=tk.LEFT)
        
        # Instructions
        instructions = tk.Label(search_frame, 
                              text="Enter keywords separated by spaces (AND) or use + for OR search\nExample: 'laptop' or 'laptop+moto'",
                              font=('Arial', 10), bg='#f0f0f0', fg='#666')
        instructions.pack(pady=(10, 0))
        
    def create_results_section(self):
        """Create the results display section"""
        results_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Results label
        self.results_label = tk.Label(results_frame, text="Search Results", 
                                    font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#333')
        self.results_label.pack(pady=(0, 10))
        
        # Create scrollable frame for images
        canvas = tk.Canvas(results_frame, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def search_images(self):
        """Perform image search and display results"""
        query = self.search_var.get().strip()
        
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query")
            return
            
        try:
            # Clear previous results
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
                
            # Perform search
            results = search_images(query)
            
            if not results:
                no_results_label = tk.Label(self.scrollable_frame, 
                                          text="No images found for your search query.",
                                          font=('Arial', 14), bg='#f0f0f0', fg='#666')
                no_results_label.pack(pady=50)
                return
                
            # Update results label
            self.results_label.config(text=f"Search Results ({len(results)} images found)")
            
            # Display images in a grid
            self.display_images(results)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def display_images(self, image_files):
        """Display images in a grid layout"""
        images_per_row = 3
        row = 0
        col = 0
        
        for image_file in image_files:
            try:
                # Create frame for each image
                img_frame = tk.Frame(self.scrollable_frame, bg='white', relief=tk.RAISED, bd=2)
                img_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
                
                # Load and resize image
                image_path = os.path.join('images', image_file)
                if os.path.exists(image_path):
                    # Load image
                    pil_image = Image.open(image_path)
                    
                    # Resize image to fit in frame (max 200x200)
                    pil_image.thumbnail((200, 200), Image.Resampling.LANCZOS)
                    
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(pil_image)
                    
                    # Create image label
                    img_label = tk.Label(img_frame, image=photo, bg='white')
                    img_label.image = photo  # Keep a reference
                    img_label.pack(pady=5)
                    
                    # Create filename label
                    filename_label = tk.Label(img_frame, text=image_file, 
                                           font=('Arial', 10), bg='white', fg='#333')
                    filename_label.pack(pady=(0, 5))
                    
                else:
                    # Image file not found
                    error_label = tk.Label(img_frame, text=f"File not found:\n{image_file}", 
                                         font=('Arial', 10), bg='white', fg='red')
                    error_label.pack(pady=20)
                    
                # Update grid position
                col += 1
                if col >= images_per_row:
                    col = 0
                    row += 1
                    
            except Exception as e:
                # Handle image loading errors
                error_frame = tk.Frame(self.scrollable_frame, bg='white', relief=tk.RAISED, bd=2)
                error_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
                
                error_label = tk.Label(error_frame, text=f"Error loading:\n{image_file}\n{str(e)}", 
                                     font=('Arial', 10), bg='white', fg='red')
                error_label.pack(pady=20)
                
                col += 1
                if col >= images_per_row:
                    col = 0
                    row += 1
        
        # Configure grid weights
        for i in range(images_per_row):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)

def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = ImageSearchGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
