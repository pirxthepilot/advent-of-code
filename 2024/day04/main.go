package main

import (
	"flag"
	"fmt"

	"utils"
)

var inputFile = flag.String("input", "", "Input text file")

type LetterMatrix struct {
	*utils.Matrix
}

func newLetterMatrix(text []string) *LetterMatrix {
	m := utils.NewMatrix(text)
	return &LetterMatrix{m}
}

func (m LetterMatrix) isWord(word string, x int, y int, xStep int, yStep int) bool {
	// Check if word will exceed matrix boundaries
	if x+(xStep*(len(word)-1)) >= len(m.Elems[0]) ||
		x+(xStep*(len(word)-1)) < 0 ||
		y+(yStep*(len(word)-1)) >= len(m.Elems) ||
		y+(yStep*(len(word)-1)) < 0 {
		return false
	}

	// Check for word
	actualWord := ""
	for i := range len(word) {
		actualWord += m.Elems[x+(xStep*i)][y+(yStep*i)]
	}
	return word == actualWord
}

func p1(text []string) {
	m := newLetterMatrix(text)
	matches := 0

	for y := range len(m.Elems[0]) {
		for x := range m.Elems {
			current := m.Elems[x][y]
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
	m := newLetterMatrix(text)
	matches := 0

	for y := range len(m.Elems[0]) - 2 {
		for x := range len(m.Elems) - 2 {
			current := m.Elems[x][y]
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
