import React, { useState, useRef } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Badge } from '../ui/badge';
import { 
  Scan, 
  Camera, 
  Keyboard, 
  CheckCircle, 
  AlertCircle, 
  Loader2,
  Package
} from 'lucide-react';
import openFoodFactsService from '../../services/openFoodFactsService';

const NutritionBarScanner = ({ userId, onProductScanned }) => {
  const [scanMode, setScanMode] = useState('manual'); // 'manual' or 'camera'
  const [manualBarcode, setManualBarcode] = useState('');
  const [scannedProduct, setScannedProduct] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [error, setError] = useState(null);
  const [scanHistory, setScanHistory] = useState([]);
  
  const fileInputRef = useRef(null);

  const handleManualBarcodeSubmit = async () => {
    if (!manualBarcode.trim()) return;

    // Validate barcode format
    const validation = openFoodFactsService.validateBarcode(manualBarcode);
    if (!validation.valid) {
      setError(validation.error);
      return;
    }

    await lookupBarcode(validation.barcode);
  };

  const lookupBarcode = async (barcode) => {
    setIsScanning(true);
    setError(null);
    setScannedProduct(null);

    try {
      const result = await openFoodFactsService.getProductByBarcode(barcode);

      if (result.success && result.product) {
        setScannedProduct(result.product);
        
        // Add to scan history
        const historyItem = {
          barcode,
          product: result.product,
          timestamp: new Date().toISOString()
        };
        setScanHistory(prev => [historyItem, ...prev.slice(0, 4)]);
        
        setManualBarcode(''); // Clear input
      } else {
        setError(result.error || 'Product not found. Try entering the barcode manually or use photo recognition instead.');
      }
    } catch (error) {
      console.error('Barcode lookup error:', error);
      setError('An error occurred while looking up the barcode');
    } finally {
      setIsScanning(false);
    }
  };

  const handleProductAdd = () => {
    if (scannedProduct && onProductScanned) {
      onProductScanned(scannedProduct);
      setScannedProduct(null);
      setError(null);
    }
  };

  const clearResult = () => {
    setScannedProduct(null);
    setError(null);
    setManualBarcode('');
  };

  // Sample popular barcodes for testing
  const sampleBarcodes = [
    { barcode: '0041520893304', name: 'Quaker Oats Original' },
    { barcode: '0074570087648', name: 'Greek Yogurt Plain' },
    { barcode: '0012345678905', name: 'Sample Product' },
    { barcode: '3017624010701', name: 'Nutella Hazelnut Spread' },
    { barcode: '7613036817042', name: 'Nestlé KitKat' }
  ];

  const NutritionInfo = ({ product }) => (
    <div className="space-y-3">
      <div className="flex items-start gap-3">
        {product.image && (
          <img 
            src={product.image} 
            alt={product.name}
            className="w-20 h-20 object-cover rounded-lg border"
          />
        )}
        <div className="flex-1">
          <h3 className="font-semibold text-lg text-green-900">{product.name}</h3>
          {product.brand && (
            <p className="text-green-700 text-sm">{product.brand}</p>
          )}
          <div className="flex gap-2 mt-2">
            <Badge variant="outline">
              📊 {product.source === 'usda' ? 'USDA' : 'OpenFoodFacts'}
            </Badge>
            {product.nutritionGrade && (
              <Badge className={
                product.nutritionGrade.toLowerCase() === 'a' ? 'bg-green-100 text-green-800' :
                product.nutritionGrade.toLowerCase() === 'b' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }>
                Grade: {product.nutritionGrade.toUpperCase()}
              </Badge>
            )}
          </div>
        </div>
      </div>

      {/* Nutrition Facts */}
      <div className="bg-white border-2 border-gray-300 rounded-lg p-4">
        <h4 className="font-bold text-center border-b-2 border-gray-800 pb-1 mb-3">
          Nutrition Facts
        </h4>
        <div className="text-sm space-y-2">
          <div className="flex justify-between items-center border-b border-gray-200 pb-1">
            <span className="font-medium">Serving Size</span>
            <span>{product.nutrition.servingSize || '100g'}</span>
          </div>
          <div className="flex justify-between items-center text-lg font-bold border-b-4 border-gray-800 pb-2">
            <span>Calories</span>
            <span>{product.nutrition.calories || 0}</span>
          </div>
          
          <div className="space-y-1">
            <div className="flex justify-between">
              <span className="font-medium">Total Fat</span>
              <span className="font-medium">{product.nutrition.fat || 0}g</span>
            </div>
            <div className="flex justify-between">
              <span className="font-medium">Total Carbohydrates</span>
              <span className="font-medium">{product.nutrition.carbs || 0}g</span>
            </div>
            {product.nutrition.fiber > 0 && (
              <div className="flex justify-between ml-4">
                <span>Dietary Fiber</span>
                <span>{product.nutrition.fiber}g</span>
              </div>
            )}
            {product.nutrition.sugar > 0 && (
              <div className="flex justify-between ml-4">
                <span>Total Sugars</span>
                <span>{product.nutrition.sugar}g</span>
              </div>
            )}
            <div className="flex justify-between">
              <span className="font-medium">Protein</span>
              <span className="font-medium">{product.nutrition.protein || 0}g</span>
            </div>
            {product.nutrition.sodium > 0 && (
              <div className="flex justify-between">
                <span className="font-medium">Sodium</span>
                <span className="font-medium">{product.nutrition.sodium}mg</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Additional Info */}
      {(product.ingredients || product.categories.length > 0 || product.allergens.length > 0) && (
        <div className="space-y-2 text-sm">
          {product.categories.length > 0 && (
            <div>
              <span className="font-medium text-gray-700">Categories: </span>
              <span className="text-gray-600">
                {product.categories.slice(0, 3).join(', ')}
              </span>
            </div>
          )}
          {product.ingredients && (
            <div>
              <span className="font-medium text-gray-700">Ingredients: </span>
              <span className="text-gray-600">
                {product.ingredients.substring(0, 200)}
                {product.ingredients.length > 200 ? '...' : ''}
              </span>
            </div>
          )}
          {product.allergens.length > 0 && (
            <div>
              <span className="font-medium text-red-700">Allergens: </span>
              <span className="text-red-600">
                {product.allergens.slice(0, 5).join(', ')}
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Package className="h-5 w-5" />
            Barcode Scanner
          </CardTitle>
          <p className="text-sm text-gray-600">
            Scan or enter a product barcode to instantly get nutrition information
          </p>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Scan Mode Selector */}
          <div className="flex gap-2">
            <Button
              variant={scanMode === 'manual' ? 'default' : 'outline'}
              onClick={() => setScanMode('manual')}
              className="flex-1"
            >
              <Keyboard className="h-4 w-4 mr-2" />
              Manual Entry
            </Button>
            <Button
              variant={scanMode === 'camera' ? 'default' : 'outline'}
              onClick={() => setScanMode('camera')}
              className="flex-1"
              disabled
            >
              <Camera className="h-4 w-4 mr-2" />
              Camera Scan
              <Badge variant="secondary" className="ml-2">Coming Soon</Badge>
            </Button>
          </div>

          {/* Manual Barcode Entry */}
          {scanMode === 'manual' && (
            <div className="space-y-4">
              <div className="flex gap-2">
                <Input
                  placeholder="Enter barcode (e.g., 0041520893304)"
                  value={manualBarcode}
                  onChange={(e) => setManualBarcode(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleManualBarcodeSubmit()}
                  disabled={isScanning}
                />
                <Button
                  onClick={handleManualBarcodeSubmit}
                  disabled={!manualBarcode.trim() || isScanning}
                >
                  {isScanning ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Scanning...
                    </>
                  ) : (
                    <>
                      <Scan className="h-4 w-4 mr-2" />
                      Lookup
                    </>
                  )}
                </Button>
              </div>

              {/* Sample Barcodes for Testing */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 className="font-medium text-blue-900 mb-2">Try these sample barcodes:</h4>
                <div className="flex flex-wrap gap-2">
                  {sampleBarcodes.map((sample, index) => (
                    <Button
                      key={index}
                      variant="outline"
                      size="sm"
                      onClick={() => setManualBarcode(sample.barcode)}
                      className="text-xs"
                    >
                      {sample.name}
                    </Button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Camera Scan Mode (Placeholder) */}
          {scanMode === 'camera' && (
            <div className="text-center py-8">
              <Camera className="h-16 w-16 mx-auto mb-4 text-gray-400" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Camera Scanner Coming Soon
              </h3>
              <p className="text-gray-600 mb-4">
                Camera-based barcode scanning will be available in a future update.
              </p>
              <Button variant="outline" onClick={() => setScanMode('manual')}>
                Use Manual Entry Instead
              </Button>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-800">
              <AlertCircle className="h-5 w-5" />
              <span className="text-sm">{error}</span>
            </div>
          )}

          {/* Scanned Product Results */}
          {scannedProduct && (
            <Card className="border-green-200 bg-green-50">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <CardTitle className="text-lg text-green-900">Product Found!</CardTitle>
                  </div>
                  <div className="flex gap-2">
                    <Button onClick={handleProductAdd}>
                      Add to Food Log
                    </Button>
                    <Button variant="outline" onClick={clearResult}>
                      Clear
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <NutritionInfo product={scannedProduct} />
              </CardContent>
            </Card>
          )}

          {/* Scan History */}
          {scanHistory.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Recent Scans</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {scanHistory.map((item, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer"
                      onClick={() => lookupBarcode(item.barcode)}
                    >
                      <div className="flex items-center gap-3">
                        {item.product.image && (
                          <img 
                            src={item.product.image}
                            alt={item.product.name}
                            className="w-8 h-8 object-cover rounded"
                          />
                        )}
                        <div>
                          <p className="font-medium text-sm">{item.product.name}</p>
                          <p className="text-xs text-gray-500">
                            {item.barcode} • {new Date(item.timestamp).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                      <Button size="sm" variant="outline">
                        <Scan className="h-3 w-3" />
                      </Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Instructions */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <h4 className="font-medium text-yellow-900 mb-2">How to find barcodes:</h4>
            <ul className="text-sm text-yellow-800 space-y-1">
              <li>• Look for the black and white striped barcode on product packaging</li>
              <li>• The barcode number is usually printed below the stripes</li>
              <li>• Common barcode formats: UPC-A (12 digits), EAN-13 (13 digits)</li>
              <li>• Most packaged foods, drinks, and supplements have barcodes</li>
              <li>• Fresh produce may not have barcodes - use search or photo recognition instead</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default NutritionBarScanner;