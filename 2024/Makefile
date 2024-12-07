DAY :=
IN := test.txt

ROOTDIR := ./day$(DAY)
BIN := $(ROOTDIR)/bin/day$(DAY)

prep:
	@mkdir -p $(ROOTDIR)/bin

build: prep
	@go build -C $(ROOTDIR)/ -o $(BIN)

run: build
	$(BIN) -input $(ROOTDIR)/$(IN)
