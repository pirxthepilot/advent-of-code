DAY :=
IN := test.txt

ROOTDIR := day$(DAY)
BIN := bin/day$(DAY)

prep:
	@mkdir -p $(ROOTDIR)/bin

build: prep
	@go build -C $(ROOTDIR) -o $(BIN)

run: build
	$(ROOTDIR)/$(BIN) -input $(ROOTDIR)/$(IN)
