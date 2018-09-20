# download taxonomy-all.tab from uniprot database
TAXONOMY_URL="https://www.uniprot.org/taxonomy/?query=*&compress=yes&format=tab&force=true"
curl $TAXONOMY_URL | gunzip > taxonomy-all.tab
