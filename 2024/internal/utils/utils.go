package utils

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

//
// Input file reader
//

func ReadFile(path string) []string {
	f, err := os.Open(path)
	if err != nil {
		fmt.Println(err)
	}
	defer f.Close()

	s := bufio.NewScanner(f)
	s.Split(bufio.ScanLines)

	var lines []string
	for s.Scan() {
		lines = append(lines, s.Text())
	}

	return lines
}

//
// 2D Matrix
//

type Matrix struct {
	Elems [][]string
}

func NewMatrix(text []string) *Matrix {
	// Initialize matrix
	rows := len(text)
	cols := len(strings.Split(text[0], ""))
	m := Matrix{make([][]string, rows)}
	for i := range m.Elems {
		m.Elems[i] = make([]string, cols)
	}

	// Populate
	for y, yVal := range text {
		for x, xVal := range strings.Split(yVal, "") {
			m.Elems[x][y] = xVal
		}
	}

	return &m
}

func (m Matrix) All(yield func(string) bool) {
	for y := range len(m.Elems[0]) {
		for x := range m.Elems {
			if !yield(m.Elems[x][y]) {
				return
			}
		}
	}
}

func (m Matrix) Print() {
	show := ""
	counter := 0
	for v := range m.All {
		show += v
		counter++
		if counter%len(m.Elems[0]) == 0 {
			show += "\n"
		}
	}
	fmt.Println(show)
}
