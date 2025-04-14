# Given temperature data
temperatures = [12, 15, 18, 20, 22, 25, 28]

# Find min and max values
min_temp = min(temperatures)
max_temp = max(temperatures)

# Apply Min-Max Normalization
normalized_temps = [(temp - min_temp) / (max_temp - min_temp) for temp in temperatures]

# Display the result
print("Original Temperatures:", temperatures)
print("Normalized Temperatures (Range [0, 1]):", normalized_temps)
