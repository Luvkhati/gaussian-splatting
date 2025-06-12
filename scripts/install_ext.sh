#!/bin/bash
cd submodules/simple-knn && python setup.py install && cd ../..
cd submodules/diff-gaussian-rasterization && python setup.py install && cd ../..
cd submodules/fused-ssim && python setup.py install && cd ../..
