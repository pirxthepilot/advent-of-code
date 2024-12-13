package main

import (
	"flag"
	"fmt"
	"strings"

	"utils"
)

const (
	UP    = "^"
	RIGHT = ">"
	DOWN  = "v"
	LEFT  = "<"
	OBS   = "#"
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

func (m *Map) up() error {
	newY := m.position.y - 1
	if newY < 0 {
		return fmt.Errorf("Outside the map")
	}
	if m.Elems[m.position.x][newY] == OBS {
		err := m.right()
		if err != nil {
			return err
		}
		return nil
	}
	m.saveState(m.position.x, newY, UP)
	return nil
}

func (m *Map) right() error {
	newX := m.position.x + 1
	if newX >= len(m.Elems[0]) {
		return fmt.Errorf("Outside the map")
	}
	if m.Elems[newX][m.position.y] == OBS {
		err := m.down()
		if err != nil {
			return err
		}
		return nil
	}
	m.saveState(newX, m.position.y, RIGHT)
	return nil
}

func (m *Map) down() error {
	newY := m.position.y + 1
	if newY >= len(m.Elems) {
		return fmt.Errorf("Outside the map")
	}
	if m.Elems[m.position.x][newY] == OBS {
		err := m.left()
		if err != nil {
			return err
		}
		return nil
	}
	m.saveState(m.position.x, newY, DOWN)
	return nil
}

func (m *Map) left() error {
	newX := m.position.x - 1
	if newX < 0 {
		return fmt.Errorf("Outside the map")
	}
	if m.Elems[newX][m.position.y] == OBS {
		err := m.up()
		if err != nil {
			return err
		}
		return nil
	}
	m.saveState(newX, m.position.y, LEFT)
	return nil
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
