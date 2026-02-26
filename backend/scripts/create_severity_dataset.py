"""
Create a severity-labeled dataset from your existing disease dataset
This will include both wheat and rice images
"""
import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
from datetime import datetime

class SeverityLabeler:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.output_path = os.path.join(os.path.dirname(dataset_path), 'severity_dataset')
        self.current_image = None
        self.current_path = None
        self.images_to_label = []
        self.labels = {}
        self.label_counts = {'Low': 0, 'Medium': 0, 'High': 0, 'Very High': 0}
        
        # Create output directories for both crops
        os.makedirs(self.output_path, exist_ok=True)
        for severity in ['Low', 'Medium', 'High', 'Very High']:
            os.makedirs(os.path.join(self.output_path, severity), exist_ok=True)
        
        # Load existing labels if any
        self.labels_file = os.path.join(self.output_path, 'labels.json')
        if os.path.exists(self.labels_file):
            with open(self.labels_file, 'r') as f:
                self.labels = json.load(f)
        
        self.setup_gui()
    
    def load_images_from_both_crops(self):
        """Load images from both wheat and rice folders"""
        images = []
        
        # Wheat path
        wheat_path = os.path.join(self.dataset_path, 'Wheat')
        if os.path.exists(wheat_path):
            for disease in os.listdir(wheat_path):
                disease_path = os.path.join(wheat_path, disease)
                if os.path.isdir(disease_path):
                    for img in os.listdir(disease_path):
                        if img.lower().endswith(('.jpg', '.jpeg', '.png')):
                            full_path = os.path.join(disease_path, img)
                            images.append({
                                'path': full_path,
                                'crop': 'wheat',
                                'disease': disease
                            })
        
        # Rice path
        rice_path = os.path.join(self.dataset_path, 'Rice')
        if os.path.exists(rice_path):
            for disease in os.listdir(rice_path):
                disease_path = os.path.join(rice_path, disease)
                if os.path.isdir(disease_path):
                    for img in os.listdir(disease_path):
                        if img.lower().endswith(('.jpg', '.jpeg', '.png')):
                            full_path = os.path.join(disease_path, img)
                            images.append({
                                'path': full_path,
                                'crop': 'rice',
                                'disease': disease
                            })
        
        return images
    
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("🌾🌱 Crop Disease Severity Labeler (Wheat & Rice)")
        self.root.geometry("1200x700")
        
        # Title
        title = tk.Label(self.root, text="Severity Labeling Tool - Wheat & Rice", 
                        font=('Arial', 16, 'bold'))
        title.pack(pady=10)
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left frame - Image display
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.image_label = tk.Label(left_frame, bg='gray')
        self.image_label.pack(pady=10)
        
        self.image_info = tk.Label(left_frame, text="No image loaded", font=('Arial', 10))
        self.image_info.pack()
        
        # Right frame - Controls
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        
        # Progress
        ttk.Label(right_frame, text="Progress:", font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0,5))
        self.progress_text = tk.StringVar(value="0/0 images labeled")
        ttk.Label(right_frame, textvariable=self.progress_text).pack(anchor='w')
        
        self.progress_bar = ttk.Progressbar(right_frame, length=250, mode='determinate')
        self.progress_bar.pack(pady=5)
        
        # Severity buttons with visual indicators
        ttk.Label(right_frame, text="Select Severity:", font=('Arial', 12, 'bold')).pack(anchor='w', pady=(10,5))
        
        # Low severity
        low_frame = tk.Frame(right_frame, bg='#8BC34A', relief='raised', bd=2)
        low_frame.pack(fill=tk.X, pady=2)
        low_btn = tk.Button(low_frame, text="🌱 Low (0-10% affected)", bg='#8BC34A', fg='black',
                           font=('Arial', 11, 'bold'), height=2,
                           command=lambda: self.label_image('Low'))
        low_btn.pack(fill=tk.X)
        
        # Medium severity
        med_frame = tk.Frame(right_frame, bg='#FFC107', relief='raised', bd=2)
        med_frame.pack(fill=tk.X, pady=2)
        med_btn = tk.Button(med_frame, text="🌿 Medium (10-30% affected)", bg='#FFC107', fg='black',
                           font=('Arial', 11, 'bold'), height=2,
                           command=lambda: self.label_image('Medium'))
        med_btn.pack(fill=tk.X)
        
        # High severity
        high_frame = tk.Frame(right_frame, bg='#FF9800', relief='raised', bd=2)
        high_frame.pack(fill=tk.X, pady=2)
        high_btn = tk.Button(high_frame, text="🔥 High (30-50% affected)", bg='#FF9800', fg='black',
                            font=('Arial', 11, 'bold'), height=2,
                            command=lambda: self.label_image('High'))
        high_btn.pack(fill=tk.X)
        
        # Very High severity
        vhigh_frame = tk.Frame(right_frame, bg='#F44336', relief='raised', bd=2)
        vhigh_frame.pack(fill=tk.X, pady=2)
        vhigh_btn = tk.Button(vhigh_frame, text="⚠️ Very High (>50% affected)", bg='#F44336', fg='white',
                             font=('Arial', 11, 'bold'), height=2,
                             command=lambda: self.label_image('Very High'))
        vhigh_btn.pack(fill=tk.X)
        
        # Skip button
        skip_btn = tk.Button(right_frame, text="⏭️ Skip Image", bg='#9E9E9E', fg='white',
                            font=('Arial', 11, 'bold'), height=2,
                            command=self.skip_image)
        skip_btn.pack(pady=10, fill=tk.X)
        
        # Statistics
        ttk.Label(right_frame, text="Statistics:", font=('Arial', 12, 'bold')).pack(anchor='w', pady=(20,5))
        
        self.stats_text = tk.Text(right_frame, height=8, width=35)
        self.stats_text.pack()
        self.update_stats()
        
        # Navigation buttons
        nav_frame = ttk.Frame(right_frame)
        nav_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(nav_frame, text="📂 Load Next Batch", command=self.load_next_batch).pack(fill=tk.X, pady=2)
        ttk.Button(nav_frame, text="💾 Save & Exit", command=self.save_and_exit).pack(fill=tk.X, pady=2)
        
        # Instructions
        instructions = """
        📝 Instructions:
        ------------------------
        1. Look at the image carefully
        2. Estimate what percentage of the leaf is affected:
        
        🟢 LOW: <10% affected
           - Few small spots
           - Healthy > diseased
        
        🟡 MEDIUM: 10-30% affected
           - Several spots
           - Disease clearly visible
        
        🟠 HIGH: 30-50% affected
           - Large areas diseased
           - More disease than health
        
        🔴 VERY HIGH: >50% affected
           - Most of leaf diseased
           - Severe infection
        
        3. Click the corresponding button
        4. Image will be saved for training
        
        Total images needed: ~400 per severity
        """
        
        ttk.Label(right_frame, text=instructions, justify=tk.LEFT, 
                 wraplength=300, font=('Arial', 9)).pack(pady=10)
        
        # Load first batch
        self.all_images = self.load_images_from_both_crops()
        self.load_next_batch()
        self.root.mainloop()
    
    def load_next_batch(self):
        """Load next batch of unlabeled images"""
        self.images_to_label = []
        
        for img_info in self.all_images:
            if img_info['path'] not in self.labels:
                self.images_to_label.append(img_info)
                if len(self.images_to_label) >= 10:  # Load 10 at a time
                    break
        
        if self.images_to_label:
            self.load_image(self.images_to_label[0])
        else:
            messagebox.showinfo("Complete", "🎉 All images labeled! Great job!")
    
    def load_image(self, img_info):
        """Load and display an image"""
        self.current_image_info = img_info
        self.current_path = img_info['path']
        
        # Load image
        pil_image = Image.open(img_info['path'])
        
        # Resize for display
        pil_image.thumbnail((600, 500))
        
        # Convert to PhotoImage
        self.current_image = ImageTk.PhotoImage(pil_image)
        self.image_label.config(image=self.current_image)
        
        # Update info with crop and disease
        rel_path = os.path.basename(img_info['path'])
        self.image_info.config(
            text=f"📁 Crop: {img_info['crop'].upper()}\n"
                 f"🦠 Disease: {img_info['disease']}\n"
                 f"📄 File: {rel_path}\n"
                 f"📏 Size: {pil_image.size}"
        )
        
        # Update progress
        total = len(self.all_images)
        current = len(self.labels) + 1
        self.progress_text.set(f"Progress: {current}/{total} images")
        self.progress_bar['value'] = (current / total) * 100
    
    def label_image(self, severity):
        """Label current image with severity"""
        if self.current_path:
            # Copy image to severity folder
            filename = os.path.basename(self.current_path)
            dest_path = os.path.join(self.output_path, severity, filename)
            shutil.copy2(self.current_path, dest_path)
            
            # Store label with metadata
            self.labels[self.current_path] = {
                'severity': severity,
                'crop': self.current_image_info['crop'],
                'disease': self.current_image_info['disease'],
                'timestamp': datetime.now().isoformat(),
                'original_path': self.current_path,
                'dest_path': dest_path
            }
            
            self.label_counts[severity] += 1
            self.update_stats()
            
            # Remove from queue and load next
            self.images_to_label.pop(0)
            if self.images_to_label:
                self.load_image(self.images_to_label[0])
            else:
                self.load_next_batch()
    
    def skip_image(self):
        """Skip current image"""
        if self.current_path:
            self.images_to_label.pop(0)
            if self.images_to_label:
                self.load_image(self.images_to_label[0])
            else:
                self.load_next_batch()
    
    def update_stats(self):
        """Update statistics display"""
        self.stats_text.delete(1.0, tk.END)
        total = sum(self.label_counts.values())
        
        self.stats_text.insert(tk.END, "📊 CURRENT STATISTICS:\n")
        self.stats_text.insert(tk.END, "="*30 + "\n")
        
        for severity, count in self.label_counts.items():
            percentage = (count / total * 100) if total > 0 else 0
            bar = "█" * int(percentage/5)
            self.stats_text.insert(tk.END, f"{severity:10}: {count:3d} ({percentage:5.1f}%)\n")
        
        self.stats_text.insert(tk.END, f"\nTotal labeled: {total}")
        
        # Target progress
        self.stats_text.insert(tk.END, "\n\n🎯 TARGET (400 each):\n")
        for severity in ['Low', 'Medium', 'High', 'Very High']:
            count = self.label_counts.get(severity, 0)
            target = 400
            progress = min(100, (count/target)*100)
            bar = "█" * int(progress/5)
            self.stats_text.insert(tk.END, f"{severity:10}: {bar} {progress:.0f}%\n")
    
    def save_and_exit(self):
        """Save labels and exit"""
        with open(self.labels_file, 'w') as f:
            json.dump(self.labels, f, indent=2)
        
        # Summary
        summary = f"""
        ================================
        SAVED: {len(self.labels)} images labeled
        ================================
        Low: {self.label_counts['Low']}
        Medium: {self.label_counts['Medium']}
        High: {self.label_counts['High']}
        Very High: {self.label_counts['Very High']}
        ================================
        """
        
        messagebox.showinfo("Saved", summary)
        self.root.quit()

if __name__ == "__main__":
    dataset_path = r"C:\Users\anshu varma\CropSafe\backend\data\raw\archive (1)\Final_Dataset"
    print("="*60)
    print("🌾🌱 SEVERITY LABELING TOOL FOR WHEAT & RICE")
    print("="*60)
    print("\nThis tool will help you create a severity dataset")
    print("by labeling images from both wheat and rice folders.")
    print("\nTarget: 400 images per severity level (1600 total)")
    print("="*60)
    
    app = SeverityLabeler(dataset_path)