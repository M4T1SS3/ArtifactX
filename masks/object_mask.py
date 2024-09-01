import numpy as np

def create_object_mask(image, threshold=0.1):
    """
    Create a mask of the main object in a medical image without using external libraries like ndimage.
    
    Parameters:
    - image: np.ndarray, the input grayscale image normalized to range [0, 1].
    - threshold: float, the threshold value for binarizing the image.
    
    Returns:
    - mask: np.ndarray, the binary mask of the object (same shape as input image).
    """
    # Normalize the image to [0, 1] if not already done
    if np.max(image) > 1:
        image = image / 255.0
    
    # Binarize the image using the threshold
    mask = np.where(image > threshold, 1.0, 0.0)
    
    # Finding connected components using basic NumPy operations
    visited = np.zeros_like(mask)
    labels = np.zeros_like(mask)
    label_count = 1
    
    def flood_fill(x, y, label):
        """ Iteratively label connected components """
        stack = [(x, y)]
        
        while stack:
            cx, cy = stack.pop()
            
            if cx < 0 or cx >= mask.shape[0] or cy < 0 or cy >= mask.shape[1]:
                continue
            if mask[cx, cy] == 0 or visited[cx, cy] == 1:
                continue
            
            visited[cx, cy] = 1
            labels[cx, cy] = label
            
            # Add neighbors to stack (4-connectivity)
            stack.append((cx + 1, cy))
            stack.append((cx - 1, cy))
            stack.append((cx, cy + 1))
            stack.append((cx, cy - 1))
    
    # Label connected components
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if mask[i, j] == 1.0 and visited[i, j] == 0:
                flood_fill(i, j, label_count)
                label_count += 1
    
    # Find the largest connected component
    unique_labels, counts = np.unique(labels, return_counts=True)
    largest_label = unique_labels[np.argmax(counts[1:]) + 1]  # +1 to skip background
    
    # Create the final mask with only the largest connected component
    final_mask = np.where(labels == largest_label, 1.0, 0.0)
    
    return final_mask