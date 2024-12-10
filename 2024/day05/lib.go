package main

import (
	"fmt"
	"slices"
	"strconv"
	"strings"
)

//
// Page
//

type Page struct {
	num  int
	next []*Page
	prev []*Page
}

func newPage(num int) *Page {
	return &Page{
		num:  num,
		next: []*Page{},
		prev: []*Page{},
	}
}

func (p *Page) addPrev(page *Page) {
	p.prev = append(p.prev, page)
}

func (p *Page) addNext(page *Page) {
	p.next = append(p.next, page)
}

func (p *Page) allPrevNums() []int {
	all := []int{}
	for _, n := range p.prev {
		all = append(all, n.num)
	}
	return all
}

func (p *Page) allNextNums() []int {
	all := []int{}
	for _, n := range p.next {
		all = append(all, n.num)
	}
	return all
}

func (p *Page) hasNext(num int) bool {
	i := slices.IndexFunc(p.next, func(pi *Page) bool {
		return pi.num == num
	})
	return i != -1
}

func (p *Page) hasPrev(num int) bool {
	i := slices.IndexFunc(p.prev, func(pi *Page) bool {
		return pi.num == num
	})
	return i != -1
}

//
// Rules
//

type Rules []*Page

func (r *Rules) addPage(page *Page) {
	*r = append(*r, page)
}

func (r *Rules) addNewPage(num int) *Page {
	new := newPage(num)
	r.addPage(new)
	return new
}

func (r *Rules) getPage(num int, createIfNil bool) *Page {
	rule := *r
	i := slices.IndexFunc(rule, func(p *Page) bool {
		return p.num == num
	})
	if i == -1 {
		if createIfNil {
			return r.addNewPage(num)
		} else {
			return nil
		}
	}
	return rule[i]
}

//
// Updates
//

type Update struct {
	pageNums []int
}

func newUpdate(text string) *Update {
	pageNums := []int{}
	tmpSlice := strings.Split(text, ",")
	for _, v := range tmpSlice {
		intVal, _ := strconv.Atoi(v)
		pageNums = append(pageNums, intVal)
	}
	return &Update{pageNums: pageNums}
}

func (u Update) getIndex(num int) *int {
	for i, n := range u.pageNums {
		if n == num {
			return &i
		}
	}
	fmt.Printf("Unable to find index of %d in %v - this shouldn't happen!", num, u.pageNums)
	return nil
}

func (u Update) switchPositions(idx1 int, idx2 int) {
	val1 := u.pageNums[idx1]
	val2 := u.pageNums[idx2]
	u.pageNums[idx1] = val2
	u.pageNums[idx2] = val1
}

type Updates []*Update
