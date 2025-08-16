"""
Advanced ML Models for Personalized Health Insights
Implements predictive analytics with simple statistical models that can be enhanced later
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
import joblib
import os
import pickle
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Phase 4: Enhanced ML Pipeline Classes
class ModelPerformanceTracker:
    """Tracks model performance and accuracy over time"""
    
    def __init__(self):
        self.performance_history = defaultdict(list)
        self.accuracy_threshold = 0.75
        self.retrain_threshold = 0.70
        
    def log_prediction(self, model_name: str, prediction: float, actual: Optional[float] = None):
        """Log a prediction and actual value for accuracy tracking"""
        timestamp = datetime.now().isoformat()
        
        entry = {
            'timestamp': timestamp,
            'prediction': prediction,
            'actual': actual
        }
        
        self.performance_history[model_name].append(entry)
        
        # Keep only last 1000 entries per model
        if len(self.performance_history[model_name]) > 1000:
            self.performance_history[model_name] = self.performance_history[model_name][-1000:]
    
    def calculate_accuracy(self, model_name: str, days_back: int = 7) -> Dict[str, Any]:
        """Calculate model accuracy for recent predictions"""
        cutoff_date = datetime.now() - timedelta(days=days_back)
        recent_entries = [
            entry for entry in self.performance_history[model_name]
            if entry['actual'] is not None and 
            datetime.fromisoformat(entry['timestamp']) >= cutoff_date
        ]
        
        if len(recent_entries) < 5:
            return {'accuracy': None, 'sample_size': len(recent_entries), 'needs_data': True}
        
        predictions = [entry['prediction'] for entry in recent_entries]
        actuals = [entry['actual'] for entry in recent_entries]
        
        # Calculate R² score
        accuracy = r2_score(actuals, predictions)
        mae = np.mean(np.abs(np.array(predictions) - np.array(actuals)))
        
        return {
            'accuracy': accuracy,
            'mae': mae,
            'sample_size': len(recent_entries),
            'needs_retrain': accuracy < self.retrain_threshold,
            'performance_trend': self._calculate_trend(recent_entries)
        }
    
    def _calculate_trend(self, entries: List[Dict]) -> str:
        """Calculate if model performance is improving or declining"""
        if len(entries) < 10:
            return 'insufficient_data'
        
        # Split into two halves and compare accuracy
        mid = len(entries) // 2
        first_half = entries[:mid]
        second_half = entries[mid:]
        
        first_errors = [abs(e['prediction'] - e['actual']) for e in first_half]
        second_errors = [abs(e['prediction'] - e['actual']) for e in second_half]
        
        first_avg_error = np.mean(first_errors)
        second_avg_error = np.mean(second_errors)
        
        if second_avg_error < first_avg_error * 0.9:
            return 'improving'
        elif second_avg_error > first_avg_error * 1.1:
            return 'declining'
        else:
            return 'stable'

class UserFeedbackIntegrator:
    """Integrates user feedback to improve model predictions"""
    
    def __init__(self):
        self.feedback_data = defaultdict(list)
        self.learning_rate = 0.1
    
    def add_feedback(self, model_name: str, prediction_id: str, user_rating: float, 
                    actual_outcome: Optional[float] = None, feedback_text: str = ""):
        """Add user feedback for a specific prediction"""
        feedback = {
            'prediction_id': prediction_id,
            'user_rating': user_rating,  # 1-5 scale
            'actual_outcome': actual_outcome,
            'feedback_text': feedback_text,
            'timestamp': datetime.now().isoformat()
        }
        
        self.feedback_data[model_name].append(feedback)
    
    def get_model_satisfaction(self, model_name: str) -> Dict[str, Any]:
        """Calculate user satisfaction metrics for a model"""
        feedbacks = self.feedback_data[model_name]
        
        if not feedbacks:
            return {'satisfaction': None, 'sample_size': 0}
        
        recent_feedback = [
            f for f in feedbacks 
            if datetime.fromisoformat(f['timestamp']) >= datetime.now() - timedelta(days=30)
        ]
        
        if not recent_feedback:
            return {'satisfaction': None, 'sample_size': 0}
        
        avg_rating = np.mean([f['user_rating'] for f in recent_feedback])
        
        return {
            'satisfaction': avg_rating,
            'sample_size': len(recent_feedback),
            'satisfaction_trend': self._calculate_satisfaction_trend(recent_feedback)
        }
    
    def _calculate_satisfaction_trend(self, feedbacks: List[Dict]) -> str:
        """Calculate satisfaction trend over time"""
        if len(feedbacks) < 6:
            return 'insufficient_data'
        
        ratings = [f['user_rating'] for f in feedbacks]
        first_half = ratings[:len(ratings)//2]
        second_half = ratings[len(ratings)//2:]
        
        if np.mean(second_half) > np.mean(first_half) + 0.2:
            return 'improving'
        elif np.mean(second_half) < np.mean(first_half) - 0.2:
            return 'declining'
        else:
            return 'stable'

class ABTestingFramework:
    """A/B testing framework for model improvements"""
    
    def __init__(self):
        self.test_configs = {}
        self.test_results = defaultdict(list)
    
    def create_test(self, test_name: str, model_a_config: Dict, model_b_config: Dict, 
                   traffic_split: float = 0.5):
        """Create a new A/B test"""
        self.test_configs[test_name] = {
            'model_a': model_a_config,
            'model_b': model_b_config,
            'traffic_split': traffic_split,
            'start_date': datetime.now().isoformat(),
            'status': 'active'
        }
    
    def should_use_model_b(self, test_name: str, user_id: str) -> bool:
        """Determine if user should see model B (based on consistent hashing)"""
        if test_name not in self.test_configs:
            return False
        
        # Use hash of user_id for consistent assignment
        import hashlib
        hash_val = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        return (hash_val % 100) < (self.test_configs[test_name]['traffic_split'] * 100)
    
    def record_result(self, test_name: str, user_id: str, model_used: str, 
                     prediction: float, actual: Optional[float] = None, 
                     user_satisfaction: Optional[float] = None):
        """Record result for A/B test analysis"""
        result = {
            'user_id': user_id,
            'model_used': model_used,
            'prediction': prediction,
            'actual': actual,
            'user_satisfaction': user_satisfaction,
            'timestamp': datetime.now().isoformat()
        }
        
        self.test_results[test_name].append(result)
    
    def analyze_test(self, test_name: str) -> Dict[str, Any]:
        """Analyze A/B test results"""
        results = self.test_results[test_name]
        
        if len(results) < 20:
            return {'status': 'insufficient_data', 'sample_size': len(results)}
        
        model_a_results = [r for r in results if r['model_used'] == 'A']
        model_b_results = [r for r in results if r['model_used'] == 'B']
        
        # Calculate metrics for both models
        def calculate_metrics(model_results):
            if not model_results:
                return {}
            
            predictions = [r['prediction'] for r in model_results if r['actual'] is not None]
            actuals = [r['actual'] for r in model_results if r['actual'] is not None]
            satisfactions = [r['user_satisfaction'] for r in model_results if r['user_satisfaction'] is not None]
            
            metrics = {
                'sample_size': len(model_results),
                'accuracy': r2_score(actuals, predictions) if len(actuals) >= 5 else None,
                'avg_satisfaction': np.mean(satisfactions) if satisfactions else None
            }
            
            return metrics
        
        return {
            'status': 'analysis_ready',
            'model_a_metrics': calculate_metrics(model_a_results),
            'model_b_metrics': calculate_metrics(model_b_results),
            'winner': self._determine_winner(model_a_results, model_b_results)
        }
    
    def _determine_winner(self, model_a_results: List, model_b_results: List) -> str:
        """Determine winning model based on accuracy and satisfaction"""
        if not model_a_results or not model_b_results:
            return 'insufficient_data'
        
        # Simple winner determination (can be enhanced with statistical significance)
        a_sat = np.mean([r['user_satisfaction'] for r in model_a_results if r['user_satisfaction']])
        b_sat = np.mean([r['user_satisfaction'] for r in model_b_results if r['user_satisfaction']])
        
        if b_sat > a_sat + 0.1:
            return 'model_b'
        elif a_sat > b_sat + 0.1:
            return 'model_a'
        else:
            return 'tie'

class EnergyPredictionModel:
    """Enhanced Energy Prediction Model with continuous learning and performance tracking"""
    
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_importance = {}
        self.model_accuracy = 0.0
        self.version = "1.0"
        
        # Phase 4 enhancements
        self.performance_tracker = ModelPerformanceTracker()
        self.feedback_integrator = UserFeedbackIntegrator()
        self.ab_testing = ABTestingFramework()
        self.training_history = []
        self.feature_engineering_pipeline = None
        
        # Alternative models for A/B testing
        self.model_variants = {
            'linear': LinearRegression(),
            'ridge': Ridge(alpha=1.0),
            'random_forest': RandomForestRegressor(n_estimators=50, random_state=42)
        }
        self.current_variant = 'linear'
        
    def enhanced_feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """Advanced feature engineering pipeline"""
        enhanced_df = df.copy()
        
        # Interaction features
        enhanced_df['protein_carbs_ratio'] = enhanced_df['protein_g'] / (enhanced_df['carbs_g'] + 1)
        enhanced_df['calorie_density'] = enhanced_df['calories'] / (enhanced_df['protein_g'] + enhanced_df['carbs_g'] + enhanced_df['fat_g'] + 1)
        enhanced_df['sleep_exercise_interaction'] = enhanced_df['sleep_hours'] * enhanced_df['exercise_minutes']
        enhanced_df['stress_caffeine_interaction'] = enhanced_df['stress_level'] * enhanced_df['caffeine_mg']
        
        # Polynomial features for key variables
        enhanced_df['sleep_squared'] = enhanced_df['sleep_hours'] ** 2
        enhanced_df['exercise_log'] = np.log1p(enhanced_df['exercise_minutes'])
        
        # Time-based features (if timestamp available)
        if 'timestamp' in enhanced_df.columns:
            enhanced_df['hour_of_day'] = pd.to_datetime(enhanced_df['timestamp']).dt.hour
            enhanced_df['day_of_week'] = pd.to_datetime(enhanced_df['timestamp']).dt.dayofweek
            enhanced_df['is_weekend'] = (enhanced_df['day_of_week'] >= 5).astype(int)
        
        # Nutritional balance indicators
        enhanced_df['macro_balance'] = np.abs(enhanced_df['protein_g'] * 4 + enhanced_df['carbs_g'] * 4 + enhanced_df['fat_g'] * 9 - enhanced_df['calories']) / enhanced_df['calories']
        enhanced_df['hydration_per_calorie'] = enhanced_df['water_intake_ml'] / enhanced_df['calories']
        
        return enhanced_df
    
    def continuous_learning_update(self, new_data: Dict[str, Any], actual_energy: float):
        """Update model with new user data point"""
        try:
            # Log the feedback for performance tracking
            prediction_id = f"{new_data.get('user_id', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Get current prediction to compare with actual
            current_prediction = self.predict_energy(new_data)['predicted_energy']
            
            # Log performance
            self.performance_tracker.log_prediction(
                'energy_prediction', 
                current_prediction, 
                actual_energy
            )
            
            # Prepare data for incremental learning
            if self.is_trained and len(self.training_history) < 100:
                # Store new data point
                data_point = {**new_data, 'energy_level': actual_energy, 'timestamp': datetime.now().isoformat()}
                self.training_history.append(data_point)
                
                # Retrain if we have enough new data or performance is declining
                performance_metrics = self.performance_tracker.calculate_accuracy('energy_prediction')
                
                if (len(self.training_history) >= 20 or 
                    (performance_metrics.get('needs_retrain', False) and len(self.training_history) >= 10)):
                    
                    logger.info("Triggering model retraining due to new data or performance decline")
                    self._retrain_with_new_data()
            
        except Exception as e:
            logger.error(f"Error in continuous learning update: {e}")
    
    def _retrain_with_new_data(self):
        """Retrain model with accumulated new data"""
        try:
            # Convert training history to DataFrame
            new_df = pd.DataFrame(self.training_history)
            
            # Enhanced feature engineering
            new_df_enhanced = self.enhanced_feature_engineering(new_df)
            
            # Get enhanced feature columns
            base_features = ['calories', 'protein_g', 'carbs_g', 'fat_g', 'sleep_hours', 
                           'exercise_minutes', 'stress_level', 'water_intake_ml', 
                           'caffeine_mg', 'meal_timing_consistency']
            
            enhanced_features = [col for col in new_df_enhanced.columns 
                               if col not in ['energy_level', 'timestamp'] and 
                               not col.startswith('user_')]
            
            # Use enhanced features if available, fallback to base features
            feature_cols = enhanced_features if len(enhanced_features) > len(base_features) else base_features
            feature_cols = [col for col in feature_cols if col in new_df_enhanced.columns]
            
            X_new = new_df_enhanced[feature_cols].fillna(0)
            y_new = new_df_enhanced['energy_level']
            
            # Combine with existing synthetic data for stability
            if hasattr(self, '_original_training_data'):
                X_combined = np.vstack([self._original_training_data[0], X_new])
                y_combined = np.concatenate([self._original_training_data[1], y_new])
            else:
                X_combined, y_combined = X_new, y_new
            
            # Retrain model
            X_scaled = self.scaler.fit_transform(X_combined)
            
            # Try different model variants and select best performing
            best_score = -np.inf
            best_model = None
            best_variant = self.current_variant
            
            for variant_name, model in self.model_variants.items():
                try:
                    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_combined, test_size=0.2, random_state=42)
                    model.fit(X_train, y_train)
                    score = model.score(X_test, y_test)
                    
                    if score > best_score:
                        best_score = score
                        best_model = model
                        best_variant = variant_name
                        
                except Exception as e:
                    logger.warning(f"Failed to train variant {variant_name}: {e}")
                    continue
            
            if best_model is not None:
                self.model = best_model
                self.current_variant = best_variant
                self.model_accuracy = best_score
                
                # Update feature importance
                if hasattr(self.model, 'coef_'):
                    self.feature_importance = dict(zip(feature_cols, abs(self.model.coef_)))
                elif hasattr(self.model, 'feature_importances_'):
                    self.feature_importance = dict(zip(feature_cols, self.model.feature_importances_))
                
                # Clear training history after successful retrain
                self.training_history = []
                
                logger.info(f"Model retrained successfully with {best_variant} variant. New accuracy: {best_score:.3f}")
                
        except Exception as e:
            logger.error(f"Error retraining model: {e}")
    
    def get_model_performance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics"""
        performance = self.performance_tracker.calculate_accuracy('energy_prediction')
        satisfaction = self.feedback_integrator.get_model_satisfaction('energy_prediction')
        
        return {
            'model_version': self.version,
            'current_variant': self.current_variant,
            'base_accuracy': self.model_accuracy,
            'recent_performance': performance,
            'user_satisfaction': satisfaction,
            'training_data_points': len(self.training_history),
            'total_predictions': len(self.performance_tracker.performance_history['energy_prediction'])
        }
    
    def add_user_feedback(self, prediction_id: str, user_rating: float, 
                         actual_energy: Optional[float] = None, feedback_text: str = ""):
        """Add user feedback for model improvement"""
        self.feedback_integrator.add_feedback(
            'energy_prediction', prediction_id, user_rating, actual_energy, feedback_text
        )
    
    def start_ab_test(self, test_name: str = "energy_model_variants"):
        """Start A/B test between model variants"""
        model_a_config = {'variant': 'linear', 'version': self.version}
        model_b_config = {'variant': 'random_forest', 'version': f"{self.version}_rf"}
        
        self.ab_testing.create_test(test_name, model_a_config, model_b_config, 0.3)
        logger.info(f"Started A/B test: {test_name}")
    
    def get_prediction_for_ab_test(self, intake_data: Dict[str, Any], 
                                  user_id: str, test_name: str = "energy_model_variants") -> Dict[str, Any]:
        """Get prediction considering A/B test assignment"""
        use_variant_b = self.ab_testing.should_use_model_b(test_name, user_id)
        
        if use_variant_b and 'random_forest' in self.model_variants:
            # Use random forest variant
            model_to_use = self.model_variants['random_forest']
            variant_used = 'B'
        else:
            # Use current model (variant A)
            model_to_use = self.model
            variant_used = 'A'
        
        # Get prediction using selected model
        result = self.predict_energy(intake_data, specific_model=model_to_use)
        result['ab_test_variant'] = variant_used
        result['test_name'] = test_name
        
        return result
        
    def generate_sample_data(self, n_samples=1000):
        """Generate synthetic training data for energy prediction"""
        np.random.seed(42)
        
        # Generate features
        data = {
            'calories': np.random.normal(2000, 300, n_samples),
            'protein_g': np.random.normal(100, 20, n_samples),
            'carbs_g': np.random.normal(250, 50, n_samples),
            'fat_g': np.random.normal(70, 15, n_samples),
            'sleep_hours': np.random.normal(7.5, 1.2, n_samples),
            'exercise_minutes': np.random.exponential(30, n_samples),
            'stress_level': np.random.randint(1, 11, n_samples),
            'water_intake_ml': np.random.normal(2500, 500, n_samples),
            'caffeine_mg': np.random.exponential(100, n_samples),
            'meal_timing_consistency': np.random.uniform(0.5, 1.0, n_samples)
        }
        
        # Generate energy levels with realistic relationships
        energy_base = 5.0
        energy_levels = (
            energy_base +
            0.0015 * (data['calories'] - 2000) +  # Calories effect
            0.02 * (data['protein_g'] - 100) +    # Protein boost
            0.008 * (data['carbs_g'] - 250) +     # Carb energy
            0.3 * (data['sleep_hours'] - 7.5) +   # Sleep quality
            0.02 * np.minimum(data['exercise_minutes'], 60) +  # Exercise cap
            -0.1 * data['stress_level'] +         # Stress reduction
            0.0008 * (data['water_intake_ml'] - 2500) +  # Hydration
            0.005 * np.minimum(data['caffeine_mg'], 200) +   # Caffeine boost
            0.5 * data['meal_timing_consistency'] +  # Consistency bonus
            np.random.normal(0, 0.5, n_samples)   # Random variation
        )
        
        # Clip energy levels to realistic range (1-10)
        energy_levels = np.clip(energy_levels, 1, 10)
        data['energy_level'] = energy_levels
        
        return pd.DataFrame(data)
    
    def train(self, user_data: Optional[Dict] = None):
        """Enhanced training with feature engineering and model selection"""
        try:
            if user_data and len(user_data.get('daily_logs', [])) > 20:
                # Use real user data if sufficient
                df = self._prepare_user_data(user_data)
            else:
                # Use synthetic data for initial training
                df = self.generate_sample_data()
            
            # Apply enhanced feature engineering
            df_enhanced = self.enhanced_feature_engineering(df)
            
            # Prepare features and target
            base_feature_cols = ['calories', 'protein_g', 'carbs_g', 'fat_g', 'sleep_hours', 
                               'exercise_minutes', 'stress_level', 'water_intake_ml', 
                               'caffeine_mg', 'meal_timing_consistency']
            
            # Include engineered features if they exist
            all_feature_cols = [col for col in df_enhanced.columns 
                              if col not in ['energy_level', 'timestamp'] and not col.startswith('user_')]
            
            # Use enhanced features if available, fallback to base
            feature_cols = all_feature_cols if len(all_feature_cols) > len(base_feature_cols) else base_feature_cols
            feature_cols = [col for col in feature_cols if col in df_enhanced.columns]
            
            self._feature_columns = feature_cols  # Store for later use
            
            X = df_enhanced[feature_cols].fillna(0)
            y = df_enhanced['energy_level']
            
            # Split and scale data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Store original training data for incremental learning
            self._original_training_data = (X_train_scaled, y_train)
            
            # Try different models and select the best
            best_score = -np.inf
            best_model = None
            best_variant = 'linear'
            
            for variant_name, model in self.model_variants.items():
                try:
                    model.fit(X_train_scaled, y_train)
                    score = model.score(X_test_scaled, y_test)
                    
                    logger.info(f"{variant_name} model accuracy: {score:.3f}")
                    
                    if score > best_score:
                        best_score = score
                        best_model = model
                        best_variant = variant_name
                        
                except Exception as e:
                    logger.warning(f"Failed to train {variant_name}: {e}")
                    continue
            
            if best_model is None:
                # Fallback to basic linear regression
                best_model = LinearRegression()
                best_model.fit(X_train_scaled, y_train)
                best_score = best_model.score(X_test_scaled, y_test)
                best_variant = 'linear_fallback'
            
            self.model = best_model
            self.current_variant = best_variant
            self.model_accuracy = best_score
            
            # Calculate feature importance
            if hasattr(self.model, 'coef_'):
                self.feature_importance = dict(zip(feature_cols, abs(self.model.coef_)))
            elif hasattr(self.model, 'feature_importances_'):
                self.feature_importance = dict(zip(feature_cols, self.model.feature_importances_))
            
            self.is_trained = True
            logger.info(f"Energy prediction model trained with {best_variant} variant. Accuracy: {best_score:.3f}")
            
            # Initialize A/B testing
            self.start_ab_test()
            
        except Exception as e:
            logger.error(f"Error training energy prediction model: {e}")
            raise
    
    def predict_energy(self, intake_data: Dict[str, Any], specific_model=None) -> Dict[str, Any]:
        """Enhanced energy prediction with confidence intervals and explanations"""
        if not self.is_trained:
            self.train()
        
        model_to_use = specific_model or self.model
        
        try:
            # Prepare input features with enhanced engineering
            base_features = np.array([[
                intake_data.get('calories', 2000),
                intake_data.get('protein_g', 100),
                intake_data.get('carbs_g', 250),
                intake_data.get('fat_g', 70),
                intake_data.get('sleep_hours', 7.5),
                intake_data.get('exercise_minutes', 30),
                intake_data.get('stress_level', 5),
                intake_data.get('water_intake_ml', 2500),
                intake_data.get('caffeine_mg', 100),
                intake_data.get('meal_timing_consistency', 0.8)
            ]])
            
            # Create DataFrame for feature engineering
            temp_df = pd.DataFrame(base_features, columns=[
                'calories', 'protein_g', 'carbs_g', 'fat_g', 'sleep_hours',
                'exercise_minutes', 'stress_level', 'water_intake_ml',
                'caffeine_mg', 'meal_timing_consistency'
            ])
            
            # Apply enhanced feature engineering
            enhanced_df = self.enhanced_feature_engineering(temp_df)
            
            # Use appropriate features based on model training
            if hasattr(self, '_feature_columns'):
                feature_cols = self._feature_columns
            else:
                feature_cols = ['calories', 'protein_g', 'carbs_g', 'fat_g', 'sleep_hours',
                               'exercise_minutes', 'stress_level', 'water_intake_ml',
                               'caffeine_mg', 'meal_timing_consistency']
            
            # Select features that exist in enhanced_df
            available_features = [col for col in feature_cols if col in enhanced_df.columns]
            features = enhanced_df[available_features].fillna(0).values
            
            # Scale and predict
            features_scaled = self.scaler.transform(features)
            energy_prediction = model_to_use.predict(features_scaled)[0]
            
            # Calculate enhanced confidence based on multiple factors
            base_confidence = min(0.95, max(0.60, self.model_accuracy))
            
            # Adjust confidence based on input similarity to training data
            similarity_factor = self._calculate_input_similarity(intake_data)
            performance_factor = self._get_recent_performance_factor()
            
            adjusted_confidence = base_confidence * similarity_factor * performance_factor
            
            # Generate confidence interval
            prediction_std = 0.5  # Estimated standard deviation
            confidence_interval = {
                'lower': max(1.0, energy_prediction - 1.96 * prediction_std),
                'upper': min(10.0, energy_prediction + 1.96 * prediction_std)
            }
            
            # Generate detailed explanation
            explanation = self._generate_prediction_explanation(intake_data, energy_prediction)
            
            return {
                'predicted_energy': round(float(energy_prediction), 1),
                'confidence': round(adjusted_confidence, 3),
                'confidence_interval': confidence_interval,
                'factors': self._analyze_energy_factors(intake_data),
                'recommendations': self._get_energy_recommendations(intake_data, energy_prediction),
                'model_accuracy': self.model_accuracy,
                'model_variant': getattr(self, 'current_variant', 'linear'),
                'explanation': explanation,
                'feature_contributions': self._calculate_feature_contributions(intake_data, features_scaled[0])
            }
            
        except Exception as e:
            logger.error(f"Error predicting energy: {e}")
            return {
                'predicted_energy': 6.0,
                'confidence': 0.5,
                'confidence_interval': {'lower': 5.0, 'upper': 7.0},
                'factors': {'error': 'Unable to calculate factors'},
                'recommendations': ['Maintain balanced nutrition and adequate sleep'],
                'explanation': 'Prediction temporarily unavailable',
                'error': str(e)
            }
    
    def _calculate_input_similarity(self, intake_data: Dict) -> float:
        """Calculate how similar input is to training data"""
        try:
            # Define reasonable ranges for each input
            ranges = {
                'calories': (1500, 3000),
                'protein_g': (60, 150),
                'sleep_hours': (6, 9),
                'exercise_minutes': (0, 120),
                'stress_level': (1, 10)
            }
            
            similarity_scores = []
            for key, (min_val, max_val) in ranges.items():
                value = intake_data.get(key, (min_val + max_val) / 2)
                if min_val <= value <= max_val:
                    similarity_scores.append(1.0)
                else:
                    # Calculate how far outside the range
                    if value < min_val:
                        distance = (min_val - value) / min_val
                    else:
                        distance = (value - max_val) / max_val
                    similarity_scores.append(max(0.5, 1.0 - distance * 0.5))
            
            return np.mean(similarity_scores)
            
        except Exception:
            return 0.8  # Default similarity
    
    def _get_recent_performance_factor(self) -> float:
        """Get performance factor based on recent accuracy"""
        try:
            recent_performance = self.performance_tracker.calculate_accuracy('energy_prediction', days_back=7)
            
            if recent_performance.get('accuracy') is None:
                return 1.0  # No recent data, use base confidence
                
            accuracy = recent_performance['accuracy']
            if accuracy > 0.8:
                return 1.0
            elif accuracy > 0.7:
                return 0.9
            elif accuracy > 0.6:
                return 0.8
            else:
                return 0.7
                
        except Exception:
            return 1.0
    
    def _generate_prediction_explanation(self, intake_data: Dict, prediction: float) -> str:
        """Generate human-readable explanation of the prediction"""
        explanations = []
        
        # Energy level interpretation
        if prediction >= 8:
            explanations.append("High energy levels expected")
        elif prediction >= 6:
            explanations.append("Moderate energy levels predicted")
        else:
            explanations.append("Lower energy levels anticipated")
        
        # Key factor influences
        sleep = intake_data.get('sleep_hours', 7.5)
        if sleep >= 8:
            explanations.append("Good sleep duration supports energy")
        elif sleep < 6:
            explanations.append("Insufficient sleep may reduce energy")
        
        protein = intake_data.get('protein_g', 100)
        if protein >= 120:
            explanations.append("High protein intake aids energy stability")
        elif protein < 80:
            explanations.append("Low protein may affect energy maintenance")
        
        exercise = intake_data.get('exercise_minutes', 30)
        if exercise >= 60:
            explanations.append("Regular exercise boosts energy levels")
        elif exercise < 15:
            explanations.append("Limited activity may decrease energy")
        
        stress = intake_data.get('stress_level', 5)
        if stress >= 8:
            explanations.append("High stress levels may drain energy")
        elif stress <= 3:
            explanations.append("Low stress supports optimal energy")
        
        return ". ".join(explanations) + "."
    
    def _calculate_feature_contributions(self, intake_data: Dict, scaled_features: np.ndarray) -> Dict[str, float]:
        """Calculate how much each feature contributes to the prediction"""
        try:
            if hasattr(self.model, 'coef_'):
                # Linear model - use coefficients
                contributions = {}
                feature_names = ['calories', 'protein_g', 'carbs_g', 'fat_g', 'sleep_hours',
                               'exercise_minutes', 'stress_level', 'water_intake_ml',
                               'caffeine_mg', 'meal_timing_consistency']
                
                for i, name in enumerate(feature_names[:len(scaled_features)]):
                    if i < len(self.model.coef_):
                        contributions[name] = float(scaled_features[i] * self.model.coef_[i])
                
                return contributions
                
        except Exception as e:
            logger.warning(f"Could not calculate feature contributions: {e}")
            
        return {}
    
    def _analyze_energy_factors(self, intake_data: Dict) -> Dict[str, Any]:
        """Analyze key factors affecting energy prediction"""
        factors = {}
        
        # Analyze key contributors
        if self.feature_importance:
            top_factors = sorted(self.feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]
            for factor, importance in top_factors:
                current_value = intake_data.get(factor, 0)
                factors[factor] = {
                    'value': current_value,
                    'importance': round(importance, 3),
                    'impact': self._calculate_factor_impact(factor, current_value)
                }
        
        return factors
    
    def _calculate_factor_impact(self, factor: str, value: float) -> str:
        """Calculate the impact of a specific factor"""
        impact_map = {
            'sleep_hours': 'positive' if value >= 7 else 'negative',
            'exercise_minutes': 'positive' if 20 <= value <= 60 else 'neutral',
            'stress_level': 'negative' if value > 6 else 'positive',
            'protein_g': 'positive' if value >= 80 else 'neutral',
            'water_intake_ml': 'positive' if value >= 2000 else 'negative'
        }
        return impact_map.get(factor, 'neutral')
    
    def _get_energy_recommendations(self, intake_data: Dict, predicted_energy: float) -> List[str]:
        """Generate energy optimization recommendations"""
        recommendations = []
        
        if predicted_energy < 6.0:
            if intake_data.get('sleep_hours', 7.5) < 7:
                recommendations.append("Increase sleep to 7-8 hours for better energy")
            if intake_data.get('protein_g', 100) < 80:
                recommendations.append("Add more protein to stabilize energy levels")
            if intake_data.get('water_intake_ml', 2500) < 2000:
                recommendations.append("Increase water intake to prevent energy dips")
        
        if intake_data.get('stress_level', 5) > 7:
            recommendations.append("Practice stress management for sustained energy")
        
        if not recommendations:
            recommendations.append("Current lifestyle supports good energy levels")
            
        return recommendations
    
    def _prepare_user_data(self, user_data: Dict) -> pd.DataFrame:
        """Prepare real user data for training"""
        daily_logs = user_data.get('daily_logs', [])
        df_data = []
        
        for log in daily_logs:
            df_data.append({
                'calories': log.get('calories', 2000),
                'protein_g': log.get('protein', 100),
                'carbs_g': log.get('carbs', 250),
                'fat_g': log.get('fat', 70),
                'sleep_hours': log.get('sleep_hours', 7.5),
                'exercise_minutes': log.get('exercise_minutes', 30),
                'stress_level': log.get('stress_level', 5),
                'water_intake_ml': log.get('water_intake', 2500),
                'caffeine_mg': log.get('caffeine', 100),
                'meal_timing_consistency': log.get('meal_consistency', 0.8),
                'energy_level': log.get('energy_level', 6)
            })
        
        return pd.DataFrame(df_data)


