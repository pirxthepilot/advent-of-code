package main

import (
	"flag"
	"fmt"
	"regexp"
	"strconv"

	"utils"
)

var inputFile = flag.String("input", "", "Input text file")

func findValidOperations(line string) []string {
	pattern := regexp.MustCompile(`mul\(\d+,\d+\)`)
	return pattern.FindAllString(line, -1)
}

func findValidOperationsV2(line string) []string {
	pattern := regexp.MustCompile(`(mul\(\d+,\d+\))|(do\(\))|(don't\(\))`)
	return pattern.FindAllString(line, -1)
}

func runOperation(op string) int {
	pattern := regexp.MustCompile(`mul\((\d+),(\d+)\)`)
	match := pattern.FindStringSubmatch(op)
	lhs, _ := strconv.Atoi(match[1])
	rhs, _ := strconv.Atoi(match[2])

	return lhs * rhs
}

func p1(text []string) {
	total := 0
	for _, line := range text {
		for _, op := range findValidOperations(line) {
			total += runOperation(op)
		}
	}

	fmt.Println(total)
}

func p2(text []string) {
	total := 0
	isActive := true
	for _, line := range text {
		for _, op := range findValidOperationsV2(line) {
			if op == "do()" {
				isActive = true
			} else if op == "don't()" {
				isActive = false
			} else if isActive {
				total += runOperation(op)
			}
		}
	}

	fmt.Println(total)
}

func main() {
	flag.Parse()

	p1(utils.ReadFile(*inputFile))
	p2(utils.ReadFile(*inputFile))
}
