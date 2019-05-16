PDFLATEX = xelatex
DIPLOMA_REPORT_PDF = diploma_report
PRACTICE_REPORT_PDF = practice_report
TASK_REPORT_PDF = task_report
BIBTEX = bibtex
MAKEINDEX = makeindex
RM = rm -f
MAKEDIR = mkdir -p
COPY = cp -f


all: $(DIPLOMA_REPORT_PDF).pdf $(PRACTICE_REPORT_PDF).pdf $(TASK_REPORT_PDF).pdf

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
	$(MAKEDIR) diploma_out
	$(COPY) $(DIPLOMA_REPORT_PDF).* ./diploma_out/
	$(RM) *.aux *.log *.out *.toc *.gz *.gz\(busy\) *.blg *.bbl *.nlo *.nls *.ilg *.fls *.fdb_latexmk



$(PRACTICE_REPORT_PDF).pdf: *.tex *.bib
	$(PDFLATEX) $(PRACTICE_REPORT_PDF)
	$(MAKEINDEX) $(PRACTICE_REPORT_PDF).nlo -s nomencl.ist -o $(PRACTICE_REPORT_PDF).nls
	$(BIBTEX) $(PRACTICE_REPORT_PDF).aux
	$(PDFLATEX) $(PRACTICE_REPORT_PDF)
	$(PDFLATEX) $(PRACTICE_REPORT_PDF)
	# Citations count fixing
	$(PDFLATEX) $(PRACTICE_REPORT_PDF)
	$(MAKEDIR) practice_out
	$(COPY) $(PRACTICE_REPORT_PDF).* ./practice_out/
	$(RM) *.aux *.log *.out *.toc *.gz *.gz\(busy\) *.blg *.bbl *.nlo *.nls *.ilg *.fls *.fdb_latexmk

$(TASK_REPORT_PDF).pdf: *.tex *.bib
	$(PDFLATEX) $(TASK_REPORT_PDF)
	$(MAKEINDEX) $(TASK_REPORT_PDF).nlo -s nomencl.ist -o $(TASK_REPORT_PDF).nls
	$(PDFLATEX) $(TASK_REPORT_PDF)
	$(PDFLATEX) $(TASK_REPORT_PDF)
	# Citations count fixing
	$(PDFLATEX) $(TASK_REPORT_PDF)
	$(MAKEDIR) task_out 
	$(COPY) $(TASK_REPORT_PDF).* ./task_out/
	$(RM) *.aux *.log *.out *.toc *.gz *.gz\(busy\) *.blg *.bbl *.nlo *.nls *.ilg *.fls *.fdb_latexmk

review.pdf: review.tex preamble.tex
	$(PDFLATEX) review

cleanall: clean
	$(RM)  *.pdf

.PHONY: clean cleanall
clean:
	$(RM) *.aux *.log *.out *.toc *.gz *.gz\(busy\) *.blg *.bbl *.nlo *.nls *.ilg *.fls *.fdb_latexmk
