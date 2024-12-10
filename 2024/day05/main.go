package main

import (
	"flag"
	"fmt"
	"regexp"
	"strconv"

	"utils"
)

var inputFile = flag.String("input", "", "Input text file")

func getParts(text []string) (Rules, Updates) {
	rules := Rules{}
	updates := Updates{}
	rulesPart := true
	for _, l := range text {
		if l == "" {
			rulesPart = false
			continue
		}
		if rulesPart {
			pat := regexp.MustCompile(`(\d+)\|(\d+)`)
			match := pat.FindStringSubmatch(l)
			lhs, _ := strconv.Atoi(match[1])
			rhs, _ := strconv.Atoi(match[2])
			lPage := rules.getPage(lhs, true)
			rPage := rules.getPage(rhs, true)
			lPage.addNext(rPage)
			rPage.addPrev(lPage)
		} else {
			updates = append(updates, newUpdate(l))
		}
	}
	return rules, updates
}

func getSliceCopy(src []int) []int {
	sliceCopy := make([]int, len(src))
	copy(sliceCopy, src)
	return sliceCopy
}

func p1(text []string) {
	rules, updates := getParts(text)
	sumOfMiddles := 0

	for _, update := range updates {
		var middleNumber int
		isCorrectOrder := true
		for idx, num := range update.pageNums {
			rule := rules.getPage(num, false)
			if rule == nil {
				continue
			}

			prevPages := getSliceCopy(update.pageNums)[:idx]
			nextPages := getSliceCopy(update.pageNums)[idx+1:]

			// Compare previous pages
			for _, num := range prevPages {
				if !rule.hasPrev(num) {
					isCorrectOrder = false
					break
				}
			}
			if !isCorrectOrder {
				break
			}

			// Compare next pages
			for _, num := range nextPages {
				if !rule.hasNext(num) {
					isCorrectOrder = false
					break
				}
			}
			if !isCorrectOrder {
				break
			}

			// Find middle number
			if len(prevPages) == len(nextPages) {
				middleNumber = num
			}
		}

		// In correct order! Do stuff
		sumOfMiddles += middleNumber
	}

	fmt.Println(sumOfMiddles)
}

func p2(text []string) {
	rules, updates := getParts(text)
	sumOfMiddles := 0

	for _, update := range updates {
		var middleNumber int
		firstPass := true
		for {
			tryAgain := false
			for idx, num := range update.pageNums {
				rule := rules.getPage(num, false)
				if rule == nil {
					continue
				}

				prevPages := getSliceCopy(update.pageNums)[:idx]
				nextPages := getSliceCopy(update.pageNums)[idx+1:]

				// Compare previous pages
				for _, prevNum := range prevPages {
					if !rule.hasPrev(prevNum) {
						tryAgain = true
						update.switchPositions(idx, *update.getIndex(prevNum))
						break
					}
				}

				// Compare next pages
				for _, nextNum := range nextPages {
					if !rule.hasNext(nextNum) {
						tryAgain = true
						update.switchPositions(idx, *update.getIndex(nextNum))
						break
					}
				}

				// Find middle number
				if len(prevPages) == len(nextPages) {
					middleNumber = num
				}
			}

			// If order is correct the first time, ignore this update and move to the next
			if firstPass && !tryAgain {
				break
			}

			// Do another pass if needs correction
			if tryAgain {
				if firstPass {
					firstPass = false
				}
				continue
			}

			// Finally corrected! Do stuff
			if !firstPass && !tryAgain {
				sumOfMiddles += middleNumber
				break
			}
		}
	}

	fmt.Println(sumOfMiddles)
}

func main() {
	flag.Parse()

	p1(utils.ReadFile(*inputFile))
	p2(utils.ReadFile(*inputFile))
}
