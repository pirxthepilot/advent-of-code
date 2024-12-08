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

func (m Matrix) isXmas(x int, y int, xStep int, yStep int) bool {
	// Check if word will exceed matrix boundaries
	if x+(xStep*3) >= len(m[0]) ||
		x+(xStep*3) < 0 ||
		y+(yStep*3) >= len(m) ||
		y+(yStep*3) < 0 {
		return false
	}

	// Check for word
	word := fmt.Sprintf(
		"%s%s%s%s",
		m[x][y],
		m[x+(xStep*1)][y+(yStep*1)],
		m[x+(xStep*2)][y+(yStep*2)],
		m[x+(xStep*3)][y+(yStep*3)],
	)
	// fmt.Printf("(%d,%d)(%d,%d): %s\n", x, y, xStep, yStep, word)
	return word == "XMAS"
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

			// L-R
			if m.isXmas(x, y, 1, 0) {
				matches++
			}
			// R-L
			if m.isXmas(x, y, -1, 0) {
				matches++
			}
			// U-D
			if m.isXmas(x, y, 0, 1) {
				matches++
			}
			// D-U
			if m.isXmas(x, y, 0, -1) {
				matches++
			}
			// UL-DR
			if m.isXmas(x, y, 1, 1) {
				matches++
			}
			// DR-UL
			if m.isXmas(x, y, -1, -1) {
				matches++
			}
			// DL-UR
			if m.isXmas(x, y, 1, -1) {
				matches++
			}
			// UR-DL
			if m.isXmas(x, y, -1, 1) {
				matches++
			}
		}
	}

	fmt.Println(matches)
}

// func p2(text []string) {
// }

func main() {
	flag.Parse()

	p1(utils.ReadFile(*inputFile))
}
