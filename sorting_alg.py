def quicksort(array,start,end):
    """quicksort is a recursive function to put things in the right position relative
       to a pivot point"""
    if start < end:
        part_index = partition(array,start,end)
        quicksort(array,start,part_index - 1)  # for the sub array before the partition index
        quicksort(array,part_index + 1,end)  # here we make the sub array starting at one more than the partition index

def partition(array,start,end):
    pivot = array[end][0]  # in this form of quicksort i am choosing the pivot to be at the end of the array
    i = start - 1

    for j in range(start,end):  # not sure if this needs to be until end rather than end - 1
        if array[j][0] < pivot:
            i += 1
            array[i], array[j] = array[j], array[i]

    array[i + 1], array[end] = array[end], array[i + 1]  # placing the pivot point at the right point in the list
    return(i + 1)

""" psudocode for quicksort algorithm.

partition (arr[], low, high)
    #pivot (Element to be placed at right position)
    pivot = arr[high];

    i = (low - 1)  # Index of smaller element

    for (j = low; j <= high- 1; j+=1)

        #If current element is smaller than the pivot
        if (arr[j] < pivot)
            i=+1   # increment index of smaller element
            swap arr[i] and arr[j]
  
    swap arr[i + 1] and arr[high])
    return (i + 1)


#low  --> Starting index,  high  --> Ending index
quickSort(arr[], low, high)
    if (low < high)
    
        #pi is partitioning index, arr[pi] is now at right place
        pi = partition(arr, low, high);

        quickSort(arr, low, pi - 1);  // Before pi
        quickSort(arr, pi + 1, high); // After pi
"""
