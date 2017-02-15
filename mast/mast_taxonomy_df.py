import pandas as pd
from itertools import chain

from . import MastFile


class MastTaxData(MastFile):
    """Wrapper for MastFile

    Include taxonomy data from both the UniProt and NCBI databases,
    and a DataFrame attribute with entries corresponding to MastSequence objects
    """
    def __init__(self, record, uniprot_taxa, ncbi_taxa, attr_cols=None):
        """Generate a DataFrame from MAST file given taxonomy database info.

        record : Bio.motifs.mast.Record object
        uniprot_taxa : uniprot_taxonomy.Taxonomy object
        ncbi_taxa : ete2.NCBITaxa object
        attr_cols : list of str
            MastSequence attributes/subattributes to be included in DataFrame
        """
        MastFile.__init__(self, record)
        self.__add_uniprot_tax_data(uniprot_taxa)
        self.__add_ncbi_tax_data(ncbi_taxa)
        self.__make_dataframe(attr_cols=attr_cols)

    def __add_uniprot_tax_data(self, uniprot_taxa):
        """Add taxonomy information from uniprot_taxonomy.Taxonomy object."""
        for sequence in self.sequences:
            sequence.uniprot_organism = uniprot_taxa[sequence.organism_mnemonic]

    def __add_ncbi_tax_data(self, ncbi_taxa):
        """Add taxonomy information from ete2.NCBITaxa object."""
        for sequence in self.sequences:
            sequence.ncbi_lineage_taxids = ncbi_taxa.get_lineage(sequence.uniprot_organism.taxon)
            names = ncbi_taxa.get_taxid_translator(sequence.ncbi_lineage_taxids)
            sequence.ncbi_lineage = [str(names[taxid]) for taxid in sequence.ncbi_lineage_taxids]

    def __make_dataframe(self, attr_cols=None):
        """Add dataframe attribute."""
        if attr_cols:
            self.df = pd.DataFrame([{attr: (getattr(seq, attr, None) or
                                            getattr(seq.uniprot_organism, attr, None) or
                                            getattr(seq.diagram, attr, None))
                                     for attr in attr_cols}
                                    for seq in self.sequences])
        else:
            self.df = pd.DataFrame([dict(chain(seq.__dict__.items(),
                                               seq.uniprot_organism.__dict__.items()))
                                    for seq in self.sequences])
        self.df['motifs'] = self.df['motifs'].apply(lambda l: ','.join([str(m.num) for m in l]))
        self.df['lineage'] = self.df['lineage'].apply(lambda l: ','.join(l))
        self.df['ncbi_lineage'] = self.df['ncbi_lineage'].apply(lambda l: ','.join(l))

    def get_df_subset(self, gene_classification, uniprot_node):
        return self.df.loc[(self.df['gene_classification'] == gene_classification) &
                           (self.df['lineage'].str.contains(uniprot_node))]

    def get_tree(self, gene_classification, node_name):
        seq_df = self.get_df_subset(gene_classification, node_name)
        if seq_df.empty:
            raise Exception('No sequences matching criteria.')
        return self.ncbi_taxa.get_topology(seq_df['taxon'].values)

    def write_tree(self, gene_classification, node_name, outfile=None):
        tree = self.get_tree(gene_classification, node_name)
        return tree.write(outfile=outfile)
