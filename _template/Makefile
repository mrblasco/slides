OUTDIR := _export
INPUT := presentation.Rmd

SLUG 	?=  preso
PDF 	:= $(OUTDIR)/$(SLUG).pdf
PPTX 	:= $(OUTDIR)/$(SLUG).pptx

# ---- targets 
.PHONY: all pdf pptx view view-pptx clear

all: $(PDF) $(PPTX)

pdf: $(PDF)
pptx: $(PPTX)

view:
	open $(PDF)

view-pptx:
	open $(PPTX)

clear: 
	rm -r $(OUTDIR)

$(PDF): $(INPUT)
	@echo "Rendering $@..."
	@mkdir -p "$(dir $@)"
	@Rscript -e 'rmarkdown::render("$<", output_format = "beamer_presentation", output_file = "$(SLUG).pdf", output_dir = "$(OUTDIR)")'

# PowerPoint uses the EU Policy Lab layouts in reference.pptx (see make_reference.py)
$(PPTX): $(INPUT) reference.pptx _output.yml
	@echo "Rendering $@..."
	@mkdir -p "$(dir $@)"
	@Rscript -e 'rmarkdown::render("$<", output_format = "powerpoint_presentation", output_file = "$(SLUG).pptx", output_dir = "$(OUTDIR)")'

reference.pptx: eu_policy_lab_corporate_template.pptx make_reference.py
	python3 make_reference.py $< $@
