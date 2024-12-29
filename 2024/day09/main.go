package main

import (
	"flag"
	"fmt"
	"strconv"

	"utils"
)

var inputFile = flag.String("input", "", "Input text file")

type File struct {
	size int
	free int
}

type Disk struct {
	blocks    map[int]string
	totalUsed int
}

func newDisk(text []string) *Disk {
	// First, parse files
	files := []File{}
	var (
		size int
		free int
	)
	for i, c := range text[0] {
		if i%2 == 0 {
			size, _ = strconv.Atoi(string(c))
			if i == len(text[0])-1 {
				files = append(files, File{size, 0})
			}
		} else {
			free, _ = strconv.Atoi(string(c))
			files = append(files, File{size, free})
		}
	}

	// Use files to create a Disk
	blocks := make(map[int]string)
	bIdx := 0
	for i, f := range files {
		for range f.size {
			blocks[bIdx] = strconv.Itoa(i)
			bIdx++
		}
		for range f.free {
			blocks[bIdx] = "."
			bIdx++
		}
	}

	return &Disk{
		blocks,
		len(blocks),
	}
}

func (d *Disk) Print() string {
	blocksStr := ""
	for k := range len(d.blocks) {
		blocksStr += d.blocks[k]
	}
	return blocksStr
}

func (d *Disk) popLastFullBlock() string {
	for i := range d.totalUsed {
		idx := d.totalUsed - 1 - i
		if d.blocks[idx] != "." {
			popped := d.blocks[idx]
			d.blocks[idx] = "."
			d.totalUsed = idx + 1
			return popped
		}
	}
	panic("This shouldn't be possible!")
}

func (d *Disk) defrag() {
	for k := range len(d.blocks) {
		if k >= d.totalUsed-1 {
			return
		}
		if d.blocks[k] == "." {
			tmpVal := d.popLastFullBlock()
			if k >= d.totalUsed-1 {
				d.blocks[d.totalUsed-1] = tmpVal
				return
			}
			d.blocks[k] = tmpVal
		}
	}
}

func (d *Disk) getChecksum() int {
	checksum := 0
	for k := range len(d.blocks) {
		v := d.blocks[k]
		if v == "." {
			break
		}
		id, _ := strconv.Atoi(v)
		checksum += k * id
	}
	return checksum
}

func p1(text []string) {
	disk := newDisk(text)
	disk.defrag()
	fmt.Println(disk.getChecksum())
}

// func p2(text []string) {
// }

func main() {
	flag.Parse()

	p1(utils.ReadFile(*inputFile))
}
