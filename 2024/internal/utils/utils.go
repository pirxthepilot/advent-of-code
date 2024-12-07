package utils

import (
	"bufio"
	"fmt"
	"os"
)

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
