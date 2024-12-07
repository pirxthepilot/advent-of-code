package main

import (
	"flag"
	"fmt"
	"sort"
	"strconv"
	"strings"

	"utils"
)

const FILE = "test.txt"

var inputFile = flag.String("input", "", "Input text file")

func calculateDiff(a int, b int) int {
	if a >= b {
		return a - b
	} else {
		return b - a
	}
}

func textToLists(text []string) ([]int, []int) {
	var listA []int
	var listB []int

	for _, line := range text {
		items := strings.Split(line, "   ")
		left, _ := strconv.Atoi(items[0])
		right, _ := strconv.Atoi(items[1])
		listA = append(listA, left)
		listB = append(listB, right)
	}

	return listA, listB
}

func countOccurences(locationId int, list []int) int {
	count := 0
	for _, n := range list {
		if n == locationId {
			count += 1
		}
	}
	return count
}

func p1(text []string) {
	listA, listB := textToLists(text)

	sort.Ints(listA)
	sort.Ints(listB)

	sum := 0
	for i := range listA {
		sum += calculateDiff(listA[i], listB[i])
	}

	fmt.Println(sum)
}

func p2(text []string) {
	listA, listB := textToLists(text)
	result := 0

	for _, n := range listA {
		result += n * countOccurences(n, listB)
	}

	fmt.Println(result)
}

func main() {
	flag.Parse()

	p1(utils.ReadFile(*inputFile))
	p2(utils.ReadFile(*inputFile))
}
