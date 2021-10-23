def test_lead(self):
    '\n        Determine what the next person hired in the same department makes.\n        Because the dataset is ambiguous, the name is also part of the\n        ordering clause. No default is provided, so None/NULL should be\n        returned.\n        '
    qs = Employee.objects.annotate(lead=Window(expression=Lead(expression='salary'), order_by=[F('hire_date').asc(), F('name').desc()], partition_by='department')).order_by('department', F('hire_date').asc(), F('name').desc())
    self.assertQuerysetEqual(qs, [('Jones', 45000, 'Accounting', datetime.date(2005, 11, 1), 45000), ('Jenson', 45000, 'Accounting', datetime.date(2008, 4, 1), 37000), ('Williams', 37000, 'Accounting', datetime.date(2009, 6, 1), 50000), ('Adams', 50000, 'Accounting', datetime.date(2013, 7, 1), None), ('Wilkinson', 60000, 'IT', datetime.date(2011, 3, 1), 34000), ('Moore', 34000, 'IT', datetime.date(2013, 8, 1), None), ('Miller', 100000, 'Management', datetime.date(2005, 6, 1), 80000), ('Johnson', 80000, 'Management', datetime.date(2005, 7, 1), None), ('Smith', 38000, 'Marketing', datetime.date(2009, 10, 1), 40000), ('Johnson', 40000, 'Marketing', datetime.date(2012, 3, 1), None), ('Smith', 55000, 'Sales', datetime.date(2007, 6, 1), 53000), ('Brown', 53000, 'Sales', datetime.date(2009, 9, 1), None)], transform=(lambda row: (row.name, row.salary, row.department, row.hire_date, row.lead)))