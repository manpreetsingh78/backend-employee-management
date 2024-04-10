from django.db import models

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f"id={self.id}, employee_name = {self.full_name}, department = {self.department}, is_active = {self.is_active}"

class SalaryStructure(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='salary_structure',blank=True, null=True)
    
    
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    da_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    provident_fund_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def calculate_hra(self):
        return (self.base_salary * self.hra_percentage) / 100
    
    def calculate_da(self):
        return (self.base_salary * self.da_percentage) / 100
    
    def calculate_total_deductions(self):
        return (self.base_salary * self.provident_fund_percentage) / 100 + (self.base_salary * self.tax_percentage) / 100
    
    def calculate_net_salary(self):
        total_allowances = self.calculate_hra() + self.calculate_da()
        total_deductions = self.calculate_total_deductions()
        return self.base_salary + total_allowances - total_deductions