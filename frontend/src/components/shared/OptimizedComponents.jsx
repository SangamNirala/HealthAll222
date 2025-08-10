import React, { useState, useEffect, useMemo } from 'react';
import { useResponsive, useDebounce, useLazyLoad } from '../../hooks/useResponsive';

// Optimized image component with lazy loading
export const OptimizedImage = ({ 
  src, 
  alt, 
  className = '', 
  fallback = '/placeholder.jpg',
  sizes = '(max-width: 768px) 100vw, (max-width: 1024px) 50vw, 33vw'
}) => {
  const [imageRef, isVisible] = useLazyLoad();
  const [isLoaded, setIsLoaded] = useState(false);
  const [error, setError] = useState(false);
  const { isMobile } = useResponsive();

  const optimizedSrc = useMemo(() => {
    if (!src) return fallback;
    
    // Add responsive image parameters for mobile
    if (isMobile && src.includes('unsplash')) {
      return `${src}&w=400&q=80`;
    } else if (src.includes('unsplash')) {
      return `${src}&w=800&q=85`;
    }
    
    return src;
  }, [src, isMobile, fallback]);

  return (
    <div ref={imageRef} className={`overflow-hidden ${className}`}>
      {isVisible && (
        <img
          src={optimizedSrc}
          alt={alt}
          sizes={sizes}
          className={`transition-opacity duration-300 ${isLoaded ? 'opacity-100' : 'opacity-0'} ${className}`}
          onLoad={() => setIsLoaded(true)}
          onError={() => setError(true)}
          loading="lazy"
        />
      )}
      
      {/* Loading placeholder */}
      {!isLoaded && !error && (
        <div className={`bg-gray-200 animate-pulse ${className}`} />
      )}
      
      {/* Error fallback */}
      {error && (
        <div className={`bg-gray-100 flex items-center justify-center ${className}`}>
          <span className="text-gray-400 text-sm">Image unavailable</span>
        </div>
      )}
    </div>
  );
};

