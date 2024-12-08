package main

import (
	"flag"
	"fmt"
	"strings"

	"utils"
)

var inputFile = flag.String("input", "", "Input text file")

type Matrix [][]string

func (m Matrix) all(yield func(string) bool) {
	for y := range len(m[0]) {
		for x := range m {
			if !yield(m[x][y]) {
				return
			}
		}
	}
}

func (m Matrix) print() {
	show := ""
	counter := 0
	for v := range m.all {
		show += v
		counter++
		if counter%len(m[0]) == 0 {
			show += "\n"
		}
	}
	fmt.Println(show)
}

func (m Matrix) isWord(word string, x int, y int, xStep int, yStep int) bool {
	// Check if word will exceed matrix boundaries
	if x+(xStep*(len(word)-1)) >= len(m[0]) ||
		x+(xStep*(len(word)-1)) < 0 ||
		y+(yStep*(len(word)-1)) >= len(m) ||
		y+(yStep*(len(word)-1)) < 0 {
		return false
	}

	// Check for word
	actualWord := ""
	for i := range len(word) {
		actualWord += m[x+(xStep*i)][y+(yStep*i)]
	}
	// fmt.Printf("(%d,%d)(%d,%d): %s\n", x, y, xStep, yStep, actualWord)
	return word == actualWord
}

func textTo2dMatrix(text []string) Matrix {
	// Initialize matrix
	rows := len(text)
	cols := len(strings.Split(text[0], ""))
	var matrix = make([][]string, rows)
	for i := range matrix {
		matrix[i] = make([]string, cols)
	}

	// Populate
	for y, yVal := range text {
		for x, xVal := range strings.Split(yVal, "") {
			matrix[x][y] = xVal
		}
	}

	return matrix
}

func p1(text []string) {
	m := textTo2dMatrix(text)
	// m.print()
	matches := 0

	for y := range len(m[0]) {
		for x := range m {
			current := m[x][y]
			if current != "X" {
				continue
			}

			word := "XMAS"

			// L-R
			if m.isWord(word, x, y, 1, 0) {
				matches++
			}
			// R-L
			if m.isWord(word, x, y, -1, 0) {
				matches++
			}
			// U-D
			if m.isWord(word, x, y, 0, 1) {
				matches++
			}
			// D-U
			if m.isWord(word, x, y, 0, -1) {
				matches++
			}
			// UL-DR
			if m.isWord(word, x, y, 1, 1) {
				matches++
			}
			// DR-UL
			if m.isWord(word, x, y, -1, -1) {
				matches++
			}
			// DL-UR
			if m.isWord(word, x, y, 1, -1) {
				matches++
			}
			// UR-DL
			if m.isWord(word, x, y, -1, 1) {
				matches++
			}
		}
	}

	fmt.Println(matches)
}

func p2(text []string) {
	m := textTo2dMatrix(text)
	matches := 0

	for y := range len(m[0]) - 2 {
		for x := range len(m) - 2 {
			current := m[x][y]
			if current != "M" && current != "S" {
				continue
			}

			if (m.isWord("MAS", x, y, 1, 1) || m.isWord("SAM", x, y, 1, 1)) &&
				(m.isWord("MAS", x+2, y, -1, 1) || m.isWord("SAM", x+2, y, -1, 1)) {
				matches++
			}
		}
	}

	fmt.Println(matches)
}

func main() {
	flag.Parse()

	p1(utils.ReadFile(*inputFile))
	p2(utils.ReadFile(*inputFile))
}
