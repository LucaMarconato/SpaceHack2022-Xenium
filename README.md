# SpaceHack2022-Xenium
Our team work on Xenium data for the SpaceHack 2022

## Resources
- [SpatialData quick start](spatialdata.md)

## Slides
- [Google slides for results](https://docs.google.com/presentation/d/1uDC-YL4miMirfymsOrJFC4NmRo4JcPb1iX5XEZXXNoI/edit#slide=id.p)

## Biohakcathon 2022::Xenium omni-workflow (a potential plan)

### infrastructure --> **Luca and Gleb | Txsim/MCMICRO**
- [ ] having a single step-wise workflow 
- [ ] effect of method choice for each step

### Segmentation refinement by integration --> **Gleb and Art1m | Txsim/MCMICRO**
- [ ] Other segmentation methods
- [ ] Using the H&E image
	
### Robustness --> **Luca and Gleb | Txsim/MCMICRO** 
- [ ] robustness to noise at each step
- [ ] Simulation by subseting 
- [ ] Simulation by purturbing segmentation boundries 
- [ ] Xenium to ISS transformation simulation
	
### Initial QC metrics --> **Elyas and Art0m | Txsim/MCMICRO**
- [ ] scFFPEseq vs. scRNAseq vs. Xenium
- [ ] cell type transferability 
	
### Importing Xenium in spatialdata--> **Luca, Gleb, and Art1m** 
- [ ] alignment with and deconvolution of visium 
- [ ] alignment with h&e and ROI selection
	
### Automatic ROI/niche selection from xenium --> **Elyas and Art1m**
- [ ] evaluation with H&E
	
### Gene panel selection --> **Elyas and Art0m**
- [ ] gene module 
- [ ] spatially variable genes
- [ ] Visium deconv.
	
### Cell typing --> **Elyas, Art0m, Olga | Txsim/MCMICRO**
- [ ] defining QC metrics
- [ ] maybe look into SpatialTX
	
### Finding clones in space --> **Art0m and Olga**
- [ ] H&E annotation for ducts/domains
- [ ] Visium based + Xenium + H&E
	
### Post processing --> **Elays and Art0m**
- [ ] ideas for cell-cell comm. 
