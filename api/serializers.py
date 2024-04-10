from rest_framework import serializers
from django.db import transaction
from .models import Employee,SalaryStructure

class SalaryStructureSerializer(serializers.ModelSerializer):
    hra = serializers.SerializerMethodField()
    da = serializers.SerializerMethodField()
    total_deductions = serializers.SerializerMethodField()
    net_salary = serializers.SerializerMethodField()

    class Meta:
        model = SalaryStructure
        # fields = '__all__'
        exclude = ('employee','id',)

    def get_hra(self, obj):
        return (obj.base_salary * obj.hra_percentage) / 100

    def get_da(self, obj):
        return (obj.base_salary * obj.da_percentage) / 100

    def get_total_deductions(self, obj):
        provident_fund_deduction = (obj.base_salary * obj.provident_fund_percentage) / 100
        tax_deduction = (obj.base_salary * obj.tax_percentage) / 100
        return provident_fund_deduction + tax_deduction

    def get_net_salary(self, obj):
        total_allowances = self.get_hra(obj) + self.get_da(obj)
        total_deductions = self.get_total_deductions(obj)
        return obj.base_salary + total_allowances - total_deductions
    
class EmployeeSerializer(serializers.ModelSerializer):
    salary_structure = SalaryStructureSerializer()

    class Meta:
        model = Employee
        fields = '__all__'
        # exclude = ('id',)

    def create(self, validated_data):
        salary_data = validated_data.pop('salary_structure')
        employee = Employee.objects.create(**validated_data)
        SalaryStructure.objects.create(employee=employee, **salary_data)
        return employee

    def update(self, instance, validated_data):
        salary_data = validated_data.pop('salary_structure')
        salary_structure = instance.salary_structure

        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.department = validated_data.get('department', instance.department)
        instance.age = validated_data.get('age', instance.age)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.employee_id = validated_data.get('employee_id', instance.employee_id)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        salary_structure.base_salary = salary_data.get('base_salary', salary_structure.base_salary)
        salary_structure.hra_percentage = salary_data.get('hra_percentage', salary_structure.hra_percentage)
        salary_structure.da_percentage = salary_data.get('da_percentage', salary_structure.da_percentage)
        salary_structure.provident_fund_percentage = salary_data.get('provident_fund_percentage', salary_structure.provident_fund_percentage)
        salary_structure.tax_percentage = salary_data.get('tax_percentage', salary_structure.tax_percentage)
        salary_structure.save()

        return instance