# NLP-PubMiner
Utilize NLP text mining methods to identify relevant research articles for data mining based on large database.
> [!NOTE]
> * <b>Step I.</b> Publication data Pretreatment: Preprocessing publication record data based on title, abstract, and author keywords
> * <b>Step II.</b> Publication data Identification: Applying topic keywords and anti-keywords to identify relevant publications

The agorithm shared in this repository is a updated, simplified version mainly designed to retrieve and organize data based on publication records from the Web of Science. The method was initially developed in 2020 as part of the text mining aglorithem was designed for Zhu et al. (2021) and citation can be made for:
- [x] Zhu, J. J., Dressel, W., Pacion, K., & Ren, Z. J. (2021). ES&T in the 21st century: a data-driven analysis of research topics, interconnections, and trends in the past 20 years. *Environmental Science & Technology*, 55(6), 3453-3464. [https://doi.org/10.1021/acs.est.0c07551](https://doi.org/10.1021/acs.est.0c07551)
<br>

## Applications
### Environmental data science
- [x] Zhu, J.-J., Yang, M., & Ren, Z. J. (2023). Machine learning in environmental research: common pitfalls and best practices. *Environmental Science & Technology*, 57(46), 17671-17689. [https://doi.org/10.1021/acs.est.3c00026](https://doi.org/10.1021/acs.est.3c00026)
- [x] Schneider, M. Y.*, Quaghebeur, W., Borzooei, S., Froemelt, A., Li, F., Saagi, R., Wade, M. J., Zhu, J.-J., & Torfs, E. (2022). Hybrid modelling of water resource recovery facilities: status and opportunities. *Water Science and Technology*, 85(9), 2503-2524. [https://doi.org/10.2166/wst.2022.115](https://doi.org/10.2166/wst.2022.115)
- [x] Zhu, J. J., & Ren, Z. J. (2023). The evolution of research in resources, conservation & recycling revealed by Word2vec-enhanced data mining. *Resources, conservation and recycling*, 190, 106876. [https://doi.org/10.1016/j.resconrec.2023.106876](https://doi.org/10.1016/j.resconrec.2023.106876)

### Decarbonization
- [x] Song, C., Zhu, J. J., Willis, J. L., Moore, D. P., Zondlo, M. A., & Ren, Z. J. (2023). Methane emissions from municipal wastewater collection and treatment systems. *Environmental science & technology*, 57(6), 2248-2261. [https://doi.org/10.1021/acs.est.2c04388](https://doi.org/10.1021/acs.est.2c04388)
- [x] Song, C., Zhu, J. J., Willis, J. L., Moore, D. P., Zondlo, M. A., & Ren, Z. J. (2024). Oversimplification and misestimation of nitrous oxide emissions from wastewater treatment plants. *Nature Sustainability*, 7(10), 1348-1358. [https://doi.org/10.1038/s41893-024-01420-9](https://doi.org/10.1038/s41893-024-01420-9)
- [x] Song, C., Zhu, J. J., Yuan, Z., van Loosdrecht, M. C., & Ren, Z. J. (2024). Defining and achieving net-zero emissions in the wastewater sector. *Nature Water*, 2(10), 927-935. [https://doi.org/10.1038/s44221-024-00318-2](https://doi.org/10.1038/s44221-024-00318-2)
- [x] Yan, Y., Zhu, J. J., May, H. D., Song, C., Jiang, J., Du, L., & Ren, Z. J. (2024). Methanogenic Potential of Sewer Microbiomes and Its Implications for Methane Emission. Environmental Science & Technology, 58(45), 19990-19998. [https://doi.org/10.1021/acs.est.4c04005](https://doi.org/10.1021/acs.est.4c04005)

### Resource recovery
- [x] Yang, M., Zhu, J. J., McGaughey, A., Zheng, S., Priestley, R. D., & Ren, Z. J. (2023). Predicting extraction selectivity of acetic acid in pervaporation by machine learning models with data leakage management. *Environmental Science & Technology*, 57(14), 5934-5946. [https://doi.org/10.1021/acs.est.2c06382](https://doi.org/10.1021/acs.est.2c06382)
- [x] Yang, M., Zhu, J. J., McGaughey, A. L., Priestley, R. D., Hoek, E. M., Jassby, D., & Ren, Z. J. (2024). Machine learning for polymer design to enhance pervaporation-based organic recovery. *Environmental Science & Technology*, 58(23), 10128-10139. [https://doi.org/10.1021/acs.est.4c00060](https://doi.org/10.1021/acs.est.4c00060)
<br>

## Why NLP-PubMiner?
### Example of publication search in decarbonization & wastewater
> [!TIP]
> Summary of outcomes (the numbers were obtained in 2023):

| Database | Accessibility | Method | Number of publications |
| --- | --- | --- | --- |
| PubMed | Free | Direct search | 910 |
| Scopus | Subscription | Direct search | 4119 |
| WOS (Core data) | Subscription | Direct search | 2787 |
| WOS (Core data) | Subscription | NLP-PubMiner | 4500 |

*Direct search via WOS (Core data)*
<img src="https://github.com/starfriend10/NLP-PubMiner/blob/main/Example%20search.png" width="1000">
<br>

## Example of use case
### Indentify wastewater N2O emission publications
> [!TIP]
> Major steps ([Song et al. (2024)](https://doi.org/10.1038/s41893-024-01420-9)):
* Step 1. This step roughly collected about >330,000 of raw full publication records between 1900-2023 (in January 2023) from Web of Science based on general keywords, including <i>wastewater, waste-water, waste water, activated sludge, sewage, sewer, sewerage, anaerobic digestion, anaerobic codigestion, anaerobic co-digestion, anammox, water resource recovery facility, nitrification, denitrification, black water, grey water, gray water, blackwater, greywater, graywater.</i>
* Step 2 (Step I in NLP-PubMiner). Titles, abstracts, and keywords of the collected publications were pretreated using natural language processing (NLP) methods, including n-grams (one, two, three, and four adjacent words) word-tokenization, lowercasing, stop-word removal, and stemming. This step helped to develop a searchable database for the step 3.
* Step 3 (the first part of Step II in NLP-PubMiner). To better exclude irrelevant literature, we applied a finer screening based on N2O keywords (n2o, nitrous oxide), emission keyword (emission), and wastewater-related terminologies (to exclude noises from raw data), including:
<i>wastewater, wastewater treatment, wastewater treatment process, wastewater treatment plant, wwtp, waste water, waste water treatment, waste water treatment process, waste water treatment plant, wastewater utility, sewage, sewage water, sewage treatment, sewage water treatment, sewage treatment plant, sewage water treatment plant, water resource recovery facility, wrrf, wastewater treatment facility, wwtf, water reclamation plant, activated sludge, activated sludge process,  activated sludge model, sewer, sewerage, primary clarifier, secondary clarifier, grit tank, anoxic tank, denitrification, nitrification, anaerobic digestion, anaerobic codigestion, anaerobic co digestion, struvite precipitation, anammox, nitrogen removal, partial nitrification, mlss, mlvss, solids retention time, solids residence time, mean cell residence time, aerobic reactor,  nitrifier denitrification, heterotrophic denitrification, biological nitrogen removal, tertiary treatment, enhanced biological nitrogen removal, denitrifying phosphorus removal, ebpr, collection system, sequencing batch reactor,  advanced oxidation process, sludge age, sludge volume index, return activated sludge, mixed liquor suspended solids, wasted sludge, granular sludge,  sludge blanket, extracellular polymeric substance, sludge granule, sludge treatment, sludge handling, sludge disposal, sludge pretreatment, sludge dewatering, combined sewage overflow, cso, publicly owned treatment work, potw, biosolids, F/M ratio, stabilization pond, rotating biological disk, upflow anaerobic sludge, up flow anaerobic sludge, uasb, trickling filter, biofilm, biofilm reactor, biofilm bioreactor, membrane bioreactor, black water, grey water, gray water, blackwater, greywater, graywater, anaerobic baffled reactor, anaerobic/anoxic/oxic, anaerobic anoxic oxic, a2o, a2/o, anoxic/oxic, rotatory biological contactor, anaerobic/oxic, upflow anaerobic filter, modified ludzack ettinger, contact stabilization, step feed, high purity oxygen, extended aeration, oxidation ditch, nitritation, denitritation, force main, gravity main, rising main, pumping station.</i>
* Step 4 (the second part of Step II in NLP-PubMiner). The step 3 helped to retain about 1540 relevant papers. A further fine search was conducted using abstract (tokenized to sentences). The search was taken to exclude irrelevant or laboratory-scale keywords (e.g., life cycle assessment, bench scale, laboratory scale) and other domain-focused (e.g., river, lake, surface water, wetland, soil, aquifer, groundwater) papers. Papers mentioned model-related keywords were not removed at this step because we found that it was possible for these studied to use field measurement data to calibrate model. This step left about 970 papers for a general inspection. 
* Step 5. A general inspection was taken based on the title and abstract. Relevant papers were subsequently retrieved and gathered for manual review and data acquisition. It is worthwhile to note that a large fraction of potential papers was related to N2O production rather than N2O emission and some other papers investigated N2O emissions from industrial activities (e.g., swine wastewater, dairy farm, abattoir, decentralized treatment), grasslands, farmland wastewater treatment, so they were excluded from the database. In addition, we only focused on intensive engineered treatment systems and excluded studies on natural or constructed wetlands.
<br>

## License

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

