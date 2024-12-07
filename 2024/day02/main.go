package main

import (
	"flag"
	"fmt"
	"slices"
	"strconv"
	"strings"

	"utils"
)

var inputFile = flag.String("input", "", "Input text file")

func isSafe(values []int) bool {
	var (
		isAscending *bool
		previous    int
		diff        int
	)
	for i, v := range values {
		current := v
		if i != 0 {
			if isAscending == nil {
				isAscending = new(bool)
				if current > previous {
					*isAscending = true
				} else if current < previous {
					*isAscending = false
				} else {
					return false
				}
			}

			if current > previous {
				if !*isAscending {
					return false
				}
				diff = current - previous
			} else {
				if *isAscending {
					return false
				}
				diff = previous - current
			}

			if !(diff >= 1 && diff <= 3) {
				return false
			}
		}
		previous = v
	}

	return true
}

func getValuesFromReport(report string) []int {
	values := []int{}
	for _, s := range strings.Split(report, " ") {
		n, _ := strconv.Atoi(s)
		values = append(values, n)
	}
	return values
}

func getValueIterations(values []int) [][]int {
	iterations := [][]int{values}
	for i := 0; i < len(values); i++ {
		tmpValues := make([]int, len(values))
		copy(tmpValues, values)
		truncatedValues := slices.Delete(tmpValues, i, i+1)
		iterations = append(iterations, truncatedValues)
	}
	return iterations
}

func p1(text []string) {
	safeCount := 0
	for _, report := range text {
		if isSafe(getValuesFromReport(report)) {
			safeCount += 1
		}
	}

	fmt.Println(safeCount)
}

func p2(text []string) {
	safeCount := 0
	for _, report := range text {
		for _, iteration := range getValueIterations(getValuesFromReport(report)) {
			if isSafe(iteration) {
				safeCount += 1
				break
			}
		}
	}

	fmt.Println(safeCount)
}

func main() {
	flag.Parse()

	p1(utils.ReadFile(*inputFile))
	p2(utils.ReadFile(*inputFile))
}
