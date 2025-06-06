 Feature: Bubble Sort Algorithm in Retail Application

    Scenario: Verifying the correctness of the Bubble Sort algorithm for an array of integers
      Given a retail application with a implemented Bubble Sort function and helper printArray function
      And an array of integers [64, 34, 25, 12, 22, 11, 90] defined
      When the Bubble Sort algorithm is executed on the given array
      Then the sorted array should be [11, 12, 22, 25, 34, 64, 90]

    Scenario: Validating that the original and sorted arrays are printed correctly
      Given a retail application with a implemented Bubble Sort function and helper printArray function
      And an array of integers [64, 34, 25, 12, 22, 11, 90] defined
      When the original array is printed using the printArray function
      Then "Original array:n64 34 25 12 22 11 90" should be displayed
      When the Bubble Sort algorithm is executed on the given array
      And the sorted array is printed using the printArray function
      Then "Sorted array:n11 12 22 25 34 64 90" should be displayed