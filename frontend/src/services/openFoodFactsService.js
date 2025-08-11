class OpenFoodFactsService {
  constructor() {
    this.baseURL = 'https://world.openfoodfacts.org/api/v0';
    this.usdaBaseURL = 'https://api.nal.usda.gov/fdc/v1';
    this.usdaApiKey = '66fxtMzVPB1BQrLb4cndxu6aGkD4pMveNadUYX8Y'; // Your USDA API key
  }

  async getProductByBarcode(barcode) {
    try {
      // First try Open Food Facts
      const offResponse = await this.getFromOpenFoodFacts(barcode);
      if (offResponse.success) {
        return offResponse;
      }

      // Fallback to USDA FoodData Central
      const usdaResponse = await this.searchUSDAByUPC(barcode);
      return usdaResponse;

    } catch (error) {
      console.error('Barcode lookup error:', error);
      return {
        success: false,
        error: error.message,
        product: null
      };
    }
  }

  async getFromOpenFoodFacts(barcode) {
    try {
      const response = await fetch(`${this.baseURL}/product/${barcode}.json`);
      const data = await response.json();

      if (data.status === 1 && data.product) {
        const product = data.product;
        
        return {
          success: true,
          product: {
            name: product.product_name || 'Unknown Product',
            brand: product.brands || '',
            image: product.image_front_url || product.image_url || null,
            barcode: barcode,
            nutrition: {
              calories: this.getNutrientValue(product.nutriments, 'energy-kcal_100g'),
              protein: this.getNutrientValue(product.nutriments, 'proteins_100g'),
              carbs: this.getNutrientValue(product.nutriments, 'carbohydrates_100g'),
              fat: this.getNutrientValue(product.nutriments, 'fat_100g'),
              fiber: this.getNutrientValue(product.nutriments, 'fiber_100g'),
              sugar: this.getNutrientValue(product.nutriments, 'sugars_100g'),
              sodium: this.getNutrientValue(product.nutriments, 'sodium_100g'),
              servingSize: product.serving_size || '100g'
            },
            categories: product.categories_tags || [],
            ingredients: product.ingredients_text || '',
            allergens: product.allergens_tags || [],
            labels: product.labels_tags || [],
            nutritionGrade: product.nutrition_grades || '',
            source: 'openfoodfacts'
          }
        };
      } else {
        return {
          success: false,
          error: 'Product not found in Open Food Facts',
          product: null
        };
      }
    } catch (error) {
      console.error('Open Food Facts API error:', error);
      return {
        success: false,
        error: error.message,
        product: null
      };
    }
  }

  async searchUSDAByUPC(upc) {
    try {
      const response = await fetch(
        `${this.usdaBaseURL}/foods/search?api_key=${this.usdaApiKey}&query=${upc}&dataType=Branded&pageSize=1`
      );
      
      if (!response.ok) {
        throw new Error(`USDA API error: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.foods && data.foods.length > 0) {
        const food = data.foods[0];
        
        return {
          success: true,
          product: {
            name: food.description || 'Unknown Product',
            brand: food.brandOwner || food.brandName || '',
            image: null, // USDA doesn't provide images
            barcode: upc,
            nutrition: {
              calories: this.getUSDANutrient(food.foodNutrients, 'Energy'),
              protein: this.getUSDANutrient(food.foodNutrients, 'Protein'),
              carbs: this.getUSDANutrient(food.foodNutrients, 'Carbohydrate, by difference'),
              fat: this.getUSDANutrient(food.foodNutrients, 'Total lipid (fat)'),
              fiber: this.getUSDANutrient(food.foodNutrients, 'Fiber, total dietary'),
              sugar: this.getUSDANutrient(food.foodNutrients, 'Sugars, total including NLEA'),
              sodium: this.getUSDANutrient(food.foodNutrients, 'Sodium'),
              servingSize: food.servingSize || '100g'
            },
            categories: food.foodCategory ? [food.foodCategory] : [],
            ingredients: food.ingredients || '',
            allergens: [],
            labels: [],
            nutritionGrade: '',
            source: 'usda'
          }
        };
      } else {
        return {
          success: false,
          error: 'Product not found in USDA database',
          product: null
        };
      }
    } catch (error) {
      console.error('USDA API error:', error);
      return {
        success: false,
        error: error.message,
        product: null
      };
    }
  }

  async searchProducts(query, limit = 20) {
    try {
      // Search in Open Food Facts
      const offResults = await this.searchOpenFoodFacts(query, limit);
      
      // Search in USDA (if OFF results are insufficient)
      const usdaResults = offResults.products.length < limit ? 
        await this.searchUSDA(query, limit - offResults.products.length) : 
        { products: [] };

      return {
        success: true,
        products: [...offResults.products, ...usdaResults.products],
        total: offResults.products.length + usdaResults.products.length
      };
    } catch (error) {
      console.error('Product search error:', error);
      return {
        success: false,
        error: error.message,
        products: []
      };
    }
  }

  async searchOpenFoodFacts(query, limit = 20) {
    try {
      const response = await fetch(
        `${this.baseURL}/cgi/search.pl?search_terms=${encodeURIComponent(query)}&search_simple=1&action=process&json=1&page_size=${limit}`
      );
      
      const data = await response.json();
      
      if (data.products) {
        const products = data.products
          .filter(product => product.product_name && product.nutriments)
          .map(product => ({
            name: product.product_name || 'Unknown Product',
            brand: product.brands || '',
            image: product.image_front_small_url || product.image_small_url || null,
            barcode: product.code || '',
            nutrition: {
              calories: this.getNutrientValue(product.nutriments, 'energy-kcal_100g'),
              protein: this.getNutrientValue(product.nutriments, 'proteins_100g'),
              carbs: this.getNutrientValue(product.nutriments, 'carbohydrates_100g'),
              fat: this.getNutrientValue(product.nutriments, 'fat_100g'),
              servingSize: product.serving_size || '100g'
            },
            categories: product.categories_tags || [],
            nutritionGrade: product.nutrition_grades || '',
            source: 'openfoodfacts'
          }));

        return {
          success: true,
          products,
          total: data.count || products.length
        };
      }

      return {
        success: true,
        products: [],
        total: 0
      };
    } catch (error) {
      console.error('Open Food Facts search error:', error);
      return {
        success: false,
        error: error.message,
        products: []
      };
    }
  }

  async searchUSDA(query, limit = 10) {
    try {
      const response = await fetch(
        `${this.usdaBaseURL}/foods/search?api_key=${this.usdaApiKey}&query=${encodeURIComponent(query)}&pageSize=${limit}`
      );
      
      if (!response.ok) {
        throw new Error(`USDA API error: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.foods) {
        const products = data.foods.map(food => ({
          name: food.description || 'Unknown Product',
          brand: food.brandOwner || food.brandName || '',
          image: null,
          barcode: '',
          nutrition: {
            calories: this.getUSDANutrient(food.foodNutrients, 'Energy'),
            protein: this.getUSDANutrient(food.foodNutrients, 'Protein'),
            carbs: this.getUSDANutrient(food.foodNutrients, 'Carbohydrate, by difference'),
            fat: this.getUSDANutrient(food.foodNutrients, 'Total lipid (fat)'),
            servingSize: '100g'
          },
          categories: food.foodCategory ? [food.foodCategory] : [],
          nutritionGrade: '',
          source: 'usda'
        }));

        return {
          success: true,
          products,
          total: data.totalHits || products.length
        };
      }

      return {
        success: true,
        products: [],
        total: 0
      };
    } catch (error) {
      console.error('USDA search error:', error);
      return {
        success: false,
        error: error.message,
        products: []
      };
    }
  }

  getNutrientValue(nutriments, key) {
    return parseFloat(nutriments[key]) || 0;
  }

  getUSDANutrient(nutrients, nutrientName) {
    if (!nutrients || !Array.isArray(nutrients)) return 0;
    
    const nutrient = nutrients.find(n => 
      n.nutrientName === nutrientName || 
      n.nutrientName?.toLowerCase().includes(nutrientName.toLowerCase())
    );
    
    return nutrient ? parseFloat(nutrient.value) || 0 : 0;
  }

  // Manual barcode entry validation
  validateBarcode(barcode) {
    // Remove any non-numeric characters
    const cleanBarcode = barcode.replace(/\D/g, '');
    
    // Check if it's a valid length (UPC-A: 12 digits, EAN-13: 13 digits, etc.)
    const validLengths = [8, 12, 13, 14];
    
    if (!validLengths.includes(cleanBarcode.length)) {
      return {
        valid: false,
        error: 'Barcode must be 8, 12, 13, or 14 digits long'
      };
    }

    return {
      valid: true,
      barcode: cleanBarcode
    };
  }

  // Get popular/trending foods
  async getPopularFoods(category = '', limit = 20) {
    try {
      const searchTerm = category || 'popular';
      const response = await this.searchOpenFoodFacts(searchTerm, limit);
      
      // Sort by popularity indicators (if available)
      if (response.success && response.products.length > 0) {
        response.products.sort((a, b) => {
          // Prefer products with nutrition grades and images
          const aScore = (a.nutritionGrade ? 1 : 0) + (a.image ? 1 : 0);
          const bScore = (b.nutritionGrade ? 1 : 0) + (b.image ? 1 : 0);
          return bScore - aScore;
        });
      }
      
      return response;
    } catch (error) {
      console.error('Popular foods error:', error);
      return {
        success: false,
        error: error.message,
        products: []
      };
    }
  }
}

export default new OpenFoodFactsService();