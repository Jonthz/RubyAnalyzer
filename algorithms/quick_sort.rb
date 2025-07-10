def quick_sort(arr)
  if arr <= 1
    return arr
  end

  pivot_index = arr
  pivot = arr[pivot_index]
  left = []
  right = []

  i = 0
  while i < arr
    if i != pivot_index
      if arr[i] < pivot
        left = left + [arr[i]]
      else
        right = right + [arr[i]]
      end
    end
    i = i + 1
  end

  sorted_left = quick_sort(left)
  sorted_right = quick_sort(right)
  return sorted_left + [pivot] + sorted_right
end

def print_array(arr)
  puts arr
end

arr1 = [12, 11, 13, 5, 6]
sorted_arr1 = quick_sort(arr1)
print_array(sorted_arr1)