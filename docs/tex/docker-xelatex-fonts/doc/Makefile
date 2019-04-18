PDFLATEX = xelatex
DIPLOMA_REPORT_PDF = diploma_report
PRACTICE_REPORT_PDF = practice_report
BIBTEX = bibtex
MAKEINDEX = makeindex
RM = rm -f


all: $(DIPLOMA_REPORT_PDF).pdf $(PRACTICE_REPORT_PDF).pdf

fast: *.tex
	latexmk -pdf -xelatex $(DIPLOMA_REPORT_PDF)


$(DIPLOMA_REPORT_PDF).pdf: *.tex *.bib
	$(PDFLATEX) $(DIPLOMA_REPORT_PDF)
	$(MAKEINDEX) $(DIPLOMA_REPORT_PDF).nlo -s nomencl.ist -o $(DIPLOMA_REPORT_PDF).nls
	$(BIBTEX) $(DIPLOMA_REPORT_PDF).aux
	$(PDFLATEX) $(DIPLOMA_REPORT_PDF)
	$(PDFLATEX) $(DIPLOMA_REPORT_PDF)
	# Citations count fixing
	$(PDFLATEX) $(DIPLOMA_REPORT_PDF)


$(PRACTICE_REPORT_PDF).pdf: *.tex *.bib
	$(PDFLATEX) $(PRACTICE_REPORT_PDF)
	$(MAKEINDEX) $(PRACTICE_REPORT_PDF).nlo -s nomencl.ist -o $(PRACTICE_REPORT_PDF).nls
	$(BIBTEX) $(PRACTICE_REPORT_PDF).aux
	$(PDFLATEX) $(PRACTICE_REPORT_PDF)
	$(PDFLATEX) $(PRACTICE_REPORT_PDF)
	# Citations count fixing
	$(PDFLATEX) $(PRACTICE_REPORT_PDF)

review.pdf: review.tex preamble.tex
	$(PDFLATEX) review

cleanall: clean
	$(RM)  *.pdf

.PHONY: clean cleanall
clean:
	$(RM) *.aux *.log *.out *.toc *.gz *.gz\(busy\) *.blg *.bbl *.nlo *.nls *.ilg *.fls *.fdb_latexmk
