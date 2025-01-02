package main

import (
	"flag"
	"fmt"
	"iter"
	"slices"
	"strconv"
	"strings"

	"utils"
)

var inputFile = flag.String("input", "", "Input text file")

type Coordinates = utils.Coordinates

type Map struct {
	positions  [][]int
	trailheads []Coordinates
	paths      *[][]Coordinates
}

func newMap(text []string) *Map {
	rows := len(text)
	cols := len(strings.Split(text[0], ""))
	positions := make([][]int, rows)
	for i := range positions {
		positions[i] = make([]int, cols)
	}

	// Populate
	trailheads := []Coordinates{}
	for y, yVal := range text {
		for x, xVal := range strings.Split(yVal, "") {
			height, _ := strconv.Atoi(xVal)
			positions[x][y] = height
			if height == 0 {
				c := Coordinates{X: x, Y: y}
				trailheads = append(trailheads, c)
			}
		}
	}

	return &Map{
		positions,
		trailheads,
		&[][]Coordinates{},
	}
}

func (m Map) Print() {
	show := ""
	for y := range len(m.positions[0]) {
		for x := range len(m.positions) {
			show += strconv.Itoa(m.positions[x][y])
		}
		show += "\n"
	}
	fmt.Println(show)
}

func (m *Map) getAdjacent(pos Coordinates) iter.Seq[Coordinates] {
	return func(yield func(Coordinates) bool) {
		for _, c := range []Coordinates{
			{X: pos.X + 1, Y: pos.Y},
			{X: pos.X, Y: pos.Y + 1},
			{X: pos.X - 1, Y: pos.Y},
			{X: pos.X, Y: pos.Y - 1},
		} {
			if !(c.X < 0 || c.Y < 0 || c.X > len(m.positions[0])-1 || c.Y > len(m.positions)-1) {
				if !yield(c) {
					return
				}
			}
		}
	}
}

func (m *Map) findPaths() *[][]Coordinates {
	var queue [][]Coordinates

	// Populate initial queue
	for _, t := range m.trailheads {
		queue = append(queue, []Coordinates{t})
	}

	// BFS
	for {
		if len(queue) == 0 {
			break
		}
		current := queue[0]
		queue = queue[1:]

		vertex := current[len(current)-1]

		if m.positions[vertex.X][vertex.Y] == 9 {
			*m.paths = append(*m.paths, current)
			continue
		}

		for a := range m.getAdjacent(vertex) {
			if m.positions[a.X][a.Y]-m.positions[vertex.X][vertex.Y] == 1 {
				next := make([]Coordinates, len(current))
				copy(next, current)
				queue = append(queue, append(next, a))
			}
		}
	}

	return m.paths
}

func (m *Map) getScore() int {
	scores := make(map[Coordinates][]Coordinates)
	for _, p := range *m.paths {
		start := p[0]
		end := p[len(p)-1]
		if !slices.Contains(scores[start], end) {
			scores[start] = append(scores[start], end)
		}
	}

	total := 0
	for _, s := range scores {
		total += len(s)
	}
	return total
}

func (m *Map) PrintPath(path []Coordinates) string {
	values := ""
	for _, p := range path {
		values += strconv.Itoa(m.positions[p.X][p.Y])
	}
	return values
}

func p1(text []string) {
	m := newMap(text)
	m.findPaths()
	fmt.Println(m.getScore())
}

// func p2(text []string) {
// }

func main() {
	flag.Parse()

	p1(utils.ReadFile(*inputFile))
}
