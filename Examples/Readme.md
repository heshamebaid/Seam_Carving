
# Seam Carving for Content-Aware Image Resizing

## 🔹 Overview  
This project implements **Seam Carving**, an advanced image resizing technique that removes pixels **intelligently** to reduce the width and height while preserving important content.

### ✅ Supports Three Resizing Cases:
1️⃣ **Reducing both Width & Height**  
2️⃣ **Reducing only Height**  
3️⃣ **Reducing only Width**  

---

## 🖼️ Examples of Seam Carving  

### **1️⃣ Reducing Both Width & Height**
- **Original image is resized**, maintaining key features.
- Visualization shows removed seams in **red**.

📌 **Seams Visualization:**  
![Seams Both](examples/seams_Height&Width.jpg)  

📌 **Final Resized Image:**  
![Resized Both](examples/resized_Height&Width.jpg)  

---

### **2️⃣ Reducing Only Height**
- **Only height is reduced**, width remains unchanged.
- Seam carving removes **horizontal seams**.

📌 **Seams Visualization:**  
![Seams Height](examples/seams_Height.jpg)  

📌 **Final Resized Image:**  
![Resized Height](examples/resized_Height.jpg)  

---

### **3️⃣ Reducing Only Width**
- **Only width is reduced**, height remains unchanged.
- Seam carving removes **vertical seams**.

📌 **Seams Visualization:**  
![Seams Width](examples/seams_width.jpg)  

📌 **Final Resized Image:**  
![Resized Width](examples/resized_Width.jpg)  

---

## 📌 How It Works  
✔️ Computes an **energy map** to detect the least important pixels.  
✔️ Uses **dynamic programming** to find the optimal seam.  
✔️ **Removes seams iteratively** until the target size is reached.  

---

## 🚀 How to Use  

### **1️⃣ Install Dependencies**  
```bash
pip install numpy pillow
