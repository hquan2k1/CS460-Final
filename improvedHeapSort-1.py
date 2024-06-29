import time
import random
import os
import psutil
import matplotlib.pyplot as plt
import numpy as np

def heapify(arr, n, i):
    # Initialize the largest as the root
    largest = i

    # Left and right children
    l = 2 * i + 1
    r = 2 * i + 2

    # If the left child is larger than the root
    if l < n and arr[i] < arr[l]:
        # Set the left child as the largest
        largest = l

    # If the right child is larger than the root
    if r < n and arr[largest] < arr[r]:
        # Set the right child as the largest
        largest = r

    # If the largest is not the root
    if largest != i:
        # Swap the root with the largest
        arr[i], arr[largest] = arr[largest], arr[i]
        # Recursively heapify the affected sub-tree
        heapify(arr, n, largest)


def heapSort(arr):
    n = len(arr)

    # Build a maxheap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # One by one extract elements
    for i in range(n - 1, 0, -1):
        # Move the current root to the end
        arr[i], arr[0] = arr[0], arr[i]  # Swap
        heapify(arr, i, 0)  # Maintain heap property

def improvedHeapify(arr, n, i):
    # Initialize the largest as the root
    largest = i
    # Left, middle and right children
    l = 3 * i + 1
    m = 3 * i + 2
    r = 3 * i + 3

    # If the left child is larger than the root
    if l < n and arr[i] < arr[l]:
        # Set the left child as the largest
        largest = l

    # If the middle child is larger than the root
    if m < n and arr[largest] < arr[m]:
        # Set the middle child as the largest
        largest = m

    # If the right child is larger than the root
    if r < n and arr[largest] < arr[r]:
        # Set the right child as the largest
        largest = r

    # If the largest is not the root
    if largest != i:
        # Swap the root with the largest
        arr[i], arr[largest] = arr[largest], arr[i]
        improvedHeapify(arr, n, largest)

# Function to check if the array is partly sorted
def isPartlySorted(arr, n):
    # Iterate through the array
    for i in range(1, n):
        # If the current element is less than the previous element
        if arr[i] < arr[i-1]:
            return False
    # If the array is partly sorted
    return True

# Insertion sort function
def insertionSort(arr, left, right):
    # Iterate through the array
    for i in range(left + 1, right + 1):
        # Store the current element
        key = arr[i]
        # Move elements of arr[0..i-1], that are greater than key, 
        # to one position ahead of their current position
        j = i - 1

        # Iterate through the array
        while j >= left and key < arr[j]:
            # Move the elements
            arr[j + 1] = arr[j]
            # Decrement the index
            j -= 1
        # Insert the element
        arr[j + 1] = key

def improvedHeapSort(arr):
    n = len(arr)
    # Start from the last non-leaf node and move upwards to the root
    for i in range(n // 3 - 1, -1, -1):
        improvedHeapify(arr, n, i)

    # One by one extract elements
    for i in range(n - 1, 0, -1):
        # Move the current root to the end
        arr[i], arr[0] = arr[0], arr[i]  # Swap
        improvedHeapify(arr, i, 0)  # Maintain heap property

    # Check if the array is partly sorted
    if not isPartlySorted(arr, n):
        insertionSort(arr, 0, n - 1)

# Initialize lists for data collection
times_heap_sort = []
memory_heap_sort = []
times_improved_heap_sort = []
memory_improved_heap_sort = []

# Collect data for time and memory usage
def test(arr):
    process = psutil.Process(os.getpid())
    start = time.time()
    heapSort(arr)
    end = time.time()
    times_heap_sort.append(end - start)
    memory_heap_sort.append(process.memory_info().rss / 1024 ** 2)

    process2 = psutil.Process(os.getpid())
    start = time.time()
    improvedHeapSort(arr)
    end = time.time()
    times_improved_heap_sort.append(end - start)
    memory_improved_heap_sort.append(process2.memory_info().rss / 1024 ** 2)

# Generate random array
arr = [random.randint(0, 1000000) for i in range(1000000)]

# Run test function 10 times
for i in range(5):
    test(arr)

# Calculate averages
avg_time_heap_sort = np.mean(times_heap_sort)
avg_memory_heap_sort = np.mean(memory_heap_sort)
avg_time_improved_heap_sort = np.mean(times_improved_heap_sort)
avg_memory_improved_heap_sort = np.mean(memory_improved_heap_sort)

# Indices of the groups, starting from 1
ind = np.arange(1, len(times_heap_sort) + 1)  # the x locations for the groups, starting at 1
width = 0.35  # the width of the bars

plt.figure(figsize=(12, 6))

# Plotting run time comparison with time taken in the middle - Switch to horizontal bar chart
plt.subplot(1, 2, 1)
middle_positions = ind  # For horizontal bars, positions are straightforward
bar1 = plt.barh(middle_positions - width, times_heap_sort, height=width, label='Heap Sort', color='tab:blue')
bar2 = plt.barh(middle_positions, times_improved_heap_sort, height=width, label='Improved Heap Sort', color='tab:orange')

# Adding text inside bars
for i, (time_hs, time_ihs) in enumerate(zip(times_heap_sort, times_improved_heap_sort)):
    plt.text(time_hs / 2, i + 1 - width, f'{time_hs:.2f}', ha='center', va='center', color='white')
    plt.text(time_ihs / 2, i + 1, f'{time_ihs:.2f}', ha='center', va='center', color='white')

plt.xlabel('Time Taken (seconds)')
plt.title('Run Time Comparison')
plt.yticks(ind)  # Adjust yticks for horizontal bars
plt.legend()

# Plotting memory usage comparison remains unchanged
plt.subplot(1, 2, 2)
bar3 = plt.bar(ind - width/2, memory_heap_sort, width, label='Heap Sort', color='tab:blue')
bar4 = plt.bar(ind + width/2, memory_improved_heap_sort, width, label='Improved Heap Sort', color='tab:orange')

plt.ylabel('Memory Used (MB)')
plt.title('Memory Usage Comparison')
plt.xticks(ind)  # Adjust xticks to align with the middle of grouped bars
plt.legend()

plt.tight_layout()
plt.show()

# Display averages
print(f"Average time for normal heap sort: {np.mean(times_heap_sort)} seconds")
print(f"Average memory for normal heap sort: {np.mean(memory_heap_sort)} MB")
print(f"Average time for improved heap sort: {np.mean(times_improved_heap_sort)} seconds")
print(f"Average memory for improved heap sort: {np.mean(memory_improved_heap_sort)} MB")
