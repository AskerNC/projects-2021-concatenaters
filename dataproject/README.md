# Data analysis project

Our project is titled **Air transport in the European Union** and examines the correlation between income and air travel in the 27 EU member states.

The **results** of the project can be seen from running [dataproject.ipynb](dataproject.ipynb).

This **loades three datasets**:

1. 'avia_tf_acc' imported via API from [eurostat](https://ec.europa.eu/eurostat/databrowser/view/avia_tf_acc/default/table)
1. 'nama_10_pc' imported via API from [eurostat](https://ec.europa.eu/eurostat/databrowser/view/NAMA_10_PC/default/table)
1. 'demo_pjan' imported via API from [eurostat](https://ec.europa.eu/eurostat/databrowser/view/DEMO_PJAN/default/table)

The datasets are combined and extended. The dataset used in the main analysis is saved as 'eu27_pas_gdp.xlsx' in the data folder.

**Dependencies:** Apart from a standard Anaconda Python 3 installation, the project requires the following installations:

``pip install EurostatAPIClient``
