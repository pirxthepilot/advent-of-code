package utils

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
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

// []string to []int converter
func StringToIntSlice(inputs []string) []int {
	ints := []int{}
	for _, v := range inputs {
		intVal, _ := strconv.Atoi(v)
		ints = append(ints, intVal)
	}
	return ints
}

// Value combinations
func GetValueCombinations(values []string, length int) [][]string {
	var (
		results [][]string
		queue   [][]string
	)

	// Initial values
	for _, o := range values {
		queue = append(queue, []string{o})
	}

	// Start BFS
	for {
		if len(queue) == 0 {
			break
		}
		current := queue[0]
		queue = queue[1:]
		if len(current) == length {
			results = append(results, current)
			continue
		}
		for _, o := range values {
			next := make([]string, len(current))
			copy(next, current)
			next = append(next, o)
			queue = append(queue, next)
		}
	}

	return results
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

// Coordinates
type Coordinates struct {
	X int
	Y int
}
