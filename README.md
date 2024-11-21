# NutriVLM Datasets
This repository hosts the dataset branch for the research project **NutriVLM: Optimizing Multimodal Models for Comprehensive Nutritional Assessment**. The dataset serves as a foundation for evaluating multimodal models in food recognition and nutritional analysis.

## Dataset Overview

The dataset comprises a high-quality collection of over **5,000 annotated food images** across **10 food categories**:

- Categories:
  - Fruits
  - Vegetables
  - Western Desserts
  - Western Dishes
  - Chinese Desserts
  - Chinese Dishes
  - Packaged Ready-to-Eat Food
  - Packaged Food Requiring Preparation
  - Beverages
  - Bubble Tea

![image-20241121170638636](.\image-20241121170638636.png)

### Features

1. **Annotations**:
   - Each image is annotated with:
     - Food category
     - Weight (in grams)
     - Nutritional information including calories, protein, fat, and carbohydrates.
2. **Image Quality**:
   - Enhanced via preprocessing techniques such as:
     - Noise reduction
     - Color correction
     - Edge detection
     - Contrast enhancement
     - Sharpening
3. **Dataset Splits**:
   - **Training set**: 70%
   - **Validation set**: 15%
   - **Testing set**: 15%

### Purpose

This dataset is developed for:

- **Food Type Recognition**: Identifying the category of food in an image.
- **Weight Estimation**: Predicting the weight of the food.
- **Nutritional Analysis**: Estimating nutritional values directly from food images.
