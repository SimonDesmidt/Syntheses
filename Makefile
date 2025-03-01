TEX_FILES := $(shell find . -type f -name '*.tex')
PDF_FILES := $(TEX_FILES:.tex=.pdf)

all: $(PDF_FILES) move

move:
	cp $(PDF_FILES) compiled/

%.pdf: %.tex
	latexmk -pdf -output-directory=$(dir $@) $<

clean:
	latexmk -C
	find . -type f -name "*.aux" -o -name "*.log" -o -name "*.synctex.gz" -o -name "*.out" | xargs rm -f
