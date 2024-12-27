package main

import (
	"flag"
	"fmt"
	"strconv"
	"strings"

	"utils"
)

var inputFile = flag.String("input", "", "Input text file")

func allTests(text []string) func(func(int, []int) bool) {
	return func(yield func(int, []int) bool) {
		for _, l := range text {
			parts := strings.Split(l, ": ")
			value, _ := strconv.Atoi(parts[0])
			operands := utils.StringToIntSlice(strings.Split(parts[1], " "))
			if !yield(value, operands) {
				return
			}
		}
	}
}

type OperationCache map[int][][]string

func (o OperationCache) getOperationSets(values []string, length int) [][]string {
	operationSet, ok := o[length]
	if ok {
		return operationSet
	}
	o[length] = utils.GetValueCombinations(values, length)
	return o[length]
}

func operationIsTrue(value int, operands []int, operators []string) bool {
	valueSoFar := 0
	for i := range operands {
		if valueSoFar > value {
			return false
		}

		if i == 0 {
			valueSoFar += operands[i]
			continue
		}

		switch operators[i-1] {
		case "+":
			valueSoFar = valueSoFar + operands[i]
		case "*":
			valueSoFar = valueSoFar * operands[i]
		case "||":
			valueSoFar = concatInts(valueSoFar, operands[i])
		default:
			panic("Invalid operation")
		}

		if i == len(operands)-1 && valueSoFar == value {
			return true
		}
	}
	return false
}

func concatInts(num1 int, num2 int) int {
	result, _ := strconv.Atoi(strconv.Itoa(num1) + strconv.Itoa(num2))
	return result
}

func p1(text []string) {
	trueValueSum := 0
	opCache := OperationCache{}

	for value, operands := range allTests(text) {
		operationSet := opCache.getOperationSets(
			[]string{"+", "*"},
			len(operands)-1,
		)
		// Individual tests
		for _, ops := range operationSet {
			if operationIsTrue(value, operands, ops) {
				trueValueSum += value
				break
			}
		}
	}

	fmt.Println(trueValueSum)
}

func p2(text []string) {
	trueValueSum := 0
	opCache := OperationCache{}

	for value, operands := range allTests(text) {
		operationSet := opCache.getOperationSets(
			[]string{"+", "*", "||"},
			len(operands)-1,
		)
		// Individual tests
		for _, ops := range operationSet {
			if operationIsTrue(value, operands, ops) {
				trueValueSum += value
				break
			}
		}
	}

	fmt.Println(trueValueSum)
}

func main() {
	flag.Parse()

	p1(utils.ReadFile(*inputFile))
	p2(utils.ReadFile(*inputFile))
}
