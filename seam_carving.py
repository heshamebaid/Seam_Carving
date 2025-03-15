import numpy as np
from PIL import Image
import os

class SeamCarver:
    def __init__(self, image_path):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Error: File '{image_path}' not found!")
        
        self.image = np.array(Image.open(image_path).convert("RGB"))
        self.original = self.image.copy()
        self.h, self.w = self.image.shape[:2]
        self.coord_grid = np.stack(np.indices((self.h, self.w)), axis=-1)
        self.seams = []

    def compute_energy(self):
        gray = np.dot(self.image[..., :3], [0.299, 0.587, 0.114])
        dx = np.abs(np.pad(gray, ((0, 0), (1, 1)), mode='edge')[:, 2:] - 
                     np.pad(gray, ((0, 0), (1, 1)), mode='edge')[:, :-2])
        dy = np.abs(np.pad(gray, ((1, 1), (0, 0)), mode='edge')[2:] - 
                     np.pad(gray, ((1, 1), (0, 0)), mode='edge')[:-2])
        return dx + dy

    def find_vertical_seam(self, energy):
        h, w = energy.shape
        cum_energy = energy.copy()
        path = np.zeros_like(cum_energy, dtype=int)

        for i in range(1, h):
            for j in range(w):
                left = cum_energy[i-1, j-1] if j > 0 else np.inf
                mid = cum_energy[i-1, j]
                right = cum_energy[i-1, j+1] if j < w-1 else np.inf
                min_energy = min(left, mid, right)
                cum_energy[i, j] += min_energy
                path[i, j] = -1 if min_energy == left else 1 if min_energy == right else 0

        seam = [np.argmin(cum_energy[-1])]
        for i in range(h-2, -1, -1):
            seam.append(seam[-1] + path[i+1, seam[-1]])
        
        return np.array(seam[::-1])

    def remove_seam(self, seam):
        h, w = self.image.shape[:2]
        mask = np.ones((h, w), dtype=bool)
        mask[np.arange(h), seam] = False
        self.image = self.image[mask].reshape((h, w-1, 3))
        self.coord_grid = self.coord_grid[mask].reshape((h, w-1, 2))

    def carve_seams(self, target_width, target_height):
        while self.image.shape[1] > target_width:
            energy = self.compute_energy()
            seam = self.find_vertical_seam(energy)
            self.seams.extend(self.coord_grid[np.arange(self.h), seam].tolist())
            self.remove_seam(seam)

        self.image = self.image.transpose(1, 0, 2)
        self.coord_grid = self.coord_grid.transpose(1, 0, 2)
        
        while self.image.shape[1] > target_height:
            energy = self.compute_energy()
            seam = self.find_vertical_seam(energy)
            seam = np.clip(seam, 0, self.image.shape[1]-1)
            self.seams.extend(self.coord_grid[np.arange(self.image.shape[0]), seam].tolist())
            self.remove_seam(seam)
        
        self.image = self.image.transpose(1, 0, 2)
        
        return self.get_result_images()

    def get_result_images(self):
        vis = self.original.copy()
        for i, j in set(tuple(coord) for coord in self.seams):
            vis[i, j] = [255, 0, 0]
        return Image.fromarray(self.image), Image.fromarray(vis)

if __name__ == "__main__":
    image_path = "D:/test3.png"
    carver = SeamCarver(image_path)
    target_w, target_h = carver.w // 2, carver.h
    resized, vis = carver.carve_seams(target_w, target_h)
    resized.save("resized.jpg")
    vis.save("seams.jpg")
    print(f"Resized from {carver.original.shape[:2]} to {resized.size}")
