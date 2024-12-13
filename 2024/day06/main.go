package main

import (
	"flag"
	"fmt"
	"strings"

	"utils"
)

const (
	UP     = "^"
	RIGHT  = ">"
	DOWN   = "v"
	LEFT   = "<"
	OBS    = "#"
	NEWOBS = "0"
)

var inputFile = flag.String("input", "", "Input text file")

type Coordinates struct {
	x int
	y int
}

type Map struct {
	*utils.Matrix
	visited   map[Coordinates]bool
	position  Coordinates
	direction string
}

func newMap(text []string) *Map {
	m := utils.NewMatrix(text)
	// Get start coords
	for y, yVal := range text {
		for x, xVal := range strings.Split(yVal, "") {
			m.Elems[x][y] = xVal
		}
	}
	start := *getStartCoordinates(m.Elems)
	return &Map{
		m,
		map[Coordinates]bool{start: true},
		start,
		UP,
	}
}

func getStartCoordinates(matrix [][]string) *Coordinates {
	for y := range len(matrix[0]) {
		for x := range matrix {
			if matrix[x][y] == UP {
				return &Coordinates{x, y}
			}
		}
	}
	return nil
}

func (m *Map) saveState(x int, y int, direction string) {
	position := &Coordinates{x, y}
	m.visited[*position] = true
	m.position = *position
	m.direction = direction
}

func (m *Map) move(xInc int, yInc int, direction string) error {
	var err error
	newX := m.position.x + xInc
	newY := m.position.y + yInc
	if newX < 0 || newY < 0 || newX >= len(m.Elems[0]) || newY >= len(m.Elems) {
		return fmt.Errorf("Outside the map")
	}
	if m.Elems[newX][newY] == OBS {
		if yInc == -1 {
			err = m.right()
		} else if xInc == 1 {
			err = m.down()
		} else if yInc == 1 {
			err = m.left()
		} else if xInc == -1 {
			err = m.up()
		} else {
			panic("Impossible condition")
		}
		if err != nil {
			return err
		}
		return nil
	}
	m.saveState(newX, newY, direction)
	return nil
}

func (m *Map) up() error {
	return m.move(0, -1, UP)
}

func (m *Map) right() error {
	return m.move(1, 0, RIGHT)
}

func (m *Map) down() error {
	return m.move(0, 1, DOWN)
}

func (m *Map) left() error {
	return m.move(-1, 0, LEFT)
}

func p1(text []string) {
	var err error
	m := newMap(text)
	for {
		switch m.direction {
		case UP:
			err = m.up()
		case RIGHT:
			err = m.right()
		case DOWN:
			err = m.down()
		case LEFT:
			err = m.left()
		default:
			panic("Invalid direction")
		}
		if err != nil {
			break
		}
	}
	fmt.Println(len(m.visited))
}

// func p2(text []string) {
// }

func main() {
	flag.Parse()

	p1(utils.ReadFile(*inputFile))
}
