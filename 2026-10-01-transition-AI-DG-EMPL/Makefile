OUTDIR := _export
PRESO := $(OUTDIR)/repoint_AI_model.pdf

all: $(PRESO)

$(OUTDIR)/%.pdf: %.Rmd
	@mkdir -p "$(dir $@)"
	@Rscript -e 'rmarkdown::render("$<", output_format = "beamer_presentation", output_dir = "$(dir $@)")'

view:
	open -a Skim $(PRESO)

clear: 
	rm -r $(OUTDIR)