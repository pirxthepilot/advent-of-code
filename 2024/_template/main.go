package main

import (
	"flag"

	"utils"
)

var inputFile = flag.String("input", "", "Input text file")

func p1(text []string) {
}

func p2(text []string) {
}

func main() {
	flag.Parse()

	p1(utils.ReadFile(*inputFile))
}
