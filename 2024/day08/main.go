package main

import (
	"flag"
	"fmt"
	"slices"
	"strings"

	"utils"
)

var inputFile = flag.String("input", "", "Input text file")

type Coordinates = utils.Coordinates

type Map struct {
	*utils.Matrix
	antennas  map[string][]Coordinates
	antinodes []Coordinates
}

func newMap(text []string) *Map {
	rows := len(text)
	cols := len(strings.Split(text[0], ""))
	m := utils.Matrix{Elems: make([][]string, rows)}
	for i := range m.Elems {
		m.Elems[i] = make([]string, cols)
	}

	// Populate
	antennas := make(map[string][]Coordinates)
	for y, yVal := range text {
		for x, xVal := range strings.Split(yVal, "") {
			m.Elems[x][y] = xVal
			if xVal != "." {
				c := Coordinates{X: x, Y: y}
				antennas[xVal] = append(antennas[xVal], c)
			}
		}
	}

	return &Map{
		&m,
		antennas,
		[]Coordinates{},
	}
}

func (m *Map) getCombos(antennaSymbol string) [][]Coordinates {
	combos := [][]Coordinates{}
	for _, current := range m.antennas[antennaSymbol] {
		for _, pair := range m.antennas[antennaSymbol] {
			if current == pair {
				continue
			}
			combos = append(combos, []Coordinates{current, pair})
		}
	}
	return combos
}

func (m *Map) addAntinode(coords Coordinates) {
	if !slices.Contains(m.antinodes, coords) {
		m.antinodes = append(m.antinodes, coords)
	}
}

func (m *Map) getAntinodes(extended bool) []Coordinates {
	// antinodes := []Coordinates{}
	for key := range m.antennas {
		for _, locPairs := range m.getCombos(key) {
			locA := locPairs[0]
			locB := locPairs[1]
			deltaX := locA.X - locB.X
			deltaY := locA.Y - locB.Y
			if extended {
				m.addAntinode(Coordinates{X: locA.X, Y: locA.Y})
			}

			currX := locA.X
			currY := locA.Y
			for {
				antinodeX := currX + deltaX
				antinodeY := currY + deltaY
				if antinodeX < 0 ||
					antinodeX >= len(m.Elems) ||
					antinodeY < 0 ||
					antinodeY >= len(m.Elems[0]) {
					break
				}
				c := Coordinates{X: antinodeX, Y: antinodeY}
				m.addAntinode(c)
				if !extended {
					break
				}
				currX = antinodeX
				currY = antinodeY
			}
		}
	}
	return m.antinodes
}

func p1(text []string) {
	m := newMap(text)
	fmt.Println(len(m.getAntinodes(false)))
}

func p2(text []string) {
	m := newMap(text)
	fmt.Println(len(m.getAntinodes(true)))
}

func main() {
	flag.Parse()

	p1(utils.ReadFile(*inputFile))
	p2(utils.ReadFile(*inputFile))
}
