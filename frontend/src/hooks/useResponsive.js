import { useState, useEffect } from 'react';

// Hook to detect mobile and responsive breakpoints
export const useResponsive = () => {
  const [windowSize, setWindowSize] = useState({
    width: typeof window !== 'undefined' ? window.innerWidth : 1024,
    height: typeof window !== 'undefined' ? window.innerHeight : 768,
  });

  const [isMobile, setIsMobile] = useState(false);
  const [isTablet, setIsTablet] = useState(false);
  const [isDesktop, setIsDesktop] = useState(true);

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      const height = window.innerHeight;
      
      setWindowSize({ width, height });
      setIsMobile(width < 768);
      setIsTablet(width >= 768 && width < 1024);
      setIsDesktop(width >= 1024);
    };

    // Set initial values
    handleResize();

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const getBreakpoint = () => {
    const width = windowSize.width;
    if (width < 640) return 'xs';
    if (width < 768) return 'sm';
    if (width < 1024) return 'md';
    if (width < 1280) return 'lg';
    return 'xl';
  };

  return {
    windowSize,
    isMobile,
    isTablet,
    isDesktop,
    breakpoint: getBreakpoint(),
    // Utility functions
    isMobileOrTablet: isMobile || isTablet,
    isSmallScreen: windowSize.width < 640,
    isTouchDevice: 'ontouchstart' in window || navigator.maxTouchPoints > 0
  };
};

// Responsive grid utility
export const getResponsiveGridCols = (breakpoint, itemCount = 12) => {
  const gridCols = {
    xs: Math.min(itemCount, 1),
    sm: Math.min(itemCount, 2),
    md: Math.min(itemCount, 3),
    lg: Math.min(itemCount, 4),
    xl: Math.min(itemCount, 6)
  };
  
  return gridCols[breakpoint] || gridCols.lg;
};

// Responsive spacing utility
export const getResponsiveSpacing = (breakpoint) => {
  const spacing = {
    xs: 'space-y-2 p-2',
    sm: 'space-y-3 p-3',
    md: 'space-y-4 p-4',
    lg: 'space-y-6 p-6',
    xl: 'space-y-8 p-8'
  };
  
  return spacing[breakpoint] || spacing.md;
};

// Responsive text sizing
export const getResponsiveTextSize = (breakpoint, variant = 'body') => {
  const textSizes = {
    heading: {
      xs: 'text-xl',
      sm: 'text-2xl',
      md: 'text-3xl',
      lg: 'text-4xl',
      xl: 'text-5xl'
    },
    subheading: {
      xs: 'text-lg',
      sm: 'text-xl',
      md: 'text-2xl',
      lg: 'text-3xl',
      xl: 'text-4xl'
    },
    body: {
      xs: 'text-sm',
      sm: 'text-base',
      md: 'text-base',
      lg: 'text-lg',
      xl: 'text-lg'
    },
    small: {
      xs: 'text-xs',
      sm: 'text-sm',
      md: 'text-sm',
      lg: 'text-base',
      xl: 'text-base'
    }
  };
  
  return textSizes[variant]?.[breakpoint] || textSizes[variant]?.md || 'text-base';
};

// Performance optimization utilities
export const useDebounce = (value, delay) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};

// Lazy loading intersection observer
export const useLazyLoad = (options = {}) => {
  const [isIntersecting, setIsIntersecting] = useState(false);
  const [targetRef, setTargetRef] = useState(null);

  useEffect(() => {
    if (!targetRef) return;

    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setIsIntersecting(true);
        observer.disconnect();
      }
    }, {
      threshold: 0.1,
      rootMargin: '50px',
      ...options
    });

    observer.observe(targetRef);

    return () => observer.disconnect();
  }, [targetRef, options]);

  return [setTargetRef, isIntersecting];
};

// Touch gesture utilities for mobile
export const useTouchGestures = () => {
  const [touchStart, setTouchStart] = useState(null);
  const [touchEnd, setTouchEnd] = useState(null);

  const minSwipeDistance = 50;

  const onTouchStart = (e) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientX);
  };

  const onTouchMove = (e) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return;
    
    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;

    return { isLeftSwipe, isRightSwipe, distance };
  };

  return { onTouchStart, onTouchMove, onTouchEnd };
};

// Accessibility utilities
export const getAccessibilityProps = (role, label, description) => {
  const props = {
    role: role || 'button',
    'aria-label': label,
  };

  if (description) {
    props['aria-describedby'] = description;
  }

  return props;
};

// Responsive modal sizing
export const getModalSize = (breakpoint) => {
  const sizes = {
    xs: 'max-w-sm w-11/12',
    sm: 'max-w-md w-11/12',
    md: 'max-w-lg w-5/6',
    lg: 'max-w-2xl w-4/5',
    xl: 'max-w-4xl w-3/4'
  };
  
  return sizes[breakpoint] || sizes.md;
};

// Performance monitoring
export const usePerformanceMonitor = () => {
  const [metrics, setMetrics] = useState({
    renderTime: 0,
    componentCount: 0,
    memoryUsage: 0
  });

  useEffect(() => {
    const startTime = performance.now();

    // Monitor render time
    const observer = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      entries.forEach((entry) => {
        if (entry.entryType === 'measure') {
          setMetrics(prev => ({
            ...prev,
            renderTime: entry.duration
          }));
        }
      });
    });

    observer.observe({ entryTypes: ['measure'] });

    // Monitor memory usage (if available)
    if ('memory' in performance) {
      setMetrics(prev => ({
        ...prev,
        memoryUsage: (performance as any).memory.usedJSHeapSize
      }));
    }

    return () => {
      observer.disconnect();
      const endTime = performance.now();
      console.log(`Component lifecycle: ${endTime - startTime}ms`);
    };
  }, []);

  return metrics;
};