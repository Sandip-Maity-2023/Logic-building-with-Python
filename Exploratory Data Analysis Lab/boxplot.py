import matplotlib.pyplot as plt

# Given data
data = [0, 0, 2, 5, 8, 8, 8, 9, 9, 10, 10, 10, 11, 12, 12, 12, 14, 15, 20, 25]

# Create the plot
plt.figure(figsize=(10, 3))

# Draw the boxplot
plt.boxplot(data, vert=False, patch_artist=True, #patch_artist=True makes the boxplot filled with color
            boxprops=dict(facecolor='skyblue', color='blue'), #boxprops sets the color of the box
            flierprops=dict(marker='o', markerfacecolor='red', markersize=8, linestyle='none'),
            medianprops=dict(color='darkblue'),
            whiskerprops=dict(color='black'), ##whiskerprops sets the color of the whiskers
            capprops=dict(color='black')) #capprops sets the color of the caps

# Add labels and title
plt.title('Box Plot of Textbook Ownership')
plt.xlabel('Number of Textbooks')
plt.grid(True, axis='x', linestyle='--', alpha=0.6)

# Show the plot
plt.show()