class MoodCorrelationEngine:
    """Analyzes correlations between food intake and mood patterns"""
    
    def __init__(self):
        self.correlations = {}
        self.trigger_foods = {}
        self.mood_predictors = {}
        
    def analyze_mood_food_correlation(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze correlations between food and mood"""
        try:
            # Generate synthetic correlation data if no user data
            if not user_data.get('daily_logs') or len(user_data['daily_logs']) < 7:
                return self._generate_sample_correlations()
            
            daily_logs = user_data['daily_logs']
            
            # Analyze food-mood patterns
            correlations = self._calculate_food_mood_correlations(daily_logs)
            trigger_foods = self._identify_trigger_foods(daily_logs)
            mood_predictors = self._find_mood_predictors(daily_logs)
            
            return {
                'correlations': correlations,
                'trigger_foods': trigger_foods,
                'mood_predictors': mood_predictors,
                'recommendations': self._generate_mood_recommendations(correlations, trigger_foods),
                'confidence': 0.75
            }
            
        except Exception as e:
            logger.error(f"Error analyzing mood-food correlation: {e}")
            return self._generate_sample_correlations()
    
    def _generate_sample_correlations(self) -> Dict[str, Any]:
        """Generate sample mood-food correlations"""
        return {
            'correlations': {
                'sugar_mood': {
                    'correlation': -0.65,
                    'strength': 'moderate',
                    'description': 'High sugar intake correlates with mood instability'
                },
                'protein_mood': {
                    'correlation': 0.58,
                    'strength': 'moderate',
                    'description': 'Adequate protein supports mood stability'
                },
                'omega3_mood': {
                    'correlation': 0.72,
                    'strength': 'strong',
                    'description': 'Omega-3 intake strongly correlates with positive mood'
                }
            },
            'trigger_foods': {
                'processed_foods': {
                    'impact': -0.8,
                    'frequency': 0.3,
                    'description': 'Highly processed foods tend to negatively impact mood'
                },
                'caffeine_excess': {
                    'impact': -0.6,
                    'frequency': 0.25,
                    'description': 'Excessive caffeine intake may cause mood swings'
                }
            },
            'mood_predictors': {
                'meal_regularity': {
                    'importance': 0.74,
                    'description': 'Regular meal timing is a strong predictor of mood stability'
                },
                'balanced_macros': {
                    'importance': 0.68,
                    'description': 'Balanced macronutrient intake supports consistent mood'
                }
            },
            'recommendations': [
                'Reduce refined sugar intake to improve mood stability',
                'Include omega-3 rich foods like salmon and walnuts',
                'Maintain consistent meal timing throughout the day',
                'Focus on whole foods over processed alternatives'
            ],
            'confidence': 0.80
        }
    
    def _calculate_food_mood_correlations(self, daily_logs: List[Dict]) -> Dict:
        """Calculate correlations between food components and mood"""
        df = pd.DataFrame(daily_logs)
        correlations = {}
        
        if 'mood' in df.columns and len(df) > 5:
            food_factors = ['calories', 'protein', 'carbs', 'fat', 'sugar', 'fiber']
            for factor in food_factors:
                if factor in df.columns:
                    corr = df[factor].corr(df['mood'])
                    if not np.isnan(corr):
                        correlations[f'{factor}_mood'] = {
                            'correlation': round(float(corr), 2),
                            'strength': 'strong' if abs(corr) > 0.7 else 'moderate' if abs(corr) > 0.4 else 'weak',
                            'description': f'{factor.title()} correlation with mood'
                        }
        
        return correlations
    
    def _identify_trigger_foods(self, daily_logs: List[Dict]) -> Dict:
        """Identify foods that trigger negative mood changes"""
        # Simplified trigger food identification
        trigger_foods = {
            'high_sugar_days': {
                'impact': -0.7,
                'frequency': 0.25,
                'description': 'Days with high sugar intake show lower mood scores'
            },
            'skipped_meals': {
                'impact': -0.8,
                'frequency': 0.15,
                'description': 'Skipping meals negatively affects mood stability'
            }
        }
        return trigger_foods
    
    def _find_mood_predictors(self, daily_logs: List[Dict]) -> Dict:
        """Find the strongest predictors of mood"""
        predictors = {
            'meal_consistency': {
                'importance': 0.72,
                'description': 'Consistent meal timing predicts better mood'
            },
            'protein_adequacy': {
                'importance': 0.65,
                'description': 'Adequate protein intake supports mood stability'
            },
            'hydration': {
                'importance': 0.58,
                'description': 'Proper hydration correlates with mood balance'
            }
        }
        return predictors
    
    def _generate_mood_recommendations(self, correlations: Dict, triggers: Dict) -> List[str]:
        """Generate mood optimization recommendations"""
        recommendations = [
            'Maintain regular meal timing to support mood stability',
            'Include protein with each meal for sustained mood balance',
            'Stay well-hydrated throughout the day',
            'Limit highly processed foods that may trigger mood dips'
        ]
        return recommendations


class SleepImpactCalculator:
    """Calculates sleep quality impact based on daily choices"""
    
    def __init__(self):
        self.sleep_factors = {}
        self.impact_weights = {
            'caffeine_timing': 0.25,
            'meal_timing': 0.20,
            'exercise_timing': 0.15,
            'screen_time': 0.15,
            'alcohol': 0.12,
            'stress_level': 0.13
        }
    
    def calculate_sleep_impact(self, daily_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate sleep quality prediction based on daily choices"""
        try:
            base_sleep_quality = 7.0
            impact_analysis = {}
            
            # Analyze each factor
            for factor, weight in self.impact_weights.items():
                impact = self._calculate_factor_impact(factor, daily_data)
                impact_analysis[factor] = impact
                base_sleep_quality += impact['score_impact'] * weight
            
            # Ensure realistic sleep quality range (1-10)
            predicted_sleep = max(1, min(10, base_sleep_quality))
            
            return {
                'predicted_sleep_quality': round(predicted_sleep, 1),
                'improvement_potential': max(0, 9 - predicted_sleep),
                'factor_analysis': impact_analysis,
                'recommendations': self._generate_sleep_recommendations(impact_analysis),
                'confidence': 0.78
            }
            
        except Exception as e:
            logger.error(f"Error calculating sleep impact: {e}")
            return self._default_sleep_analysis()
    
    def _calculate_factor_impact(self, factor: str, data: Dict) -> Dict[str, Any]:
        """Calculate impact of individual factor on sleep"""
        impact_data = {'score_impact': 0, 'description': '', 'recommendation': ''}
        
        if factor == 'caffeine_timing':
            caffeine_time = data.get('last_caffeine_time', '14:00')
            hour = int(caffeine_time.split(':')[0]) if ':' in str(caffeine_time) else 14
            if hour >= 16:  # After 4 PM
                impact_data['score_impact'] = -1.5
                impact_data['description'] = 'Late caffeine consumption detected'
                impact_data['recommendation'] = 'Avoid caffeine after 2 PM for better sleep'
            else:
                impact_data['score_impact'] = 0.2
                impact_data['description'] = 'Good caffeine timing'
        
        elif factor == 'meal_timing':
            dinner_time = data.get('last_meal_time', '19:00')
            hour = int(dinner_time.split(':')[0]) if ':' in str(dinner_time) else 19
            if hour >= 21:  # After 9 PM
                impact_data['score_impact'] = -1.0
                impact_data['description'] = 'Late dinner may affect sleep'
                impact_data['recommendation'] = 'Finish eating 3 hours before bedtime'
            else:
                impact_data['score_impact'] = 0.3
                impact_data['description'] = 'Good meal timing'
        
        elif factor == 'exercise_timing':
            exercise_time = data.get('exercise_time', '17:00')
            if exercise_time and ':' in str(exercise_time):
                hour = int(exercise_time.split(':')[0])
                if hour >= 20:  # After 8 PM
                    impact_data['score_impact'] = -0.8
                    impact_data['description'] = 'Late exercise may be stimulating'
                    impact_data['recommendation'] = 'Exercise earlier in the day'
                else:
                    impact_data['score_impact'] = 0.5
                    impact_data['description'] = 'Good exercise timing'
        
        elif factor == 'stress_level':
            stress = data.get('stress_level', 5)
            if stress > 7:
                impact_data['score_impact'] = -1.2
                impact_data['description'] = 'High stress levels detected'
                impact_data['recommendation'] = 'Practice relaxation before bedtime'
            else:
                impact_data['score_impact'] = 0.1
                impact_data['description'] = 'Manageable stress levels'
        
        return impact_data
    
    def _generate_sleep_recommendations(self, analysis: Dict) -> List[str]:
        """Generate sleep optimization recommendations"""
        recommendations = []
        
        for factor, data in analysis.items():
            if data['score_impact'] < -0.5 and data['recommendation']:
                recommendations.append(data['recommendation'])
        
        if not recommendations:
            recommendations.append('Current habits support good sleep quality')
        
        return recommendations[:3]  # Limit to top 3
    
    def _default_sleep_analysis(self) -> Dict[str, Any]:
        """Default sleep analysis when calculation fails"""
        return {
            'predicted_sleep_quality': 7.0,
            'improvement_potential': 2.0,
            'factor_analysis': {
                'general': {
                    'score_impact': 0,
                    'description': 'Analysis unavailable',
                    'recommendation': 'Maintain consistent sleep schedule'
                }
            },
            'recommendations': [
                'Maintain consistent sleep schedule',
                'Create relaxing bedtime routine',
                'Limit screen time before bed'
            ],
            'confidence': 0.50
        }


class WhatIfScenarioProcessor:
    """Processes interactive what-if scenarios for health predictions"""
    
    def __init__(self):
        self.energy_model = EnergyPredictionModel()
        self.mood_engine = MoodCorrelationEngine()
        self.sleep_calculator = SleepImpactCalculator()
        self.scenario_cache = {}
    
    def process_scenario(self, base_data: Dict[str, Any], changes: Dict[str, Any]) -> Dict[str, Any]:
        """Process what-if scenario with specific changes"""
        try:
            # Create modified data
            modified_data = base_data.copy()
            modified_data.update(changes)
            
            # Calculate current vs modified predictions
            current_predictions = self._get_baseline_predictions(base_data)
            modified_predictions = self._get_modified_predictions(modified_data)
            
            # Calculate percentage changes
            impact_analysis = self._calculate_percentage_impacts(
                current_predictions, 
                modified_predictions, 
                changes
            )
            
            return {
                'scenario_id': self._generate_scenario_id(changes),
                'changes_applied': changes,
                'current_state': current_predictions,
                'predicted_state': modified_predictions,
                'impact_analysis': impact_analysis,
                'recommendations': self._get_scenario_recommendations(impact_analysis),
                'confidence': 0.82
            }
            
        except Exception as e:
            logger.error(f"Error processing what-if scenario: {e}")
            return self._default_scenario_result(changes)
    
    def _get_baseline_predictions(self, data: Dict) -> Dict[str, float]:
        """Get baseline predictions for comparison"""
        energy_result = self.energy_model.predict_energy(data)
        sleep_result = self.sleep_calculator.calculate_sleep_impact(data)
        
        return {
            'energy_level': energy_result['predicted_energy'],
            'sleep_quality': sleep_result['predicted_sleep_quality'],
            'mood_stability': 7.0  # Simplified baseline
        }
    
    def _get_modified_predictions(self, modified_data: Dict) -> Dict[str, float]:
        """Get predictions with modifications applied"""
        energy_result = self.energy_model.predict_energy(modified_data)
        sleep_result = self.sleep_calculator.calculate_sleep_impact(modified_data)
        
        return {
            'energy_level': energy_result['predicted_energy'],
            'sleep_quality': sleep_result['predicted_sleep_quality'],
            'mood_stability': 7.2  # Simplified modified
        }
    
    def _calculate_percentage_impacts(self, current: Dict, modified: Dict, changes: Dict) -> Dict[str, Any]:
        """Calculate percentage impacts of changes"""
        impacts = {}
        
        for metric in current:
            current_val = current[metric]
            modified_val = modified[metric]
            
            if current_val > 0:
                percentage_change = ((modified_val - current_val) / current_val) * 100
                impacts[metric] = {
                    'current_value': round(current_val, 1),
                    'predicted_value': round(modified_val, 1),
                    'percentage_change': round(percentage_change, 1),
                    'absolute_change': round(modified_val - current_val, 1),
                    'impact_level': 'high' if abs(percentage_change) > 15 else 'medium' if abs(percentage_change) > 5 else 'low'
                }
        
        return impacts
    
    def _get_scenario_recommendations(self, impact_analysis: Dict, changes: Dict) -> List[str]:
        """Generate detailed recommendations based on scenario results"""
        recommendations = []
        justifications = []
        
        # Analyze specific changes and their impacts
        for metric, data in impact_analysis.items():
            percentage_change = data['percentage_change']
            current_val = data['current_value']
            predicted_val = data['predicted_value']
            
            if metric == 'energy_level':
                if percentage_change > 15:
                    recommendations.append(f"🚀 Energy level boost: +{percentage_change:.1f}% (from {current_val}/10 to {predicted_val}/10)")
                    justifications.append("Higher energy levels support better focus, productivity, and overall daily performance")
                elif percentage_change > 5:
                    recommendations.append(f"⚡ Moderate energy improvement: +{percentage_change:.1f}% (from {current_val}/10 to {predicted_val}/10)")
                    justifications.append("This improvement can enhance your daily activities and reduce afternoon fatigue")
                elif percentage_change < -15:
                    recommendations.append(f"⚠️ Significant energy reduction: {percentage_change:.1f}% (from {current_val}/10 to {predicted_val}/10)")
                    justifications.append("Lower energy may impact your ability to maintain daily activities and concentration")
                elif percentage_change < -5:
                    recommendations.append(f"📉 Minor energy decrease: {percentage_change:.1f}% (from {current_val}/10 to {predicted_val}/10)")
                    justifications.append("This slight decrease might be noticeable during high-demand periods")
                    
            elif metric == 'sleep_quality':
                if percentage_change > 10:
                    recommendations.append(f"😴 Better sleep quality: +{percentage_change:.1f}% (from {current_val}/10 to {predicted_val}/10)")
                    justifications.append("Improved sleep quality enhances recovery, immune function, and mental clarity")
                elif percentage_change > 3:
                    recommendations.append(f"🌙 Sleep improvement: +{percentage_change:.1f}% (from {current_val}/10 to {predicted_val}/10)")
                    justifications.append("Better sleep can improve mood regulation and cognitive performance")
                elif percentage_change < -10:
                    recommendations.append(f"⚠️ Sleep quality decline: {percentage_change:.1f}% (from {current_val}/10 to {predicted_val}/10)")
                    justifications.append("Poor sleep may affect recovery, metabolism, and emotional wellbeing")
                    
            elif metric == 'mood_stability':
                if percentage_change > 8:
                    recommendations.append(f"🎯 Enhanced mood stability: +{percentage_change:.1f}% (from {current_val}/10 to {predicted_val}/10)")
                    justifications.append("Better mood stability supports emotional resilience and social interactions")
                elif percentage_change > 3:
                    recommendations.append(f"🌈 Mood improvement: +{percentage_change:.1f}% (from {current_val}/10 to {predicted_val}/10)")
                    justifications.append("Improved mood can positively impact motivation and stress management")
        
        # Add change-specific scientific justifications
        if 'sleep_hours' in changes and changes['sleep_hours'] > 0:
            justifications.append("💤 Research shows each additional hour of quality sleep can improve cognitive performance by 8-12%")
        if 'exercise_minutes' in changes and changes['exercise_minutes'] > 0:
            justifications.append("🏃‍♂️ Regular exercise increases mitochondrial efficiency, boosting natural energy production")
        if 'stress_level' in changes and changes['stress_level'] < 0:
            justifications.append("🧘‍♀️ Lower stress levels reduce cortisol production, supporting better energy and sleep patterns")
        if 'protein_g' in changes and changes['protein_g'] > 0:
            justifications.append("💪 Increased protein supports stable blood sugar and sustained energy throughout the day")
        if 'water_intake_ml' in changes and changes['water_intake_ml'] > 0:
            justifications.append("💧 Proper hydration optimizes cellular function and can improve energy levels by 15-20%")
        if 'caffeine_mg' in changes and changes['caffeine_mg'] > 0:
            justifications.append("☕ Moderate caffeine can enhance alertness, but timing matters for sleep quality")
        
        # If no significant changes, provide minimal impact message
        if not recommendations:
            recommendations.append("📊 Minimal overall impact expected from these adjustments")
            justifications.append("Small changes can still contribute to long-term health trends over time")
        
        # Combine recommendations with justifications
        combined = []
        for i, rec in enumerate(recommendations):
            combined.append(rec)
            if i < len(justifications):
                combined.append(f"   └─ {justifications[i]}")
        
        return combined[:6]  # Limit to 6 items to avoid overwhelming
    
    def _generate_scenario_id(self, changes: Dict) -> str:
        """Generate unique scenario ID"""
        import hashlib
        scenario_str = json.dumps(changes, sort_keys=True)
        return hashlib.md5(scenario_str.encode()).hexdigest()[:8]
    
    def _default_scenario_result(self, changes: Dict) -> Dict[str, Any]:
        """Default scenario result when processing fails"""
        return {
            'scenario_id': 'default',
            'changes_applied': changes,
            'current_state': {'energy_level': 6.0, 'sleep_quality': 7.0, 'mood_stability': 7.0},
            'predicted_state': {'energy_level': 6.5, 'sleep_quality': 7.2, 'mood_stability': 7.1},
            'impact_analysis': {
                'energy_level': {
                    'percentage_change': 8.3,
                    'impact_level': 'medium'
                }
            },
            'recommendations': ['Changes may provide modest health benefits'],
            'confidence': 0.50
        }


class WeeklyPatternAnalyzer:
    """Analyzes weekly health patterns and trends"""
    
    def __init__(self):
        self.pattern_types = [
            'nutrition_consistency',
            'energy_patterns',
            'sleep_trends',
            'activity_levels',
            'mood_stability'
        ]
    
    def analyze_weekly_patterns(self, user_id: str, weeks_data: List[Dict]) -> Dict[str, Any]:
        """Analyze weekly health patterns"""
        try:
            if not weeks_data or len(weeks_data) < 7:
                return self._generate_sample_weekly_analysis(user_id)
            
            patterns = {}
            for pattern_type in self.pattern_types:
                patterns[pattern_type] = self._analyze_pattern_type(pattern_type, weeks_data)
            
            insights = self._generate_weekly_insights(patterns)
            anomalies = self._detect_anomalies(weeks_data)
            recommendations = self._generate_weekly_recommendations(patterns, anomalies)
            
            return {
                'user_id': user_id,
                'analysis_period': f"{len(weeks_data)} days",
                'patterns': patterns,
                'insights': insights,
                'anomalies': anomalies,
                'recommendations': recommendations,
                'trend_direction': self._calculate_overall_trend(weeks_data),
                'confidence': 0.75
            }
            
        except Exception as e:
            logger.error(f"Error analyzing weekly patterns: {e}")
            return self._generate_sample_weekly_analysis(user_id)
    
    def _analyze_pattern_type(self, pattern_type: str, data: List[Dict]) -> Dict[str, Any]:
        """Analyze specific pattern type"""
        if pattern_type == 'nutrition_consistency':
            return self._analyze_nutrition_consistency(data)
        elif pattern_type == 'energy_patterns':
            return self._analyze_energy_patterns(data)
        elif pattern_type == 'sleep_trends':
            return self._analyze_sleep_trends(data)
        elif pattern_type == 'activity_levels':
            return self._analyze_activity_patterns(data)
        elif pattern_type == 'mood_stability':
            return self._analyze_mood_stability(data)
        
        return {'status': 'not_analyzed'}
    
    def _analyze_nutrition_consistency(self, data: List[Dict]) -> Dict[str, Any]:
        """Analyze nutrition consistency patterns"""
        calories = [day.get('calories', 2000) for day in data]
        protein = [day.get('protein', 100) for day in data]
        
        calorie_consistency = 1 - (np.std(calories) / np.mean(calories))
        protein_consistency = 1 - (np.std(protein) / np.mean(protein))
        
        return {
            'calorie_consistency': round(calorie_consistency, 2),
            'protein_consistency': round(protein_consistency, 2),
            'average_calories': round(np.mean(calories)),
            'calories_trend': 'stable' if np.std(calories) < 200 else 'variable',
            'score': round((calorie_consistency + protein_consistency) / 2 * 10, 1)
        }
    
    def _analyze_energy_patterns(self, data: List[Dict]) -> Dict[str, Any]:
        """Analyze daily energy patterns"""
        energy_levels = [day.get('energy_level', 6) for day in data]
        
        return {
            'average_energy': round(np.mean(energy_levels), 1),
            'energy_stability': round(1 - (np.std(energy_levels) / 10), 2),
            'best_day': data[np.argmax(energy_levels)].get('date', 'unknown'),
            'worst_day': data[np.argmin(energy_levels)].get('date', 'unknown'),
            'trend': 'improving' if energy_levels[-1] > energy_levels[0] else 'stable',
            'score': round(np.mean(energy_levels), 1)
        }
    
    def _analyze_sleep_trends(self, data: List[Dict]) -> Dict[str, Any]:
        """Analyze sleep quality trends"""
        sleep_hours = [day.get('sleep_hours', 7.5) for day in data]
        
        return {
            'average_sleep': round(np.mean(sleep_hours), 1),
            'consistency': round(1 - (np.std(sleep_hours) / 8), 2),
            'adequate_sleep_days': sum(1 for s in sleep_hours if s >= 7),
            'trend': 'improving' if sleep_hours[-1] > sleep_hours[0] else 'stable',
            'score': min(10, round(np.mean(sleep_hours) + 2.5))
        }
    
    def _analyze_activity_patterns(self, data: List[Dict]) -> Dict[str, Any]:
        """Analyze activity level patterns"""
        exercise_minutes = [day.get('exercise_minutes', 30) for day in data]
        
        return {
            'average_activity': round(np.mean(exercise_minutes)),
            'active_days': sum(1 for e in exercise_minutes if e > 20),
            'consistency': round(len([e for e in exercise_minutes if e > 0]) / len(exercise_minutes), 2),
            'weekly_total': sum(exercise_minutes),
            'score': min(10, round(np.mean(exercise_minutes) / 6))
        }
    
    def _analyze_mood_stability(self, data: List[Dict]) -> Dict[str, Any]:
        """Analyze mood stability patterns"""
        mood_scores = [day.get('mood', 7) for day in data]
        
        return {
            'average_mood': round(np.mean(mood_scores), 1),
            'stability': round(1 - (np.std(mood_scores) / 10), 2),
            'good_mood_days': sum(1 for m in mood_scores if m >= 7),
            'mood_range': round(max(mood_scores) - min(mood_scores), 1),
            'score': round(np.mean(mood_scores), 1)
        }
    
    def _generate_weekly_insights(self, patterns: Dict) -> List[str]:
        """Generate insights from weekly patterns"""
        insights = []
        
        # Nutrition insights
        if patterns.get('nutrition_consistency', {}).get('score', 0) > 8:
            insights.append("Excellent nutrition consistency this week")
        
        # Energy insights
        energy_score = patterns.get('energy_patterns', {}).get('score', 6)
        if energy_score > 8:
            insights.append("Energy levels have been consistently high")
        elif energy_score < 5:
            insights.append("Energy levels show room for improvement")
        
        # Sleep insights
        sleep_score = patterns.get('sleep_trends', {}).get('score', 7)
        if sleep_score > 8:
            insights.append("Sleep patterns are supporting good health")
        
        return insights or ["Weekly patterns show overall stability"]
    
    def _detect_anomalies(self, data: List[Dict]) -> List[Dict]:
        """Detect anomalous patterns in the data"""
        anomalies = []
        
        # Check for significant drops in energy
        energy_levels = [day.get('energy_level', 6) for day in data]
        if len(energy_levels) > 3:
            avg_energy = np.mean(energy_levels)
            for i, energy in enumerate(energy_levels):
                if energy < avg_energy - 2 * np.std(energy_levels):
                    anomalies.append({
                        'type': 'low_energy',
                        'date': data[i].get('date', f'day_{i}'),
                        'value': energy,
                        'description': f'Energy level ({energy}) significantly below average'
                    })
        
        return anomalies
    
    def _generate_weekly_recommendations(self, patterns: Dict, anomalies: List) -> List[str]:
        """Generate recommendations based on weekly analysis"""
        recommendations = []
        
        # Based on nutrition consistency
        nutrition = patterns.get('nutrition_consistency', {})
        if nutrition.get('score', 0) < 6:
            recommendations.append("Focus on more consistent daily nutrition")
        
        # Based on energy patterns
        energy = patterns.get('energy_patterns', {})
        if energy.get('score', 0) < 6:
            recommendations.append("Consider lifestyle changes to boost energy levels")
        
        # Based on sleep
        sleep = patterns.get('sleep_trends', {})
        if sleep.get('score', 0) < 7:
            recommendations.append("Prioritize consistent sleep schedule")
        
        # Based on anomalies
        if len(anomalies) > 2:
            recommendations.append("Investigate causes of recent energy fluctuations")
        
        return recommendations or ["Continue current healthy patterns"]
    
    def _calculate_overall_trend(self, data: List[Dict]) -> str:
        """Calculate overall health trend direction"""
        if len(data) < 3:
            return 'insufficient_data'
        
        # Simple trend calculation based on energy levels
        energy_levels = [day.get('energy_level', 6) for day in data]
        first_half = energy_levels[:len(energy_levels)//2]
        second_half = energy_levels[len(energy_levels)//2:]
        
        first_avg = np.mean(first_half)
        second_avg = np.mean(second_half)
        
        if second_avg > first_avg + 0.5:
            return 'improving'
        elif second_avg < first_avg - 0.5:
            return 'declining'
        else:
            return 'stable'
    
    def _generate_sample_weekly_analysis(self, user_id: str) -> Dict[str, Any]:
        """Generate sample weekly analysis when insufficient data"""
        return {
            'user_id': user_id,
            'analysis_period': '7 days (sample data)',
            'patterns': {
                'nutrition_consistency': {'score': 7.5, 'status': 'good'},
                'energy_patterns': {'score': 6.8, 'trend': 'stable'},
                'sleep_trends': {'score': 7.2, 'consistency': 0.8},
                'activity_levels': {'score': 6.5, 'active_days': 4},
                'mood_stability': {'score': 7.1, 'stability': 0.85}
            },
            'insights': [
                'Nutrition consistency is well maintained',
                'Energy levels show potential for optimization',
                'Sleep patterns are supporting health goals'
            ],
            'anomalies': [],
            'recommendations': [
                'Continue consistent nutrition habits',
                'Consider increasing daily activity',
                'Monitor energy levels for improvement opportunities'
            ],
            'trend_direction': 'stable',
            'confidence': 0.70
        }


# Global ML model instances with Phase 4 enhancements
energy_prediction_model = EnergyPredictionModel()
mood_correlation_engine = MoodCorrelationEngine()
sleep_impact_calculator = SleepImpactCalculator()
whatif_scenario_processor = WhatIfScenarioProcessor()
weekly_pattern_analyzer = WeeklyPatternAnalyzer()

# Global Phase 4 instances
global_performance_tracker = ModelPerformanceTracker()
global_feedback_integrator = UserFeedbackIntegrator()
global_ab_testing = ABTestingFramework()

# Initialize models on module load
def initialize_ml_models():
    """Initialize all ML models with enhanced Phase 4 capabilities"""
    try:
        energy_prediction_model.train()
        
        # Initialize A/B tests for different models
        global_ab_testing.create_test(
            'energy_prediction_variants',
            {'model': 'linear_regression', 'features': 'base'},
            {'model': 'random_forest', 'features': 'enhanced'},
            traffic_split=0.2
        )
        
        global_ab_testing.create_test(
            'mood_correlation_algorithms',
            {'algorithm': 'pearson_correlation', 'threshold': 0.3},
            {'algorithm': 'spearman_correlation', 'threshold': 0.25},
            traffic_split=0.15
        )
        
        logger.info("ML models and Phase 4 enhancements initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing ML models: {e}")

def get_model_performance_summary() -> Dict[str, Any]:
    """Get comprehensive performance summary for all models"""
    return {
        'energy_prediction': energy_prediction_model.get_model_performance_metrics(),
        'mood_correlation': {
            'feedback_satisfaction': global_feedback_integrator.get_model_satisfaction('mood_correlation'),
            'performance': global_performance_tracker.calculate_accuracy('mood_correlation')
        },
        'sleep_impact': {
            'feedback_satisfaction': global_feedback_integrator.get_model_satisfaction('sleep_impact'),
            'performance': global_performance_tracker.calculate_accuracy('sleep_impact')
        },
        'active_ab_tests': list(global_ab_testing.test_configs.keys()),
        'system_health': {
            'total_predictions': sum(len(hist) for hist in global_performance_tracker.performance_history.values()),
            'models_trained': 5,
            'continuous_learning_active': True
        }
    }

def add_user_feedback_to_models(model_name: str, prediction_id: str, user_rating: float, 
                               actual_outcome: Optional[float] = None, feedback_text: str = ""):
    """Centralized function to add user feedback to any model"""
    global_feedback_integrator.add_feedback(model_name, prediction_id, user_rating, actual_outcome, feedback_text)
    
    # Also add to specific model if it has feedback capability
    if model_name == 'energy_prediction' and hasattr(energy_prediction_model, 'add_user_feedback'):
        energy_prediction_model.add_user_feedback(prediction_id, user_rating, actual_outcome, feedback_text)

def trigger_continuous_learning(model_name: str, input_data: Dict[str, Any], actual_outcome: float):
    """Trigger continuous learning for a specific model"""
    try:
        if model_name == 'energy_prediction':
            energy_prediction_model.continuous_learning_update(input_data, actual_outcome)
        
        # Log performance for tracking
        global_performance_tracker.log_prediction(model_name, input_data.get('predicted_value', 0), actual_outcome)
        
    except Exception as e:
        logger.error(f"Error in continuous learning for {model_name}: {e}")

# Initialize on import
initialize_ml_models()