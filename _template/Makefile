OUTDIR := _export
INPUT := presentation.Rmd

SLUG 	?=  preso.pdf
FORMAT 	:= beamer_presentation
PRESO 	:= $(OUTDIR)/$(SLUG)

# ---- targets 
.PHONY: all view clear

all: $(PRESO)

view:
	open $(PRESO)

clear: 
	rm -r $(OUTDIR)

$(PRESO): presentation.Rmd
	@echo "Rendering $@..."
	@mkdir -p "$(dir $@)"
	@Rscript -e 'rmarkdown::render("$<", output_format = "$(FORMAT)", output_file = "$(PRESO)")'