// Debounced search component for performance
export const DebouncedSearch = ({ 
  onSearch, 
  placeholder = 'Search...', 
  delay = 300,
  className = '' 
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearchTerm = useDebounce(searchTerm, delay);

  useEffect(() => {
    if (onSearch) {
      onSearch(debouncedSearchTerm);
    }
  }, [debouncedSearchTerm, onSearch]);

  return (
    <input
      type="text"
      placeholder={placeholder}
      value={searchTerm}
      onChange={(e) => setSearchTerm(e.target.value)}
      className={`w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent ${className}`}
    />
  );
};

// Virtualized list component for large datasets
export const VirtualizedList = ({ 
  items, 
  itemHeight = 60, 
  containerHeight = 400,
  renderItem,
  className = ''
}) => {
  const [scrollTop, setScrollTop] = useState(0);
  const { windowSize } = useResponsive();

  const visibleItems = useMemo(() => {
    const startIndex = Math.floor(scrollTop / itemHeight);
    const endIndex = Math.min(
      startIndex + Math.ceil(containerHeight / itemHeight) + 1,
      items.length
    );
    
    return items.slice(startIndex, endIndex).map((item, index) => ({
      ...item,
      originalIndex: startIndex + index
    }));
  }, [items, scrollTop, itemHeight, containerHeight]);

  const totalHeight = items.length * itemHeight;
  const offsetY = Math.floor(scrollTop / itemHeight) * itemHeight;

  return (
    <div 
      className={`relative overflow-auto ${className}`}
      style={{ height: containerHeight }}
      onScroll={(e) => setScrollTop(e.target.scrollTop)}
    >
      <div style={{ height: totalHeight }}>
        <div style={{ transform: `translateY(${offsetY}px)` }}>
          {visibleItems.map((item) => (
            <div key={item.originalIndex} style={{ height: itemHeight }}>
              {renderItem(item, item.originalIndex)}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Memoized card component to prevent unnecessary re-renders
export const MemoizedCard = React.memo(({ 
  title, 
  content, 
  actions, 
  className = '',
  theme = 'blue' 
}) => {
  const getThemeClasses = () => {
    switch (theme) {
      case 'blue':
        return 'border-blue-200 bg-blue-50';
      case 'emerald':
        return 'border-emerald-200 bg-emerald-50';
      case 'amber':
        return 'border-amber-200 bg-amber-50';
      case 'purple':
        return 'border-purple-200 bg-purple-50';
      default:
        return 'border-gray-200 bg-gray-50';
    }
  };

  return (
    <div className={`border rounded-lg p-4 ${getThemeClasses()} ${className}`}>
      {title && (
        <h3 className="text-lg font-semibold mb-2 text-gray-900">{title}</h3>
      )}
      
      {content && (
        <div className="text-gray-700 mb-3">{content}</div>
      )}
      
      {actions && (
        <div className="flex items-center space-x-2">{actions}</div>
      )}
    </div>
  );
});

// Responsive grid container
export const ResponsiveGrid = ({ 
  children, 
  minItemWidth = 280,
  gap = 4,
  className = '' 
}) => {
  const { windowSize } = useResponsive();
  
  const columns = Math.max(1, Math.floor(windowSize.width / minItemWidth));
  
  return (
    <div 
      className={`grid gap-${gap} ${className}`}
      style={{ 
        gridTemplateColumns: `repeat(${columns}, 1fr)`,
        gridAutoRows: 'min-content'
      }}
    >
      {children}
    </div>
  );
};

// Performance metrics display component
export const PerformanceMonitor = ({ show = false }) => {
  const [metrics, setMetrics] = useState({
    fps: 0,
    loadTime: 0,
    memoryUsage: 0,
    renderCount: 0
  });

  useEffect(() => {
    if (!show) return;

    let frameCount = 0;
    let lastTime = performance.now();
    let renderCount = 0;

    const measureFPS = () => {
      frameCount++;
      const currentTime = performance.now();
      
      if (currentTime >= lastTime + 1000) {
        setMetrics(prev => ({
          ...prev,
          fps: Math.round(frameCount * 1000 / (currentTime - lastTime)),
          renderCount: ++renderCount
        }));
        
        frameCount = 0;
        lastTime = currentTime;
      }
      
      requestAnimationFrame(measureFPS);
    };

    measureFPS();

    // Monitor load time
    const loadTime = performance.timing
      ? performance.timing.loadEventEnd - performance.timing.navigationStart
      : 0;
    
    setMetrics(prev => ({ ...prev, loadTime }));

    // Monitor memory (if available)
    if (performance.memory) {
      setMetrics(prev => ({
        ...prev,
        memoryUsage: Math.round(performance.memory.usedJSHeapSize / 1024 / 1024)
      }));
    }
  }, [show]);

  if (!show) return null;

  return (
    <div className="fixed bottom-4 right-4 bg-black bg-opacity-80 text-white p-3 rounded-lg text-xs font-mono z-50">
      <div>FPS: {metrics.fps}</div>
      <div>Load: {metrics.loadTime}ms</div>
      <div>Memory: {metrics.memoryUsage}MB</div>
      <div>Renders: {metrics.renderCount}</div>
    </div>
  );
};

// Optimized button with touch feedback
export const OptimizedButton = React.memo(({ 
  children, 
  onClick, 
  disabled = false,
  variant = 'primary',
  size = 'medium',
  className = '',
  ...props 
}) => {
  const [isPressed, setIsPressed] = useState(false);
  const { isTouchDevice } = useResponsive();

  const getVariantClasses = () => {
    switch (variant) {
      case 'primary':
        return 'bg-blue-600 hover:bg-blue-700 text-white';
      case 'secondary':
        return 'bg-gray-200 hover:bg-gray-300 text-gray-900';
      case 'outline':
        return 'border border-gray-300 hover:bg-gray-50 text-gray-700';
      default:
        return 'bg-blue-600 hover:bg-blue-700 text-white';
    }
  };

  const getSizeClasses = () => {
    switch (size) {
      case 'small':
        return 'px-3 py-1.5 text-sm';
      case 'medium':
        return 'px-4 py-2 text-base';
      case 'large':
        return 'px-6 py-3 text-lg';
      default:
        return 'px-4 py-2 text-base';
    }
  };

  const handleTouchStart = () => {
    if (isTouchDevice) setIsPressed(true);
  };

  const handleTouchEnd = () => {
    if (isTouchDevice) setIsPressed(false);
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
      className={`
        ${getVariantClasses()} 
        ${getSizeClasses()}
        ${isPressed ? 'scale-95' : 'scale-100'}
        transition-all duration-150 ease-in-out
        focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
        disabled:opacity-50 disabled:cursor-not-allowed
        rounded-md font-medium
        ${className}
      `}
      {...props}
    >
      {children}
    </button>
  );
});

// Skeleton loading component
export const Skeleton = ({ 
  width = '100%', 
  height = '1rem', 
  className = '',
  variant = 'rounded' 
}) => {
  const getVariantClass = () => {
    switch (variant) {
      case 'circular':
        return 'rounded-full';
      case 'rectangular':
        return 'rounded-none';
      default:
        return 'rounded';
    }
  };

  return (
    <div 
      className={`bg-gray-200 animate-pulse ${getVariantClass()} ${className}`}
      style={{ width, height }}
    />
  );
};

MemoizedCard.displayName = 'MemoizedCard';
OptimizedButton.displayName = 'OptimizedButton';