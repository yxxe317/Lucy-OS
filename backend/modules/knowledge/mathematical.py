"""
Mathematical Reasoning - Math problem solving and calculation
"""

import math
import re
from typing import Dict, List, Optional, Any, Union

class MathematicalReasoning:
    """
    Mathematical problem solving and calculation
    """
    
    def __init__(self):
        self.constants = {
            'pi': math.pi,
            'e': math.e,
            'c': 299792458,  # speed of light
            'G': 6.67430e-11,  # gravitational constant
            'h': 6.62607015e-34,  # Planck constant
        }
        
        self.operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '^': lambda x, y: x ** y,
            'sqrt': lambda x: math.sqrt(x),
            'sin': lambda x: math.sin(x),
            'cos': lambda x: math.cos(x),
            'tan': lambda x: math.tan(x),
            'log': lambda x: math.log10(x),
            'ln': lambda x: math.log(x),
        }
    
    def calculate(self, expression: str) -> Optional[float]:
        """
        Evaluate a mathematical expression
        """
        # Clean expression
        expression = expression.replace(' ', '')
        
        # Replace constants
        for const_name, const_value in self.constants.items():
            if const_name in expression:
                expression = expression.replace(const_name, str(const_value))
        
        try:
            # Safe eval with math functions
            result = eval(expression, {"__builtins__": {}}, math.__dict__)
            return float(result)
        except:
            return None
    
    def solve_equation(self, equation: str, variable: str = 'x') -> List[float]:
        """
        Solve a simple equation (linear or quadratic)
        """
        # Clean equation
        equation = equation.replace(' ', '')
        
        # Parse equation format: ax + b = c
        if '=' in equation:
            left, right = equation.split('=')
            
            # Try linear: ax + b
            if variable in left:
                # Extract coefficient
                pattern = f"([+-]?[0-9.]*){variable}([+-][0-9.]+)?"
                match = re.match(pattern, left)
                
                if match:
                    a = float(match.group(1) or 1)
                    b = float(match.group(2) or 0)
                    c = float(right)
                    
                    # Solve ax + b = c
                    if a != 0:
                        return [(c - b) / a]
        
        # Try quadratic: ax^2 + bx + c = 0
        if '^2' in equation:
            # Parse quadratic
            a_match = re.search(r'([+-]?[0-9.]*)?x\^2', equation)
            b_match = re.search(r'([+-][0-9.]+)?x(?!\^)', equation)
            c_match = re.search(r'([+-][0-9.]+)(?!x)', equation)
            
            a = float(a_match.group(1) or 1) if a_match else 0
            b = float(b_match.group(1) or 0) if b_match else 0
            c = float(c_match.group(1) or 0) if c_match else 0
            
            # Quadratic formula
            discriminant = b**2 - 4*a*c
            if discriminant >= 0:
                sqrt_disc = math.sqrt(discriminant)
                return [(-b + sqrt_disc)/(2*a), (-b - sqrt_disc)/(2*a)]
        
        return []
    
    def solve_system(self, equations: List[str], variables: List[str]) -> Dict[str, float]:
        """
        Solve system of linear equations
        """
        # Simplified for 2x2 systems
        if len(equations) == 2 and len(variables) == 2:
            # Parse coefficients
            coeffs = []
            constants = []
            
            for eq in equations:
                # Format: a*x + b*y = c
                eq = eq.replace(' ', '')
                left, right = eq.split('=')
                
                # Parse x coefficient
                x_match = re.search(r'([+-]?[0-9.]*)?\*?x', left)
                a = float(x_match.group(1) or 1) if x_match else 0
                
                # Parse y coefficient
                y_match = re.search(r'([+-][0-9.]+)?\*?y', left)
                b = float(y_match.group(1) or 0) if y_match else 0
                
                coeffs.append([a, b])
                constants.append(float(right))
            
            # Solve using Cramer's rule
            a1, b1 = coeffs[0]
            a2, b2 = coeffs[1]
            c1, c2 = constants
            
            det = a1*b2 - a2*b1
            if det != 0:
                x = (c1*b2 - c2*b1) / det
                y = (a1*c2 - a2*c1) / det
                return {variables[0]: x, variables[1]: y}
        
        return {}
    
    def derivative(self, expression: str, variable: str = 'x') -> str:
        """
        Compute symbolic derivative (simplified)
        """
        # Handle power rule: x^n -> n*x^(n-1)
        if '^' in expression:
            base, exp = expression.split('^')
            if base == variable:
                exp_num = float(exp)
                return f"{exp_num}*{variable}^{exp_num-1}"
        
        # Handle linear: a*x + b -> a
        if variable in expression and '+' not in expression and '-' not in expression:
            if expression.startswith(variable):
                return "1"
            elif expression.startswith(f"{variable}*"):
                coeff = expression.split('*')[0]
                return coeff
        
        return "0"  # Constant derivative
    
    def integral(self, expression: str, variable: str = 'x', 
                  lower: float = None, upper: float = None) -> Union[str, float]:
        """
        Compute integral (simplified)
        """
        # Power rule: x^n -> x^(n+1)/(n+1)
        if '^' in expression:
            base, exp = expression.split('^')
            if base == variable:
                exp_num = float(exp)
                integral = f"{variable}^{exp_num+1}/{exp_num+1}"
                
                if lower is not None and upper is not None:
                    # Definite integral
                    f_lower = lower**(exp_num+1)/(exp_num+1)
                    f_upper = upper**(exp_num+1)/(exp_num+1)
                    return f_upper - f_lower
                return integral + " + C"
        
        return expression + "*" + variable + " + C"
    
    def statistics(self, numbers: List[float]) -> Dict[str, float]:
        """
        Calculate basic statistics
        """
        if not numbers:
            return {}
        
        n = len(numbers)
        mean = sum(numbers) / n
        variance = sum((x - mean) ** 2 for x in numbers) / n
        std_dev = math.sqrt(variance)
        
        sorted_nums = sorted(numbers)
        median = sorted_nums[n//2] if n % 2 else (sorted_nums[n//2-1] + sorted_nums[n//2]) / 2
        
        return {
            'count': n,
            'sum': sum(numbers),
            'mean': mean,
            'median': median,
            'min': min(numbers),
            'max': max(numbers),
            'range': max(numbers) - min(numbers),
            'variance': variance,
            'std_dev': std_dev
        }
    
    def prime_factors(self, n: int) -> List[int]:
        """
        Find prime factors of a number
        """
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors
    
    def fibonacci(self, n: int) -> List[int]:
        """
        Generate Fibonacci sequence
        """
        if n <= 0:
            return []
        if n == 1:
            return [0]
        
        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[-1] + fib[-2])
        return fib[:n]