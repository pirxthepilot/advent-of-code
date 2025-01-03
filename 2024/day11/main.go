package main

import (
	"flag"
	"fmt"
	"iter"
	"strconv"
	"strings"

	"utils"
)

var inputFile = flag.String("input", "", "Input text file")

type Stone struct {
	number int
	prev   *Stone
	next   *Stone
}

func (s *Stone) linkPrev(stone *Stone) {
	s.prev = stone
	if stone != nil {
		stone.next = s
	}
}

func (s *Stone) linkNext(stone *Stone) {
	s.next = stone
	if stone != nil {
		stone.prev = s
	}
}

func insertStones(stones []Stone, insertAfter *Stone, insertBefore *Stone) (*Stone, *Stone) {
	var (
		first    *Stone
		last     *Stone
		previous *Stone
	)
	for i, s := range stones {
		current := &s
		if i == 0 {
			first = current
		} else {
			current.linkPrev(previous)
		}
		if i == len(stones)-1 {
			last = &s
		}
		previous = current
	}
	if insertAfter != nil {
		first.linkPrev(insertAfter)
	}
	if insertBefore != nil {
		last.linkNext(insertBefore)
	}
	return first, last
}

func newStones(text []string) *Stone {
	stones := []Stone{}
	for _, n := range strings.Split(text[0], " ") {
		number, _ := strconv.Atoi(string(n))
		stones = append(stones, Stone{number, nil, nil})
	}
	first, _ := insertStones(stones, nil, nil)
	return first
}

func getStones(first *Stone) iter.Seq[*Stone] {
	current := first
	return func(yield func(*Stone) bool) {
		for {
			if !yield(current) || current.next == nil {
				return
			}
			current = current.next
		}
	}
}

func PrintStones(first *Stone) string {
	stones := []string{}
	for s := range getStones(first) {
		stones = append(stones, strconv.Itoa(s.number))
	}
	return strings.Join(stones, " -> ")
}

func blink(first *Stone) *Stone {
	newFirst := first
	current := first
	var f, l *Stone
	for {
		if current.number == 0 { // Rule 1
			f, l = insertStones(
				[]Stone{{1, nil, nil}},
				current.prev,
				current.next,
			)
		} else if len(strconv.Itoa(current.number))%2 == 0 { // Rule 2
			numberStr := strconv.Itoa(current.number)
			splitIdx := len(numberStr) / 2
			leftNum, _ := strconv.Atoi(numberStr[:splitIdx])
			rightNum, _ := strconv.Atoi(numberStr[splitIdx:])
			f, l = insertStones(
				[]Stone{
					{leftNum, nil, nil},
					{rightNum, nil, nil},
				},
				current.prev,
				current.next,
			)
		} else { // Rule 3
			f, l = insertStones(
				[]Stone{{current.number * 2024, nil, nil}},
				current.prev,
				current.next,
			)
		}

		if f.prev == nil {
			newFirst = f
		}
		current = l

		if current.next == nil {
			break
		}
		current = current.next
	}
	return newFirst
}

func getStoneCount(first *Stone) int {
	count := 0
	for range getStones(first) {
		count++
	}
	return count
}

func p1(text []string) {
	first := newStones(text)
	// fmt.Println(PrintStones(first))
	for range 25 {
		first = blink(first)
	}
	// fmt.Println(PrintStones(first))
	fmt.Println(getStoneCount(first))
}

func p2(text []string) {
	first := newStones(text)
	for range 75 {
		first = blink(first)
	}
	fmt.Println(getStoneCount(first))
}

func main() {
	flag.Parse()

	p1(utils.ReadFile(*inputFile))
	p2(utils.ReadFile(*inputFile))
}
