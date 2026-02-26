"""
Weather-based Early Warning System
Predicts disease risk before symptoms appear
"""
import requests
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List

class EarlyWarningSystem:
    def __init__(self):
        # Disease risk thresholds based on ICAR research
        self.disease_thresholds = {
            'wheat': {
                'YellowRust': {
                    'name_hi': 'पीला रतुआ',
                    'temp_min': 8, 'temp_max': 16,
                    'humidity_min': 80,
                    'rain_days': 2,
                    'warning_days': 5,  # Warning before outbreak
                    'risk_colors': {
                        'LOW': '#4CAF50',
                        'MEDIUM': '#FFC107',
                        'HIGH': '#F44336'
                    }
                },
                'BrownRust': {
                    'name_hi': 'भूरा रतुआ',
                    'temp_min': 15, 'temp_max': 25,
                    'humidity_min': 75,
                    'rain_days': 1,
                    'warning_days': 7,
                    'risk_colors': {
                        'LOW': '#4CAF50',
                        'MEDIUM': '#FFC107',
                        'HIGH': '#F44336'
                    }
                },
                'BlackRust': {
                    'name_hi': 'काला रतुआ',
                    'temp_min': 18, 'temp_max': 28,
                    'humidity_min': 70,
                    'rain_days': 1,
                    'warning_days': 7,
                    'risk_colors': {
                        'LOW': '#4CAF50',
                        'MEDIUM': '#FFC107',
                        'HIGH': '#F44336'
                    }
                },
                'Aphid': {
                    'name_hi': 'एफिड (माहू)',
                    'temp_min': 15, 'temp_max': 25,
                    'humidity_min': 60,
                    'rain_days': 0,
                    'warning_days': 3,
                    'risk_colors': {
                        'LOW': '#4CAF50',
                        'MEDIUM': '#FFC107',
                        'HIGH': '#F44336'
                    }
                }
            },
            'rice': {
                'Blast': {
                    'name_hi': 'ब्लास्ट (झुलसा)',
                    'temp_min': 24, 'temp_max': 30,
                    'humidity_min': 85,
                    'rain_days': 2,
                    'warning_days': 5,
                    'risk_colors': {
                        'LOW': '#4CAF50',
                        'MEDIUM': '#FFC107',
                        'HIGH': '#F44336'
                    }
                },
                'BrownSpot': {
                    'name_hi': 'भूरा धब्बा',
                    'temp_min': 25, 'temp_max': 32,
                    'humidity_min': 80,
                    'rain_days': 1,
                    'warning_days': 7,
                    'risk_colors': {
                        'LOW': '#4CAF50',
                        'MEDIUM': '#FFC107',
                        'HIGH': '#F44336'
                    }
                },
                'LeafBlast': {
                    'name_hi': 'पत्ती झुलसा',
                    'temp_min': 24, 'temp_max': 28,
                    'humidity_min': 90,
                    'rain_days': 2,
                    'warning_days': 5,
                    'risk_colors': {
                        'LOW': '#4CAF50',
                        'MEDIUM': '#FFC107',
                        'HIGH': '#F44336'
                    }
                }
            }
        }
    
    def get_weather_forecast(self, lat: float, lon: float, days: int = 7):
        """Fetch weather forecast from Open-Meteo (free, no API key)"""
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "relative_humidity_2m_max",
                "wind_speed_10m_max"
            ],
            "forecast_days": days,
            "timezone": "auto"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Weather API error: {e}")
            return None
    
    def calculate_disease_risk(self, weather_data: Dict, crop_type: str) -> List[Dict]:
        """Calculate disease risk for next 7 days"""
        if not weather_data or 'daily' not in weather_data:
            return []
        
        daily_data = weather_data['daily']
        risks = []
        
        for day in range(min(7, len(daily_data['time']))):
            date = daily_data['time'][day]
            temp_max = daily_data['temperature_2m_max'][day]
            temp_min = daily_data['temperature_2m_min'][day]
            avg_temp = (temp_max + temp_min) / 2
            humidity = daily_data['relative_humidity_2m_max'][day]
            rain = daily_data['precipitation_sum'][day]
            wind = daily_data.get('wind_speed_10m_max', [0]*7)[day]
            
            day_risks = {
                'date': date,
                'day': day + 1,
                'temperature': round(avg_temp, 1),
                'humidity': round(humidity, 1),
                'rainfall': round(rain, 1),
                'wind_speed': round(wind, 1),
                'diseases': []
            }
            
            # Check each disease for this crop
            for disease, thresholds in self.disease_thresholds[crop_type].items():
                # Calculate risk score (0-100)
                risk_score = 0
                
                # Temperature check
                if thresholds['temp_min'] <= avg_temp <= thresholds['temp_max']:
                    risk_score += 40
                elif avg_temp < thresholds['temp_min'] - 5 or avg_temp > thresholds['temp_max'] + 5:
                    risk_score += 10
                else:
                    risk_score += 20
                
                # Humidity check
                if humidity >= thresholds['humidity_min']:
                    risk_score += 40
                elif humidity >= thresholds['humidity_min'] - 10:
                    risk_score += 20
                else:
                    risk_score += 10
                
                # Rainfall check
                if rain > 0:
                    risk_score += 20
                
                # Determine risk level
                if risk_score >= 70:
                    risk_level = "HIGH"
                    advisory = f"High risk of {disease}. Take preventive action now!"
                    advisory_hi = f"{thresholds['name_hi']} का उच्च जोखिम। तुरंत निवारक उपाय करें!"
                elif risk_score >= 40:
                    risk_level = "MEDIUM"
                    advisory = f"Medium risk of {disease}. Monitor fields closely."
                    advisory_hi = f"{thresholds['name_hi']} का मध्यम जोखिम। खेत की निगरानी करें।"
                else:
                    risk_level = "LOW"
                    advisory = f"Low risk of {disease}. Continue normal monitoring."
                    advisory_hi = f"{thresholds['name_hi']} का कम जोखिम। सामान्य निगरानी जारी रखें।"
                
                if risk_score >= 40:  # Only include if at least medium risk
                    day_risks['diseases'].append({
                        'disease': disease,
                        'disease_hi': thresholds['name_hi'],
                        'risk_level': risk_level,
                        'risk_score': risk_score,
                        'advisory': advisory,
                        'advisory_hi': advisory_hi,
                        'warning_days': thresholds['warning_days'],
                        'color': thresholds['risk_colors'][risk_level]
                    })
            
            # Sort diseases by risk score (highest first)
            day_risks['diseases'].sort(key=lambda x: x['risk_score'], reverse=True)
            risks.append(day_risks)
        
        return risks
    
    def get_early_warning(self, lat: float, lon: float, crop_type: str, farmer_name: str = "किसान") -> Dict:
        """Get complete early warning report"""
        weather = self.get_weather_forecast(lat, lon)
        
        if not weather:
            return {
                'success': False,
                'error': 'Unable to fetch weather data'
            }
        
        risks = self.calculate_disease_risk(weather, crop_type)
        
        # Get location name (reverse geocoding)
        location_name = self.get_location_name(lat, lon)
        
        # Find highest risk in next 3 days
        high_risk_alerts = []
        for day_risk in risks[:3]:  # Check next 3 days
            for disease in day_risk['diseases']:
                if disease['risk_level'] == 'HIGH':
                    high_risk_alerts.append({
                        'day': day_risk['day'],
                        'date': day_risk['date'],
                        'disease': disease['disease'],
                        'disease_hi': disease['disease_hi'],
                        'advisory': disease['advisory'],
                        'advisory_hi': disease['advisory_hi']
                    })
        
        return {
            'success': True,
            'location': {
                'lat': lat,
                'lon': lon,
                'name': location_name
            },
            'crop': crop_type,
            'generated_at': datetime.now().isoformat(),
            'weather_forecast': risks,
            'high_risk_alerts': high_risk_alerts,
            'summary': {
                'total_high_risk': len(high_risk_alerts),
                'critical_days': [a['day'] for a in high_risk_alerts],
                'message': f"⚠️ {len(high_risk_alerts)} high risk alerts in next 3 days" if high_risk_alerts else "✅ No high risk in next 3 days",
                'message_hi': f"⚠️ अगले 3 दिनों में {len(high_risk_alerts)} उच्च जोखिम" if high_risk_alerts else "✅ अगले 3 दिनों में कोई उच्च जोखिम नहीं"
            }
        }
    
    def get_location_name(self, lat: float, lon: float) -> str:
        """Get location name from coordinates (simplified)"""
        # You can integrate with a reverse geocoding API here
        # For now, return coordinates
        return f"{lat:.2f}°N, {lon:.2f}°E"