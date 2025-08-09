import React from 'react';
import { Label } from '../ui/label';
import { Input } from '../ui/input';
import { Textarea } from '../ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Checkbox } from '../ui/checkbox';
import { RadioGroup, RadioGroupItem } from '../ui/radio-group';
import { Alert, AlertDescription } from '../ui/alert';
import { AlertCircle, HelpCircle } from 'lucide-react';
import { Popover, PopoverContent, PopoverTrigger } from '../ui/popover';

const FormField = ({
  type = 'input',
  label,
  value,
  onChange,
  placeholder,
  required = false,
  error,
  helpText,
  options = [],
  rows = 3,
  min,
  max,
  step,
  disabled = false,
  className = '',
  ...props
}) => {
  const fieldId = React.useId();

  const renderField = () => {
    switch (type) {
      case 'input':
      case 'email':
      case 'number':
      case 'tel':
      case 'password':
        return (
          <Input
            id={fieldId}
            type={type}
            value={value || ''}
            onChange={(e) => onChange(e.target.value)}
            placeholder={placeholder}
            disabled={disabled}
            min={min}
            max={max}
            step={step}
            className={error ? 'border-red-500' : ''}
            {...props}
          />
        );

      case 'textarea':
        return (
          <Textarea
            id={fieldId}
            value={value || ''}
            onChange={(e) => onChange(e.target.value)}
            placeholder={placeholder}
            disabled={disabled}
            rows={rows}
            className={error ? 'border-red-500' : ''}
            {...props}
          />
        );

      case 'select':
        return (
          <Select value={value} onValueChange={onChange} disabled={disabled}>
            <SelectTrigger className={error ? 'border-red-500' : ''}>
              <SelectValue placeholder={placeholder || 'Select an option'} />
            </SelectTrigger>
            <SelectContent>
              {options.map((option) => (
                <SelectItem key={option.value} value={option.value}>
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        );

      case 'checkbox':
        return (
          <div className="flex items-center space-x-2">
            <Checkbox
              id={fieldId}
              checked={value || false}
              onCheckedChange={onChange}
              disabled={disabled}
            />
            <Label htmlFor={fieldId} className="text-sm font-normal">
              {label}
            </Label>
          </div>
        );

      case 'radio':
        return (
          <RadioGroup value={value} onValueChange={onChange} disabled={disabled}>
            {options.map((option) => (
              <div key={option.value} className="flex items-center space-x-2">
                <RadioGroupItem value={option.value} id={`${fieldId}-${option.value}`} />
                <Label htmlFor={`${fieldId}-${option.value}`} className="text-sm font-normal">
                  {option.label}
                </Label>
              </div>
            ))}
          </RadioGroup>
        );

      default:
        return null;
    }
  };

  if (type === 'checkbox') {
    return (
      <div className={`space-y-2 ${className}`}>
        {renderField()}
        {helpText && (
          <p className="text-sm text-gray-500">{helpText}</p>
        )}
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
      </div>
    );
  }

  return (
    <div className={`space-y-2 ${className}`}>
      {label && (
        <div className="flex items-center space-x-2">
          <Label htmlFor={fieldId} className="text-sm font-medium">
            {label}
            {required && <span className="text-red-500 ml-1">*</span>}
          </Label>
          {helpText && (
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger>
                  <HelpCircle className="h-4 w-4 text-gray-400" />
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-xs">{helpText}</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          )}
        </div>
      )}

      {renderField()}

      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
    </div>
  );
};

export default FormField;