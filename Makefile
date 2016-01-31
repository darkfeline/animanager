.PHONY: all clean build package

OUTPUTDIR=output

all: build package

clean:
	find ${OUTPUTDIR} -name "*.html" -print0 | xargs -0 rm

build: index.html

package:
	mkdir -p ${OUTPUTDIR}
	find . -path ./${OUTPUTDIR} -prune -o -name "*.html" -exec mv {} ${OUTPUTDIR}/{} \;

%.html: %.m4
	m4 -Iinclude $< > $@
